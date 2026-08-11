# Lý thuyết Tuần 9 — MLX trên Mac + local inference stack

> Đọc trước khi chạy các lệnh trong [`02_mlx_commands.md`](02_mlx_commands.md). Tuần này chạy trên Mac — các số liệu không kiểm chứng được từ máy Windows này đều ghi rõ; nguồn cuối file (xác minh 2026-08-11).

---

## 1. Unified memory — vì sao Mac 24GB "chứa" được model mà 8GB VRAM không chứa nổi

Kiến trúc Apple Silicon: CPU và GPU **dùng chung một vùng RAM** — không có "VRAM rời". Hệ quả bằng số học byte (tự kiểm): model 13B ở 4-bit ≈ 6.5 GB trọng số + working memory fine-tune → nằm trong 24 GB unified, nhưng vượt xa 8 GB của 3070 Ti. Trade-off: băng thông/throughput thấp hơn GPU rời — README ước "~2–4× chậm hơn NVIDIA"; [Chưa xác minh] con số này với chính hai máy của bạn — đo thật ở mục 4 chính là deliverable.

## 2. MLX fine-tune flow — 3 lệnh, cùng bản chất với Tuần 8

`mlx-lm` (repo `ml-explore/mlx-lm`, MIT — xác minh 2026-08-11, có tài liệu LoRA riêng `mlx_lm/LORA.md`):

```
1. Tải model MLX-format:   HF repo mlx-community/<model>
2. LoRA train:             mlx_lm.lora --model <m> --train --data <d> --iters 500
3. Fuse adapter:           mlx_lm.fuse --model <m> --adapter-path <a>
```

Khái niệm không có gì mới — vẫn là LoRA Tuần 6 (adapter hạng thấp, base đóng băng), chỉ đổi framework + phần cứng. Data format của `mlx_lm.lora` là JSONL — xem ví dụ trong [`02_mlx_commands.md`](02_mlx_commands.md). "Fuse" = "merge" của Tuần 6: `W' = W + (α/r)BA`.

## 3. Local inference stack — GGUF, Ollama, LM Studio

- **GGUF** = định dạng file model của llama.cpp (nhắc lần 3 trong roadmap vì hay nhầm): một file chứa trọng số đã quantize (Q4_K_M, Q5_K_M, Q8_0…) + metadata + tokenizer. **Không phải thuật toán** — cùng một model có nhiều bản GGUF ở mức bit khác nhau.
- **Ollama**: serve model local qua API; `Modelfile` khai báo GGUF nguồn + template chat + tham số. Đây là backend generate cho RAG Tuần 10.
- **LM Studio**: GUI chạy cả GGUF lẫn MLX — tiện so sánh nhanh hai format trên cùng máy Mac.
- Quy tắc chọn mức quantize (mục nâng cao B4): 8-bit gần như không mất chất lượng, 4-bit là điểm ngọt local; bit càng thấp perplexity càng tăng — nghi ngờ chất lượng thì thử lại ở Q8_0 trước khi đổ lỗi cho model.

## 4. Đo tốc độ Mac vs 3070 Ti — làm cho ra số, đừng cảm nhận

Protocol tối thiểu (điền kết quả vào [`03_hardware_decision.md`](03_hardware_decision.md)):

1. Cùng model, cùng mức quantize (vd. cùng file GGUF Q4_K_M), cùng prompt, cùng `max_tokens`.
2. Chạy ≥3 lần mỗi máy, bỏ lần đầu (warmup/load), lấy trung bình **tokens/giây** (Ollama in sẵn `eval rate`).
3. Ghi kèm: nhiệt/throttling nếu có, RAM/VRAM chiếm dụng, ngày đo.

Kết quả bảng này + trải nghiệm fine-tune là căn cứ viết bảng quyết định Mac vs 3070 Ti vs cloud — không chép ước lượng của người khác.

## 5. Kiểm tra catastrophic forgetting — bắt buộc với model song ngữ

Fine-tune lệch về một thứ tiếng có thể làm suy giảm khả năng thứ tiếng kia. Đừng tranh luận lý thuyết — **đo**:

1. Trước khi fine-tune: chốt bộ 10 prompt cố định (5 tiếng Việt + 5 tiếng Anh, có cả nghiệp vụ lẫn thường thức), sinh và lưu output của base.
2. Sau fine-tune: chạy đúng 10 prompt đó (temperature 0), so từng cặp.
3. Suy giảm rõ ở tiếng Anh → giảm tỷ lệ data một chiều, trộn thêm data tiếng Anh (chiến lược mục 8 của [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md)), train lại.

Bộ 10 prompt này giữ cố định vĩnh viễn — nó là "bài kiểm tra sức khỏe song ngữ" cho mọi model sau này của dự án.

Bài kiểm tra này có chỗ dựa từ paper chứ không phải lo xa: Biderman et al. 2024 (PDF trong repo: [`../docs/papers/2405.09673_lora-learns-less-forgets-less.pdf`](../docs/papers/2405.09673_lora-learns-less-forgets-less.pdf)) đo được full fine-tuning quên kiến thức ngoài domain đích nhiều hơn hẳn LoRA — tức là mức quên **phụ thuộc cách bạn fine-tune**, và chỉ có đo mới biết mình đang ở đâu trên trade-off đó. LoRA của MLX ở mục 2 nằm ở phía "quên ít" của phổ này, nhưng số của máy bạn vẫn phải tự đo.

## 6. Tiếng Việt trong tuần này

- Mục 5 chính là nội dung tiếng Việt trọng tâm của tuần: **giữ được song ngữ sau fine-tune là một deliverable đo được**, không phải cảm nhận.
- Khi viết `Modelfile` cho Ollama: **template chat phải khớp đúng template lúc fine-tune** (bài học Tuần 6 mục 3) — sai template, model tiếng Việt trả lời lẫn tiếng Anh hoặc lặp vô hạn là triệu chứng kinh điển. [Suy luận] — dựa trên cơ chế model học phân phối template; gặp triệu chứng thì kiểm template đầu tiên.
- Kiểm tra sanity encoding: prompt có dấu tiếng Việt qua API Ollama phải ra text có dấu chuẩn NFC (Tuần 10 sẽ dùng nghiêm túc — thấy mojibake thì soi encoding client trước khi nghi model).

## 7. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| ml-explore/mlx-lm (MIT, có LORA.md) | https://github.com/ml-explore/mlx-lm | 2 |
| Biderman et al. 2024 — LoRA Learns Less and Forgets Less (CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2405.09673 — PDF local: [`../docs/papers/`](../docs/papers/README.md) | 5 |

(Ollama, LM Studio, llama.cpp/GGUF: link trong README nguồn học — công cụ cài trên máy, tự xác minh version lúc cài. Các con số tốc độ trong tuần này do BẠN đo, không có số tham khảo nào đáng tin hơn máy của chính bạn.)

## Sau khi đọc xong

1. Cài `mlx-lm` trên Mac, chạy flow 3 lệnh (mục 2) theo [`02_mlx_commands.md`](02_mlx_commands.md).
2. Chốt bộ 10 prompt song ngữ TRƯỚC khi fine-tune (mục 5).
3. Dựng Ollama + LM Studio, đo tốc độ hai máy theo protocol mục 4.
4. Viết [`03_hardware_decision.md`](03_hardware_decision.md) từ số đo thật; làm [`quiz.md`](quiz.md).
