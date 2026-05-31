"""
FlowBeast Demo UI — Minimal Streamlit single-page demo.

Role: Demonstrates the full FlowBeast workflow:
Topic Input → FP3 Retrieval → GRAFT Structure → Generated Script → Audio → Prompt Package

Run: uv run streamlit run flowbeast/demo/app.py --server.port 8501
"""

import json
import time
import urllib.request
from pathlib import Path

import streamlit as st

API_BASE = "http://localhost:8000"


def api_post(path: str, data: dict) -> dict:
    """Simple POST to the FastAPI server."""
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def api_get(path: str) -> dict:
    """Simple GET from the FastAPI server."""
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def download_file(file_type: str, run_id: str) -> bytes:
    """Download a file from the API."""
    url = f"{API_BASE}/api/v1/download/{file_type}/{run_id}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


# ==================== Page Config ====================
st.set_page_config(
    page_title="FlowBeast Demo",
    page_icon="🎬",
    layout="wide",
)

# ==================== Header ====================
st.title("🎬 FlowBeast — Viral Prompt Compiler")
st.caption("Retrieve viral structure → GRAFT transfer → Generate new script → Export assets")

# ==================== Sidebar: Server Status ====================
with st.sidebar:
    st.subheader("Server Status")
    try:
        health = api_get("/health")
        st.success(f"✅ {health.get('status', 'unknown')}")
    except Exception:
        st.error("❌ API server not running")
        st.info("Start with: `uvicorn flowbeast.api.main:app --reload --port 8000`")
        st.stop()

# ==================== Main: Topic Input ====================
st.subheader("1. Topic Input")

recommended_topics = [
    "AI Agent 取代白领",
    "通用人工智能诞生",
    "人类最后一份工作",
    "硅基生命觉醒",
    "脑机接口求职",
    "美股 AI 泡沫破裂",
    "火星移民骗局",
    "量子霸权时刻",
    "自动驾驶夺走司机",
    "机器人养老困境",
    "克苏鲁苏醒",
    "火星地下文明",
    "AI 召唤古神",
    "数字生命地狱",
    "太空虫族入侵",
]

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    topic = st.text_input("Enter a topic:", value="", key="topic_input")
with col2:
    use_graft = st.checkbox("Use GRAFT", value=True)
with col3:
    generate_clicked = st.button("🚀 Generate", type="primary")

# Topic selector
st.caption("Recommended topics:")
cols = st.columns(5)
for i, t in enumerate(recommended_topics):
    with cols[i % 5]:
        if st.button(t, key=f"topic_{i}", use_container_width=True):
            st.session_state.topic_input = t
            st.rerun()

# ==================== Generate ====================
if generate_clicked and topic:
    # Submit task
    with st.spinner("Submitting generation task..."):
        resp = api_post("/api/v1/generate", {"topic": topic, "use_graft": use_graft})
        task_id = resp["task_id"]
        st.session_state["last_task_id"] = task_id
        st.success(f"Task submitted: `{task_id}`")

# ==================== Task Status ====================
if "last_task_id" in st.session_state:
    st.subheader("2. Task Status")
    task_id = st.session_state["last_task_id"]

    # Poll for status
    status_placeholder = st.empty()
    progress_bar = st.progress(0)

    max_polls = 120  # 10 minutes max
    poll_interval = 5  # seconds
    final_task = None

    for _ in range(max_polls):
        try:
            task_data = api_get(f"/api/v1/tasks/{task_id}")
        except Exception:
            status_placeholder.warning("Waiting for API server...")
            time.sleep(poll_interval)
            continue

        status = task_data.get("status", "UNKNOWN")
        stage = task_data.get("current_stage", "")
        progress = task_data.get("progress", 0)

        # Update UI
        status_placeholder.info(f"Status: **{status}** | Stage: `{stage}` | Progress: `{progress}%`")
        progress_bar.progress(progress / 100.0)

        if status in ("COMPLETE", "FAILED"):
            final_task = task_data
            break

        time.sleep(poll_interval)

    # ==================== Results ====================
    if final_task and final_task.get("status") == "COMPLETE":
        st.success("✅ Generation complete!")
        result = final_task.get("result", {})
        graft_info = final_task.get("graft_info")

        # 3. Retrieved Viral Structure
        if graft_info and graft_info.get("graft_applied"):
            st.subheader("3. Retrieved Viral Structure (GRAFT)")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### Hook Structure")
                hs = graft_info.get("extracted_hook_structure", {})
                st.json({
                    "hook_type": hs.get("hook_type"),
                    "time_to_hook": hs.get("time_to_hook"),
                    "emotional_payload": hs.get("emotional_payload"),
                    "audience_question": hs.get("audience_question"),
                })
            with col_b:
                st.markdown("#### Conflict Pattern")
                cp = graft_info.get("extracted_conflict_pattern", {})
                st.json({
                    "conflict_type": cp.get("conflict_type"),
                    "escalation_curve": " → ".join(cp.get("escalation_curve", [])),
                    "reversal_count": cp.get("reversal_count"),
                    "highest_stakes": cp.get("highest_stakes"),
                })
            st.markdown(f"**Source:** {graft_info.get('source_viral_script', {}).get('source_title', 'N/A')}")

        # 4. Generated Script
        st.subheader("4. Generated Script")
        st.markdown(f"**Title:** {result.get('title', '')}")
        st.markdown(f"**Core Hook:** {result.get('core_hook', '')}")
        st.markdown(f"**Genre:** {result.get('genre', '')} | **Quality:** {result.get('quality_score', 0):.2f} ({result.get('quality_action', '')})")

        # Show scenes
        scenes = result.get("scenes", [])
        if scenes:
            with st.expander("View Scenes", expanded=True):
                for scene in scenes:
                    st.markdown(f"### Scene {scene.get('id', '?')} — {scene.get('beat_type', '')}")
                    for line in scene.get("dialogue", []):
                        speaker = line.get("speaker", "")
                        text = line.get("text", "")
                        emotion = line.get("emotion", "")
                        st.markdown(f"**{speaker}** ({emotion}): {text}")
                    st.divider()

        # 5. Audio Player
        st.subheader("5. Audio")
        episode_audio_path = result.get("episode_audio_path")
        if episode_audio_path and Path(episode_audio_path).exists():
            st.audio(episode_audio_path)
        else:
            st.info(f"Audio files are in: `{result.get('script_path', '').replace('script.json', 'audio/')}`")

        # 6. Downloads
        st.subheader("6. Downloads")
        run_id = result.get("run_id", "")
        if run_id:
            col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)
            with col_dl1:
                try:
                    pp_data = download_file("prompt_package", run_id)
                    st.download_button(
                        label="📦 Prompt Package",
                        data=pp_data,
                        file_name="prompt_package.json",
                        mime="application/json",
                    )
                except Exception:
                    st.button("📦 Prompt Package", disabled=True)

            with col_dl2:
                try:
                    script_data = download_file("script", run_id)
                    st.download_button(
                        label="📄 Script",
                        data=script_data,
                        file_name="script.json",
                        mime="application/json",
                    )
                except Exception:
                    st.button("📄 Script", disabled=True)

            with col_dl3:
                try:
                    report_data = download_file("report", run_id)
                    st.download_button(
                        label="📊 Report",
                        data=report_data,
                        file_name="production_report.json",
                        mime="application/json",
                    )
                except Exception:
                    st.button("📊 Report", disabled=True)

            with col_dl4:
                try:
                    audio_data = download_file("episode_audio", run_id)
                    st.download_button(
                        label="🎵 Episode Audio",
                        data=audio_data,
                        file_name="episode_audio.mp3",
                        mime="audio/mpeg",
                    )
                except Exception:
                    st.button("🎵 Episode Audio", disabled=True)

    elif final_task and final_task.get("status") == "FAILED":
        st.error(f"❌ Task failed: {final_task.get('error', 'Unknown error')}")

elif generate_clicked and not topic:
    st.warning("Please enter a topic first.")
