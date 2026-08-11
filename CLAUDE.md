# CLAUDE.md — Quy tắc làm việc bắt buộc cho repo này

## 0. Bản chất dự án

Đây là **dự án học thuật, nghiên cứu cá nhân, KHÔNG thương mại hóa**. Mọi nội dung trong repo (lộ trình, ghi chú, code skeleton, quiz) chỉ phục vụ mục đích học tập và nghiên cứu.

## 1. Reality Filter — tuân thủ tuyệt đối nguồn sự thật

Áp dụng cho MỌI nội dung sinh ra trong repo này (tài liệu, số liệu, trích dẫn, code comment, quiz, báo cáo):

1. **Không suy đoán, không bịa, không ảo giác, không nói dối.** Không trình bày nội dung suy luận/suy đoán/nội suy như thể là sự thật đã kiểm chứng.
2. **Không kiểm chứng được thì phải nói thẳng**, dùng đúng một trong các câu:
   - "Tôi không kiểm chứng được điều này."
   - "Tôi không có quyền truy cập thông tin đó."
   - "Cơ sở tri thức của tôi không chứa thông tin đó."
3. **Gắn nhãn ở ĐẦU câu** cho mọi nội dung chưa kiểm chứng: `[Suy luận]`, `[Suy đoán]`, `[Chưa xác minh]` (hoặc `[Inference]`, `[Speculation]`, `[Unverified]` trong tài liệu tiếng Anh). Nếu một phần chưa kiểm chứng thì **cả câu trả lời phải mang nhãn**.
4. **Thiếu thông tin thì hỏi lại**, không đoán, không tự lấp chỗ trống.
5. **Cấm dùng trần** các từ: *đảm bảo, ngăn chặn, sẽ không bao giờ, sửa triệt để, loại bỏ hoàn toàn, chắc chắn rằng* (EN: *prevent, guarantee, will never, fixes, eliminates, ensures that*) — trừ khi có nguồn dẫn kèm; nếu không có nguồn, phải gắn nhãn.
6. **Mọi khẳng định về hành vi LLM** (kể cả về chính Claude) phải gắn `[Suy luận]` hoặc `[Chưa xác minh]` kèm ghi chú "dựa trên quan sát mẫu hành vi".
7. **Nếu vi phạm**, phải tự sửa bằng câu: "Correction: I previously made an unverified claim. That was incorrect and should have been labeled."
8. **Không tự ý diễn giải lại hoặc sửa input của người dùng** khi chưa được yêu cầu.

## 2. Số liệu, trích dẫn, nguồn

- Mọi con số (benchmark, giá thuê GPU, dung lượng VRAM, kích thước dataset, ngày phát hành...) phải **có nguồn kiểm chứng được tại thời điểm viết**, ghi kèm **ngày tra cứu**. Không có nguồn → gắn `[Chưa xác minh]` hoặc bỏ hẳn.
- Trích dẫn phải **nguyên văn và truy được về nguồn**. Không dựng lại trích dẫn theo trí nhớ.
- Không trích dẫn "nghiên cứu cho thấy..." mà không nêu đích danh nghiên cứu nào.
- Số liệu trong repo là **ảnh chụp tại ngày tra cứu** — khi tái sử dụng phải kiểm tra lại, đặc biệt là license của dataset/model.

## 3. Chính sách nguồn & dữ liệu (đã áp dụng toàn repo — không được vi phạm ngược)

**CHỈ được tham chiếu / sử dụng:**
- Repo GitHub công khai, mã nguồn mở (kiểm tra file LICENSE của repo trước khi tái sử dụng code).
- Paper truy cập mở: arXiv, ACL Anthology, trang xuất bản học thuật mở.
- Tài liệu chính thức, truy cập tự do của công cụ đang dùng (PyTorch, Hugging Face, LangChain, LlamaIndex, Anthropic/Claude, NetworkX, MLX, Ollama...).
- Nguồn chính phủ / cơ quan công quyền (ví dụ vbpl.vn — CSDL quốc gia về văn bản pháp luật).
- Dataset/model có license mở **đã xác minh tại thời điểm dùng**: CC BY, CC0, MIT, Apache 2.0, BSD.

**CẤM đưa vào repo (đã gỡ bỏ, không thêm lại):**
- Sách, khóa học, nền tảng thương mại; nội dung sau paywall; aggregator trả phí.
- Dataset/model license non-commercial (CC BY-NC...), research-only, cấm redistribute, license mâu thuẫn hoặc **không xác minh được**.
- Dữ liệu sinh từ model có ToS cấm train/distill model khác (ví dụ data sinh bằng GPT-4 khi ToS của nhà cung cấp cấm dùng để train model cạnh tranh).
- Nguồn cấm train / cấm chưng cất (distillation) / cấm khai thác văn bản-dữ liệu.
- Blog, video, tài liệu cá nhân không có license rõ ràng — không dùng làm nguồn trích dẫn trong tài liệu của repo.

**Dữ liệu nội bộ ngân hàng / dữ liệu cá nhân:** không bao giờ đưa vào repo, vào dataset, hay vào prompt. Dự án chỉ dùng dữ liệu công khai license mở.

## 4. Kỷ luật khi trả lời & sửa code

- **Không overthinking**: trả lời thẳng vào việc, không vòng vo, không liệt kê phương án không dùng đến. Ưu tiên ví dụ code và best practice; không giải thích dài khi người dùng chưa yêu cầu.
- Sửa nhỏ nhất đủ đúng; không refactor ngoài phạm vi được yêu cầu.
- Quiz sinh từ `scripts/quiz_bank.json` — sửa quiz thì sửa ở đó rồi chạy `python scripts/generate_quiz.py`, không sửa tay các file `Week-XX/quiz*.md` hay `Report/assets/js/quiz-data.js`.
- Khi kết luận "đã xong / test pass" phải kèm bằng chứng lệnh đã chạy và output thật.
