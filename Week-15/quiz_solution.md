# Tuần 15, Đáp án & Giải thích: Nền tảng agentic: 5 tầng engineering, Claude Agent SDK, MCP

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Mô tả 'agent loop' cơ bản.

**Trả lời mẫu:** perceive (nhận input/trạng thái) → reason (LLM suy luận, quyết định bước tiếp) → chọn tool → execute tool → quan sát kết quả → lặp lại cho tới khi đạt mục tiêu, rồi trả về structured output. Khác với một lần gọi LLM, agent có vòng lặp nhiều bước có dùng công cụ và trạng thái.

**Giải thích:** Đây là khung chung của Claude Agent SDK và mọi agent framework.

## Câu 2 (Trắc nghiệm)

MCP (Model Context Protocol) là gì?

- **A.** Một định dạng file
- **B.** Một chuẩn mở để kết nối model với tool/nguồn dữ liệu qua server/client (GitHub, Postgres, Slack, filesystem...) (đáp án đúng)
- **C.** Một thuật toán RL
- **D.** Một model ngôn ngữ

**Đáp án: B**

**Giải thích:** MCP tách 'bộ não' khỏi nguồn dữ liệu/tool, cho phép tái sử dụng các server tool chuẩn hoá.

## Câu 3 (Trắc nghiệm)

Khác biệt chính giữa LangGraph và CrewAI?

- **A.** LangGraph: graph có trạng thái, tường minh, auditable; CrewAI: crew theo vai (role) prototype nhanh (đáp án đúng)
- **B.** LangGraph chỉ cho vision, CrewAI cho text
- **C.** CrewAI không hỗ trợ tool
- **D.** Cả hai giống hệt nhau

**Đáp án: A**

**Giải thích:** LangGraph hợp workflow cần kiểm soát/audit (tài chính có quy định); CrewAI nhanh để dựng nhóm agent theo vai.

## Câu 4 (Tự luận)

Vì sao workflow tài chính có quy định nên ưu tiên LangGraph?

**Trả lời mẫu:** Vì LangGraph cho phép định nghĩa trạng thái và luồng chuyển tiếp một cách tường minh, có thể kiểm tra/ghi vết (auditable) từng bước, và chèn các human-in-the-loop gate rõ ràng. Trong domain tài chính bị ràng buộc quy định, khả năng giải trình 'vì sao agent ra quyết định này' và kiểm soát chặt từng chuyển tiếp quan trọng hơn tốc độ prototype.

**Giải thích:** CrewAI tiện cho thử nghiệm nhanh nhưng kém minh bạch hơn về luồng trạng thái.

## Câu 5 (Trắc nghiệm)

Human-in-the-loop (HITL) gate nghĩa là gì?

- **A.** Cách tính token
- **B.** Agent chạy hoàn toàn tự động không cần người
- **C.** Một loại tool
- **D.** Điểm dừng yêu cầu con người phê duyệt/sửa trước khi agent đi tiếp (đáp án đúng)

**Đáp án: D**

**Giải thích:** HITL gate đặt giữa các stage rủi ro để con người kiểm soát; thiết kế least-privilege + HITL ngay từ đầu.

## Câu 6 (Trắc nghiệm)

Mô hình 5 tầng engineering (docs/5-layers-multi-agent.jpg) xếp theo thứ tự nào, từ trong ra ngoài?

- **A.** Prompt → Context → Harness → Loop → Graph (đáp án đúng)
- **B.** Loop → Prompt → Context → Graph → Harness
- **C.** Prompt → Harness → Context → Graph → Loop
- **D.** Context → Prompt → Loop → Harness → Graph

**Đáp án: A**

**Giải thích:** Prompt (the message) → Context (the memory) → Harness (the machine: gather-act-verify) → Loop (the system: run-check-decide) → Graph (the organization: nhiều agent + shared memory). Mỗi tầng bọc tầng trước; model là commodity, hệ thống quanh nó là engineering.

## Câu 7 (Tự luận)

Bốn điều kiện nào làm loop autoresearch của Karpathy chạy được, và vì sao thiếu một cái là loop hỏng?

**Trả lời mẫu:** (1) Output verifiable, có metric đo được (val_bpb), không thì agent tối ưu thứ sai; (2) Action reversible, git reset về commit giữ lại được, thất bại không phá state; (3) Horizon ngắn, run ~5 phút cho feedback dày; (4) Environment bounded, repo giới hạn không gian hành động. Thiếu verify thì không biết giữ hay bỏ thay đổi; thiếu reversible thì một lỗi phá cả quá trình; horizon dài làm tín hiệu học thưa; environment mở làm không gian tìm kiếm nổ.

**Giải thích:** Đây là checklist trước khi cho agent chạy tự động bất kỳ việc gì, kể cả trong CornAgents.AI.

## Câu 8 (Trắc nghiệm)

Theo Xiao và Zhu (FoLLM), prompt template là gì, và nó khác prompt ở điểm nào?

- **A.** Template là bản prompt đã được LLM tối ưu tự động trên tập validation, còn prompt là bản người viết tay trước khi tối ưu
- **B.** Template là đoạn văn bản có chỗ trống hoặc biến được điền thông tin cụ thể để tạo prompt, còn prompt là văn bản đầu vào x của LLM (đáp án đúng)
- **C.** Template là phần system information mô tả vai trò và ràng buộc của LLM, còn prompt là phần nội dung người dùng nhập vào sau đó
- **D.** Template là tập demonstration dùng cho in-context learning của một tác vụ, còn prompt là câu hỏi cuối cùng mà người dùng gõ vào

**Đáp án: B**

**Giải thích:** FoLLM định nghĩa prompt là "the input text to an LLM, denoted by x" và LLM sinh y bằng cách tối đa Pr(y|x). "A template is a piece of text containing placeholders or variables, where each placeholder can be filled with specific information." Ví dụ template "If {*premise*}, what are your suggestions for a fun weekend." (FoLLM mục 3.1.1, tr. 97)

## Câu 9 (Trắc nghiệm)

Agent của bạn dùng few-shot prompt để đọc thuật ngữ pháp lý tiếng Việt chuyên ngành nhưng kết quả vẫn kém dù đã thêm nhiều demonstration. FoLLM đưa ra nhận định nào cho tình huống tương tự (ví dụ dịch tiếng Inuktitut)?

- **A.** Nếu LLM thiếu dữ liệu pre-training về ngôn ngữ đó thì nên chuyển sang zero-shot vì demonstration sai làm nhiễu mô hình
- **B.** Nếu LLM thiếu dữ liệu pre-training về ngôn ngữ đó thì cần tiếp tục huấn luyện với thêm dữ liệu, thay vì cố tìm prompt tốt hơn (đáp án đúng)
- **C.** Nếu LLM thiếu dữ liệu pre-training về ngôn ngữ đó thì cần tăng số demonstration lên vài chục để bù kiến thức nền
- **D.** Nếu LLM thiếu dữ liệu pre-training về ngôn ngữ đó thì nên đổi định dạng prompt sang code-style để mô hình dễ đọc

**Đáp án: B**

**Giải thích:** FoLLM: in-context learning được xem là cách "efficiently activate and reorganize the knowledge learned in pre-training", nên nó phụ thuộc năng lực nền của mô hình. Với ví dụ Inuktitut: "If the LLM lacks pre-training on Inuktitut data ... it will be difficult for the model to perform well in translation regardless of how we prompt it. In this case, we need to continue training the LLM with more Inuktitut data, rather than trying to find better prompts." (FoLLM mục 3.1.2, tr. 99-101)

## Câu 10 (Tự luận)

FoLLM mục 3.1.3 nêu bốn nguyên tắc viết prompt. Hãy kể tên và cho biết bạn sẽ áp dụng từng nguyên tắc thế nào khi viết system prompt cho agent tra cứu quy định ngân hàng.

**Trả lời mẫu:** Bốn nguyên tắc: (1) mô tả nhiệm vụ rõ ràng nhất có thể, ví dụ nêu đích danh loại văn bản, phạm vi và giới hạn độ dài trả lời thay vì câu chung chung; (2) hướng LLM suy nghĩ, ví dụ yêu cầu liệt kê các bước tra cứu trước khi kết luận hoặc dùng vòng thứ hai để tự kiểm tra; (3) cung cấp thông tin tham chiếu, tức đưa đoạn văn bản pháp luật đã retrieve vào prompt và yêu cầu trả lời dựa trên đó; (4) chú ý định dạng prompt, tách các trường bằng nhãn, dấu phân cách hoặc XML tag và quy định cấu trúc đầu ra. FoLLM lưu ý hiệu năng rất nhạy với prompt, đổi thứ tự câu cũng có thể đổi kết quả.

**Giải thích:** Danh sách trong sách: "Describing the task as clearly as possible", "Guiding LLMs to think", "Providing reference information", "Paying attention to prompt formats" (tr. 102 đến 105). Với nguyên tắc 3, sách nêu RAG là ví dụ: "the relevant text for the user query is provided by calling an IR system, and we prompt LLMs to generate responses based on this provided relevant text." (FoLLM mục 3.1.3, tr. 102-105)

## Câu 11 (Trắc nghiệm)

Trong kiến trúc ReAct mà SLP3 mô tả, kết quả quan sát (observation) trả về từ tool được xử lý thế nào ở vòng lặp tiếp theo?

- **A.** Được dùng để cập nhật trọng số của model qua một bước gradient nhỏ trước khi model suy luận tiếp
- **B.** Được tóm tắt bởi một model thứ hai rồi thay thế toàn bộ lịch sử trước đó trong prompt của vòng sau
- **C.** Được nối vào lịch sử dưới dạng văn bản ngữ cảnh, rồi model lặp lại reason, act, observe cho đến khi xong (đáp án đúng)
- **D.** Được lưu vào bộ nhớ ngoài và chỉ nạp lại khi model sinh một action đọc bộ nhớ ở vòng sau

**Đáp án: C**

**Giải thích:** SLP3: "the model continuously loops over three stages, Reason-Action-Observation, until it solves the user problem ... All this history is then treated as textual context, and the model loops again, reasoning, acting, and observing, until the user's task is accomplished." Không có cập nhật trọng số; ở mục 1.8 sách nhấn mạnh trực giác vẫn là dự đoán token. (SLP3 mục 1.8, tr. 25)

## Câu 12 (Trắc nghiệm)

Prompt ReAct mẫu trong SLP3 (Fig. 1.17) định nghĩa ba action: Search[entity], Lookup[keyword] và Finish[answer]. Điều gì đáng chú ý về vai trò của Finish khi bạn thiết kế agent loop của mình?

- **A.** Finish là action bắt buộc phải đi sau Lookup, vì Lookup mới cung cấp câu trả lời cuối để Finish trả về
- **B.** Finish là action chỉ có ở prompt mẫu, còn trong thực tế agent kết thúc khi model ngừng sinh token
- **C.** Finish là một action mà model tự sinh ra như các action khác, vừa trả câu trả lời vừa kết thúc nhiệm vụ (đáp án đúng)
- **D.** Finish là action do hệ thống bên ngoài gọi khi số vòng lặp vượt ngưỡng, không phải do model sinh ra

**Đáp án: C**

**Giải thích:** Nguyên văn prompt: "(3) Finish[answer], which returns the answer and finishes the task." Trong trace Fig. 1.16, model tự sinh "Act 4: Finish[keyboard function keys]" sau bốn vòng Thought, Act, Obs. Theo mục 1.8, tập action được thêm vào tập token có thể sinh, nên điều kiện dừng cũng là một token action do model quyết định. (SLP3 mục 1.8, tr. 25)

## Câu 13 (Tự luận)

FoLLM đưa ra hai mức prompt RAG khác nhau về độ ràng buộc với ngữ cảnh được cung cấp. Hai mức đó là gì và sách gợi ý dùng mức chặt hơn khi nào?

**Trả lời mẫu:** Mức thứ nhất yêu cầu LLM sinh câu trả lời dựa trên context information do hệ IR trả về và diễn đạt bằng lời của mình, không chỉ chép lại. Mức thứ hai chặt hơn: chỉ được trả lời bằng đúng thông tin trong context (ví dụ một bảng mà mỗi dòng là một bản ghi hữu ích). FoLLM nói mức chặt này áp dụng khi context information có độ tin cậy cao. Với agent ngân hàng, khi nguồn là văn bản pháp luật đã xác minh thì dùng mức chặt; khi nguồn là kết quả tìm kiếm chung thì nên giữ mức mềm hơn và cho phép mô hình từ chối.

**Giải thích:** FoLLM: "If the context information is highly reliable, we can even restrict LLMs to answering using only the provided text." Prompt mức chặt viết "Please generate an answer using only this context information" (tr. 105), còn prompt mức đầu viết "Please generate an answer based on this context information ... not just copy from the context provided." (FoLLM mục 3.1.3, tr. 104)

## Câu 14 (Trắc nghiệm)

FoLLM nhận xét rằng hiệu năng LLM rất nhạy với prompt, thậm chí đổi thứ tự câu cũng có thể đổi kết quả. Sách gợi ý cách nào để prompt dễ đọc và giảm mơ hồ?

- **A.** Rút gọn prompt xuống một câu duy nhất, bỏ mọi ví dụ và mô tả vai trò để giảm số cách hiểu
- **B.** Lặp lại yêu cầu quan trọng ở cả đầu và cuối prompt để bù cho việc model nhạy với vị trí câu
- **C.** Chia prompt thành các trường riêng, dùng dấu phân cách hoặc XML tag và nêu rõ định dạng vào ra mong muốn (đáp án đúng)
- **D.** Viết toàn bộ prompt bằng tiếng Anh vì model được pre-train chủ yếu trên dữ liệu tiếng Anh

**Đáp án: C**

**Giải thích:** FoLLM: "One example is that we define several fields for prompts and fill different information in each field. Another example is we can use code-style prompts" và "This allows us to use control characters, XML tags, and specific formatting to represent complex data. And it is useful to specify how the input and output should be formatted or structured." Sách cũng nêu ví dụ báo cho model rằng văn bản đầu vào được bao trong dấu ngoặc kép. (FoLLM mục 3.1.3, tr. 105)

## Câu 15 (Trắc nghiệm)

Bước phân loại ý định (routing) trong agent của bạn yêu cầu LLM trả về một trong ba nhãn, nhưng model thường trả về cả câu như "Yêu cầu này có thể được xếp vào nhóm khiếu nại". FoLLM gợi ý cách nào để lấy nhãn ổn định?

- **A.** Đặt bài toán thành dạng cloze và giới hạn dự đoán trong tập từ nhãn Y, chọn nhãn có xác suất cao nhất theo label = argmax Pr(y|x) (đáp án đúng)
- **B.** Tăng temperature khi sinh để model đa dạng hơn rồi lấy nhãn xuất hiện nhiều nhất trong nhiều lần chạy
- **C.** Thêm một LLM thứ hai đọc câu trả lời của LLM thứ nhất và dịch nó thành nhãn, tránh sửa prompt gốc đã hoạt động
- **D.** Huấn luyện lại toàn bộ LLM với dữ liệu gán nhãn vì prompt không thể thay đổi cách model biểu đạt đầu ra

**Đáp án: A**

**Giải thích:** FoLLM giải thích LLM "are designed to generate text but not to assign labels", nên cần label mapping. Một cách là đặt thành cloze task rồi "constrain the prediction to the set of label words and select the one with the highest probability", tức label = argmax_{y∈Y} Pr(y|x) (phương trình 3.1). Cách khác sách nêu là ràng buộc bằng prompt "Just answer: positive, negative, or neutral." Fine-tune chỉ được sách gợi ý khi bài toán rất khó và có dữ liệu gán nhãn. (FoLLM mục 3.1.4.1, tr. 107)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Anthropic phân biệt workflow và agent thế nào, và khuyến nghị nào của họ về framework?

- **A.** Workflow là hệ trong đó LLM và tool được điều phối qua các đường code định trước; agent là hệ trong đó LLM tự điều khiển quy trình và cách dùng tool; các triển khai thành công nhất dùng các pattern đơn giản, ghép được, không dùng framework phức tạp (đáp án đúng)
- **B.** Không có khác biệt
- **C.** Workflow là agent chạy nhanh hơn; nên dùng framework nặng
- **D.** Agent luôn tốt hơn workflow

**Đáp án: A**

**Giải thích:** Trích 'Building Effective AI Agents': workflows là 'Systems where LLMs and tools are orchestrated through predefined code paths'; agents là 'Systems where LLMs dynamically direct their own processes and tool usage'.

## Nâng cao 2 (Tự luận)

Jurafsky và Martin nói khác biệt kỹ thuật giữa LLM thường và agent chỉ là gì? Điều đó gợi ý cách bạn nên nhìn tool call trong log của Claude Agent SDK ra sao?

**Trả lời mẫu:** SLP3 mục 1.8 (trang 24): agent là LLM có thể hành động bằng cách gọi chương trình khác, và 'The technical difference is only that the set of actions in the world are added to the set of possible tokens to generate'. Vậy tool call trong log là một token đặc biệt được sinh ra rồi được harness thực thi; kết quả tool quay lại context như input không đáng tin, theo paper Instruction Hierarchy trong kệ paper.

**Giải thích:** Cách nhìn này nối thẳng Tuần 15 về Tuần 7: vẫn là token prediction.
