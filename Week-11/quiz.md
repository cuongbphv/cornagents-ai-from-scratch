# Tuần 11, Quiz: QLoRA fine-tuning thực tế (Unsloth)

> Tự kiểm tra **trước** khi xem solution. Tổng **8** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

QLoRA = ?

- **A.** LoRA cho mô hình vision
- **B.** Lượng tử hoá cả adapter xuống 4-bit
- **C.** LoRA chạy trên nhiều GPU
- **D.** Quantize base model xuống 4-bit (NF4, đóng băng) + chỉ train adapter LoRA ở bf16

## Câu 2 (Trắc nghiệm)

Theo bảng VRAM của Unsloth, QLoRA một model 7B cần khoảng bao nhiêu VRAM?

- **A.** ~5GB
- **B.** ~2GB
- **C.** ~24GB
- **D.** ~12GB

## Câu 3 (Tự luận)

Liệt kê config QLoRA hợp lý cho GPU 8GB.

## Câu 4 (Trắc nghiệm)

[Nâng cao] NF4 (trong QLoRA) là gì?

- **A.** Kiểu lượng tử hoá 4-bit 'normal float', phân bố các mức tối ưu cho trọng số gần Gaussian
- **B.** Một optimizer
- **C.** Một định dạng file model
- **D.** Một loại attention

## Câu 5 (Trắc nghiệm)

[Nâng cao] GGUF là gì?

- **A.** Một kiểu attention
- **B.** Một ĐỊNH DẠNG FILE của llama.cpp (chứa weight + metadata, các k-quant như Q4_K_M) mà Ollama/LM Studio load
- **C.** Một benchmark
- **D.** Một thuật toán lượng tử hoá mới

## Câu 6 (Tự luận)

Khi nào nên ngừng fine-tune local và chuyển lên cloud (4090/A100)?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

AWQ (arXiv 2306.00978) bảo vệ khoảng 1% trọng số 'salient'. Theo paper, tín hiệu nào cho biết kênh nào là salient, và vì sao họ không dùng mixed precision?

- **A.** Phân phối activation, không phải trọng số; thay vì trộn độ chính xác (khó tối ưu trên phần cứng) họ nhân scale các kênh salient bằng một phép biến đổi tương đương
- **B.** Entropy của token
- **C.** Gradient khi fine-tune
- **D.** Độ lớn của trọng số; mixed precision quá đắt để tính

## Nâng cao 2 (Tự luận)

QLoRA quantize base model xuống 4-bit nhưng vẫn train được. Hãy nêu ba thành phần paper đặt tên và giải thích vì sao adapter không bị quantize.

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
