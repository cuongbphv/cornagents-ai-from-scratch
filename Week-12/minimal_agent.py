"""
minimal_agent.py — STARTER Tuần 12. Agent tối thiểu + 1 tool.

Mục tiêu: hiểu vòng lặp agent (LLM quyết định gọi tool -> chạy tool ->
đưa kết quả lại cho LLM -> lặp tới khi xong).

Đây là minh họa với Anthropic SDK (tool use cơ bản). Khi nắm rồi, chuyển
sang Claude Agent SDK / LangGraph cho CornAgents.AI.

Cài:
    pip install anthropic
    export ANTHROPIC_API_KEY=...   # hoặc dùng subscription qua Claude Agent SDK
"""

import json
from pathlib import Path

# ---- 1) Định nghĩa tool: đọc file trong repo ----
TOOLS = [
    {
        "name": "read_file",
        "description": "Đọc nội dung một file văn bản trong thư mục làm việc.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "đường dẫn tương đối"}},
            "required": ["path"],
        },
    }
]


def run_tool(name, args):
    if name == "read_file":
        p = Path(args["path"])
        if not p.exists():
            return f"LỖI: không thấy {p}"
        return p.read_text(encoding="utf-8")[:4000]
    return f"LỖI: tool không xác định {name}"


# ---- 2) Agent loop ----
def agent(user_msg, max_turns=5):
    from anthropic import Anthropic

    client = Anthropic()
    messages = [{"role": "user", "content": user_msg}]

    for turn in range(max_turns):
        resp = client.messages.create(
            model="claude-sonnet-4-6",   # đổi theo model bạn có quyền
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": resp.content})

        # Nếu model không gọi tool -> xong, trả text
        tool_uses = [b for b in resp.content if b.type == "tool_use"]
        if not tool_uses:
            return "".join(b.text for b in resp.content if b.type == "text")

        # Chạy mọi tool model yêu cầu, trả kết quả
        results = []
        for tu in tool_uses:
            out = run_tool(tu.name, tu.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": tu.id,
                "content": out,
            })
        messages.append({"role": "user", "content": results})

    return "Hết số lượt cho phép."


if __name__ == "__main__":
    print(agent("Đọc file README.md và tóm tắt mục tiêu Tuần 12 trong 2 câu."))
