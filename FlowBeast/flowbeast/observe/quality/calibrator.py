# flowbeast/observe/quality/calibrator.py

"""
QualityGate 校准器：用真实爆款参考集校准评分维度。

工作原理：
1. 从 reverse_engineered/ 目录加载 ViralScript 参考集
2. 对每条跑 RuleBasedScorer，收集各维度分数
3. 计算 mean / std / correlation_with_total
4. 推荐 accept / review 阈值
5. 输出校准报告 JSON

Z-score 冷启动防御：样本数 < 5 时 σ=0 保护，回退到百分位数映射。
"""

import asyncio
import json
import math
from pathlib import Path
from typing import Dict, List, Optional

from loguru import logger

from .config import quality_settings
from .scorer import RuleBasedScorer
from flowbeast.fp3.schema import ViralScript


RE_DIR = Path("flowbeast/data/reverse_engineered")
CALIBRATION_OUTPUT = Path("flowbeast/data/quality_audit/calibration_report.json")


def _load_reference_scripts() -> List[ViralScript]:
    """Load all non-template JSON files from reverse_engineered/."""
    if not RE_DIR.exists():
        return []

    scripts = []
    for p in sorted(RE_DIR.glob("*.json")):
        if p.name.startswith("TEMPLATE"):
            continue
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            scripts.append(ViralScript(**data))
        except Exception as e:
            logger.warning(f"  跳过 {p.name}: {e}")
    return scripts


async def run_calibration(scripts: Optional[List[ViralScript]] = None) -> Optional[dict]:
    """
    运行校准流程。

    Returns:
        校准报告 dict，或 None（样本不足）
    """
    if scripts is None:
        scripts = _load_reference_scripts()

    if not scripts:
        logger.warning("校准：无参考数据（reverse_engineered/ 为空），跳过校准")
        return None

    logger.info(f"校准：加载 {len(scripts)} 条参考档案")

    # Filter to viral samples only for calibration
    viral_scripts = [s for s in scripts if s.quality_label == "viral"]
    if not viral_scripts:
        logger.warning("校准：无 viral 标签样本，使用全部样本")
        viral_scripts = scripts

    logger.info(f"校准：使用 {len(viral_scripts)} 条 viral 样本")

    # Score all reference scripts
    scorer = RuleBasedScorer(weights=quality_settings.weights_dict)
    dimension_scores: Dict[str, List[float]] = {}
    totals = []

    for s in viral_scripts:
        unit = s.to_viral_unit()
        result = await scorer.score(unit)
        totals.append(result.weighted_total)
        for dim, score in result.category_scores.items():
            dimension_scores.setdefault(dim, []).append(score)

    # Compute statistics per dimension
    dimension_stats = {}
    for dim, scores in dimension_scores.items():
        n = len(scores)
        mean = sum(scores) / n
        variance = sum((x - mean) ** 2 for x in scores) / max(n - 1, 1)
        std = math.sqrt(variance)
        sorted_scores = sorted(scores)
        p25 = sorted_scores[max(0, int(n * 0.25))]
        p50 = sorted_scores[max(0, int(n * 0.50))]
        p75 = sorted_scores[min(n - 1, int(n * 0.75))]

        # Correlation with total
        corr = _pearson_corr(scores, totals) if n >= 3 else 0.0

        dimension_stats[dim] = {
            "mean": round(mean, 4),
            "std": round(std, 4),
            "median": round(p50, 4),
            "p25": round(p25, 4),
            "p75": round(p75, 4),
            "correlation_with_total": round(corr, 4),
            "sample_count": n,
        }

    # Overall total stats
    n_total = len(totals)
    mean_total = sum(totals) / n_total
    std_total = math.sqrt(sum((x - mean_total) ** 2 for x in totals) / max(n_total - 1, 1))

    # Recommended thresholds: mean_total - 1σ for review, mean_total for accept
    # But cap to reasonable ranges
    rec_accept = min(0.85, max(0.50, mean_total))
    rec_review = min(0.70, max(0.30, mean_total - std_total))

    # Recommended weights: proportional to correlation with total
    dim_names = list(dimension_stats.keys())
    correlations = [max(0.01, abs(dimension_stats[d]["correlation_with_total"])) for d in dim_names]
    corr_sum = sum(correlations)
    rec_weights = {d: round(c / corr_sum, 3) for d, c in zip(dim_names, correlations)}

    # Importance ranking (by correlation)
    importance_ranking = sorted(
        dim_names,
        key=lambda d: dimension_stats[d]["correlation_with_total"],
        reverse=True,
    )

    # Cold-start warning
    cold_start = n_total < 5
    if cold_start:
        logger.warning(
            f"校准：样本不足（{n_total} < 5），σ=0 冷启动保护已启用。"
            f"z-score 映射已回退到原始分数。"
        )

    report = {
        "reference_count": n_total,
        "cold_start_protection": cold_start,
        "total_score_stats": {
            "mean": round(mean_total, 4),
            "std": round(std_total, 4),
            "min": round(min(totals), 4),
            "max": round(max(totals), 4),
        },
        "dimension_stats": dimension_stats,
        "recommended_thresholds": {
            "accept": round(rec_accept, 3),
            "review": round(rec_review, 3),
        },
        "recommended_weights": rec_weights,
        "importance_ranking": importance_ranking,
        "current_weights": quality_settings.weights_dict,
    }

    # Save report
    CALIBRATION_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(CALIBRATION_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)

    logger.success(f"校准报告已保存: {CALIBRATION_OUTPUT}")

    return report


def _pearson_corr(x: List[float], y: List[float]) -> float:
    """Simple Pearson correlation."""
    n = len(x)
    if n < 2:
        return 0.0
    mx = sum(x) / n
    my = sum(y) / n
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    dx = math.sqrt(sum((xi - mx) ** 2 for xi in x))
    dy = math.sqrt(sum((yi - my) ** 2 for yi in y))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def load_calibration_report() -> Optional[dict]:
    """Load the most recent calibration report if it exists."""
    if not CALIBRATION_OUTPUT.exists():
        return None
    with open(CALIBRATION_OUTPUT, "r", encoding="utf-8") as f:
        return json.load(f)


def _z_to_percentile(z: float) -> float:
    """Approximate z-score to percentile using error function approximation."""
    # Simple approximation: Φ(z) ≈ 0.5 * (1 + erf(z / √2))
    # erf approximation via polynomial
    x = z / math.sqrt(2)
    t = 1.0 / (1.0 + 0.3275911 * abs(x))
    poly = t * (0.254829592 + t * (-0.284496736 + t * (
        1.421413741 + t * (-1.453152027 + t * 1.061405429))))
    erf = 1.0 - poly * math.exp(-x * x)
    result = 0.5 * (1.0 + math.copysign(1, z) * erf)
    return max(0.0, min(1.0, result))


async def run_calibration_and_print():
    """Entry point for CLI / one-shot calibration run."""
    report = await run_calibration()
    if report is None:
        print("校准：无数据可用。请先使用 reverse_engineer 工具注入参考数据。")
        return

    print("\n" + "=" * 60)
    print("  QualityGate 校准报告")
    print("=" * 60)
    print(f"  参考样本数: {report['reference_count']}")
    print(f"  冷启动保护: {'是' if report['cold_start_protection'] else '否'}")
    print(f"  总分 mean={report['total_score_stats']['mean']:.3f}  std={report['total_score_stats']['std']:.3f}")
    print()
    print("  推荐阈值:")
    print(f"    accept: {report['recommended_thresholds']['accept']:.3f}")
    print(f"    review: {report['recommended_thresholds']['review']:.3f}")
    print()
    print("  维度重要性排序:")
    for i, dim in enumerate(report['importance_ranking'], 1):
        stats = report['dimension_stats'][dim]
        print(f"    {i}. {dim} (r={stats['correlation_with_total']:.3f}, mean={stats['mean']:.3f})")
    print()
    print("  推荐权重:")
    for dim, w in report['recommended_weights'].items():
        print(f"    {dim}: {w:.3f}")
    print()
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(run_calibration_and_print())
