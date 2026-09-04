# Tuần 11, Đáp án & Giải thích: QLoRA fine-tuning thực tế (Unsloth)

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

QLoRA = ?

- **A.** LoRA cho mô hình vision
- **B.** Lượng tử hoá cả adapter xuống 4-bit
- **C.** LoRA chạy trên nhiều GPU
- **D.** Quantize base model xuống 4-bit (NF4, đóng băng) + chỉ train adapter LoRA ở bf16 (đáp án đúng)

**Đáp án: D**

**Giải thích:** QLoRA nén base xuống NF4 4-bit để giảm VRAM, gradient chỉ chảy qua adapter LoRA → fine-tune 7B vừa ~5GB.

## Câu 2 (Trắc nghiệm)

Theo bảng VRAM của Unsloth, QLoRA một model 7B cần khoảng bao nhiêu VRAM?

- **A.** ~5GB (đáp án đúng)
- **B.** ~2GB
- **C.** ~24GB
- **D.** ~12GB

**Đáp án: A**

**Giải thích:** ~5GB (8B ≈ 6GB) → vừa thoải mái trên 3070 Ti 8GB. 14B ≈ 8.5GB thì vượt 8GB.

## Câu 3 (Tự luận)

Liệt kê config QLoRA hợp lý cho GPU 8GB.

**Trả lời mẫu:** load_in_4bit=True; batch_size 1-2; sequence length ≤ 1024; gradient_checkpointing=True; LoRA r=16, lora_alpha=16; target tất cả projection của attention + MLP. Nếu vẫn sát giới hạn: giảm seq len, tăng gradient accumulation, hoặc dùng Colab T4 15GB.

**Giải thích:** Threshold: nếu OOM ở batch 1 hoặc run >24h → chuyển 4090/A100 thuê.

## Câu 4 (Trắc nghiệm)

[Nâng cao] NF4 (trong QLoRA) là gì?

- **A.** Kiểu lượng tử hoá 4-bit 'normal float', phân bố các mức tối ưu cho trọng số gần Gaussian (đáp án đúng)
- **B.** Một optimizer
- **C.** Một định dạng file model
- **D.** Một loại attention

**Đáp án: A**

**Giải thích:** NF4 đặt các mức lượng tử theo phân vị của phân phối chuẩn → ít sai số hơn int4 đều cho trọng số ~Gaussian.

## Câu 5 (Trắc nghiệm)

[Nâng cao] GGUF là gì?

- **A.** Một kiểu attention
- **B.** Một ĐỊNH DẠNG FILE của llama.cpp (chứa weight + metadata, các k-quant như Q4_K_M) mà Ollama/LM Studio load (đáp án đúng)
- **C.** Một benchmark
- **D.** Một thuật toán lượng tử hoá mới

**Đáp án: B**

**Giải thích:** GGUF là định dạng đóng gói, không phải thuật toán; nhầm lẫn này rất phổ biến. Tuần 12 sẽ load GGUF qua Ollama.

## Câu 6 (Tự luận)

Khi nào nên ngừng fine-tune local và chuyển lên cloud (4090/A100)?

**Trả lời mẫu:** Khi một lần fine-tune dự kiến chạy >24h ở local, hoặc khi OOM ngay cả ở batch size 1 (sau khi đã bật 4-bit, gradient checkpointing, giảm seq len). Lúc đó thuê RTX 4090/A100 sẽ rẻ hơn nhiều về thời gian.

**Giải thích:** Đây là 'ngưỡng kích hoạt cloud' của roadmap; verify bằng smoke test ngắn trước khi cam kết run dài.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

AWQ (arXiv 2306.00978) bảo vệ khoảng 1% trọng số 'salient'. Theo paper, tín hiệu nào cho biết kênh nào là salient, và vì sao họ không dùng mixed precision?

- **A.** Phân phối activation, không phải trọng số; thay vì trộn độ chính xác (khó tối ưu trên phần cứng) họ nhân scale các kênh salient bằng một phép biến đổi tương đương (đáp án đúng)
- **B.** Entropy của token
- **C.** Gradient khi fine-tune
- **D.** Độ lớn của trọng số; mixed precision quá đắt để tính

**Đáp án: A**

**Giải thích:** Abstract AWQ: 'To identify salient weight channels, we should refer to the activation distribution, not weights' và 'To avoid the hardware-inefficient mix-precision quantization, we mathematically derive that scaling up the salient channels can reduce the quantization error'.

## Nâng cao 2 (Tự luận)

QLoRA quantize base model xuống 4-bit nhưng vẫn train được. Hãy nêu ba thành phần paper đặt tên và giải thích vì sao adapter không bị quantize.

**Trả lời mẫu:** Ba thành phần: NF4, kiểu dữ liệu 4-bit 'information theoretically optimal for normally distributed weights'; double quantization, quantize cả các hằng số quantization; paged optimizers để xử lý đỉnh bộ nhớ (arXiv 2305.14314, abstract). Gradient được lan ngược qua base đã đóng băng và quantize vào adapter LoRA; adapter là phần đang học, cần tích lũy thay đổi nhỏ nên giữ ở độ chính xác cao hơn, đúng lý do Fleuret nêu cho training (Little Book mục 8.2).

**Giải thích:** Kết quả paper báo: fine-tune model 65B trên một GPU 48GB mà giữ hiệu năng full 16-bit.
