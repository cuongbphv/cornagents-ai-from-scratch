#!/usr/bin/env python3
"""
Kéo dataset license mở đã vet trong Week-00/datasets_finance_banking.md
vào docs/datasets/ (thư mục gitignored, trừ README + MANIFEST).

Chỉ tải bộ nằm trong allowlist license (CC BY / CC0 / MIT / Apache-2.0 / BSD / ODC-By)
và nguồn Gutenberg public domain. Kiểm tra lại license qua Hugging Face API
tại thời điểm chạy.

Bỏ qua (có lý do ghi vào MANIFEST):
  - HuggingFaceFW/fineweb-edu default (~6 TB) — chỉ kéo sample-10BT trên ổ D
  - gbharti/finance-alpaca — card ghi chứa cặp sinh GPT-3.5 + Stanford Alpaca
  - Josephgflowers/Finance-Instruct-500k — card tự nhận nhiễu; ~2 GB
  - TeraflopAI/SEC-EDGAR, eloukas/edgar-corpus — hàng chục–hàng trăm GB

Chạy:
  python scripts/download_datasets.py
  python scripts/download_datasets.py --only banking77,uts2017
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import shutil
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "datasets"
HF_API = "https://huggingface.co/api/datasets/"
ALLOWED = {
    "apache-2.0",
    "mit",
    "bsd-2-clause",
    "bsd-3-clause",
    "bsd-3",
    "cc-by-4.0",
    "cc-by-3.0",
    "cc-by-2.0",
    "cc0-1.0",
    "cc0",
    "odc-by",
    "public-domain",
}
TODAY = date.today().isoformat()
UA = "cornagents-ai-from-scratch/dataset-prep (academic, research-only)"


def log(msg: str) -> None:
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((msg + "\n").encode("utf-8", errors="replace"))
        sys.stdout.buffer.flush()


def write_jsonl(path: Path, rows: list) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def http_get(url: str, dest: Path | None = None, timeout: int = 120):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    if dest is not None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    return data


def hf_card(repo_id: str) -> dict:
    raw = http_get(HF_API + repo_id)
    return json.loads(raw.decode("utf-8"))


def extract_license(card: dict) -> str:
    cd = card.get("cardData") or {}
    lic = cd.get("license")
    if isinstance(lic, list):
        lic = lic[0] if lic else ""
    if not lic:
        for tag in card.get("tags") or []:
            if isinstance(tag, str) and tag.startswith("license:"):
                lic = tag.split(":", 1)[1]
                break
    return str(lic or "").strip().lower()


def assert_allowed(repo_id: str, license_id: str) -> None:
    if license_id not in ALLOWED:
        raise RuntimeError(
            f"{repo_id}: license '{license_id}' không nằm trong allowlist "
            f"{sorted(ALLOWED)}"
        )


def load_hf(repo_id: str, **kwargs):
    from datasets import load_dataset

    cache = OUT / ".hf_cache"
    cache.mkdir(parents=True, exist_ok=True)
    kwargs.setdefault("cache_dir", str(cache))
    return load_dataset(repo_id, **kwargs)


def rows_from_split(ds, split: str, limit: int | None = None) -> list:
    part = ds[split] if split in ds else ds
    out = []
    for i, row in enumerate(part):
        if limit is not None and i >= limit:
            break
        item = dict(row)
        item.pop("image", None)
        out.append(item)
    return out


def record(manifest: list, **kwargs) -> None:
    kwargs.setdefault("checked_on", TODAY)
    manifest.append(kwargs)
    status = kwargs.get("status", "?")
    name = kwargs.get("id", "")
    note = kwargs.get("note", "")
    log(f"  [{status}] {name}  {note}")


# ---------------------------------------------------------------------------
# Từng nguồn
# ---------------------------------------------------------------------------

def pull_uts2017(manifest: list) -> None:
    repo = "undertheseanlp/UTS2017_Bank"
    card = hf_card(repo)
    lic = extract_license(card)
    assert_allowed(repo, lic)
    dest = OUT / "finetune_vi" / "UTS2017_Bank"
    total = 0
    for config in ("classification", "sentiment", "aspect_sentiment"):
        ds = load_hf(repo, name=config)
        for split in ds:
            n = write_jsonl(dest / f"{config}_{split}.jsonl", rows_from_split(ds, split))
            total += n
    record(
        manifest,
        id=repo,
        license=lic,
        week="8",
        purpose="finetune_vi_classification",
        status="ok",
        rows=total,
        path=str(dest.relative_to(ROOT)),
        note=f"{total} dòng, 3 config × train/test",
    )


def pull_legal_instruct_sample(manifest: list) -> None:
    repo = "duyet/vietnamese-legal-instruct"
    card = hf_card(repo)
    lic = extract_license(card)
    assert_allowed(repo, lic)
    dest = OUT / "finetune_vi"
    # usedStorage ~5.9 GB — chỉ lấy mẫu đủ cho QLoRA 500–1000 + held-out
    train = load_hf(repo, split="train", streaming=True)
    test = load_hf(repo, split="test", streaming=True)
    train_rows = [dict(r) for _, r in zip(range(4000), train)]
    test_rows = [dict(r) for _, r in zip(range(500), test)]
    n1 = write_jsonl(dest / "vietnamese-legal-instruct.train.sample.jsonl", train_rows)
    n2 = write_jsonl(dest / "vietnamese-legal-instruct.test.sample.jsonl", test_rows)
    record(
        manifest,
        id=repo,
        license=lic,
        week="8",
        purpose="finetune_vi_instruction",
        status="ok_sample",
        rows=n1 + n2,
        path=str(dest.relative_to(ROOT)),
        note=f"sample {n1} train + {n2} test (full repo ~5.9 GB, không kéo hết)",
    )


def pull_banking77(manifest: list) -> None:
    # HF datasets 4.x từ chối banking77.py (script dataset).
    # Nguồn gốc cùng license CC BY 4.0: PolyAI-LDN/task-specific-datasets.
    repo = "PolyAI/banking77"
    card = hf_card(repo)
    lic = extract_license(card)
    assert_allowed(repo, lic)
    dest = OUT / "finetune_en" / "banking77"
    base = (
        "https://raw.githubusercontent.com/PolyAI-LDN/"
        "task-specific-datasets/master/banking_data/"
    )
    total = 0
    for split in ("train", "test"):
        raw = http_get(base + f"{split}.csv").decode("utf-8")
        reader = csv.reader(io.StringIO(raw))
        rows = []
        for i, parts in enumerate(reader):
            if not parts:
                continue
            if i == 0 and parts[0].lower() in {"text", "query", "sentence"}:
                continue
            text, label = parts[0], parts[1] if len(parts) > 1 else ""
            rows.append({"text": text, "label": label})
        total += write_jsonl(dest / f"{split}.jsonl", rows)
    write_text(
        dest / "SOURCE.txt",
        "BANKING77 — Casanueva et al. 2020, CC BY 4.0\n"
        "HF card: https://huggingface.co/datasets/PolyAI/banking77\n"
        "Files: https://github.com/PolyAI-LDN/task-specific-datasets "
        "(LICENSE = CC BY 4.0, kiểm 2026-08-16)\n",
    )
    record(
        manifest,
        id=repo,
        license=lic,
        week="8,13",
        purpose="intent_routing",
        status="ok",
        rows=total,
        path=str(dest.relative_to(ROOT)),
        note=f"{total} câu từ GitHub PolyAI (HF script dataset không còn chạy)",
    )


def pull_sujet(manifest: list) -> None:
    repo = "Sujet-AI/Sujet-Finance-Instruct-177k"
    card = hf_card(repo)
    lic = extract_license(card)
    assert_allowed(repo, lic)
    dest = OUT / "finetune_en" / "sujet-finance-instruct-177k"
    ds = load_hf(repo)
    total = 0
    for split in ds:
        total += write_jsonl(dest / f"{split}.jsonl", rows_from_split(ds, split))
    record(
        manifest,
        id=repo,
        license=lic,
        week="8",
        purpose="finetune_en_instruction",
        status="ok",
        rows=total,
        path=str(dest.relative_to(ROOT)),
        note=f"{total} dòng — lựa chọn mặc định Tuần 8",
    )


def pull_fingpt_sentiment(manifest: list) -> None:
    repo = "flwrlabs/fingpt-sentiment-train"
    card = hf_card(repo)
    lic = extract_license(card)
    assert_allowed(repo, lic)
    dest = OUT / "finetune_en"
    ds = load_hf(repo)
    rows = rows_from_split(ds, "train")
    n = write_jsonl(dest / "fingpt-sentiment-train.jsonl", rows)
    record(
        manifest,
        id=repo,
        license=lic,
        week="8",
        purpose="finetune_en_sentiment",
        status="ok",
        rows=n,
        path=str((dest / "fingpt-sentiment-train.jsonl").relative_to(ROOT)),
        note=f"{n} dòng instruction/input/output",
    )


def pull_vnpdf_text(manifest: list) -> None:
    repo = "kiethuynhanh/vnpdf-financial-reports-dataset"
    card = hf_card(repo)
    lic = extract_license(card)
    assert_allowed(repo, lic)
    dest = OUT / "ocr_test"
    ds = load_hf(repo)
    rows = rows_from_split(ds, "train")  # image đã bị bỏ
    n = write_jsonl(dest / "vnpdf-financial-reports.text.jsonl", rows)
    record(
        manifest,
        id=repo,
        license=lic,
        week="10",
        purpose="ocr_pipeline_test",
        status="ok",
        rows=n,
        path=str((dest / "vnpdf-financial-reports.text.jsonl").relative_to(ROOT)),
        note=f"{n} trang, chỉ text (bỏ image để tiết kiệm đĩa)",
    )


def pull_bizbench(manifest: list) -> None:
    repo = "kensho/bizbench"
    card = hf_card(repo)
    lic = extract_license(card)
    assert_allowed(repo, lic)
    dest = OUT / "eval" / "bizbench"
    ds = load_hf(repo)
    total = 0
    for split in ds:
        total += write_jsonl(dest / f"{split}.jsonl", rows_from_split(ds, split))
    record(
        manifest,
        id=repo,
        license=lic,
        week="8,15",
        purpose="held_out_eval",
        status="ok",
        rows=total,
        path=str(dest.relative_to(ROOT)),
        note=f"{total} dòng — giữ nguyên, không đưa vào train",
    )


def _is_nhnn(row: dict) -> bool:
    blob = " ".join(
        str(row.get(k) or "")
        for k in ("co_quan_ban_hanh", "nganh", "linh_vuc", "title", "nguon_thu_thap")
    ).lower()
    keys = (
        "ngân hàng nhà nước",
        "ngan hang nha nuoc",
        "nhnn",
        "state bank of vietnam",
    )
    return any(k in blob for k in keys)


def pull_legal_documents_nhnn(manifest: list) -> None:
    repo = "th1nhng0/vietnamese-legal-documents"
    card = hf_card(repo)
    lic = extract_license(card)
    assert_allowed(repo, lic)
    dest = OUT / "rag_kg" / "vietnamese-legal-documents"
    meta = load_hf(repo, name="metadata", split="data")
    nhnn_meta = [dict(r) for r in meta if _is_nhnn(r)]
    # Tuần 10–14 không cần cả kho; giữ tối đa 400 văn bản + metadata đầy đủ của phần lọc
    cap = 400
    chosen = nhnn_meta[:cap]
    ids = {r["id"] for r in chosen if r.get("id")}
    write_jsonl(dest / "metadata_nhnn.all_filtered.jsonl", nhnn_meta)
    write_jsonl(dest / "metadata_nhnn.cap400.jsonl", chosen)

    content = load_hf(repo, name="content", split="data")
    content_rows = [dict(r) for r in content if r.get("id") in ids]
    write_jsonl(dest / "content_nhnn.cap400.jsonl", content_rows)

    rel = load_hf(repo, name="relationships", split="data")
    rel_rows = [
        dict(r)
        for r in rel
        if r.get("doc_id") in ids or r.get("other_doc_id") in ids
    ]
    write_jsonl(dest / "relationships_nhnn.cap400.jsonl", rel_rows)

    record(
        manifest,
        id=repo,
        license=lic,
        week="10,14",
        purpose="rag_kg_nhnn",
        status="ok_sample",
        rows=len(content_rows),
        path=str(dest.relative_to(ROOT)),
        note=(
            f"filter NHNN: {len(nhnn_meta)} metadata; "
            f"kéo content {len(content_rows)}/{cap}; "
            f"relationships {len(rel_rows)}. "
            "Full content.parquet ~785 MB download — không kéo hết."
        ),
    )


def pull_yuitc_eval(manifest: list) -> None:
    repo = "YuITC/Vietnamese-Legal-Documents"
    card = hf_card(repo)
    lic = extract_license(card)
    assert_allowed(repo, lic)
    dest = OUT / "eval" / "YuITC-Vietnamese-Legal-Documents"
    # usedStorage ~1.3 GB; giữ train/test đầy đủ, corpus chỉ doc được query trỏ tới
    ds = load_hf(repo)
    queries = []
    for split in ("train", "test"):
        if split in ds:
            rows = rows_from_split(ds, split)
            write_jsonl(dest / f"{split}.jsonl", rows)
            queries.extend(rows)

    needed: set[str] = set()
    for q in queries:
        for key in ("positive", "positive_passages", "relevant_docs", "doc_ids"):
            val = q.get(key)
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, str):
                        needed.add(item)
                    elif isinstance(item, dict) and item.get("id"):
                        needed.add(str(item["id"]))
        for key in ("corpus_id", "doc_id", "document_id"):
            if q.get(key):
                needed.add(str(q[key]))

    corpus_kept = []
    if "corpus" in ds:
        for row in ds["corpus"]:
            rid = str(row.get("id") or row.get("_id") or row.get("doc_id") or "")
            if not needed or rid in needed:
                item = dict(row)
                item.pop("image", None)
                corpus_kept.append(item)
                if not needed and len(corpus_kept) >= 8000:
                    break
    elif needed:
        # một số bản để corpus ở config riêng
        try:
            corpus = load_hf(repo, name="corpus")
            split = list(corpus.keys())[0]
            for row in corpus[split]:
                rid = str(row.get("id") or row.get("_id") or "")
                if rid in needed:
                    corpus_kept.append(dict(row))
        except Exception as exc:  # noqa: BLE001 — ghi nhận, không làm hỏng các bộ khác
            log(f"    (cảnh báo corpus YuITC: {type(exc).__name__}: {exc})")

    empty_corpus = dest / "corpus.referenced_or_sample.jsonl"
    if corpus_kept:
        write_jsonl(empty_corpus, corpus_kept)
    elif empty_corpus.exists():
        empty_corpus.unlink()
    write_text(
        dest / "SOURCE.txt",
        "YuITC/Vietnamese-Legal-Documents — MIT\n"
        "train/test đã chứa question + context_list + cid.\n"
        "Không kéo corpus.parquet (~1 GB): đoạn liên quan đã nằm trong query.\n",
    )
    record(
        manifest,
        id=repo,
        license=lic,
        week="11",
        purpose="retrieval_eval",
        status="ok",
        rows=len(queries),
        path=str(dest.relative_to(ROOT)),
        note=(
            f"queries {len(queries)} (mỗi dòng đã có context_list). "
            "Bỏ corpus.parquet để tiết kiệm đĩa."
        ),
    )


def pull_gutenberg(manifest: list) -> None:
    dest = OUT / "w05_pretrain"
    # Alice in Wonderland — public domain; URL ổn định của Project Gutenberg
    url = "https://www.gutenberg.org/files/11/11-0.txt"
    path = dest / "gutenberg_11_alice_in_wonderland.txt"
    try:
        http_get(url, path, timeout=60)
    except urllib.error.URLError:
        url = "https://www.gutenberg.org/cache/epub/11/pg11.txt"
        http_get(url, path, timeout=60)
    write_text(
        dest / "SOURCE.txt",
        "Project Gutenberg eBook #11 — Alice's Adventures in Wonderland\n"
        f"URL: {url}\n"
        "Status: public domain in the USA (Project Gutenberg header in the file).\n"
        f"Downloaded: {TODAY}\n"
        "Dùng cho Tuần 5: validate training loop local trên 3070 Ti.\n",
    )
    record(
        manifest,
        id="gutenberg:11",
        license="public-domain",
        week="5",
        purpose="pretrain_local_smoke",
        status="ok",
        rows=1,
        path=str(path.relative_to(ROOT)),
        note="Alice in Wonderland — text public domain, validate loop Tuần 5",
        source_url=url,
    )


def pull_cfpb_glossary(manifest: list) -> None:
    url = (
        "https://files.consumerfinance.gov/f/documents/"
        "cfpb_adult-fin-ed_vietnamese-style-guide-glossary.pdf"
    )
    dest = OUT / "glossary" / "cfpb_vietnamese_english_glossary.pdf"
    pointer = OUT / "glossary" / "SOURCE.txt"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "application/pdf,*/*",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(resp.read())
        status = "ok_unverified_terms"
        note = (
            "Tác phẩm cơ quan liên bang Mỹ (CFPB, 3/2024). "
            "[Chưa xác minh] tuyên bố quyền chính xác — chỉ dùng làm glossary, "
            "không đưa vào tập train weight."
        )
        path = str(dest.relative_to(ROOT))
    except urllib.error.HTTPError as exc:
        write_text(
            pointer,
            "CFPB Vietnamese-English Glossary of Financial Terms (3/2024)\n"
            f"URL: {url}\n"
            f"Auto-download failed: HTTP {exc.code} {exc.reason}\n"
            "Tải tay vào file cfpb_vietnamese_english_glossary.pdf trong thư mục này.\n"
            "[Chưa xác minh] tuyên bố quyền — không đưa vào tập train weight.\n",
        )
        status = "pointer_only"
        note = f"HTTP {exc.code} từ files.consumerfinance.gov — để URL trong SOURCE.txt"
        path = str(pointer.relative_to(ROOT))
    record(
        manifest,
        id="cfpb-vi-en-glossary",
        license="us-federal-work-unverified-terms",
        week="8,9",
        purpose="bilingual_terminology",
        status=status,
        rows=1,
        path=path,
        note=note,
        source_url=url,
    )


def skip_known(manifest: list) -> None:
    skips = [
        {
            "id": "HuggingFaceFW/fineweb-edu",
            "license": "odc-by",
            "week": "5",
            "purpose": "pretrain_cloud",
            "status": "on_D",
            "note": (
                "ODC-By chấp nhận 2026-08-16. sample-10BT ở "
                "D:\\AI\\datasets\\w05_pretrain\\fineweb-edu. Không kéo default ~6 TB."
            ),
        },
        {
            "id": "gbharti/finance-alpaca",
            "license": "mit",
            "week": "8",
            "purpose": "finetune_en_instruction",
            "status": "skipped",
            "note": (
                "Card HF ghi kết hợp Stanford Alpaca + cặp sinh GPT-3.5. "
                "CLAUDE.md cấm data sinh từ model đóng."
            ),
        },
        {
            "id": "Josephgflowers/Finance-Instruct-500k",
            "license": "apache-2.0",
            "week": "8",
            "purpose": "finetune_en_instruction",
            "status": "skipped",
            "note": "Card tự nhận nhiễu/PII tổng hợp; usedStorage ~2 GB. Không kéo thô.",
        },
        {
            "id": "TeraflopAI/SEC-EDGAR",
            "license": "apache-2.0",
            "week": "10",
            "purpose": "rag_pretrain_corpus",
            "status": "skipped",
            "note": "590 GB — ngoài phạm vi máy học. Pointer trong datasets_finance_banking.md.",
        },
        {
            "id": "eloukas/edgar-corpus",
            "license": "apache-2.0",
            "week": "10",
            "purpose": "rag_pretrain_corpus",
            "status": "skipped",
            "note": "40.7 GB — không kéo. Dùng corpus NHNN đã lọc cho RAG.",
        },
    ]
    for item in skips:
        record(manifest, **item)


JOBS = {
    "uts2017": pull_uts2017,
    "legal_instruct": pull_legal_instruct_sample,
    "banking77": pull_banking77,
    "sujet": pull_sujet,
    "fingpt": pull_fingpt_sentiment,
    "vnpdf": pull_vnpdf_text,
    "bizbench": pull_bizbench,
    "legal_nhnn": pull_legal_documents_nhnn,
    "yuitc": pull_yuitc_eval,
    "gutenberg": pull_gutenberg,
    "cfpb": pull_cfpb_glossary,
}


def write_readme(manifest: list) -> None:
    lines = [
        "# Datasets local (không commit file nặng)",
        "",
        f"Kéo ngày **{TODAY}** bằng `python scripts/download_datasets.py`.",
        "Nguồn vet: [`Week-00/datasets_finance_banking.md`](../../Week-00/datasets_finance_banking.md).",
        "License kiểm lại qua Hugging Face API ngay trước khi tải.",
        "",
        "File nặng nằm trong thư mục này và **không** vào git (xem `.gitignore`).",
        "`README.md` + `MANIFEST.json` thì commit được.",
        "",
        "## Đã kéo / đã bỏ",
        "",
        "| id | tuần | license | status | ghi chú |",
        "|---|---|---|---|---|",
    ]
    for item in manifest:
        note = (item.get("note") or "").replace("|", "/")
        lines.append(
            f"| `{item.get('id')}` | {item.get('week', '')} | "
            f"{item.get('license', '')} | {item.get('status', '')} | {note} |"
        )
    lines += [
        "",
        "## Map nhanh khi học Tuần 1–2 xong",
        "",
        "- Tuần 5 (smoke local): `w05_pretrain/gutenberg_11_alice_in_wonderland.txt`",
        "- Tuần 5 (pretrain cloud): `D:\\AI\\datasets\\w05_pretrain\\fineweb-edu` (sample-10BT, ODC-By)",
        "- Tuần 8 (QLoRA hành vi): `finetune_en/sujet-finance-instruct-177k/` + "
        "`finetune_vi/vietnamese-legal-instruct.*.sample.jsonl` + `UTS2017_Bank/`",
        "- Tuần 8/13 (routing): `finetune_en/banking77/`",
        "- Tuần 8/15 (eval, không train): `eval/bizbench/`",
        "- Tuần 10–14 (RAG/KG): `rag_kg/vietnamese-legal-documents/`",
        "- Tuần 11 (đo retriever): `eval/YuITC-Vietnamese-Legal-Documents/`",
        "",
        "Kiến thức quy định **không** nhồi vào weight — đọc mục 0 của tài liệu dataset.",
        "",
    ]
    write_text(OUT / "README.md", "\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--only",
        default="",
        help="Danh sách job cách nhau bởi dấu phẩy: " + ",".join(JOBS),
    )
    args = parser.parse_args()
    wanted = [s.strip() for s in args.only.split(",") if s.strip()] if args.only else list(JOBS)

    unknown = [w for w in wanted if w not in JOBS]
    if unknown:
        log("Job không tồn tại: " + ", ".join(unknown))
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    manifest: list = []
    existing_path = OUT / "MANIFEST.json"
    if args.only and existing_path.exists():
        try:
            manifest = json.loads(existing_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            manifest = []
    skip_known(manifest)
    # skip_known + job mới: ghi đè theo id
    by_id = {item.get("id"): item for item in manifest if item.get("id")}
    manifest = list(by_id.values())

    failed = []
    for name in wanted:
        log(f"\n== {name} ==")
        try:
            JOBS[name](manifest)
        except Exception as exc:  # noqa: BLE001 — từng nguồn độc lập
            failed.append(name)
            record(
                manifest,
                id=name,
                status="error",
                note=f"{type(exc).__name__}: {exc}",
            )

    by_id = {}
    for item in manifest:
        key = item.get("id")
        if key:
            by_id[key] = item
    manifest = list(by_id.values())
    (OUT / "MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_readme(manifest)

    cache = OUT / ".hf_cache"
    if cache.exists():
        shutil.rmtree(cache, ignore_errors=True)
        log("Đã xóa docs/datasets/.hf_cache sau khi xuất JSONL.")

    log("\n--- xong ---")
    log(f"MANIFEST: {OUT / 'MANIFEST.json'}")
    if failed:
        log("Lỗi: " + ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
