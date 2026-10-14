"""
Generate evidence package: 5 successful GRAFT runs with prompt packages.

Run: uv run python tests/evidence_package.py
"""

import sys
import json
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from flowbeast.vto.graft import graft_operator
from flowbeast.drama.pipeline import run_full_pipeline

TOPICS = [
    "AI Agent 取代白领",
    "通用人工智能诞生",
    "硅基生命觉醒",
    "自动驾驶夺走司机",
    "火星移民骗局",
]

OUTPUT_DIR = Path("flowbeast/data/outputs/evidence")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"🎬 FlowBeast Evidence Package — {len(TOPICS)} GRAFT runs")
print("=" * 60)

for i, topic in enumerate(TOPICS, 1):
    print(f"\n{'='*60}")
    print(f"Run {i}/{len(TOPICS)}: {topic}")
    print(f"{'='*60}")

    # Step 1: GRAFT
    graft = graft_operator(topic)
    if not graft.graft_applied:
        print(f"⚠️ GRAFT not applied for {topic}, skipping")
        continue

    print(f"  Hook: {graft.extracted_hook_structure.get('hook_type')}")
    print(f"  Conflict: {graft.extracted_conflict_pattern.get('conflict_type')}")

    # Step 2: Pipeline
    result = run_full_pipeline(topic, graft_prompt=graft.graft_prompt)
    if result is None:
        print(f"❌ Pipeline failed for {topic}")
        continue

    # Step 3: Save evidence
    run_id = result["run_id"]
    evidence = {
        "topic": topic,
        "run_id": run_id,
        "graft": graft.to_dict(),
        "script_path": str(result["script_path"]),
        "prompt_package_path": str(result["base_path"] / "prompt_package.json"),
        "report_path": str(result["report_path"]),
        "episode_audio_path": str(result.get("episode_audio_path", "")),
    }

    evidence_file = OUTPUT_DIR / f"evidence_{i:02d}_{run_id}.json"
    evidence_file.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")

    # Read quality score from report
    report = json.loads(result["report_path"].read_text(encoding="utf-8"))
    quality = report.get("quality", {})

    print(f"  ✅ Completed | Quality: {quality.get('score', 0):.2f} ({quality.get('action', '')})")
    print(f"  📦 Run ID: {run_id}")

print(f"\n{'='*60}")
print(f"🎯 Evidence package generated in: {OUTPUT_DIR}")
print(f"📊 Files: {len(list(OUTPUT_DIR.glob('*.json')))}")
print(f"{'='*60}")
