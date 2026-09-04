# Tuần 15, Quiz: Nền tảng agentic: 5 tầng engineering, Claude Agent SDK, MCP

> Tự kiểm tra **trước** khi xem solution. Tổng **17** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Tự luận)

Mô tả 'agent loop' cơ bản.

## Câu 2 (Trắc nghiệm)

MCP (Model Context Protocol) là gì?

- **A.** Một định dạng file
- **B.** Một chuẩn mở để kết nối model với tool/nguồn dữ liệu qua server/client (GitHub, Postgres, Slack, filesystem...)
- **C.** Một thuật toán RL
- **D.** Một model ngôn ngữ

## Câu 3 (Trắc nghiệm)

Khác biệt chính giữa LangGraph và CrewAI?

- **A.** LangGraph: graph có trạng thái, tường minh, auditable; CrewAI: crew theo vai (role) prototype nhanh
- **B.** LangGraph chỉ cho vision, CrewAI cho text
- **C.** CrewAI không hỗ trợ tool
- **D.** Cả hai giống hệt nhau

## Câu 4 (Tự luận)

Vì sao workflow tài chính có quy định nên ưu tiên LangGraph?

## Câu 5 (Trắc nghiệm)

Human-in-the-loop (HITL) gate nghĩa là gì?

- **A.** Cách tính token
- **B.** Agent chạy hoàn toàn tự động không cần người
- **C.** Một loại tool
- **D.** Điểm dừng yêu cầu con người phê duyệt/sửa trước khi agent đi tiếp

## Câu 6 (Trắc nghiệm)

Mô hình 5 tầng engineering (docs/5-layers-multi-agent.jpg) xếp theo thứ tự nào, từ trong ra ngoài?

- **A.** Prompt → Context → Harness → Loop → Graph
- **B.** Loop → Prompt → Context → Graph → Harness
- **C.** Prompt → Harness → Context → Graph → Loop
- **D.** Context → Prompt → Loop → Harness → Graph

## Câu 7 (Tự luận)

Bốn điều kiện nào làm loop autoresearch của Karpathy chạy được, và vì sao thiếu một cái là loop hỏng?

## Câu 8 (Trắc nghiệm)

Theo Xiao và Zhu (FoLLM), prompt template là gì, và nó khác prompt ở điểm nào?

- **A.** Template là bản prompt đã được LLM tối ưu tự động trên tập validation, còn prompt là bản người viết tay trước khi tối ưu
- **B.** Template là đoạn văn bản có chỗ trống hoặc biến được điền thông tin cụ thể để tạo prompt, còn prompt là văn bản đầu vào x của LLM
- **C.** Template là phần system information mô tả vai trò và ràng buộc của LLM, còn prompt là phần nội dung người dùng nhập vào sau đó
- **D.** Template là tập demonstration dùng cho in-context learning của một tác vụ, còn prompt là câu hỏi cuối cùng mà người dùng gõ vào

## Câu 9 (Trắc nghiệm)

Agent của bạn dùng few-shot prompt để đọc thuật ngữ pháp lý tiếng Việt chuyên ngành nhưng kết quả vẫn kém dù đã thêm nhiều demonstration. FoLLM đưa ra nhận định nào cho tình huống tương tự (ví dụ dịch tiếng Inuktitut)?

- **A.** Nếu LLM thiếu dữ liệu pre-training về ngôn ngữ đó thì nên chuyển sang zero-shot vì demonstration sai làm nhiễu mô hình
- **B.** Nếu LLM thiếu dữ liệu pre-training về ngôn ngữ đó thì cần tiếp tục huấn luyện với thêm dữ liệu, thay vì cố tìm prompt tốt hơn
- **C.** Nếu LLM thiếu dữ liệu pre-training về ngôn ngữ đó thì cần tăng số demonstration lên vài chục để bù kiến thức nền
- **D.** Nếu LLM thiếu dữ liệu pre-training về ngôn ngữ đó thì nên đổi định dạng prompt sang code-style để mô hình dễ đọc

## Câu 10 (Tự luận)

FoLLM mục 3.1.3 nêu bốn nguyên tắc viết prompt. Hãy kể tên và cho biết bạn sẽ áp dụng từng nguyên tắc thế nào khi viết system prompt cho agent tra cứu quy định ngân hàng.

## Câu 11 (Trắc nghiệm)

Trong kiến trúc ReAct mà SLP3 mô tả, kết quả quan sát (observation) trả về từ tool được xử lý thế nào ở vòng lặp tiếp theo?

- **A.** Được dùng để cập nhật trọng số của model qua một bước gradient nhỏ trước khi model suy luận tiếp
- **B.** Được tóm tắt bởi một model thứ hai rồi thay thế toàn bộ lịch sử trước đó trong prompt của vòng sau
- **C.** Được nối vào lịch sử dưới dạng văn bản ngữ cảnh, rồi model lặp lại reason, act, observe cho đến khi xong
- **D.** Được lưu vào bộ nhớ ngoài và chỉ nạp lại khi model sinh một action đọc bộ nhớ ở vòng sau

## Câu 12 (Trắc nghiệm)

Prompt ReAct mẫu trong SLP3 (Fig. 1.17) định nghĩa ba action: Search[entity], Lookup[keyword] và Finish[answer]. Điều gì đáng chú ý về vai trò của Finish khi bạn thiết kế agent loop của mình?

- **A.** Finish là action bắt buộc phải đi sau Lookup, vì Lookup mới cung cấp câu trả lời cuối để Finish trả về
- **B.** Finish là action chỉ có ở prompt mẫu, còn trong thực tế agent kết thúc khi model ngừng sinh token
- **C.** Finish là một action mà model tự sinh ra như các action khác, vừa trả câu trả lời vừa kết thúc nhiệm vụ
- **D.** Finish là action do hệ thống bên ngoài gọi khi số vòng lặp vượt ngưỡng, không phải do model sinh ra

## Câu 13 (Tự luận)

FoLLM đưa ra hai mức prompt RAG khác nhau về độ ràng buộc với ngữ cảnh được cung cấp. Hai mức đó là gì và sách gợi ý dùng mức chặt hơn khi nào?

## Câu 14 (Trắc nghiệm)

FoLLM nhận xét rằng hiệu năng LLM rất nhạy với prompt, thậm chí đổi thứ tự câu cũng có thể đổi kết quả. Sách gợi ý cách nào để prompt dễ đọc và giảm mơ hồ?

- **A.** Rút gọn prompt xuống một câu duy nhất, bỏ mọi ví dụ và mô tả vai trò để giảm số cách hiểu
- **B.** Lặp lại yêu cầu quan trọng ở cả đầu và cuối prompt để bù cho việc model nhạy với vị trí câu
- **C.** Chia prompt thành các trường riêng, dùng dấu phân cách hoặc XML tag và nêu rõ định dạng vào ra mong muốn
- **D.** Viết toàn bộ prompt bằng tiếng Anh vì model được pre-train chủ yếu trên dữ liệu tiếng Anh

## Câu 15 (Trắc nghiệm)

Bước phân loại ý định (routing) trong agent của bạn yêu cầu LLM trả về một trong ba nhãn, nhưng model thường trả về cả câu như "Yêu cầu này có thể được xếp vào nhóm khiếu nại". FoLLM gợi ý cách nào để lấy nhãn ổn định?

- **A.** Đặt bài toán thành dạng cloze và giới hạn dự đoán trong tập từ nhãn Y, chọn nhãn có xác suất cao nhất theo label = argmax Pr(y|x)
- **B.** Tăng temperature khi sinh để model đa dạng hơn rồi lấy nhãn xuất hiện nhiều nhất trong nhiều lần chạy
- **C.** Thêm một LLM thứ hai đọc câu trả lời của LLM thứ nhất và dịch nó thành nhãn, tránh sửa prompt gốc đã hoạt động
- **D.** Huấn luyện lại toàn bộ LLM với dữ liệu gán nhãn vì prompt không thể thay đổi cách model biểu đạt đầu ra

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Anthropic phân biệt workflow và agent thế nào, và khuyến nghị nào của họ về framework?

- **A.** Workflow là hệ trong đó LLM và tool được điều phối qua các đường code định trước; agent là hệ trong đó LLM tự điều khiển quy trình và cách dùng tool; các triển khai thành công nhất dùng các pattern đơn giản, ghép được, không dùng framework phức tạp
- **B.** Không có khác biệt
- **C.** Workflow là agent chạy nhanh hơn; nên dùng framework nặng
- **D.** Agent luôn tốt hơn workflow

## Nâng cao 2 (Tự luận)

Jurafsky và Martin nói khác biệt kỹ thuật giữa LLM thường và agent chỉ là gì? Điều đó gợi ý cách bạn nên nhìn tool call trong log của Claude Agent SDK ra sao?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
