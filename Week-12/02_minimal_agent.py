"""
02_minimal_agent.py — SKELETON Tuần 12. Agent tối thiểu + 1 tool.

Mục tiêu: TỰ TAY code vòng lặp agent (LLM quyết định gọi tool -> chạy tool ->
đưa kết quả lại cho LLM -> lặp tới khi xong).
Chỗ TODO là phần bạn điền. Tự làm trước, đối chiếu docs Claude Agent SDK sau.

Đây là minh họa với Anthropic SDK (tool use cơ bản). Khi nắm rồi, chuyển
sang Claude Agent SDK / LangGraph cho CornAgents.AI.

Cài:
    pip install anthropic
    export ANTHROPIC_API_KEY=...   # hoặc dùng subscription qua Claude Agent SDK
"""

from pathlib import Path

# ---- 1) Định nghĩa tool: đọc file trong repo ----
# TODO 1: khai báo schema tool `read_file` theo format tool use của Anthropic.
#   Mỗi tool là 1 dict gồm: "name", "description" (model đọc cái này để quyết
#   định khi nào gọi), và "input_schema" (JSON Schema: type object, properties
#   có "path" kiểu string, required ["path"]).
TOOLS = []  # TODO: điền schema


def run_tool(name, args):
    """Dispatch: nhận (tên tool, args) từ model -> chạy -> trả string."""
    # TODO 2: dispatch theo `name`:
    #   - name == "read_file": đọc Path(args["path"]), trả tối đa ~4000 ký tự
    #   - tên lạ: KHÔNG raise — trả string "LỖI: tool không xác định ..."
    # TODO 3: xử lý lỗi tool: file không tồn tại / đọc fail -> cũng trả STRING
    #   mô tả lỗi (vd. f"LỖI: không thấy {p}") thay vì để exception nổ vòng lặp.
    #   Bọc lỗi thành DATA đưa lại cho model — Tuần 13 sẽ học vì sao (model
    #   có thể tự sửa: đổi path, hỏi lại người dùng...).
    raise NotImplementedError("TODO: dispatch + error handling cho tool")


# ---- 2) Agent loop ----
def agent(user_msg, max_turns=5):
    from anthropic import Anthropic

    client = Anthropic()
    messages = [{"role": "user", "content": user_msg}]

    # TODO 4: ngân sách vòng lặp — vì sao cần max_turns? (tầng 4 — Loop
    #   engineering: run → check → decide; không có budget = agent chạy mãi).
    #   Giữ for-loop hữu hạn, KHÔNG dùng while True.
    for turn in range(max_turns):
        resp = client.messages.create(
            model="claude-sonnet-4-6",   # đổi theo model bạn có quyền
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )
        # TODO 5: append NGUYÊN VĂN assistant turn vào messages
        #   ({"role": "assistant", "content": resp.content}) — thiếu bước này
        #   API sẽ báo lỗi vì tool_result không có tool_use tương ứng.

        # TODO 6: điều kiện dừng — lọc các block b.type == "tool_use" trong
        #   resp.content. Nếu KHÔNG có tool_use nào -> model đã xong: return
        #   phần text ("".join các block b.type == "text").

        # TODO 7: với MỖI tool_use tu: gọi run_tool(tu.name, tu.input), gói
        #   kết quả thành {"type": "tool_result", "tool_use_id": tu.id,
        #   "content": out}, gom thành list rồi append vào messages với
        #   role="user" — vòng lặp quay lại đưa kết quả cho model.
        raise NotImplementedError("TODO: thân vòng lặp agent (TODO 5–7)")

    return "Hết số lượt cho phép."


if __name__ == "__main__":
    print(agent("Đọc file README.md và tóm tắt mục tiêu Tuần 12 trong 2 câu."))
