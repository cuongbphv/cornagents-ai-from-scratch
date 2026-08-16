# Datasets local (không commit file nặng)

Kéo ngày **2026-08-16** bằng `python scripts/download_datasets.py`.
Nguồn vet: [`Week-00/datasets_finance_banking.md`](../../Week-00/datasets_finance_banking.md).
License kiểm lại qua Hugging Face API ngay trước khi tải.

**Hai chỗ lưu:**

- Bộ nhỏ / sample (ổ C, trong repo): thư mục này. File nặng gitignored; `README.md` + `MANIFEST.json` + `LARGE_ROOT.txt` commit được.
- Bộ lớn (ổ D): `D:\AI\datasets` — kéo bằng `python scripts/download_large_datasets.py`. Xem `LARGE_ROOT.txt`.

## Đã kéo / đã bỏ

| id | tuần | license | status | ghi chú |
|---|---|---|---|---|
| `HuggingFaceFW/fineweb-edu` | 5 | odc-by | on_D | ODC-By chấp nhận 2026-08-16. sample-10BT 28.52 GB ở `D:\AI\datasets\w05_pretrain\fineweb-edu`. Không kéo default ~6 TB. |
| `gbharti/finance-alpaca` | 8 | mit | skipped | Card HF ghi kết hợp Stanford Alpaca + cặp sinh GPT-3.5. CLAUDE.md cấm data sinh từ model đóng. |
| `Josephgflowers/Finance-Instruct-500k` | 8 | apache-2.0 | on_D | Bản đầy đủ + WARNING.txt ở `D:\AI\datasets\finetune_en\`. Không train thô. |
| `TeraflopAI/SEC-EDGAR` | 10 | apache-2.0 | skipped | ~590 GB — không vừa ổ D. |
| `eloukas/edgar-corpus` | 10 | apache-2.0 | on_D | Bản đầy đủ (~40.7 GB) ở `D:\AI\datasets\rag_en\edgar-corpus`. |
| `undertheseanlp/UTS2017_Bank` | 8 | apache-2.0 | ok | 7413 dòng, 3 config × train/test |
| `duyet/vietnamese-legal-instruct` | 8 | cc-by-4.0 | ok_sample | sample 4000 train + 500 test (full repo ~5.9 GB, không kéo hết) |
| `Sujet-AI/Sujet-Finance-Instruct-177k` | 8 | apache-2.0 | ok | 177597 dòng — lựa chọn mặc định Tuần 8 |
| `flwrlabs/fingpt-sentiment-train` | 8 | mit | ok | 76772 dòng instruction/input/output |
| `kiethuynhanh/vnpdf-financial-reports-dataset` | 10 | mit | ok | 401 trang, chỉ text (bỏ image để tiết kiệm đĩa) |
| `kensho/bizbench` | 8,15 | apache-2.0 | ok | 19050 dòng — giữ nguyên, không đưa vào train |
| `th1nhng0/vietnamese-legal-documents` | 10,14 | cc-by-4.0 | ok_sample | filter NHNN: 2561 metadata; kéo content 400/400; relationships 3665 |
| `YuITC/Vietnamese-Legal-Documents` | 11 | mit | ok | queries 119007 (train+test) kèm context_list. Bỏ corpus.parquet |
| `gutenberg:11` | 5 | public-domain | ok | Alice in Wonderland — validate loop Tuần 5 |
| `PolyAI/banking77` | 8,13 | cc-by-4.0 | ok | 13083 câu từ GitHub PolyAI |
| `cfpb-vi-en-glossary` | 8,9 | us-federal-work-unverified-terms | pointer_only | HTTP 403 — URL trong glossary/SOURCE.txt |

## Map nhanh khi học Tuần 1–2 xong

- Tuần 5 (smoke local): `w05_pretrain/gutenberg_11_alice_in_wonderland.txt`
- Tuần 5 (pretrain cloud): `D:\AI\datasets\w05_pretrain\fineweb-edu` (sample-10BT, ODC-By)
- Tuần 8 (QLoRA hành vi): `finetune_en/sujet-finance-instruct-177k/` + `finetune_vi/vietnamese-legal-instruct.*.sample.jsonl` + `UTS2017_Bank/`
- Tuần 8/13 (routing): `finetune_en/banking77/`
- Tuần 8/15 (eval, không train): `eval/bizbench/`
- Tuần 10–14 (RAG/KG sample): `rag_kg/vietnamese-legal-documents/` — bản đầy đủ: `D:\AI\datasets\rag_kg\vietnamese-legal-documents`
- Tuần 10 (RAG EN 10-K): `D:\AI\datasets\rag_en\edgar-corpus`
- Tuần 11 (đo retriever sample): `eval/YuITC-Vietnamese-Legal-Documents/` — bản đầy đủ: `D:\AI\datasets\eval\YuITC-Vietnamese-Legal-Documents`

Kiến thức quy định **không** nhồi vào weight — đọc mục 0 của tài liệu dataset.
