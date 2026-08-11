# Tuần 8 — Đáp án & Giải thích: QLoRA fine-tuning thực tế (Unsloth)

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

QLoRA = ?

- **A.** LoRA chạy trên nhiều GPU
- **B.** Quantize base model xuống 4-bit (NF4, đóng băng) + chỉ train adapter LoRA ở bf16 ✅
- **C.** Lượng tử hoá cả adapter xuống 4-bit
- **D.** LoRA cho mô hình vision

**Đáp án: B**

**Giải thích:** QLoRA nén base xuống NF4 4-bit để giảm VRAM, gradient chỉ chảy qua adapter LoRA → fine-tune 7B vừa ~5GB.

## Câu 2 (Trắc nghiệm)

Theo bảng VRAM của Unsloth, QLoRA một model 7B cần khoảng bao nhiêu VRAM?

- **A.** ~2GB
- **B.** ~5GB ✅
- **C.** ~12GB
- **D.** ~24GB

**Đáp án: B**

**Giải thích:** ~5GB (8B ≈ 6GB) → vừa thoải mái trên 3070 Ti 8GB. 14B ≈ 8.5GB thì vượt 8GB.

## Câu 3 (Tự luận)

Liệt kê config QLoRA hợp lý cho GPU 8GB.

**Trả lời mẫu:** load_in_4bit=True; batch_size 1-2; sequence length ≤ 1024; gradient_checkpointing=True; LoRA r=16, lora_alpha=16; target tất cả projection của attention + MLP. Nếu vẫn sát giới hạn: giảm seq len, tăng gradient accumulation, hoặc dùng Colab T4 15GB.

**Giải thích:** Threshold: nếu OOM ở batch 1 hoặc run >24h → chuyển 4090/A100 thuê.

## Câu 4 (Trắc nghiệm)

[Nâng cao] NF4 (trong QLoRA) là gì?

- **A.** Một định dạng file model
- **B.** Kiểu lượng tử hoá 4-bit 'normal float', phân bố các mức tối ưu cho trọng số gần Gaussian ✅
- **C.** Một optimizer
- **D.** Một loại attention

**Đáp án: B**

**Giải thích:** NF4 đặt các mức lượng tử theo phân vị của phân phối chuẩn → ít sai số hơn int4 đều cho trọng số ~Gaussian.

## Câu 5 (Trắc nghiệm)

[Nâng cao] GGUF là gì?

- **A.** Một thuật toán lượng tử hoá mới
- **B.** Một ĐỊNH DẠNG FILE của llama.cpp (chứa weight + metadata, các k-quant như Q4_K_M) mà Ollama/LM Studio load ✅
- **C.** Một benchmark
- **D.** Một kiểu attention

**Đáp án: B**

**Giải thích:** GGUF là định dạng đóng gói, không phải thuật toán; nhầm lẫn này rất phổ biến. Tuần 9 sẽ load GGUF qua Ollama.

## Câu 6 (Tự luận)

Khi nào nên ngừng fine-tune local và chuyển lên cloud (4090/A100)?

**Trả lời mẫu:** Khi một lần fine-tune dự kiến chạy >24h ở local, hoặc khi OOM ngay cả ở batch size 1 (sau khi đã bật 4-bit, gradient checkpointing, giảm seq len). Lúc đó thuê RTX 4090/A100 sẽ rẻ hơn nhiều về thời gian.

**Giải thích:** Đây là 'ngưỡng kích hoạt cloud' của roadmap; verify bằng smoke test ngắn trước khi cam kết run dài.
