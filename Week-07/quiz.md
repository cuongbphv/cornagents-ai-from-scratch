# Tuần 7, Quiz: Lắp ráp & chạy mô hình GPT

> Tự kiểm tra **trước** khi xem solution. Tổng **17** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

LayerNorm trong transformer chuẩn hoá theo chiều nào?

- **A.** Theo chiều sequence
- **B.** Theo toàn bộ tensor
- **C.** Theo chiều batch (như BatchNorm)
- **D.** Theo chiều feature/embedding của từng token (last dim)

## Câu 2 (Tự luận)

Pre-LN + residual: x = x + Sublayer(LN(x)). Vì sao thiết kế này giúp train mạng sâu?

## Câu 3 (Trắc nghiệm)

Feed-forward network (FFN) trong block GPT-2 mở rộng chiều ẩn lên khoảng mấy lần d_model?

- **A.** 4 lần
- **B.** Không mở rộng
- **C.** 2 lần
- **D.** 8 lần

## Câu 4 (Trắc nghiệm)

GPT-2 small có khoảng bao nhiêu tham số (với emb_dim=768, n_layers=12, n_heads=12)?

- **A.** ~124M
- **B.** ~350M
- **C.** ~50M
- **D.** ~1.5B

## Câu 5 (Tự luận)

[Nâng cao] RMSNorm khác LayerNorm ở điểm nào, vì sao model hiện đại chuộng nó?

## Câu 6 (Trắc nghiệm)

[Nâng cao] SwiGLU FFN của Llama/Qwen thay thế phần nào của GPT-2?

- **A.** Thay LayerNorm
- **B.** Thay positional embedding
- **C.** Thay attention
- **D.** Thay FFN GELU-4× bằng một FFN có cổng (gated) dùng SiLU, ~2/3·4d chiều ẩn

## Câu 7 (Trắc nghiệm)

[Nâng cao] Trong một lớp Mixture-of-Experts (MoE), 'router' làm gì?

- **A.** Định tuyến gradient ngược
- **B.** Chọn GPU để chạy
- **C.** Chọn top-k expert (FFN con) cho mỗi token, chỉ kích hoạt số ít expert
- **D.** Sắp xếp token theo độ dài

## Câu 8 (Trắc nghiệm)

SLP3 mục 7.2 gọi attention là thành phần token-mixing. Theo mục 7.2.1, feedforward layer trong block khác attention ở điểm nào về cách xử lý các vị trí token và chia sẻ tham số?

- **A.** FFN chỉ được áp dụng lên token cuối cùng của chuỗi để tạo logits cho token kế tiếp, các vị trí khác bỏ qua để tiết kiệm tính toán.
- **B.** FFN cũng trộn thông tin giữa các vị trí nhưng chỉ trong một cửa sổ cục bộ vài token lân cận, giống một phép tích chập một chiều.
- **C.** FFN dùng chung một bộ tham số cho mọi lớp của transformer, chỉ khác nhau giữa các vị trí token để mã hóa thông tin vị trí.
- **D.** FFN là position-wise: áp dụng độc lập lên từng vị trí token, dùng cùng tham số cho mọi vị trí trong một lớp nhưng tham số khác nhau giữa các lớp.

## Câu 9 (Trắc nghiệm)

GPT của bạn theo kiến trúc prenorm có một LayerNorm cuối cùng đặt ngay trước lm_head. Theo SLP3 mục 7.2, vì sao lớp này cần thiết?

- **A.** Vì kiến trúc postnorm gốc của Vaswani et al. (2017) yêu cầu lớp này, và GPT giữ lại để tương thích với trọng số đã huấn luyện trước.
- **B.** Vì lm_head chia sẻ trọng số với ma trận embedding nên cần chuẩn hóa để hai ma trận có cùng thang đo trước khi tính logits trên vocabulary.
- **C.** Vì prenorm đặt layer norm trước attention và FFN nên đầu ra block cuối chưa được chuẩn hóa; cần một layer norm phụ ngay dưới language modeling head.
- **D.** Vì softmax của lm_head cần đầu vào có trung bình 0 và phương sai 1 để tránh tràn số khi tính exp trên một vocabulary lớn hàng chục nghìn token.

## Câu 10 (Trắc nghiệm)

Theo SLP3 mục 7.5, khi dùng weight tying, ma trận ánh xạ từ đầu ra lớp cuối h (shape [1 × d]) sang logits có shape gì, và vì sao được gọi là unembedding?

- **A.** [d × |V|], là E^T, vì nó ánh xạ ngược từ embedding [1 × d] về vector điểm trên vocabulary [1 × |V|], đảo chiều với bước embedding.
- **B.** [|V| × d], vì chính E được dùng lại nguyên dạng để ánh xạ one-hot sang embedding lần thứ hai ở phía đầu ra của mạng.
- **C.** [d × d], vì nó chiếu đầu ra lớp cuối về không gian embedding trước khi so sánh cosine với từng hàng của E.
- **D.** [N × |V|], vì nó tạo logits cho toàn bộ N vị trí trong cửa sổ ngữ cảnh cùng lúc chỉ trong một phép nhân ma trận duy nhất.

## Câu 11 (Trắc nghiệm)

Figure 7.21 của SLP3 dùng vocabulary 4 token với logits all = 1.2, the = 0.9, your = 0.1, that = -0.5. Xác suất của "all" thay đổi thế nào khi temperature τ giảm từ 1 xuống 0.5 rồi 0.1?

- **A.** Tăng từ .44 lên .50 rồi .55, vì chia logits cho τ chỉ dịch chuyển nhẹ phân phối về phía token có logit cao nhất.
- **B.** Tăng từ .44 lên .59 rồi .95, vì chia logits cho τ < 1 đưa giá trị lớn hơn vào softmax, đẩy phân phối về phía greedy decoding.
- **C.** Giảm từ .44 xuống .33 rồi .25, vì chia logits cho τ nhỏ làm phân phối tiến về phân phối đều trên 4 token.
- **D.** Giữ nguyên .44 ở cả ba giá trị, vì temperature chỉ đổi thứ hạng tương đối giữa các token chứ không đổi xác suất.

## Câu 12 (Trắc nghiệm)

Theo UDL mục 12.7.3, masked self-attention đem lại hệ quả gì về tính toán khi decoder sinh văn bản từng token?

- **A.** Có thể sinh mọi token của câu trong một lần forward duy nhất mà không cần lặp, vì mask đã tách các vị trí độc lập với nhau.
- **B.** Mỗi token mới đòi hỏi tính lại toàn bộ embedding của các token trước, vì attention weight của chúng thay đổi khi chuỗi dài thêm.
- **C.** Các embedding ở vị trí trước không phụ thuộc token sau, nên phần lớn tính toán trước đó có thể được dùng lại khi sinh token kế tiếp.
- **D.** Số phép tính giảm đúng một nửa vì ma trận attention chỉ còn tam giác dưới cần tính, bất kể chuỗi dài bao nhiêu.

## Câu 13 (Trắc nghiệm)

UDL mục 12.7.4 nêu cấu hình của GPT3. Phát biểu nào đúng theo Prince, và hãy tự kiểm tra số head nhân chiều mỗi head có khớp chiều embedding theo quy ước D/H của mục 12.3.3 không?

- **A.** 96 lớp transformer, chiều embedding 12288, 128 head với chiều query/key/value 96, huấn luyện trên 2048 tỷ token.
- **B.** 96 lớp transformer, chiều embedding 4096, 32 head với chiều query/key/value 128, huấn luyện trên 300 tỷ token.
- **C.** 48 lớp transformer, chiều embedding 12288, 96 head với chiều query/key/value 64, huấn luyện trên 175 tỷ token.
- **D.** 96 lớp transformer, chiều embedding 12288, 96 head với chiều query/key/value 128, huấn luyện trên 300 tỷ token.

## Câu 14 (Tự luận)

SLP3 mục 7.6.2 kết luận "greedy decoding is too boring, and random sampling is too random". Hãy giải thích vấn đề của từng phương pháp theo SLP3, và nêu ba phương pháp sampling được đề xuất để đứng giữa hai cực này.

## Câu 15 (Tự luận)

SLP3 mục 7.2 mô tả transformer bằng ẩn dụ residual stream (Elhage et al. 2021). Hãy giải thích ẩn dụ này, thành phần nào duy nhất đọc thông tin từ stream của token khác, và nội dung của stream thay đổi thế nào từ block thấp đến block cao trong một GPT 12 lớp được train dự đoán token kế tiếp.

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Top-p (nucleus) sampling khác top-k ở điểm nào theo Jurafsky và Martin, và vì sao điểm đó quan trọng khi ngữ cảnh đổi?

- **A.** Top-p chỉ dùng khi temperature bằng 1
- **B.** Top-p là greedy với p = 1
- **C.** Top-k giữ k token cố định còn top-p giữ tập nhỏ nhất chiếm p khối xác suất, nên số ứng viên tự co giãn theo hình dạng phân phối trong từng ngữ cảnh
- **D.** Top-p luôn chọn nhiều token hơn top-k

## Nâng cao 2 (Tự luận)

Vì sao khi kiểm tra kiến trúc GPT bằng cách load trọng số GPT-2 rồi sinh text, nên bắt đầu bằng greedy decoding thay vì sampling?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
