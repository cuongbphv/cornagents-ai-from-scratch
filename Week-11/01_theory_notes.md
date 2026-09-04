# Lý thuyết Tuần 11: QLoRA: fine-tune model 7B-8B thật trên 8GB VRAM

> Đọc trước khi chạy [`02_qlora_finetune.py`](02_qlora_finetune.py). Số học kiểm chứng 2026-08-11; nguồn cuối file. Cần nắm LoRA (Tuần 9).

---

## 1. Vì sao 8GB không chứa nổi fine-tune thường: và QLoRA lách thế nào

Số học byte thuần (tự kiểm được): model 8B tham số ở fp16/bf16 = 8B × 2 byte = **16 GB chỉ riêng trọng số**: gấp đôi VRAM 3070 Ti, chưa tính gradient + optimizer state (AdamW: thêm ~2 giá trị moment/tham số train được, Tuần 8-9). QLoRA (Dettmers et al., arXiv 2305.14314) cắt cả ba khoản:

| Thành phần | Full FT 8B | QLoRA 8B |
|-----------|-----------|----------|
| Trọng số base | 16 GB (bf16) | ~4 GB (4-bit: 8B × 0.5 byte, chưa tính overhead) |
| Gradient | mọi tham số | chỉ adapter LoRA (~0.5-1%, bảng Tuần 9) |
| Optimizer state | mọi tham số × 2 | chỉ adapter × 2 |

Con số thực tế trong [README.md](README.md) (theo bảng requirements của Unsloth): 7B ≈ 5GB, 8B ≈ 6GB, khớp bậc độ lớn với số học trên cộng overhead activation/cache.

## 2. Ba kỹ thuật trong paper QLoRA: biết để đọc log không hoang mang

1. **NF4 (4-bit NormalFloat)**: 16 mức lượng tử đặt theo phân vị của phân phối chuẩn, paper lập luận đây là lựa chọn tối ưu thông tin cho trọng số phân phối ~chuẩn. Chỉ **base model** bị quantize; adapter LoRA vẫn bf16 và là thứ duy nhất được train.
2. **Double quantization**: quantize cả các hằng số quantization → tiết kiệm thêm ~0.4 bit/tham số (số của paper).
3. **Paged optimizers**: đẩy optimizer state sang RAM khi VRAM căng, cứu các cú spike.

Điểm bản chất cần nhớ: **gradient không chảy vào trọng số 4-bit**: forward dùng base dequantize từng lớp, backward chỉ cập nhật adapter. Vì thế chất lượng phụ thuộc adapter có đủ dung lượng học (r, target modules) hay không.

## 3. LoRA hyperparameters trong thực tế

Config 8GB trong README (`r=16, α=16, target = toàn bộ attention + MLP projections`) đọc bằng lời:

- **r**: dung lượng học của adapter. r=16 trên ma trận 4096×4096 = 131,072 tham số (0.78%, kiểm chứng Tuần 9). Task hẹp: r=8-16 thường đủ; r to hơn = học được nhiều hơn nhưng dễ overfit dataset nhỏ + tốn VRAM.
- **α**: hệ số scale `α/r` (Tuần 9). Quy ước phổ biến: α = r hoặc α = 2r; giữ cố định khi thí nghiệm để chỉ xoay một núm.
- **target modules**: gắn adapter vào đâu. "Tất cả projections" (q,k,v,o + gate/up/down) là khuyến nghị của Unsloth docs; gắn ít hơn → nhẹ hơn nhưng học kém hơn.
- **Kỷ luật thí nghiệm:** đổi MỘT tham số mỗi lần, giữ seed + dataset + held-out cố định, ghi số vào nhật ký.

## 4. Quy trình chuẩn 8GB: thứ tự chống lãng phí

1. **Smoke test trước** (vài chục step): không OOM + loss giảm → mới chạy full. OOM ở batch 1 + seq 1024 → giảm seq trước, rồi mới nghĩ tới thuê máy (ngưỡng trong README: >24h hoặc OOM batch 1 → 4090/A100).
2. Theo dõi `torch.cuda.max_memory_allocated()`: ghi số VRAM đỉnh làm bằng chứng.
3. Lưu adapter (vài chục MB) riêng khỏi base, đây là artifact chính.
4. Merge + export **GGUF** khi cần chạy Ollama/LM Studio (Tuần 12). GGUF là **định dạng file** của llama.cpp, không phải thuật toán quantize (mục nâng cao B4).

## 5. Eval base vs fine-tuned: không có số thì coi như chưa làm

- Cắt **held-out set trước khi train**, không bao giờ trộn vào train.
- So sánh cùng prompt, cùng sampling (temperature 0 khi so nghiêm túc, tái lập được).
- Loss/perplexity giảm ≠ hữu ích hơn (mục nâng cao H): kèm đánh giá tay trên 10-20 mẫu.
- So model khác tokenizer → bits-per-byte thay perplexity (Tuần 8, mục 8).
- Ghi vào [`03_eval_notes.md`](03_eval_notes.md), giữ held-out này cho mọi lần fine-tune sau.

## 6. Tiếng Việt trong tuần này

- **Đo tokenizer của base model trên tiếng Việt TRƯỚC khi chọn base**: dùng đúng phương pháp Tuần 6 mục 1.3 (đếm token/từ trên 5-10 câu nghiệp vụ thật). Fertility cao → cùng seq_len 1024 chứa ít nội dung Việt hơn, cùng dataset tốn nhiều compute hơn. Vài dòng code tránh được quyết định sai đắt nhất tuần.
- Dataset tiếng Việt license sạch đã vet sẵn trong [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md) (mục 2, 3, 8): README tuần này gợi ý trộn cụ thể. ⛔ Không thêm nguồn ngoài danh sách đã vet.
- **Fine-tune dạy hành vi/định dạng, không nhồi kiến thức quy định** (nguyên tắc đã chốt trong README): với văn bản pháp luật VN thay đổi liên tục, kiến thức đi qua RAG (Tuần 13-14); đừng đánh giá model fine-tuned bằng câu hỏi tra cứu điều khoản.
- Eval held-out nên có **cả câu tiếng Việt lẫn tiếng Anh**: làm nền cho bài kiểm tra catastrophic forgetting ở Tuần 12. Chọn LoRA/QLoRA vốn đã nghiêng về phía giữ song ngữ: Biderman et al. 2024 (PDF trong repo: [`../docs/papers/2405.09673_lora-learns-less-forgets-less.pdf`](../docs/papers/2405.09673_lora-learns-less-forgets-less.pdf)) đo được LoRA "substantially underperforms full finetuning" trong domain đích nhưng "better maintains the base model's performance on tasks outside the target domain", học ít hơn, quên cũng ít hơn. Trade-off này đúng là thứ bạn muốn khi base model gánh cả hai thứ tiếng.

## 7. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| Dettmers et al. 2023, QLoRA (CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2305.14314, PDF local: [`../docs/papers/2305.14314_qlora-efficient-finetuning.pdf`](../docs/papers/2305.14314_qlora-efficient-finetuning.pdf) | 1, 2 |
| Biderman et al. 2024, LoRA Learns Less and Forgets Less (CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2405.09673, PDF local: [`../docs/papers/`](../docs/papers/README.md) | 6 |
| Unsloth docs | https://unsloth.ai/docs | 3, 4 |
| HF PEFT docs | https://huggingface.co/docs/peft | 3 |
| Hu et al. 2021, LoRA | https://arxiv.org/abs/2106.09685 | 3 |

## Sau khi đọc xong

1. Đo fertility tokenizer của 2 base ứng viên trên câu nghiệp vụ VN → chọn base.
2. Chuẩn bị dataset theo README + cắt held-out.
3. Smoke test → full run trong [`02_qlora_finetune.py`](02_qlora_finetune.py); ghi VRAM đỉnh + loss.
4. Eval vào [`03_eval_notes.md`](03_eval_notes.md); export GGUF cho Tuần 12; làm [`quiz.md`](quiz.md).

## 8. Vì sao quantization 4-bit chạy được, và inference hiệu quả nhìn từ hệ thống

Cờ `load_in_4bit` của Unsloth gói hai ý tưởng riêng: quantization cho base model và adapter cho phần học thêm. Mục này giải thích nửa quantization bằng nguồn giáo trình, rồi đặt nó vào bức tranh inference hiệu quả.

**Quantization theo Fleuret.** *The Little Book of Deep Learning* mục 8.2 (trang 154) bắt đầu từ một quan sát về phần cứng: train hay sinh nhiều luồng song song thì tận dụng được GPU lớn, nhưng chạy LLM cho một người dùng là single-stream inference, "bounded by memory size and speed far more than by computation". Tham số, activation và gradient thường được mã hóa 32 hay 16 bit; độ chính xác đó cần cho training để các thay đổi nhỏ tích lũy được. Nhưng khi inference, vì activation là tổng của nhiều số hạng, sai số do quantization được **triệt tiêu một phần nhờ hiệu ứng trung bình**, và điều này càng đúng với kiến trúc lớn: model quantize xuống 6 hay 4 bit mỗi tham số "exhibit remarkable performance". Ngoài giảm bộ nhớ, quantization còn tăng tốc inference đáng kể. Từ đó sinh ra các phần mềm post-training quantization để chạy model có sẵn trên phần cứng tiêu dùng, ví dụ llama.cpp, thứ bạn sẽ dùng ở Tuần 12 qua GGUF.

Đọc đoạn này xong, hai câu hỏi thực hành trở nên rõ: vì sao QLoRA quantize **base model đã đóng băng** xuống 4-bit nhưng vẫn giữ adapter LoRA ở độ chính xác cao hơn (adapter là phần đang được train, cần tích lũy thay đổi nhỏ, đúng lý do Fleuret nêu cho độ chính xác khi training), và vì sao mất mát chất lượng khi quantize thường nhỏ hơn trực giác (hiệu ứng trung bình trên activation). Chi tiết NF4 và double quantization nằm ở paper QLoRA trong kệ paper và mục nâng cao B4.

**Inference hiệu quả có hai trục.** Xiao và Zhu (*Foundations of LLMs* mục 5.2, trang 222) chia các cải tiến inference thành hai loại: giảm bộ nhớ và tăng tốc, với quantization và pruning là công cụ cho cả hai. Hai kỹ thuật hệ thống khác trong cùng mục đáng biết khi bạn tự serve model ở Tuần 12: caching (mục 5.2.1, trang 223), từ cache mức chuỗi (lưu cặp query và response hay gặp trong một key-value store) đến cache prefix KV (lưu KV cache của các tiền tố đã xử lý để không prefill lại); và batching (mục 5.2.2), gom nhiều chuỗi vào một forward pass để GPU luôn bận. [Suy luận] Trên máy cá nhân với một người dùng, batching ít tác dụng vì hiếm khi có nhiều request cùng lúc, còn quantization và prefix caching là hai đòn bẩy chính. Khi ghi VRAM đỉnh và tốc độ vào `03_eval_notes.md`, hãy ghi rõ bit-width và có dùng cache hay không, vì hai yếu tố đó đổi số đo nhiều hơn mọi thứ khác.

## Đọc thêm từ kệ sách

> Catalog và điều khoản ở [`../docs/books/README.md`](../docs/books/README.md). Số trang là trang in của bản PDF đã tải ngày 2026-09-04; câu trong ngoặc kép là trích nguyên văn.

- **Quantization và adapter là hai nửa của QLoRA.** Fleuret mục 8.2 Quantization (trang 154) và 8.3 Adapters (trang 155) trình bày hai kỹ thuật cạnh nhau trong cùng chương về giới hạn compute; QLoRA ghép cả hai.
- **Inference hiệu quả.** Xiao và Zhu, *Foundations of LLMs* mục 5.2 (trang 222): tối ưu inference gồm hai loại, "reducing memory requirements and accelerating the system", với quantization và pruning là công cụ. Đọc để đặt cờ 4-bit của Unsloth vào bức tranh chung.
- **Code tham chiếu mở.** Notebook `chapter12/Chapter 12 - Fine-tuning Generation Models.ipynb` trong repo Hands-On LLM (Apache-2.0) làm SFT và preference tuning bằng TRL, đối chiếu với `02_qlora_finetune.py`.
