"""
Feedback Ingest: maps real-world engagement data back to FP3 atoms.

Role: Takes engagement metrics for a specific run, computes virality
scores, and updates atom effectiveness weights in FP3. This closes
the feedback loop: generate → publish → collect feedback → learn.

Workflow: user provides engagement data → score_atoms() → update atom weights
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from loguru import logger


# ====================== Engagement Metrics ======================

@dataclass
class EngagementMetrics:
    """Real-world performance data from a published script."""
    run_id: str
    platform: str = ""  # douyin, xiaohongshu, bilibili, etc.
    publish_url: str = ""

    # Core metrics
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0       # 收藏 (bookmarks)
    follows: int = 0     # 新增粉丝 from this video

    # Engagement quality signals
    avg_watch_time_sec: float = 0    # average viewer watch time
    completion_rate: float = 0       # 0.0-1.0, % who watched full video
    replay_rate: float = 0           # 0.0-1.0, % who rewatched

    # Manual quality label (optional override)
    quality_label: str = ""  # "viral" | "good" | "average" | "poor"


def compute_virality_score(m: EngagementMetrics) -> dict:
    """
    Compute a composite virality score and sub-scores from engagement metrics.

    Returns dict with:
    - total: 0-100 composite score
    - engagement_rate: (likes + comments + shares) / views
    - depth_score: from completion_rate + replay_rate (quality signal)
    - growth_score: from follows + saves (audience building)
    """
    if m.views == 0:
        return {"total": 0, "engagement_rate": 0, "depth_score": 0, "growth_score": 0}

    # Engagement rate: weighted interaction per view
    interaction = m.likes + m.comments * 2 + m.shares * 3
    engagement_rate = min(interaction / m.views, 1.0)  # cap at 1.0

    # Depth score: how deeply people consumed the content
    depth_score = (m.completion_rate * 0.7 + m.replay_rate * 0.3)

    # Growth score: audience building (follows + saves per 1000 views)
    growth_per_k = (m.follows + m.saves) / max(m.views / 1000, 1)
    growth_score = min(growth_per_k / 100, 1.0)  # 100 growth actions per 1k views = max

    # Composite: engagement + depth + growth
    total = (
        engagement_rate * 0.35
        + depth_score * 0.35
        + growth_score * 0.30
    ) * 100

    return {
        "total": round(total, 2),
        "engagement_rate": round(engagement_rate, 4),
        "depth_score": round(depth_score, 4),
        "growth_score": round(growth_score, 4),
    }


def compute_atom_scores(m: EngagementMetrics, atoms: list[dict]) -> list[dict]:
    """
    Map virality score back to individual atoms.

    Each atom gets the same base virality_score, but their individual
    effectiveness is tracked per-atom for future aggregation.

    Returns list of atom records with embedded scores.
    """
    virality = compute_virality_score(m)

    return [
        {
            "hook": atom.get("hook", ""),
            "pattern": atom.get("pattern", ""),
            "atom_id": atom.get("atom_id", ""),
            "virality_score": virality["total"],
            "engagement_rate": virality["engagement_rate"],
            "depth_score": virality["depth_score"],
            "growth_score": virality["growth_score"],
            "views": m.views,
            "platform": m.platform,
            "run_id": m.run_id,
        }
        for atom in atoms
    ]


# ====================== Feedback Store ======================

FEEDBACK_DIR = Path("flowbeast/data/feedback")


def _ensure_feedback_dir():
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)


def save_feedback(metrics: EngagementMetrics, atom_scores: list[dict]):
    """Persist feedback to disk as a JSON file per run."""
    _ensure_feedback_dir()
    record = {
        "run_id": metrics.run_id,
        "platform": metrics.platform,
        "publish_url": metrics.publish_url,
        "engagement": {
            "views": metrics.views,
            "likes": metrics.likes,
            "comments": metrics.comments,
            "shares": metrics.shares,
            "saves": metrics.saves,
            "follows": metrics.follows,
            "avg_watch_time_sec": metrics.avg_watch_time_sec,
            "completion_rate": metrics.completion_rate,
            "replay_rate": metrics.replay_rate,
        },
        "virality": compute_virality_score(metrics),
        "atom_scores": atom_scores,
    }
    path = FEEDBACK_DIR / f"{metrics.run_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    logger.success(f"📊 Feedback saved: {path}")
    return path


def load_feedback(run_id: str) -> Optional[dict]:
    """Load feedback for a specific run."""
    path = FEEDBACK_DIR / f"{run_id}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_atom_effectiveness(atom_hook: str) -> dict:
    """
    Compute aggregated effectiveness for a specific atom hook.
    Averages virality scores across all runs where this atom was used.

    Returns dict with mean scores and run count.
    """
    _ensure_feedback_dir()
    scores = []
    run_count = 0

    for fp in FEEDBACK_DIR.glob("*.json"):
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
        for atom in data.get("atom_scores", []):
            if atom.get("hook", "") == atom_hook:
                scores.append(atom)
                run_count += 1

    if not scores:
        return {"mean_virality": 0, "mean_engagement_rate": 0, "run_count": 0}

    return {
        "mean_virality": round(sum(s["virality_score"] for s in scores) / len(scores), 2),
        "mean_engagement_rate": round(sum(s["engagement_rate"] for s in scores) / len(scores), 4),
        "run_count": run_count,
        "best_run": max(scores, key=lambda s: s["virality_score"])["run_id"],
        "worst_run": min(scores, key=lambda s: s["virality_score"])["run_id"],
    }


# ====================== CLI Interface ======================

def ingest_feedback_from_report(
    report_path: str,
    views: int = 0,
    likes: int = 0,
    comments: int = 0,
    shares: int = 0,
    saves: int = 0,
    follows: int = 0,
    completion_rate: float = 0,
    replay_rate: float = 0,
    platform: str = "",
    publish_url: str = "",
):
    """
    Main entry point: take a production_report.json path + engagement data,
    compute atom effectiveness, and persist feedback.
    """
    report_p = Path(report_path)
    if not report_p.exists():
        raise FileNotFoundError(f"Report not found: {report_path}")

    with open(report_p, "r", encoding="utf-8") as f:
        report = json.load(f)

    run_id = report.get("run_id", "unknown")
    atoms = report.get("fp3_atoms_used", [])

    if not atoms:
        logger.warning("No FP3 atoms tracked in this run. Cannot map feedback.")
        return None

    metrics = EngagementMetrics(
        run_id=run_id,
        platform=platform,
        publish_url=publish_url,
        views=views,
        likes=likes,
        comments=comments,
        shares=shares,
        saves=saves,
        follows=follows,
        completion_rate=completion_rate,
        replay_rate=replay_rate,
    )

    virality = compute_virality_score(metrics)
    atom_scores = compute_atom_scores(metrics, atoms)

    save_feedback(metrics, atom_scores)

    logger.info(
        f"📈 Virality score: {virality['total']}/100 | "
        f"Engagement: {virality['engagement_rate']:.2%} | "
        f"Depth: {virality['depth_score']:.2f} | "
        f"Growth: {virality['growth_score']:.2f}"
    )

    for atom in atom_scores:
        logger.info(
            f"  Atom [{atom['hook'][:30]}...] → virality={atom['virality_score']}/100"
        )

    return {
        "virality": virality,
        "atom_scores": atom_scores,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="FlowBeast Feedback Ingest")
    parser.add_argument("--report", required=True, help="Path to production_report.json")
    parser.add_argument("--platform", default="", help="Platform (douyin, xiaohongshu, etc.)")
    parser.add_argument("--url", default="", help="Publish URL")
    parser.add_argument("--views", type=int, default=0)
    parser.add_argument("--likes", type=int, default=0)
    parser.add_argument("--comments", type=int, default=0)
    parser.add_argument("--shares", type=int, default=0)
    parser.add_argument("--saves", type=int, default=0)
    parser.add_argument("--follows", type=int, default=0)
    parser.add_argument("--completion-rate", type=float, default=0, help="0.0-1.0")
    parser.add_argument("--replay-rate", type=float, default=0, help="0.0-1.0")

    args = parser.parse_args()

    ingest_feedback_from_report(
        report_path=args.report,
        platform=args.platform,
        publish_url=args.url,
        views=args.views,
        likes=args.likes,
        comments=args.comments,
        shares=args.shares,
        saves=args.saves,
        follows=args.follows,
        completion_rate=args.completion_rate,
        replay_rate=args.replay_rate,
    )
