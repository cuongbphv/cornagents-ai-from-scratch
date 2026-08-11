#!/usr/bin/env python3
"""
generate_quiz.py — Sinh quiz + solution cho từng tuần từ một nguồn chân lý duy nhất.

NGUỒN: scripts/quiz_bank.json
ĐẦU RA:
  - Week-XX/quiz.md            (chỉ câu hỏi — để tự kiểm tra)
  - Week-XX/quiz_solution.md   (đáp án + giải thích)
  - Report/assets/js/quiz-data.js  (window.QUIZ_DATA cho web portal — render Q&A flip-card)

CÁCH DÙNG
  # Sinh lại tất cả file từ quiz_bank.json (mặc định, không cần mạng/API):
  python scripts/generate_quiz.py

  # Chỉ một tuần:
  python scripts/generate_quiz.py --week 3

  # Dùng Claude API tạo thêm câu hỏi MỚI cho tuần 5 (cần ANTHROPIC_API_KEY):
  python scripts/generate_quiz.py --ai --week 5 --num 4
  #   thêm --save để ghi câu mới vào quiz_bank.json (mặc định chỉ thử, không lưu)

GHI CHÚ
  - Phần lõi chỉ dùng thư viện chuẩn của Python → luôn chạy được offline.
  - Chế độ --ai là TÙY CHỌN: nếu thiếu gói `anthropic` hoặc thiếu API key,
    script sẽ cảnh báo và bỏ qua phần AI, vẫn sinh file từ bank tĩnh.
  - Toán trong bank viết dạng plain-text cho dễ bảo trì JSON.
"""

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK_PATH = ROOT / "scripts" / "quiz_bank.json"
QUIZ_DATA_JS = ROOT / "Report" / "assets" / "js" / "quiz-data.js"

LETTERS = ["A", "B", "C", "D", "E", "F"]


# --------------------------------------------------------------------------- #
# Đọc / ghi bank
# --------------------------------------------------------------------------- #
def load_bank() -> dict:
    if not BANK_PATH.exists():
        sys.exit(f"[LỖI] Không thấy quiz bank: {BANK_PATH}")
    with open(BANK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_bank(bank: dict) -> None:
    with open(BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)
    print(f"[OK] Đã ghi lại bank: {BANK_PATH}")


def week_dir(n: int) -> Path:
    return ROOT / f"Week-{n:02d}"


# --------------------------------------------------------------------------- #
# Render Markdown
# --------------------------------------------------------------------------- #
def _qtype_label(q: dict) -> str:
    return "Trắc nghiệm" if q.get("type") == "mcq" else "Tự luận"


def render_quiz_md(week: dict) -> str:
    n, title, qs = week["week"], week["title"], week["questions"]
    out = [
        f"# Tuần {n} — Quiz: {title}",
        "",
        f"> Tự kiểm tra **trước** khi xem solution. Tổng **{len(qs)}** câu. "
        f"Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).",
        "> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại "
        "`python scripts/generate_quiz.py`._",
        "",
    ]
    for i, q in enumerate(qs, 1):
        out.append(f"## Câu {i} ({_qtype_label(q)})")
        out.append("")
        out.append(q["q"])
        out.append("")
        if q.get("type") == "mcq":
            for j, choice in enumerate(q["choices"]):
                out.append(f"- **{LETTERS[j]}.** {choice}")
            out.append("")
    out.append("---")
    out.append("> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, "
               "rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.")
    out.append("")
    return "\n".join(out)


def render_solution_md(week: dict) -> str:
    n, title, qs = week["week"], week["title"], week["questions"]
    out = [
        f"# Tuần {n} — Đáp án & Giải thích: {title}",
        "",
        "> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.",
        "",
    ]
    for i, q in enumerate(qs, 1):
        out.append(f"## Câu {i} ({_qtype_label(q)})")
        out.append("")
        out.append(q["q"])
        out.append("")
        if q.get("type") == "mcq":
            ans_idx = q["answer"]
            for j, choice in enumerate(q["choices"]):
                mark = " ✅" if j == ans_idx else ""
                out.append(f"- **{LETTERS[j]}.** {choice}{mark}")
            out.append("")
            out.append(f"**Đáp án: {LETTERS[ans_idx]}**")
        else:
            out.append(f"**Trả lời mẫu:** {q['answer']}")
        out.append("")
        if q.get("explain"):
            out.append(f"**Giải thích:** {q['explain']}")
            out.append("")
    return "\n".join(out)


def render_quiz_data_js(bank: dict) -> str:
    payload = {
        "meta": bank.get("meta", {}),
        "weeks": [
            {
                "week": w["week"],
                "title": w["title"],
                "questions": w["questions"],
            }
            for w in bank["weeks"]
        ],
    }
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    return (
        "/* Sinh tự động bởi scripts/generate_quiz.py — KHÔNG sửa tay.\n"
        "   Nguồn: scripts/quiz_bank.json */\n"
        f"window.QUIZ_DATA = {body};\n"
    )


# --------------------------------------------------------------------------- #
# Ghi file
# --------------------------------------------------------------------------- #
def write_week_files(week: dict) -> bool:
    n = week["week"]
    d = week_dir(n)
    if not d.exists():
        print(f"[BỎ QUA] Không thấy thư mục {d} (tuần {n}).")
        return False
    (d / "quiz.md").write_text(render_quiz_md(week), encoding="utf-8")
    (d / "quiz_solution.md").write_text(render_solution_md(week), encoding="utf-8")
    print(f"[OK] Tuần {n:>2}: quiz.md + quiz_solution.md ({len(week['questions'])} câu)")
    return True


def write_quiz_data_js(bank: dict) -> None:
    QUIZ_DATA_JS.parent.mkdir(parents=True, exist_ok=True)
    QUIZ_DATA_JS.write_text(render_quiz_data_js(bank), encoding="utf-8")
    print(f"[OK] Portal data: {QUIZ_DATA_JS.relative_to(ROOT)}")


# --------------------------------------------------------------------------- #
# Chế độ AI (tùy chọn) — dùng Claude tạo câu hỏi mới
# --------------------------------------------------------------------------- #
AI_SYSTEM = (
    "Bạn là trợ giảng tạo quiz cho khoá học 'LLM from scratch' (tiếng Việt). "
    "Tạo câu hỏi kiểm tra hiểu biết khái niệm, chính xác về kỹ thuật, súc tích. "
    "Trả về DUY NHẤT một mảng JSON, mỗi phần tử có khoá: "
    "type ('mcq'|'open'), q, (nếu mcq) choices (mảng 4 chuỗi) + answer (chỉ số 0-3), "
    "explain. Không kèm văn bản ngoài JSON. Toán viết dạng plain-text."
)


def generate_ai_questions(week: dict, num: int, model: str):
    """Trả về list câu hỏi mới, hoặc None nếu không khả dụng."""
    try:
        import anthropic  # noqa: F401
    except ImportError:
        print("[AI] Thiếu gói 'anthropic' → bỏ qua. Cài: pip install anthropic")
        return None
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("[AI] Thiếu ANTHROPIC_API_KEY → bỏ qua chế độ AI.")
        return None

    import anthropic
    existing = "\n".join(f"- {q['q']}" for q in week["questions"])
    user = (
        f"Tuần {week['week']}: {week['title']}.\n"
        f"Tạo {num} câu hỏi MỚI (không trùng ý) bổ sung cho các câu đã có sau đây:\n"
        f"{existing}\n\n"
        "Yêu cầu: trộn mcq và open; bám sát chủ đề của tuần; nếu liên quan, "
        "có thể hỏi về các chủ đề nâng cao (RoPE, GQA, KV cache, RMSNorm/SwiGLU, "
        "MoE, quantization, GRPO/RLVR, bits-per-byte...). Trả về JSON array."
    )
    try:
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model=model,
            max_tokens=2000,
            system=AI_SYSTEM,
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        start, end = text.find("["), text.rfind("]")
        if start == -1 or end == -1:
            print("[AI] Không tìm thấy JSON array trong phản hồi → bỏ qua.")
            return None
        new_qs = json.loads(text[start : end + 1])
    except Exception as e:  # noqa: BLE001 — fail mềm cho tiện học
        print(f"[AI] Lỗi khi gọi API ({e}) → bỏ qua, dùng bank tĩnh.")
        return None

    base = f"w{week['week']}ai"
    for k, q in enumerate(new_qs, 1):
        q.setdefault("id", f"{base}{k}")
    print(f"[AI] Đã tạo {len(new_qs)} câu mới cho tuần {week['week']}.")
    return new_qs


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Sinh quiz + solution từ quiz_bank.json")
    ap.add_argument("--week", type=int, default=None, help="Chỉ xử lý 1 tuần (vd. 3). Mặc định: tất cả.")
    ap.add_argument("--ai", action="store_true", help="Dùng Claude API tạo câu hỏi mới (tùy chọn).")
    ap.add_argument("--num", type=int, default=3, help="Số câu hỏi AI tạo thêm mỗi tuần (mặc định 3).")
    ap.add_argument("--model", default="claude-sonnet-4-6", help="Model cho chế độ --ai.")
    ap.add_argument("--save", action="store_true", help="Ghi câu hỏi AI vào quiz_bank.json.")
    args = ap.parse_args()

    bank = load_bank()
    weeks = bank["weeks"]
    targets = [w for w in weeks if args.week is None or w["week"] == args.week]
    if not targets:
        sys.exit(f"[LỖI] Không thấy tuần {args.week} trong bank.")

    if args.ai:
        changed = False
        for w in targets:
            new_qs = generate_ai_questions(w, args.num, args.model)
            if new_qs:
                w["questions"].extend(new_qs)
                changed = True
        if changed and args.save:
            save_bank(bank)
        elif changed:
            print("[AI] (Chưa lưu vào bank — thêm --save nếu muốn giữ.)")

    ok = sum(write_week_files(w) for w in targets)
    write_quiz_data_js(bank)
    print(f"\n[XONG] Sinh xong {ok}/{len(targets)} tuần. Mở Report/index.html để xem flip-card Q&A.")


if __name__ == "__main__":
    main()
