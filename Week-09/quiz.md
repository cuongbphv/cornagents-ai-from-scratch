# Tuần 9, Quiz: Instruction fine-tuning (classification + instruction-following + LoRA)

> Tự kiểm tra **trước** khi xem solution. Tổng **16** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Ý tưởng cốt lõi của LoRA?

- **A.** Đóng băng W, học thêm hai ma trận thấp hạng B,A sao cho W' = W + BA với rank r ≪ d
- **B.** Lượng tử hoá trọng số xuống 4-bit
- **C.** Tăng learning rate cho lớp cuối
- **D.** Cắt tỉa (prune) trọng số nhỏ

## Câu 2 (Trắc nghiệm)

Để fine-tune GPT cho classification, thay đổi kiến trúc nào là cốt lõi?

- **A.** Thêm một transformer block mới
- **B.** Thay output head (vocab_size) bằng một head nhỏ số lớp = số nhãn, thường chỉ train head + vài layer cuối
- **C.** Bỏ positional embedding
- **D.** Tăng gấp đôi số attention head

## Câu 3 (Tự luận)

Trong instruction fine-tuning, vì sao thường mask phần prompt/instruction khỏi loss (chỉ tính loss trên phần response)?

## Câu 4 (Trắc nghiệm)

Instruction fine-tuning khác pretraining ở điểm nào về DỮ LIỆU và MỤC TIÊU?

- **A.** Pretraining chỉ dùng cho model nhỏ
- **B.** Pretraining: text thô, học dự đoán token kế; instruction FT: cặp (instruction, response) có cấu trúc, học làm theo yêu cầu, cùng loss cross-entropy nhưng phân phối dữ liệu và hành vi đích khác
- **C.** Instruction FT không cần gradient
- **D.** Khác thuật toán tối ưu hoàn toàn (không dùng cross-entropy)

## Câu 5 (Trắc nghiệm)

Mask response-only (label -100 cho phần prompt) là mặc định tốt, nhưng theo Shi et al. 2024, Instruction Tuning With Loss Over Instructions (arXiv 2405.14394, dẫn ở mục 3 theory notes), tính loss CẢ trên phần instruction lại có lợi trong điều kiện nào?

- **A.** Khi dataset có instruction dài kèm output ngắn, hoặc khi có ít mẫu train, nhóm tác giả quy lợi ích cho việc giảm overfitting
- **B.** Khi model có trên 7B tham số
- **C.** Luôn luôn có lợi, nên bỏ hẳn masking
- **D.** Khi dùng optimizer khác AdamW

## Câu 6 (Trắc nghiệm)

LoRA r=16 trên ma trận 4096×4096 chỉ train ~0.78% tham số, nhưng vì sao VRAM khi train giảm còn MẠNH hơn cả tỷ lệ đó?

- **A.** Vì ma trận A, B được lưu ở CPU
- **B.** Vì AdamW giữ 2 giá trị moment cho MỖI tham số được train, LoRA cắt số tham số train ~50-100× nên cắt luôn optimizer state tương ứng, thường là phần ăn VRAM lớn nhất khi full FT
- **C.** Vì LoRA bỏ không lưu activation
- **D.** Vì LoRA tự động quantize base model xuống 4-bit

## Câu 7 (Trắc nghiệm)

Theo Fleuret, khi khởi tạo LoRA adapter, ma trận A được khởi tạo bằng giá trị Gaussian ngẫu nhiên còn B được đặt bằng 0. Mục đích của cách khởi tạo này là gì?

- **A.** Để hạng của BA đúng bằng R ngay từ bước đầu, tránh suy biến xuống hạng thấp hơn trong quá trình học
- **B.** Để tích BA bằng 0 lúc bắt đầu, nên model lúc khởi đầu fine-tune tính ra đúng output của model gốc
- **C.** Để chuẩn hóa scale của W + BA về cùng độ lớn với W, tránh activation bùng nổ ở các layer sâu
- **D.** Để gradient của A lớn hơn gradient của B, nhờ đó A học phần lớn thông tin mới trong vài bước đầu

## Câu 8 (Trắc nghiệm)

Jurafsky và Martin viết rằng LoRA "doesn't add any time during inference". Lý do là gì?

- **A.** Vì LoRA chỉ áp dụng lên các lớp attention, vốn chiếm phần nhỏ trong tổng thời gian suy luận
- **B.** Vì r rất nhỏ nên phép nhân xAB gần như không tốn thời gian so với phép nhân xW trong forward pass
- **C.** Vì tích AB có cùng kích thước với W nên có thể cộng thẳng vào trọng số pretrained trước khi suy luận
- **D.** Vì A và B chỉ được dùng trong backward pass, còn forward pass lúc suy luận vẫn chỉ tính xW như cũ

## Câu 9 (Trắc nghiệm)

Khi đánh giá model đã instruction-tune, SLP3 đề nghị leave-one-out theo cụm (cluster) tác vụ chứ không theo từng dataset. Vì sao?

- **A.** Vì các cụm tác vụ có kích thước cân bằng hơn, giúp ước lượng phương sai của điểm số ổn định hơn
- **B.** Vì số dataset quá lớn nên leave-one-out theo từng dataset đòi hỏi quá nhiều lần huấn luyện lại model
- **C.** Vì template sinh instruction được viết theo cụm tác vụ, nên chỉ có thể tách dữ liệu ở mức cụm
- **D.** Vì nhiều dataset rất giống nhau; nếu giữ dataset cùng loại trong tập train thì bài kiểm tra không còn là tác vụ mới

## Câu 10 (Trắc nghiệm)

Instruction tuning dùng đúng objective dự đoán token kế tiếp, vốn được coi là self-supervised. Vậy vì sao Jurafsky và Martin vẫn gọi nó là supervised fine-tuning (SFT)?

- **A.** Vì SFT cập nhật toàn bộ tham số của model, còn pretraining thường chỉ cập nhật một phần tham số
- **B.** Vì mỗi instruction trong dữ liệu đi kèm một đáp án đúng, tức một mục tiêu có giám sát, điều pretraining không có
- **C.** Vì dữ liệu instruction luôn do người viết tay, khác với dữ liệu web được thu thập tự động khi pretraining
- **D.** Vì loss được tính trên cả instruction lẫn response, nên tín hiệu huấn luyện dày hơn so với pretraining

## Câu 11 (Trắc nghiệm)

Theo Fleuret, ngoài việc giảm số tham số trainable, LoRA còn giảm đáng kể dấu chân bộ nhớ của optimizer như Adam. Cơ chế cụ thể là gì?

- **A.** Adam có thể lưu trạng thái ở độ chính xác thấp khi tham số là các ma trận hạng thấp như A và B
- **B.** Adam bỏ qua các tham số bị đóng băng nhưng vẫn giữ trạng thái cho chúng, chỉ không cập nhật nữa
- **C.** Adam lưu hai trung bình động cho mỗi tham số được tối ưu, nên khi chỉ tối ưu A và B thì phần trạng thái này co lại theo
- **D.** Adam chỉ cần lưu một trung bình động thay vì hai khi ma trận trọng số được phân rã thành tích BA

## Câu 12 (Trắc nghiệm)

Về quy mô dữ liệu, SLP3 so sánh instruction tuning với pretraining như thế nào?

- **A.** Instruction tuning thường chạy vài epoch trên dataset nhiều nhất là hàng triệu mẫu, thay vì hàng nghìn tỷ token
- **B.** Instruction tuning cần nhiều token hơn pretraining vì mỗi mẫu gồm cả instruction và response dài
- **C.** Cả hai đều cần hàng nghìn tỷ token, nhưng instruction tuning chỉ chạy đúng một epoch trên dữ liệu
- **D.** Hai giai đoạn dùng lượng dữ liệu tương đương, chỉ khác ở việc có mask phần prompt khỏi loss hay không

## Câu 13 (Tự luận)

Bạn cần một dataset instruction cho domain ngân hàng nhưng không có ngân sách thuê người viết. Dựa trên SLP3 mục 8.1.1, hãy nêu hai cách tạo dữ liệu rẻ hơn và một ví dụ cho thấy lượng nhỏ dữ liệu có chủ đích vẫn thay đổi được hành vi model.

## Câu 14 (Tự luận)

Khi cấu hình target_modules cho LoRA, bạn phân vân giữa chỉ gắn adapter vào attention hay gắn cả vào feed-forward. Hai cuốn sách nói gì về cách làm gốc và cách làm tiêu chuẩn, và điều đó gợi ý gì cho quyết định của bạn?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Shazeer (arXiv 2002.05202) thay FFN 'Linear rồi GELU' bằng SwiGLU có ba ma trận. Ông giữ số tham số không đổi bằng cách nào, và điều này giải thích con số nào trong config Mistral 7B?

- **A.** Chia sẻ trọng số giữa hai ma trận gate và up
- **B.** Bỏ ma trận output
- **C.** Dùng bias để bù
- **D.** Giảm số đơn vị ẩn d_ff; Mistral 7B có hidden_dim 14336 với d = 4096, tức 3,5d thay cho 4d

## Nâng cao 2 (Tự luận)

Jurafsky và Martin nói instruction tuning là supervised learning với cùng objective language modeling. Vậy khác biệt kỹ thuật duy nhất so với pretraining ở Tuần 8 nằm ở đâu, và hệ quả lên cách tính loss là gì?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
