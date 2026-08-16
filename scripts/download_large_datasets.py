#!/usr/bin/env python3
"""
Kéo bản ĐẦY ĐỦ các dataset lớn (license mở đã vet) vào ổ D.

Mặc định: D:/AI/datasets
Giữ file gốc (parquet/json) — không chuyển JSONL để khỏi nhân đôi dung lượng.

Bỏ:
  - FineWeb-Edu default (~6 TB) — chỉ kéo config sample-10BT
  - TeraflopAI/SEC-EDGAR (~590 GB, không vừa ổ D)
  - gbharti/finance-alpaca (data sinh GPT-3.5)

Chạy:
  python scripts/download_large_datasets.py
  python scripts/download_large_datasets.py --root D:/AI/datasets --only legal_docs,yuitc
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
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
}
TODAY = date.today().isoformat()
DEFAULT_ROOT = Path("D:/AI/datasets")


def log(msg: str) -> None:
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((msg + "\n").encode("utf-8", errors="replace"))
        sys.stdout.buffer.flush()


def hf_card(repo_id: str) -> dict:
    req = urllib.request.Request(
        HF_API + repo_id,
        headers={"User-Agent": "cornagents-ai-from-scratch/large-dataset-prep"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


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
        raise RuntimeError(f"{repo_id}: license '{license_id}' ngoài allowlist")


def dir_size(path: Path) -> int:
    total = 0
    if not path.exists():
        return 0
    for p in path.rglob("*"):
        if p.is_file():
            total += p.stat().st_size
    return total


def snapshot(
    repo_id: str,
    dest: Path,
    *,
    allow_patterns: list[str] | None = None,
    ignore_patterns: list[str] | None = None,
) -> Path:
    from huggingface_hub import snapshot_download

    dest.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=repo_id,
        repo_type="dataset",
        local_dir=str(dest),
        allow_patterns=allow_patterns,
        ignore_patterns=ignore_patterns,
        max_workers=4,
    )
    return dest


def record(manifest: list, **kwargs) -> None:
    kwargs.setdefault("checked_on", TODAY)
    manifest.append(kwargs)
    log(f"  [{kwargs.get('status')}] {kwargs.get('id')}  {kwargs.get('note', '')}")


def pull_legal_docs(large_root: Path, manifest: list) -> None:
    repo = "th1nhng0/vietnamese-legal-documents"
    lic = extract_license(hf_card(repo))
    assert_allowed(repo, lic)
    dest = large_root / "rag_kg" / "vietnamese-legal-documents"
    snapshot(
        repo,
        dest,
        allow_patterns=["data/*", "README.md", "CHANGELOG.md"],
        ignore_patterns=["legacy/*", "crawler/*"],
    )
    record(
        manifest,
        id=repo,
        license=lic,
        week="10,14",
        purpose="rag_kg_full",
        status="ok_full",
        path=str(dest),
        bytes=dir_size(dest),
        note="Bản đầy đủ data/*.parquet (bỏ legacy/crawler). Sample 400 doc vẫn ở docs/datasets/.",
    )


def pull_legal_instruct(large_root: Path, manifest: list) -> None:
    repo = "duyet/vietnamese-legal-instruct"
    lic = extract_license(hf_card(repo))
    assert_allowed(repo, lic)
    dest = large_root / "finetune_vi" / "vietnamese-legal-instruct"
    snapshot(repo, dest, allow_patterns=["data/*", "README.md"])
    record(
        manifest,
        id=repo,
        license=lic,
        week="8",
        purpose="finetune_vi_instruction_full",
        status="ok_full",
        path=str(dest),
        bytes=dir_size(dest),
        note="Full instruction pairs. Sample 4500 dòng vẫn ở docs/datasets/.",
    )


def pull_yuitc(large_root: Path, manifest: list) -> None:
    repo = "YuITC/Vietnamese-Legal-Documents"
    lic = extract_license(hf_card(repo))
    assert_allowed(repo, lic)
    dest = large_root / "eval" / "YuITC-Vietnamese-Legal-Documents"
    snapshot(repo, dest, allow_patterns=["*.parquet", "README.md"])
    record(
        manifest,
        id=repo,
        license=lic,
        week="11",
        purpose="retrieval_eval_full",
        status="ok_full",
        path=str(dest),
        bytes=dir_size(dest),
        note="Full corpus + train/test parquet.",
    )


def pull_edgar(large_root: Path, manifest: list) -> None:
    repo = "eloukas/edgar-corpus"
    lic = extract_license(hf_card(repo))
    assert_allowed(repo, lic)
    dest = large_root / "rag_en" / "edgar-corpus"
    snapshot(repo, dest)
    record(
        manifest,
        id=repo,
        license=lic,
        week="10",
        purpose="rag_en_10k",
        status="ok_full",
        path=str(dest),
        bytes=dir_size(dest),
        note="10-K 1993–2020, Apache 2.0. Catalog ghi ~40.7 GB.",
    )


def pull_finance_500k(large_root: Path, manifest: list) -> None:
    repo = "Josephgflowers/Finance-Instruct-500k"
    lic = extract_license(hf_card(repo))
    assert_allowed(repo, lic)
    dest = large_root / "finetune_en" / "Finance-Instruct-500k"
    snapshot(repo, dest, allow_patterns=["train.json", "README.md"])
    (dest / "WARNING.txt").write_text(
        "Card HF tự nhận nhiễu (malformed portions) và PII tổng hợp.\n"
        "KHÔNG train thô. Phải filter trước khi đưa vào QLoRA.\n"
        f"Kéo ngày {TODAY}. License: {lic}.\n",
        encoding="utf-8",
    )
    record(
        manifest,
        id=repo,
        license=lic,
        week="8",
        purpose="finetune_en_instruction_noisy",
        status="ok_full_must_filter",
        path=str(dest),
        bytes=dir_size(dest),
        note="Đã kéo + WARNING.txt. Không train thô.",
    )


def pull_fineweb_edu(large_root: Path, manifest: list) -> None:
    repo = "HuggingFaceFW/fineweb-edu"
    lic = extract_license(hf_card(repo))
    assert_allowed(repo, lic)
    dest = large_root / "w05_pretrain" / "fineweb-edu"
    snapshot(
        repo,
        dest,
        allow_patterns=["sample/10BT/*", "README.md"],
    )
    (dest / "SOURCE.txt").write_text(
        "Contains information from FineWeb-Edu (HuggingFaceFW/fineweb-edu)\n"
        "which is made available under the ODC Attribution License.\n"
        "https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu\n"
        "https://opendatacommons.org/licenses/by/1-0/\n"
        f"\nConfig: sample-10BT. Pulled {TODAY}.\n"
        "Owner accepted ODC-By for this academic repo on 2026-08-16.\n"
        "Do not download the default split (~6 TB) onto this machine.\n",
        encoding="utf-8",
    )
    record(
        manifest,
        id=repo,
        license=lic,
        week="5",
        purpose="pretrain_cloud",
        status="ok_sample_10BT",
        path=str(dest),
        bytes=dir_size(dest),
        note="sample-10BT parquet + README. ODC-By, ghi nguồn trong SOURCE.txt. Không kéo default ~6 TB.",
    )


JOBS = {
    "legal_docs": pull_legal_docs,
    "legal_instruct": pull_legal_instruct,
    "yuitc": pull_yuitc,
    "finance_500k": pull_finance_500k,
    "edgar": pull_edgar,
    "fineweb": pull_fineweb_edu,
}


def write_readme(large_root: Path, manifest: list) -> None:
    lines = [
        "# Datasets lớn (ổ D)",
        "",
        f"Kéo ngày **{TODAY}** bằng `python scripts/download_large_datasets.py`.",
        f"Thư mục: `{large_root}`.",
        "Bộ nhỏ / sample vẫn ở `docs/datasets/` trong repo.",
        "",
        "| id | tuần | license | status | bytes | ghi chú |",
        "|---|---|---|---|---|---|",
    ]
    for item in manifest:
        note = (item.get("note") or "").replace("|", "/")
        size = item.get("bytes")
        size_s = f"{size/1e9:.2f} GB" if isinstance(size, int) and size else ""
        lines.append(
            f"| `{item.get('id')}` | {item.get('week', '')} | "
            f"{item.get('license', '')} | {item.get('status', '')} | "
            f"{size_s} | {note} |"
        )
    lines += [
        "",
        "## Không kéo",
        "",
        "- `HuggingFaceFW/fineweb-edu` default (~6 TB) — chỉ kéo `sample-10BT`",
        "- `TeraflopAI/SEC-EDGAR` — ~590 GB, không vừa ổ D",
        "- `gbharti/finance-alpaca` — data sinh GPT-3.5",
        "",
    ]
    (large_root / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--only", default="")
    args = parser.parse_args()
    large_root = Path(args.root)
    large_root.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("HF_HOME", str(large_root / ".hf_home"))
    os.environ.setdefault("HF_HUB_CACHE", str(large_root / ".hf_home" / "hub"))

    wanted = (
        [s.strip() for s in args.only.split(",") if s.strip()]
        if args.only
        else list(JOBS)
    )
    unknown = [w for w in wanted if w not in JOBS]
    if unknown:
        log("Job không tồn tại: " + ", ".join(unknown))
        return 2

    manifest: list = []
    existing = large_root / "MANIFEST.json"
    if existing.exists():
        try:
            manifest = json.loads(existing.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            manifest = []

    failed = []
    for name in wanted:
        log(f"\n== {name} → {large_root} ==")
        try:
            JOBS[name](large_root, manifest)
        except Exception as exc:  # noqa: BLE001
            failed.append(name)
            record(
                manifest,
                id=name,
                status="error",
                note=f"{type(exc).__name__}: {exc}",
            )

    by_id = {item.get("id"): item for item in manifest if item.get("id")}
    manifest = list(by_id.values())
    (large_root / "MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_readme(large_root, manifest)

    pointer = ROOT / "docs" / "datasets" / "LARGE_ROOT.txt"
    pointer.write_text(
        f"Bản đầy đủ các bộ lớn: {large_root.resolve()}\n"
        f"Kéo bằng: python scripts/download_large_datasets.py --root {large_root}\n"
        f"Ngày: {TODAY}\n",
        encoding="utf-8",
    )

    log("\n--- xong ---")
    log(f"MANIFEST: {large_root / 'MANIFEST.json'}")
    if failed:
        log("Lỗi: " + ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
