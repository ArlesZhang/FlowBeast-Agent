"""
Drama Prompt: LLM prompt template for hook-driven short-drama storytelling.

Role: Provides the structured prompt template that guides the LLM to generate
viral drama scripts. Enforces 爽文 (catharsis-first) writing rules, personal
stakes, and face-slap dialogue patterns.

Workflow: generator.py → build_prompt() → inject_prompt() → llm_call()
"""

import random
from typing import Optional


# ====================== Narrative Structures ======================

NARRATIVE_STRUCTURES = [
    {
        "name": "classic_reversal",
        "pattern": "oppression → identity reveal → counterattack → catharsis",
        "emotion_global": ["suppression", "humiliation", "shock", "vindication", "catharsis"],
    },
    {
        "name": "mystery_reveal",
        "pattern": "mystery → clue → false truth → real twist → resolution",
        "emotion_global": ["curiosity", "suspense", "betrayal", "shock", "satisfaction"],
    },
    {
        "name": "double_identity",
        "pattern": "normal facade → crisis → ability leak → full reveal → face-slap",
        "emotion_global": ["pity", "mockery", "anticipation", "shock", "catharsis"],
    },
    {
        "name": "deal_with_devil",
        "pattern": "desperation → forbidden pact → power awakening → enemy crushed",
        "emotion_global": ["despair", "tension", "power", "shock", "satisfaction"],
    },
    {
        "name": "parallel_perspective",
        "pattern": "same event → perspective A → perspective B → truth → reversal",
        "emotion_global": ["confusion", "anger", "shock", "understanding", "catharsis"],
    },
]


def build_prompt(
    topic: str,
    trend_context: Optional[str] = None,
    narrative_style: Optional[str] = None,
    fp3_injected: str = "",
) -> str:
    if narrative_style is None:
        chosen = random.choice(NARRATIVE_STRUCTURES)
    else:
        chosen = next(
            (s for s in NARRATIVE_STRUCTURES if s["name"] == narrative_style),
            random.choice(NARRATIVE_STRUCTURES),
        )

    prompt = f"""You are a top-tier writer of viral Chinese short-dramas (短剧/漫剧). These are 爽文 — stories designed for maximum emotional payoff, not literary merit. Write a script about: {topic}

Structure: {chosen['name']} — {chosen['pattern']}

CRITICAL RULES:
1. HOOK (0-3s): Start with MAXIMUM conflict — slap, betrayal, public humiliation. The viewer must stop scrolling instantly.
2. PERSONAL STAKE: Ground every conflict in one person's life — not abstract society. A mother's fear, a worker's last day, a daughter's debt. Make it specific and visceral.
3. MAKE THE VILLAIN HATEABLE: The villain must do something viscerally insulting within the first 2 scenes — mock the poor, spit on the weak, betray family. The viewer should want them destroyed.
4. EVERY SCENE ESCALATES: Each scene must raise the stakes. Power reversal, money crush, public face-slap, identity reveal. No filler.
5. EMOTION CURVE MUST END ON CATHARSIS: suppression → humiliation → shock → 爆发 → 爽. The hero WINS. The villain is crushed. The viewer feels 爽 (deep satisfaction). Never end on existential dread or ambiguity.
6. FACE-SLAP MOMENT: At the climax, the hero must deliver a brutal callback line — repeating the villain's earlier mockery back at them. This is the moment viewers replay and share.
7. DIALOGUE: Short, blunt, emotional. Max 20 characters per line. NO technical jargon. NO literary prose. Think: real people screaming at each other.
8. 5-6 scenes total. Fast pacing. No exposition dumps.

JSON output format (no markdown, no explanation, no extra text):
{{
  "title": "{topic}",
  "genre": "genre tag (e.g. revenge, counterattack, face-slap)",
  "core_hook": "one sentence: the most shareable moment in this script",
  "tags": ["tag1", "tag2"],
  "emotion_curve_global": ["{chosen['emotion_global'][0]}", "...", "{chosen['emotion_global'][-1]}"],
  "characters": [{{"name": "name", "visual_desc": "physical appearance in English", "voice_tag": "id"}}],
  "scenes": [{{
    "id": 1,
    "hook": "what grabs the viewer in the first 3 seconds of this scene",
    "conflict": "who vs who, what type",
    "summary": "one-line summary",
    "emotion_curve": ["start emotion", "end emotion"],
    "climax": true or false,
    "dialogue": [{{"speaker": "name", "text": "line under 20 chars", "emotion": "emotion", "intensity": 7}}]
  }}]
}}

Output ONLY valid JSON. No markdown code fences. No explanation. No extra text."""

    if trend_context:
        prompt += f"\n\nTrending context to weave into the story: {trend_context}\n"

    if fp3_injected:
        prompt += f"\n\nReference viral patterns to incorporate:\n{fp3_injected}\n"

    return prompt
