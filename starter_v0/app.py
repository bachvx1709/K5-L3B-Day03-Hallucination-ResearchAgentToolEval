from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import assistant_tool_message, execute_tool_call, tool_results_message, trim_history
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
load_lab_env(ROOT)

st.set_page_config(
    page_title="Research Agent - Team Hallucination",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 Research Agent — Team Hallucination")
st.markdown(
    "*Agent nghiên cứu, thẩm định độ tin cậy nguồn tin (`source_credibility`), thống kê văn bản (`text_stats`) & xuất bản an toàn.*"
)

# Sidebar configurations
with st.sidebar:
    st.header("⚙️ Cấu hình Agent")
    provider_name = st.selectbox("Provider", ["openrouter", "openai", "gemini", "anthropic", "ollama"], index=0)
    version = st.text_input("Artifact Version", value="v3")
    history_window = st.number_input("History Window (turns)", min_value=1, max_value=20, value=5)
    max_tool_rounds = st.number_input("Max Tool Rounds", min_value=1, max_value=10, value=4)

    if st.button("🗑️ Xoá lịch sử chat"):
        st.session_state.messages = []
        st.session_state.history = []
        st.session_state.transcript_turns = []
        st.session_state.session_id = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        st.rerun()

    st.markdown("---")
    st.markdown("**Các tool nổi bật:**")
    st.markdown("- `source_credibility`: Thẩm định độ tin cậy URL")
    st.markdown("- `text_stats`: Đếm từ, ký tự, thời gian đọc")
    st.markdown("- `clarify`: Hỏi lại thông tin thiếu & xác nhận")
    st.markdown("- `send`: Gửi Telegram (chỉ khi xác nhận)")

# Init session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "transcript_turns" not in st.session_state:
    st.session_state.transcript_turns = []
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%dT%H%M%S%f")

system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
tools_path = ARTIFACTS_DIR / "tools.yaml"

system_prompt = system_prompt_path.read_text(encoding="utf-8")
tool_declarations = load_tool_declarations(tools_path)
openai_tools = to_openai_tools(tool_declarations)
artifact_version = build_artifact_version(version, system_prompt_path, tools_path)

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "tools" in msg and msg["tools"]:
            with st.expander("🛠️ Tool calls & results"):
                st.json(msg["tools"])

# Handle user input
if prompt := st.chat_input("Nhập câu hỏi hoặc yêu cầu nghiên cứu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    started_at = datetime.now().isoformat(timespec="seconds")
    turn_record = {
        "turn_index": len(st.session_state.transcript_turns) + 1,
        "started_at": started_at,
        "user": prompt,
        "status": "started",
    }

    try:
        provider = make_provider(provider_name)
    except Exception as e:
        st.error(f"Lỗi khởi tạo provider '{provider_name}': {e}. Vui lòng kiểm tra API key trong file .env.")
        st.stop()

    working_messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, history_window),
        {"role": "user", "content": prompt},
    ]

    all_tool_events = []
    final_text = ""
    status = "ok"

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        status_placeholder = st.empty()

        for round_idx in range(1, max_tool_rounds + 1):
            with status_placeholder.status(f"Đang xử lý (vòng {round_idx})..."):
                resp = provider.complete(working_messages, openai_tools, temperature=0.0)

            calls = resp.tool_calls
            if not calls:
                final_text = resp.text or "(Không có phản hồi)"
                message_placeholder.markdown(final_text)
                break

            working_messages.append(assistant_tool_message(resp.text, calls))
            non_clarification_events = []
            clarification_question = None

            for call in calls:
                event = execute_tool_call(call)
                all_tool_events.append(event)
                result = event.get("result", {})
                if isinstance(result, dict) and result.get("awaiting_user"):
                    clarification_question = (
                        result.get("question") or call.args.get("question") or "Bạn bổ sung thêm thông tin nhé."
                    )
                else:
                    non_clarification_events.append(event)

            with st.expander(f"🛠️ Vòng {round_idx}: Gọi {len(calls)} tool", expanded=False):
                st.json([{"name": c.name, "args": c.args} for c in calls])
                st.json(all_tool_events[-len(calls):])

            if clarification_question:
                final_text = clarification_question
                status = "waiting_for_user"
                message_placeholder.markdown(final_text)
                break

            working_messages.append(tool_results_message(non_clarification_events))
        else:
            final_text = f"Đã dừng sau {max_tool_rounds} vòng gọi tool."
            status = "max_tool_rounds"
            message_placeholder.markdown(final_text)

        status_placeholder.empty()

    turn_record["status"] = status
    turn_record["assistant"] = final_text
    turn_record["tool_events"] = all_tool_events
    turn_record["finished_at"] = datetime.now().isoformat(timespec="seconds")

    st.session_state.messages.append(
        {"role": "assistant", "content": final_text, "tools": all_tool_events}
    )
    st.session_state.history.append({"role": "user", "content": prompt})
    st.session_state.history.append({"role": "assistant", "content": final_text})
    st.session_state.transcript_turns.append(turn_record)

    # Save transcript
    transcript_id = f"{version}_{provider_name}_{st.session_state.session_id}"
    transcript_path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"
    transcript_data = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": getattr(provider, "default_model", None),
        "system_prompt": str(system_prompt_path),
        "tools": str(tools_path),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": started_at,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "turns": st.session_state.transcript_turns,
    }
    transcript_path.write_text(json.dumps(transcript_data, ensure_ascii=False, indent=2), encoding="utf-8")
