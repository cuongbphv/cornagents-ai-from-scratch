#!/usr/bin/env python3
"""
build_theory_data.py: gom ghi chú lý thuyết của 18 tuần vào một file JS cho portal.

NGUỒN: Week-XX/01_theory_notes.md (Week-04 dùng 02_theory_notes.md)
ĐẦU RA: report/assets/js/theory-data.js  (window.THEORY_DATA = {week: {file, markdown}})

Portal mở bằng file:// nên không fetch được file .md; vì thế nội dung được nhúng
dưới dạng chuỗi Markdown và chuyển sang HTML trong trình duyệt bằng marked
(tải từ cdnjs) khi người dùng mở khối "Ghi chú lý thuyết" của tuần đó.

Chạy sau mỗi lần sửa theory notes:
    python scripts/build_theory_data.py

Chỉ dùng thư viện chuẩn của Python.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "report" / "assets" / "js" / "theory-data.js"


def find_notes(week_dir: Path) -> Path | None:
    for name in ("01_theory_notes.md", "02_theory_notes.md"):
        p = week_dir / name
        if p.exists():
            return p
    return None


def main() -> None:
    data = {}
    for n in range(1, 19):
        d = ROOT / f"Week-{n:02d}"
        p = find_notes(d)
        if p is None:
            print(f"[BỎ QUA] Tuần {n}: không thấy theory notes")
            continue
        md = p.read_text(encoding="utf-8")
        # Bỏ dòng tiêu đề H1 đầu file vì thẻ tuần đã có tiêu đề riêng.
        md = re.sub(r"^# [^\n]*\n+", "", md, count=1)
        data[n] = {"file": f"{d.name}/{p.name}", "words": len(md.split()), "markdown": md}
        print(f"[OK] Tuần {n:>2}: {d.name}/{p.name} ({data[n]['words']} từ)")
    curriculum = json.loads((ROOT / "curriculum.json").read_text(encoding="utf-8"))
    core = {}
    for week in curriculum["weeks"]:
        p = ROOT / week["directory"] / "01_theory_notes.md"
        md = re.sub(r"^# [^\n]*\n+", "", p.read_text(encoding="utf-8"), count=1)
        core[week["week"]] = {"file": str(p.relative_to(ROOT)), "words": len(md.split()), "markdown": md}
    body = json.dumps(data, ensure_ascii=False)
    OUT.write_text(
        "/* Sinh tự động bởi scripts/build_theory_data.py từ Week-XX/*_theory_notes.md. KHÔNG sửa tay. */\n"
        f"window.THEORY_DATA = {body};\n"
        + "window.CORE_THEORY_DATA = " + json.dumps(core, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    print(f"[XONG] {len(data)} tuần fast-track + {len(core)} tuần lịch chính -> {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
