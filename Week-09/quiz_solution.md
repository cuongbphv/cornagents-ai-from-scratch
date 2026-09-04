# Tuần 9, Đáp án & Giải thích: Instruction fine-tuning (classification + instruction-following + LoRA)

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Ý tưởng cốt lõi của LoRA?

- **A.** Đóng băng W, học thêm hai ma trận thấp hạng B,A sao cho W' = W + BA với rank r ≪ d (đáp án đúng)
- **B.** Lượng tử hoá trọng số xuống 4-bit
- **C.** Tăng learning rate cho lớp cuối
- **D.** Cắt tỉa (prune) trọng số nhỏ

**Đáp án: A**

**Giải thích:** LoRA chỉ train BA (ít tham số) thay vì toàn bộ W → tiết kiệm VRAM lớn, là nền của QLoRA (Tuần 11).

## Câu 2 (Trắc nghiệm)

Để fine-tune GPT cho classification, thay đổi kiến trúc nào là cốt lõi?

- **A.** Thêm một transformer block mới
- **B.** Thay output head (vocab_size) bằng một head nhỏ số lớp = số nhãn, thường chỉ train head + vài layer cuối (đáp án đúng)
- **C.** Bỏ positional embedding
- **D.** Tăng gấp đôi số attention head

**Đáp án: B**

**Giải thích:** Classification không cần dự đoán token: thay head 50257 chiều bằng Linear ra num_classes (vd. spam/ham), dùng hidden state của token cuối. Đóng băng phần lớn model giúp train nhanh, ít overfit.

## Câu 3 (Tự luận)

Trong instruction fine-tuning, vì sao thường mask phần prompt/instruction khỏi loss (chỉ tính loss trên phần response)?

**Trả lời mẫu:** Mục tiêu là dạy model SINH phản hồi tốt, không phải học thuộc lại đề bài. Nếu tính loss trên cả instruction, gradient bị pha loãng bởi việc dự đoán lại phần text đã cho sẵn, model tối ưu cho việc lặp lại prompt thay vì chất lượng response. Mask (đặt label = -100 trong PyTorch) các token thuộc prompt để cross-entropy chỉ chấm phần model phải tự sinh.

**Giải thích:** Đây là chi tiết dễ bỏ sót khi tự viết collate function cho instruction dataset.

## Câu 4 (Trắc nghiệm)

Instruction fine-tuning khác pretraining ở điểm nào về DỮ LIỆU và MỤC TIÊU?

- **A.** Pretraining chỉ dùng cho model nhỏ
- **B.** Pretraining: text thô, học dự đoán token kế; instruction FT: cặp (instruction, response) có cấu trúc, học làm theo yêu cầu, cùng loss cross-entropy nhưng phân phối dữ liệu và hành vi đích khác (đáp án đúng)
- **C.** Instruction FT không cần gradient
- **D.** Khác thuật toán tối ưu hoàn toàn (không dùng cross-entropy)

**Đáp án: B**

**Giải thích:** Cơ chế học giống nhau (next-token prediction); thứ thay đổi là dữ liệu (template Alpaca-style) và hành vi mà ta muốn model hội tụ về (làm theo instruction thay vì tiếp tục văn bản).

## Câu 5 (Trắc nghiệm)

Mask response-only (label -100 cho phần prompt) là mặc định tốt, nhưng theo Shi et al. 2024, Instruction Tuning With Loss Over Instructions (arXiv 2405.14394, dẫn ở mục 3 theory notes), tính loss CẢ trên phần instruction lại có lợi trong điều kiện nào?

- **A.** Khi dataset có instruction dài kèm output ngắn, hoặc khi có ít mẫu train, nhóm tác giả quy lợi ích cho việc giảm overfitting (đáp án đúng)
- **B.** Khi model có trên 7B tham số
- **C.** Luôn luôn có lợi, nên bỏ hẳn masking
- **D.** Khi dùng optimizer khác AdamW

**Đáp án: A**

**Giải thích:** Theo mục 3 của 01_theory_notes.md: mask chuẩn vẫn là mặc định của bài tuần này; ngoại lệ 'lengthy instructions + brief outputs' và ít mẫu train là nuance từ arXiv 2405.14394 (F.cross_entropy có ignore_index=-100 mặc định nên chỉ cần gán nhãn -100 là mask).

## Câu 6 (Trắc nghiệm)

LoRA r=16 trên ma trận 4096×4096 chỉ train ~0.78% tham số, nhưng vì sao VRAM khi train giảm còn MẠNH hơn cả tỷ lệ đó?

- **A.** Vì ma trận A, B được lưu ở CPU
- **B.** Vì AdamW giữ 2 giá trị moment cho MỖI tham số được train, LoRA cắt số tham số train ~50-100× nên cắt luôn optimizer state tương ứng, thường là phần ăn VRAM lớn nhất khi full FT (đáp án đúng)
- **C.** Vì LoRA bỏ không lưu activation
- **D.** Vì LoRA tự động quantize base model xuống 4-bit

**Đáp án: B**

**Giải thích:** Mục 4 của 01_theory_notes.md: optimizer state của AdamW đi theo tham số TRAIN ĐƯỢC, không theo tổng tham số, W đóng băng thì không tốn moment. Đây là lý do bảng so sánh full FT vs LoRA của deliverable phải đo cả VRAM đỉnh (torch.cuda.max_memory_allocated()).

## Câu 7 (Trắc nghiệm)

Theo Fleuret, khi khởi tạo LoRA adapter, ma trận A được khởi tạo bằng giá trị Gaussian ngẫu nhiên còn B được đặt bằng 0. Mục đích của cách khởi tạo này là gì?

- **A.** Để hạng của BA đúng bằng R ngay từ bước đầu, tránh suy biến xuống hạng thấp hơn trong quá trình học
- **B.** Để tích BA bằng 0 lúc bắt đầu, nên model lúc khởi đầu fine-tune tính ra đúng output của model gốc (đáp án đúng)
- **C.** Để chuẩn hóa scale của W + BA về cùng độ lớn với W, tránh activation bùng nổ ở các layer sâu
- **D.** Để gradient của A lớn hơn gradient của B, nhờ đó A học phần lớn thông tin mới trong vài bước đầu

**Đáp án: B**

**Giải thích:** Fleuret viết: "The matrix A is initialized with random Gaussian values, and B is set to zero, so that the fine-tuning starts with a model that computes an output identical to that of the original one." Với B = 0 thì X(W + BA)^T = XW^T, nên fine-tune xuất phát từ đúng hành vi của base model. (Fleuret mục 8.3, tr. 156)

## Câu 8 (Trắc nghiệm)

Jurafsky và Martin viết rằng LoRA "doesn't add any time during inference". Lý do là gì?

- **A.** Vì LoRA chỉ áp dụng lên các lớp attention, vốn chiếm phần nhỏ trong tổng thời gian suy luận
- **B.** Vì r rất nhỏ nên phép nhân xAB gần như không tốn thời gian so với phép nhân xW trong forward pass
- **C.** Vì tích AB có cùng kích thước với W nên có thể cộng thẳng vào trọng số pretrained trước khi suy luận (đáp án đúng)
- **D.** Vì A và B chỉ được dùng trong backward pass, còn forward pass lúc suy luận vẫn chỉ tính xW như cũ

**Đáp án: C**

**Giải thích:** SLP3: "The weight updates can be simply added in to the pretrained weights, since AB is the same size as W. That means it doesn't add any time during inference." Cùng lý do đó, có thể xây LoRA module cho từng domain rồi cộng vào hoặc trừ ra khỏi W để đổi module. (SLP3 mục 8.2, tr. 215)

## Câu 9 (Trắc nghiệm)

Khi đánh giá model đã instruction-tune, SLP3 đề nghị leave-one-out theo cụm (cluster) tác vụ chứ không theo từng dataset. Vì sao?

- **A.** Vì các cụm tác vụ có kích thước cân bằng hơn, giúp ước lượng phương sai của điểm số ổn định hơn
- **B.** Vì số dataset quá lớn nên leave-one-out theo từng dataset đòi hỏi quá nhiều lần huấn luyện lại model
- **C.** Vì template sinh instruction được viết theo cụm tác vụ, nên chỉ có thể tách dữ liệu ở mức cụm
- **D.** Vì nhiều dataset rất giống nhau; nếu giữ dataset cùng loại trong tập train thì bài kiểm tra không còn là tác vụ mới (đáp án đúng)

**Đáp án: D**

**Giải thích:** Mục tiêu đánh giá là khả năng theo instruction trên tác vụ chưa gặp. SLP3: "Because many tasks are similar (Super-NaturalInstructions includes 25 separate textual entailment datasets!) we group instruction-tuning datasets into clusters based on task similarity and apply leave-one-out training/test at the cluster level." Ví dụ để đánh giá sentiment analysis thì bỏ toàn bộ dataset sentiment khỏi tập train. (SLP3 mục 8.1.2, tr. 213)

## Câu 10 (Trắc nghiệm)

Instruction tuning dùng đúng objective dự đoán token kế tiếp, vốn được coi là self-supervised. Vậy vì sao Jurafsky và Martin vẫn gọi nó là supervised fine-tuning (SFT)?

- **A.** Vì SFT cập nhật toàn bộ tham số của model, còn pretraining thường chỉ cập nhật một phần tham số
- **B.** Vì mỗi instruction trong dữ liệu đi kèm một đáp án đúng, tức một mục tiêu có giám sát, điều pretraining không có (đáp án đúng)
- **C.** Vì dữ liệu instruction luôn do người viết tay, khác với dữ liệu web được thu thập tự động khi pretraining
- **D.** Vì loss được tính trên cả instruction lẫn response, nên tín hiệu huấn luyện dày hơn so với pretraining

**Đáp án: B**

**Giải thích:** SLP3: "we call this method supervised fine-tuning (or SFT) because unlike in pretraining, each instruction or question in the instruction tuning data has a supervised objective: a correct answer to the question or a response to the instruction." Lựa chọn về loss trên instruction sai vì cùng đoạn viết "here we train only on the response". (SLP3 mục 8.1, tr. 210)

## Câu 11 (Trắc nghiệm)

Theo Fleuret, ngoài việc giảm số tham số trainable, LoRA còn giảm đáng kể dấu chân bộ nhớ của optimizer như Adam. Cơ chế cụ thể là gì?

- **A.** Adam có thể lưu trạng thái ở độ chính xác thấp khi tham số là các ma trận hạng thấp như A và B
- **B.** Adam bỏ qua các tham số bị đóng băng nhưng vẫn giữ trạng thái cho chúng, chỉ không cập nhật nữa
- **C.** Adam lưu hai trung bình động cho mỗi tham số được tối ưu, nên khi chỉ tối ưu A và B thì phần trạng thái này co lại theo (đáp án đúng)
- **D.** Adam chỉ cần lưu một trung bình động thay vì hai khi ma trận trọng số được phân rã thành tích BA

**Đáp án: C**

**Giải thích:** Fleuret: "Since fine-tuning with LoRA adapters drastically reduces the number of trainable parameters, it reduces the memory footprint required by optimizers such as Adam, which generally store two running averages per parameter to optimize." Ngoài ra backward pass cũng nhẹ đi một chút. Đây là lý do VRAM khi train giảm mạnh hơn tỷ lệ tham số trainable. (Fleuret mục 8.3, tr. 157)

## Câu 12 (Trắc nghiệm)

Về quy mô dữ liệu, SLP3 so sánh instruction tuning với pretraining như thế nào?

- **A.** Instruction tuning thường chạy vài epoch trên dataset nhiều nhất là hàng triệu mẫu, thay vì hàng nghìn tỷ token (đáp án đúng)
- **B.** Instruction tuning cần nhiều token hơn pretraining vì mỗi mẫu gồm cả instruction và response dài
- **C.** Cả hai đều cần hàng nghìn tỷ token, nhưng instruction tuning chỉ chạy đúng một epoch trên dữ liệu
- **D.** Hai giai đoạn dùng lượng dữ liệu tương đương, chỉ khác ở việc có mask phần prompt khỏi loss hay không

**Đáp án: A**

**Giải thích:** SLP3: "Rather than trillions of tokens, training typically involves several epochs over instruction datasets with at most millions of examples. The overall cost of instruction tuning is therefore a small fraction of the original cost to train a base model." (SLP3 mục 8.1, tr. 211)

## Câu 13 (Tự luận)

Bạn cần một dataset instruction cho domain ngân hàng nhưng không có ngân sách thuê người viết. Dựa trên SLP3 mục 8.1.1, hãy nêu hai cách tạo dữ liệu rẻ hơn và một ví dụ cho thấy lượng nhỏ dữ liệu có chủ đích vẫn thay đổi được hành vi model.

**Trả lời mẫu:** Cách thứ nhất là tái sử dụng các dataset NLP có giám sát sẵn có (phân loại, QA, dịch), tách các trường và nhãn thành cặp key/value rồi đổ vào template để tạo instruction, và dùng language model sinh paraphrase cho prompt để đa dạng cách diễn đạt. Cách thứ hai, được SLP3 gọi là phổ biến nhất, là để chính language model viết dữ liệu instruction dựa trên các dataset khác nhau. Ví dụ Bianchi et al. (2024a) chọn câu hỏi có hại, dùng LM sinh paraphrase và câu trả lời an toàn, duyệt tay rồi trộn vào dataset; chỉ 500 safety instruction đã đủ giảm đáng kể tính có hại của model.

**Giải thích:** SLP3 mô tả việc template hóa từ các dataset như SQuAD và Super-NaturalInstructions (Fig. 8.3, 8.4) và viết: "The most common way to generate instruction-tuning datasets is to have language models write them, based on various datasets." Về Bianchi et al.: "even 500 safety instructions mixed in with a large instruction tuning dataset was enough to substantially reduce the harmfulness of models." (SLP3 mục 8.1.1, tr. 212-213)

## Câu 14 (Tự luận)

Khi cấu hình target_modules cho LoRA, bạn phân vân giữa chỉ gắn adapter vào attention hay gắn cả vào feed-forward. Hai cuốn sách nói gì về cách làm gốc và cách làm tiêu chuẩn, và điều đó gợi ý gì cho quyết định của bạn?

**Trả lời mẫu:** SLP3 cho biết bản LoRA gốc chỉ áp dụng lên các ma trận trong attention (WQ, WK, WV, WO) và có nhiều biến thể khác. Fleuret cũng mô tả thủ tục tiêu chuẩn là chỉ đổi các ma trận trọng số trong attention block và giữ MLP của feed-forward không đổi; tổng tham số cần tối ưu thường chỉ vài phần trăm model gốc. Vậy cấu hình chỉ attention là điểm xuất phát có căn cứ trong sách; mở rộng sang feed-forward là biến thể bạn cần tự đo lường vì hai sách không đưa số liệu so sánh.

**Giải thích:** SLP3: "In its original version LoRA was applied just to the matrices in the attention computation (the WQ, WK, WV, and WO layers). Many variants of LoRA exist." Fleuret: "The standard procedure to fine-tune a transformer with such adapters is to change only the weight matrices in the attention blocks, and to keep the MLP of the feed-forward blocks unchanged." (SLP3 mục 8.2, tr. 215; Fleuret mục 8.3, tr. 157)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Shazeer (arXiv 2002.05202) thay FFN 'Linear rồi GELU' bằng SwiGLU có ba ma trận. Ông giữ số tham số không đổi bằng cách nào, và điều này giải thích con số nào trong config Mistral 7B?

- **A.** Chia sẻ trọng số giữa hai ma trận gate và up
- **B.** Bỏ ma trận output
- **C.** Dùng bias để bù
- **D.** Giảm số đơn vị ẩn d_ff; Mistral 7B có hidden_dim 14336 với d = 4096, tức 3,5d thay cho 4d (đáp án đúng)

**Đáp án: D**

**Giải thích:** Shazeer mục 3: 'we reduce the number of hidden units d_ff'. Mistral 7B Table 1 (arXiv 2310.06825).

## Nâng cao 2 (Tự luận)

Jurafsky và Martin nói instruction tuning là supervised learning với cùng objective language modeling. Vậy khác biệt kỹ thuật duy nhất so với pretraining ở Tuần 8 nằm ở đâu, và hệ quả lên cách tính loss là gì?

**Trả lời mẫu:** Khác ở dữ liệu (cặp instruction và response) và ở việc mask loss: chỉ tính cross-entropy trên phần response để model học sinh phản hồi, không học lặp lại đề bài; trong PyTorch đặt label -100 cho token prompt. Hàm loss, optimizer và cấu trúc training loop giữ nguyên (SLP3 mục 8.1, trang 210).

**Giải thích:** Paper 'Instruction Tuning With Loss Over Instructions' trong kệ paper thử ngược điều này và tìm thấy hai ngoại lệ đáng nhớ.
