# Tuần 12, Quiz: Fine-tuning Mac/MLX + local inference stack

> Tự kiểm tra **trước** khi xem solution. Tổng **16** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Vì sao MacBook 24GB có thể fine-tune model lớn hơn RTX 3070 Ti 8GB?

- **A.** Mac có nhiều GPU hơn
- **B.** Unified memory 24GB dùng chung cho cả 'GPU', cho phép chứa model 13-14B (đổi lại chậm hơn ~2-4×)
- **C.** MLX nén model xuống 1-bit
- **D.** CPU Mac nhanh hơn GPU

## Câu 2 (Tự luận)

Mô tả luồng fine-tune → phục vụ bằng MLX trên Mac.

## Câu 3 (Trắc nghiệm)

Ollama và LM Studio đóng vai trò gì?

- **A.** Lớp inference/serving local, tải, quản lý và chat với model (GGUF/MLX) qua API/GUI
- **B.** Train model from scratch
- **C.** Vector database cho RAG
- **D.** Tokenizer

## Câu 4 (Tự luận)

Tóm tắt phân vai 3070 Ti vs Mac 24GB vs Cloud.

## Câu 5 (Trắc nghiệm)

Theo Ilharco et al. 2022 (task arithmetic, mục 7 theory notes), 'task vector' là gì và cộng/trừ nó dùng để làm gì?

- **A.** Gradient trung bình của batch cuối cùng khi train
- **B.** Một hàng của ma trận LoRA A
- **C.** τ = W_finetuned − W_base, 'hướng' fine-tune đã đẩy model tới trong không gian trọng số; CỘNG nhiều τ để ghép nhiều kỹ năng vào một model, PHỦ ĐỊNH (−τ) để giảm một hành vi mà ít ảnh hưởng task khác
- **D.** Vector embedding của mô tả task, dùng để retrieve adapter phù hợp

## Câu 6 (Tự luận)

Mô tả quy trình kiểm tra catastrophic forgetting song ngữ bắt buộc của repo (mục 5 theory notes) và làm gì khi phát hiện suy giảm.

## Câu 7 (Trắc nghiệm)

Theo FoLLM, vì sao prefilling được coi là compute-bound còn decoding là memory-bound?

- **A.** Prefilling xử lý cả chuỗi x trong một lần self-attention song song nên nút thắt là năng lực tính toán; decoding sinh từng token và truy cập KV cache liên tục nên nút thắt là bộ nhớ
- **B.** Prefilling chạy trên CPU để chuẩn bị embedding và mask cho toàn bộ prompt; decoding chạy trên GPU nơi dung lượng bộ nhớ là giới hạn chính của hệ thống
- **C.** Prefilling không dùng KV cache nên phải tính lại attention cho mọi cặp token; decoding lưu toàn bộ activation của mọi layer nên bộ nhớ tăng theo số token sinh ra
- **D.** Prefilling phải tính softmax trên toàn bộ vocabulary cho mọi vị trí của prompt nên nặng về tính toán; decoding chỉ tính một softmax mỗi bước nên phần còn lại là chi phí đọc trọng số

## Câu 8 (Trắc nghiệm)

FoLLM so sánh giai đoạn prefilling với BERT. Điểm giống và điểm khác là gì?

- **A.** Giống ở việc mã hóa chuỗi đầu vào thành biểu diễn ngữ cảnh (ở đây là KV cache) thay vì sinh token; khác ở việc prefilling là một chiều
- **B.** Giống ở việc dùng masked language modeling để học biểu diễn; khác ở việc prefilling không có lớp softmax đầu ra
- **C.** Giống ở việc dùng một encoder riêng cho input; khác ở việc prefilling chia sẻ tham số với decoder sinh token
- **D.** Giống ở việc xử lý toàn bộ chuỗi song song trên GPU; khác ở việc BERT không dùng self-attention nhân quả

## Câu 9 (Trắc nghiệm)

Khi benchmark inference trên Mac và trên 3070 Ti, metric nào của FoLLM phản ánh chủ yếu chi phí prefilling, và metric nào phản ánh hiệu quả decoding?

- **A.** Tokens Per Second phản ánh prefilling; Resource Utilization phản ánh decoding
- **B.** Request Latency phản ánh prefilling; Throughput phản ánh decoding
- **C.** Throughput phản ánh prefilling; Request Latency phản ánh decoding
- **D.** Time to First Token phản ánh prefilling; Inter-token Latency phản ánh decoding

## Câu 10 (Trắc nghiệm)

Trong mục 2.3.3.1, FoLLM nêu các cách làm KV cache có kích thước cố định. Cách nào chỉ cần lưu một cặp key-value duy nhất trong lúc suy luận?

- **A.** Trung bình động có trọng số của nc cặp gần nhất với các hệ số β tăng dần theo vị trí
- **B.** Trung bình cộng dồn của toàn bộ key và value tới vị trí hiện tại, cập nhật theo công thức đệ quy
- **C.** Một mạng neural làm bộ nhớ, nhận đầu ra bộ nhớ trước và trạng thái hiện tại để sinh đầu ra mới
- **D.** Cửa sổ trượt gồm nc cặp key-value gần nhất, được xem là một dạng local attention

## Câu 11 (Trắc nghiệm)

FoLLM mô tả trade-off khi chọn batch size trong inference. Phát biểu nào đúng?

- **A.** Batch nhỏ cho throughput cao hơn vì ít padding hơn; batch lớn cho latency thấp hơn nhờ các chuỗi chia sẻ chung một KV cache
- **B.** Batch nhỏ cho latency thấp hơn nhưng để GPU nhàn rỗi; batch lớn tận dụng song song tốt hơn nhưng phải padding và chờ chuỗi dài nhất xong
- **C.** Batch nhỏ và batch lớn cho cùng throughput trên GPU; khác biệt chỉ nằm ở lượng VRAM dành cho KV cache của mỗi chuỗi
- **D.** Batch lớn luôn tốt hơn về cả latency và throughput miễn là còn đủ VRAM; batch nhỏ chỉ dùng khi hết bộ nhớ

## Câu 12 (Trắc nghiệm)

Hệ thống của bạn dùng một system prompt dài giống nhau cho mọi request. Kỹ thuật nào trong FoLLM mục 5.2.1 giúp tránh tính lại phần này, và nó hoạt động thế nào?

- **A.** Continuous batching: gộp các request có cùng system prompt vào một batch để tính attention chung một lần
- **B.** Fixed-size KV cache: cắt bỏ phần system prompt khỏi cache ngay sau khi prefilling xong để tiết kiệm bộ nhớ
- **C.** Prefix cache: lưu KV cache của các tiền tố; request mới có chung tiền tố x<k thì khởi tạo KV cache bằng cache<k và chỉ tính các token còn lại
- **D.** Sequence-level cache: lưu cặp query-response, có tác dụng khi input mới trùng khớp chính xác với một query đã lưu

## Câu 13 (Tự luận)

FoLLM viết log Pr(y|x) = log Pr([x, y]) − log Pr(x) rồi nói trong cài đặt thực tế người ta tính trực tiếp theo cách khác. Hãy nêu cách tính trực tiếp đó và hai bài toán con mà FoLLM tách ra từ bài toán inference.

## Câu 14 (Tự luận)

So sánh request-level scheduling và continuous batching theo FoLLM. Vì sao continuous batching giảm lãng phí khi các response trong batch có độ dài rất khác nhau?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Rolling buffer cache của Mistral 7B hoạt động thế nào và cho tiết kiệm bao nhiêu theo paper?

- **A.** Cache chỉ giữ token đầu tiên
- **B.** Cache có kích thước cố định W; cặp K, V ở bước i ghi vào ô i mod W nên khi i vượt W cache ghi đè và không lớn thêm; ở chuỗi 32k paper báo giảm 8 lần bộ nhớ cache mà không ảnh hưởng chất lượng
- **C.** Cache lưu toàn bộ K, V nhưng nén 8 bit
- **D.** Cache lưu trên CPU

## Nâng cao 2 (Tự luận)

Khi đo tốc độ inference trên Mac và trên 3070 Ti, vì sao nên tách tốc độ prefill và tốc độ decode thay vì báo một con số tokens mỗi giây?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
