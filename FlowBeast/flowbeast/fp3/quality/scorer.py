import re
from abc import ABC, abstractmethod
from typing import Dict, Tuple
from loguru import logger

from .models import ScoreResult
from ..schema import ViralUnit


class BaseScorer(ABC):
    """Abstract scoring engine. Implementations range from rule-based to ML."""

    @abstractmethod
    async def score(self, unit: ViralUnit) -> ScoreResult:
        """Score a ViralUnit candidate across all quality dimensions."""
        ...


class RuleBasedScorer(BaseScorer):
    """
    Heuristic scorer analyzing ViralUnit text fields.
    Each _score_* method returns (score_0_to_1, explanation_string).
    """

    _STRONG_HOOK_MARKERS = re.compile(
        r"(绝|惊|爆|反转|身份|秘密|真相|竟然|穿越|重生|隐藏|原来|前世|"
        r"芯片|万亿|全球|富豪|契约|情报|卧底|觉醒|系统|金手指|"
        r"shock|reveal|twist|secret|hidden|identity|betray|"
        r"billion|crisis|viral|expose)",
        re.IGNORECASE,
    )
    _CLIFFHANGER_MARKERS = re.compile(
        r"(突然|下一秒|此刻|谁知|没想到|殊不知|然而|就在这时|竟然|"
        r"suddenly|but then|just then|however|unexpectedly)",
        re.IGNORECASE,
    )
    _ACTION_MARKERS = re.compile(
        r"(撕|毁|爆|抢|威胁|逼迫|下跪|死|开除|跪求|碾压|虐|"
        r"kill|destroy|threat|expose|crush|dominate|humiliate)",
        re.IGNORECASE,
    )

    def __init__(self, weights: Dict[str, float]):
        self.weights = weights

    async def score(self, unit: ViralUnit) -> ScoreResult:
        scores: Dict[str, float] = {}
        explanations: Dict[str, str] = {}

        scorers = [
            ("hook_strength", self._score_hook_strength),
            ("emotional_intensity", self._score_emotional_intensity),
            ("novelty", self._score_novelty),
            ("retention_potential", self._score_retention_potential),
            ("virality_signals", self._score_virality_signals),
            ("pacing", self._score_pacing),
            ("engagement_density", self._score_engagement_density),
            ("conflict_density", self._score_conflict_density),
            ("replay_potential", self._score_replay_potential),
        ]

        for name, fn in scorers:
            scores[name], explanations[name] = fn(unit)

        weighted_total = sum(
            scores[n] * self.weights.get(n, 0.0) for n in scores
        )
        weighted_total = round(max(0.0, min(1.0, weighted_total)), 4)

        logger.debug(
            f"Scored [hook={unit.hook[:30]}...] => "
            f"total={weighted_total:.3f} cats={ {k: round(v, 3) for k, v in scores.items()} }"
        )

        return ScoreResult(
            category_scores=scores,
            weighted_total=weighted_total,
            explanations=explanations,
        )

    def _score_hook_strength(self, unit: ViralUnit) -> Tuple[float, str]:
        hook = unit.hook.strip()
        length = len(hook)
        if length == 0:
            return 0.0, "Empty hook"

        if length < 5:
            length_score = 0.2
        elif length <= 40:
            length_score = min(1.0, length / 25.0)
        else:
            length_score = max(0.3, 1.0 - (length - 40) / 60.0)

        markers = len(self._STRONG_HOOK_MARKERS.findall(hook))
        marker_score = min(1.0, markers * 0.25)

        specificity = bool(re.search(r"[A-Z一-鿿]{3,}", hook))
        spec_score = 0.15 if specificity else 0.0

        total = 0.3 * 0.2 + length_score * 0.4 + marker_score * 0.3 + spec_score
        return round(total, 4), f"len={length}, markers={markers}, specific={'yes' if specificity else 'no'}"

    def _score_emotional_intensity(self, unit: ViralUnit) -> Tuple[float, str]:
        emotions = unit.emotion
        unique = set(e.lower() for e in emotions)
        count = len(emotions)
        unique_count = len(unique)

        if count == 0:
            return 0.1, "No emotion tags"

        count_score = min(1.0, count / 3.0)
        diversity_score = min(1.0, unique_count / 3.0)

        high_arousal = {"shock", "anger", "fear", "excitement", "satisfaction",
                        "tension", "revenge", "despair", "anticipation",
                        "震惊", "愤怒", "恐惧", "兴奋", "满足", "紧张", "复仇", "绝望"}
        arousal_hits = sum(1 for e in emotions if e.lower() in high_arousal)
        arousal_score = min(1.0, arousal_hits * 0.33)

        total = count_score * 0.3 + diversity_score * 0.4 + arousal_score * 0.3
        return round(total, 4), f"count={count}, unique={unique_count}, high_arousal={arousal_hits}"

    def _score_novelty(self, unit: ViralUnit) -> Tuple[float, str]:
        hook = unit.hook
        rare_chars = len(re.findall(r"[^一-鿿\w\s,.;:!?，。；：！？]", hook))
        pattern_length = len(unit.pattern)
        pattern_diversity = len(set(unit.pattern))

        novelty = min(1.0, rare_chars * 0.2 + min(pattern_length, 20) / 40.0 + pattern_diversity / 30.0)
        return round(novelty, 4), f"rare_chars={rare_chars}, pattern_len={pattern_length}"

    def _score_retention_potential(self, unit: ViralUnit) -> Tuple[float, str]:
        hook = unit.hook
        cliffhangers = len(self._CLIFFHANGER_MARKERS.findall(hook))
        questions = hook.count("?") + hook.count("？")

        curiosity = 0.0
        if questions > 0:
            curiosity = min(1.0, questions * 0.5)
        elif any(w in hook for w in ["秘密", "真相", "竟然", "隐藏", "secret", "truth", "hidden", "reveal"]):
            curiosity = 0.6

        total = min(1.0, cliffhangers * 0.25 + curiosity * 0.5 + 0.2)
        return round(total, 4), f"cliffhangers={cliffhangers}, curiosity={curiosity:.2f}"

    def _score_virality_signals(self, unit: ViralUnit) -> Tuple[float, str]:
        hook_lower = unit.hook.lower()
        controversy = sum(1 for w in ["开除", "背叛", "欺凌", "侮辱", "跪", "偷",
                                       "betray", "fire", "humiliate", "cheat", "lie", "steal"] if w in hook_lower)
        relatable = sum(1 for w in ["总裁", "老板", "同事", "前女友", "老公", "妈妈",
                                     "boss", "ceo", "ex", "wife", "husband", "mother", "family"] if w in hook_lower)
        reversal = sum(1 for w in ["身份", "反转", "竟然", "原来", "谁知",
                                    "identity", "twist", "plot", "actually", "revealed"] if w in hook_lower)

        total = min(1.0, controversy * 0.25 + relatable * 0.15 + reversal * 0.35 + 0.15)
        return round(total, 4), f"controversy={controversy}, relatable={relatable}, reversal={reversal}"

    def _score_pacing(self, unit: ViralUnit) -> Tuple[float, str]:
        hook = unit.hook.strip()
        length = len(hook)

        if length <= 10:
            pace = 0.9
        elif length <= 20:
            pace = 0.7
        elif length <= 40:
            pace = 0.5
        else:
            pace = 0.3

        urgency = len(re.findall(r"(立刻|马上|突然|三秒|下一秒|紧急|瞬间|immediately|sudden|urgent|seconds|crisis)",
                                  hook, re.IGNORECASE))
        total = min(1.0, pace + min(0.3, urgency * 0.15))
        return round(total, 4), f"len={length}, urgency={urgency}"

    def _score_engagement_density(self, unit: ViralUnit) -> Tuple[float, str]:
        hook_lower = unit.hook.lower()
        actions = len(self._ACTION_MARKERS.findall(unit.hook))
        stakes = sum(1 for w in ["亿", "万", "死", "总裁", "全球", "家族", "万亿",
                                  "billion", "million", "ceo", "global", "life", "death"] if w in hook_lower)
        power = sum(1 for w in ["开除", "跪求", "碾压", "身份", "契约",
                                 "fire", "beg", "dominate", "crush", "identity", "contract"] if w in hook_lower)

        total = min(1.0, actions * 0.3 + stakes * 0.25 + power * 0.30 + 0.1)
        return round(total, 4), f"actions={actions}, stakes={stakes}, power={power}"

    def _score_conflict_density(self, unit: ViralUnit) -> Tuple[float, str]:
        hook = unit.hook
        opposition = len(re.findall(r"(vs|vs\.|对抗|对决|PK|战|fight|versus|against)", hook, re.IGNORECASE))
        status = len(re.findall(r"(开除|跪求|羞辱|碾压|穷|富|上位|下跪|fire|beg|humiliate|poor|rich|beggar)", hook, re.IGNORECASE))
        betrayal = len(re.findall(r"(背叛|欺骗|卧底|间谍|秘密|双重|betray|spy|double|deceive|secret)", hook, re.IGNORECASE))

        total = min(1.0, opposition * 0.3 + status * 0.35 + betrayal * 0.35 + 0.1)
        return round(total, 4), f"opposition={opposition}, status={status}, betrayal={betrayal}"

    def _score_replay_potential(self, unit: ViralUnit) -> Tuple[float, str]:
        hook = unit.hook
        twists = len(re.findall(r"(竟然|原来|反转|真相|其实|隐藏|前世|卧底|twist|actually|truth|reveal|hidden|secret|double|plot)", hook, re.IGNORECASE))
        layers = len(re.findall(r"(细节|暗示|伏笔|线索|暗号|密码|clue|foreshadow|hidden|code|detail)", hook, re.IGNORECASE))

        total = min(1.0, twists * 0.35 + layers * 0.40 + 0.15)
        return round(total, 4), f"twists={twists}, layers={layers}"
