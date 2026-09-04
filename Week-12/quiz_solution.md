# Tuần 12, Đáp án & Giải thích: Fine-tuning Mac/MLX + local inference stack

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Vì sao MacBook 24GB có thể fine-tune model lớn hơn RTX 3070 Ti 8GB?

- **A.** CPU Mac nhanh hơn GPU
- **B.** Unified memory 24GB dùng chung cho cả 'GPU', cho phép chứa model 13-14B (đổi lại chậm hơn ~2-4×) ✅
- **C.** MLX nén model xuống 1-bit
- **D.** Mac có nhiều GPU hơn

**Đáp án: B**

**Giải thích:** Unified memory là lợi thế của Apple Silicon: dung lượng lớn hơn VRAM rời 8GB, dù thông lượng thấp hơn NVIDIA.

## Câu 2 (Tự luận)

Mô tả luồng fine-tune → phục vụ bằng MLX trên Mac.

**Trả lời mẫu:** 1) mlx_lm.lora --model ... --train --data ... --iters 500 để train adapter LoRA. 2) mlx_lm.fuse --model ... --adapter-path ... để gộp adapter vào base. 3) Phục vụ qua Ollama (tạo Modelfile) hoặc LM Studio (load GGUF/MLX) để chat. Với 24GB có thể LoRA/QLoRA tới ~13-14B.

**Giải thích:** Mac dùng định dạng MLX (mlx-community/...); Ollama/LM Studio là lớp serving.

## Câu 3 (Trắc nghiệm)

Ollama và LM Studio đóng vai trò gì?

- **A.** Train model from scratch
- **B.** Lớp inference/serving local, tải, quản lý và chat với model (GGUF/MLX) qua API/GUI ✅
- **C.** Vector database cho RAG
- **D.** Tokenizer

**Đáp án: B**

**Giải thích:** Chúng giúp chạy model local dễ dàng; Ollama có API kiểu OpenAI tiện cắm vào RAG/agents.

## Câu 4 (Tự luận)

Tóm tắt phân vai 3070 Ti vs Mac 24GB vs Cloud.

**Trả lời mẫu:** 3070 Ti (8GB): code from-scratch, train nhỏ/validate loop, QLoRA 7B-8B nhanh. Mac 24GB: chứa & fine-tune model 13-14B, chạy yên tĩnh local, inference quantized. Cloud (RunPod/Lambda): lần pretrain GPT-2 một lần (~$15-35), full fine-tune, iterate nhanh khi local quá chậm/OOM.

**Giải thích:** Đây là nội dung deliverable 03_hardware_decision.md.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Rolling buffer cache của Mistral 7B hoạt động thế nào và cho tiết kiệm bao nhiêu theo paper?

- **A.** Cache lưu toàn bộ K, V nhưng nén 8 bit
- **B.** Cache có kích thước cố định W; cặp K, V ở bước i ghi vào ô i mod W nên khi i vượt W cache ghi đè và không lớn thêm; ở chuỗi 32k paper báo giảm 8 lần bộ nhớ cache mà không ảnh hưởng chất lượng ✅
- **C.** Cache chỉ giữ token đầu tiên
- **D.** Cache lưu trên CPU

**Đáp án: B**

**Giải thích:** Mistral 7B mục 2 (arXiv 2310.06825), Rolling Buffer Cache. FoLLM mục 2.3.3.1 gọi cùng ý là fixed-size KV cache.

## Nâng cao 2 (Tự luận)

Khi đo tốc độ inference trên Mac và trên 3070 Ti, vì sao nên tách tốc độ prefill và tốc độ decode thay vì báo một con số tokens mỗi giây?

**Trả lời mẫu:** Inference gồm hai pha (FoLLM mục 5.1.2, trang 207): prefill xử lý cả prompt trong một lượt nên gom nhiều token vào một lần nhân ma trận, còn decode sinh từng token và mỗi bước đọc lại toàn bộ trọng số và KV cache, bị giới hạn bởi băng thông bộ nhớ (Fleuret mục 8.2; Leviathan et al. mục 1). Hai pha có nút thắt khác nhau nên một con số gộp che mất việc máy nào mạnh ở pha nào; prompt dài với câu trả lời ngắn và ngược lại cho cảm giác rất khác.

**Giải thích:** Ghi tách hai số cho mỗi máy vào 03_hardware_decision.md.
