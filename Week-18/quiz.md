# Tuần 18, Quiz: Capstone + evaluation/observability

> Tự kiểm tra **trước** khi xem solution. Tổng **11** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Tự luận)

Use case capstone khuyến nghị và 3 thành phần kỹ thuật của nó?

## Câu 2 (Trắc nghiệm)

Bộ ba metric đánh giá capstone agentic gồm?

- **A.** FPS, latency, throughput
- **B.** Loss, perplexity, BLEU
- **C.** Precision, recall, F1 (chỉ vậy)
- **D.** Success rate, human-override rate, groundedness

## Câu 3 (Tự luận)

Vì sao chiến lược 'Claude làm brain + model 7B fine-tuned cho sub-task' lại hợp lý?

## Câu 4 (Trắc nghiệm)

'Groundedness' đo điều gì?

- **A.** Chi phí token
- **B.** Tốc độ agent
- **C.** Số agent dùng
- **D.** Mức độ output bám vào/được hỗ trợ bởi tài liệu nguồn (chống bịa)

## Câu 5 (Tự luận)

Viết retrospective 'nối về Phase 1' nghĩa là gì?

## Câu 6 (Trắc nghiệm)

Eval set capstone của bạn được xây từ chính các văn bản đã dùng để fine-tune model 7B ở Tuần 11. SLP3 gọi hiện tượng này là gì, hệ quả lên metric là gì, và sách nêu cách giảm nhẹ nào?

- **A.** Overfitting; metric sẽ thấp hơn thực tế vì model học thuộc dữ liệu huấn luyện; giảm nhẹ bằng regularization và early stopping khi fine-tune
- **B.** Goodhart's Law; metric mất ý nghĩa khi bị tối ưu trực tiếp làm mục tiêu; giảm nhẹ bằng cách đổi metric định kỳ và giữ nhiều metric song song
- **C.** Data contamination; metric sẽ thổi phồng hiệu năng thật; giảm nhẹ bằng cách công khai dữ liệu huấn luyện hoặc báo cáo phần trùng với test set
- **D.** Label leakage; metric sẽ dao động mạnh giữa các lần chạy vì nhãn lọt vào input; giảm nhẹ bằng cách tăng kích cỡ test set và chạy nhiều seed

## Câu 7 (Tự luận)

Bạn dùng LLM-as-a-judge để chấm groundedness cho capstone. SLP3 khuyên phải làm gì để tin được phán xét của judge, phân biệt hai chế độ chấm nào, và Goodhart's Law cảnh báo gì khi bạn tối ưu agent theo điểm judge?

## Câu 8 (Trắc nghiệm)

Agent capstone trả lời "Lãi suất tối đa là 6,5% một năm" trong khi đáp án chuẩn là "6,5%/năm". Theo SLP3 mục 11.6, độ đo nào phù hợp cho câu trả lời dạng văn bản tự do như vậy và nó được tính thế nào?

- **A.** Mean average precision, xếp hạng các token dự đoán theo xác suất rồi tính precision tại mỗi token trùng với đáp án và lấy trung bình
- **B.** Perplexity, tính xác suất model gán cho đáp án chuẩn khi cho trước câu hỏi; câu trả lời dài hơn đáp án thì perplexity thấp hơn
- **C.** Exact match, vì mọi câu hỏi có đáp án chuẩn đều phải khớp từng ký tự với đáp án; câu trả lời này bị tính 0 điểm dù đúng về nội dung
- **D.** Token F1, coi câu dự đoán và đáp án chuẩn là hai túi token, tính F1 cho từng câu hỏi rồi lấy trung bình trên toàn bộ câu hỏi

## Câu 9 (Trắc nghiệm)

Người dùng thử capstone phàn nàn agent "đứng im khá lâu rồi mới bắt đầu trả lời", còn khi đã trả lời thì chữ hiện đều. Theo FoLLM mục 5.1.4, metric hiệu năng nào phản ánh đúng phàn nàn này và nó chủ yếu đo giai đoạn gì?

- **A.** Inter-token Latency (ITL), là thời gian sinh mỗi token sau token đầu tiên, phản ánh hiệu suất của giai đoạn decoding trên GPU
- **B.** Resource Utilization, là mức sử dụng CPU, GPU và bộ nhớ của model trong quá trình suy luận, đo trên toàn bộ vòng đời của request
- **C.** Time to First Token (TTFT), chủ yếu là thời gian prefilling và dự đoán token đầu tiên nếu truyền dữ liệu không tốn nhiều thời gian
- **D.** Throughput, là số token hoặc số request mà model xử lý được mỗi giây trên toàn hệ thống phục vụ, gồm cả prefilling và decoding

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

PDF Karpathy-Loop yêu cầu khai báo complexity budget trước mỗi run và làm gì khi hết budget?

- **A.** Trả artifact tốt nhất hiện có kèm danh sách việc chưa xử lý và lý do dừng; không che partial failure sau một câu trả lời trôi chảy
- **B.** Xóa artifact và báo lỗi
- **C.** Tự động tăng budget
- **D.** Chạy tiếp đến khi xong

## Nâng cao 2 (Tự luận)

Hãy nối ba metric capstone (success rate, human-override rate, groundedness) với các số đo trong giáo trình: accuracy trên test set chưa thấy, exact match, token F1, precision.

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
