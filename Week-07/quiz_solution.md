# Tuần 7, Đáp án & Giải thích: Lắp ráp & chạy mô hình GPT

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

LayerNorm trong transformer chuẩn hoá theo chiều nào?

- **A.** Theo chiều sequence
- **B.** Theo toàn bộ tensor
- **C.** Theo chiều batch (như BatchNorm)
- **D.** Theo chiều feature/embedding của từng token (last dim) (đáp án đúng)

**Đáp án: D**

**Giải thích:** LayerNorm chuẩn hoá theo feature của mỗi token độc lập (không phụ thuộc batch) → ổn định, hợp với độ dài chuỗi thay đổi.

## Câu 2 (Tự luận)

Pre-LN + residual: x = x + Sublayer(LN(x)). Vì sao thiết kế này giúp train mạng sâu?

**Trả lời mẫu:** Residual tạo một 'đường cao tốc' để gradient chảy thẳng về các lớp đầu mà không bị nhân nhỏ dần qua nhiều lớp (chống vanishing gradient). Đặt LayerNorm TRƯỚC sublayer (pre-LN) giữ đầu vào mỗi sublayer ở thang đo ổn định, làm việc xếp chồng hàng chục block ổn định hơn so với post-LN. Nhờ vậy có thể train transformer rất sâu.

**Giải thích:** Ngoài vai trò shortcut gradient, residual còn cho phép mỗi block tinh chỉnh dần biểu diễn (residual stream).

## Câu 3 (Trắc nghiệm)

Feed-forward network (FFN) trong block GPT-2 mở rộng chiều ẩn lên khoảng mấy lần d_model?

- **A.** 4 lần (đáp án đúng)
- **B.** Không mở rộng
- **C.** 2 lần
- **D.** 8 lần

**Đáp án: A**

**Giải thích:** FFN: Linear(d → 4d) → GELU → Linear(4d → d). Hệ số 4× là chuẩn của GPT-2.

## Câu 4 (Trắc nghiệm)

GPT-2 small có khoảng bao nhiêu tham số (với emb_dim=768, n_layers=12, n_heads=12)?

- **A.** ~124M (đáp án đúng)
- **B.** ~350M
- **C.** ~50M
- **D.** ~1.5B

**Đáp án: A**

**Giải thích:** ~124M. Verify số tham số là cách kiểm tra nhanh kiến trúc đã ghép đúng.

## Câu 5 (Tự luận)

[Nâng cao] RMSNorm khác LayerNorm ở điểm nào, vì sao model hiện đại chuộng nó?

**Trả lời mẫu:** RMSNorm bỏ bước trừ mean và bỏ bias β; chỉ chia cho căn của trung bình bình phương rồi nhân γ: x / sqrt(mean(x^2) + eps) · γ. Ít phép tính hơn LayerNorm nhưng ổn định tương đương, nên Llama/Qwen dùng để rẻ và nhanh hơn ở quy mô lớn.

**Giải thích:** Xem mục A2 trong advanced_topics_vi.md.

## Câu 6 (Trắc nghiệm)

[Nâng cao] SwiGLU FFN của Llama/Qwen thay thế phần nào của GPT-2?

- **A.** Thay LayerNorm
- **B.** Thay positional embedding
- **C.** Thay attention
- **D.** Thay FFN GELU-4× bằng một FFN có cổng (gated) dùng SiLU, ~2/3·4d chiều ẩn (đáp án đúng)

**Đáp án: D**

**Giải thích:** SwiGLU = (SiLU(x W_gate) ⊙ x W_up) W_down; có 3 ma trận nên giảm chiều ẩn để giữ số tham số tương đương.

## Câu 7 (Trắc nghiệm)

[Nâng cao] Trong một lớp Mixture-of-Experts (MoE), 'router' làm gì?

- **A.** Định tuyến gradient ngược
- **B.** Chọn GPU để chạy
- **C.** Chọn top-k expert (FFN con) cho mỗi token, chỉ kích hoạt số ít expert (đáp án đúng)
- **D.** Sắp xếp token theo độ dài

**Đáp án: C**

**Giải thích:** Router gán mỗi token cho top-k experts → tổng tham số lớn nhưng tham số active mỗi token nhỏ; cần lo load balancing. Qwen3-MoE, gpt-oss, DeepSeek dùng MoE.

## Câu 8 (Trắc nghiệm)

SLP3 mục 7.2 gọi attention là thành phần token-mixing. Theo mục 7.2.1, feedforward layer trong block khác attention ở điểm nào về cách xử lý các vị trí token và chia sẻ tham số?

- **A.** FFN chỉ được áp dụng lên token cuối cùng của chuỗi để tạo logits cho token kế tiếp, các vị trí khác bỏ qua để tiết kiệm tính toán.
- **B.** FFN cũng trộn thông tin giữa các vị trí nhưng chỉ trong một cửa sổ cục bộ vài token lân cận, giống một phép tích chập một chiều.
- **C.** FFN dùng chung một bộ tham số cho mọi lớp của transformer, chỉ khác nhau giữa các vị trí token để mã hóa thông tin vị trí.
- **D.** FFN là position-wise: áp dụng độc lập lên từng vị trí token, dùng cùng tham số cho mọi vị trí trong một lớp nhưng tham số khác nhau giữa các lớp. (đáp án đúng)

**Đáp án: D**

**Giải thích:** SLP3 viết "The feedforward layer is position-wise, meaning that it operates on each token position i independently. This makes a contrast with the attention network, whose job is to mix information from different token positions. The feedforward weights are shared across positions ... but are different from layer to layer." Đó là lý do trong code bạn áp một nn.Sequential lên tensor (B, T, d) mà không cần vòng lặp theo T. (SLP3 mục 7.2.1, tr. 186)

## Câu 9 (Trắc nghiệm)

GPT của bạn theo kiến trúc prenorm có một LayerNorm cuối cùng đặt ngay trước lm_head. Theo SLP3 mục 7.2, vì sao lớp này cần thiết?

- **A.** Vì kiến trúc postnorm gốc của Vaswani et al. (2017) yêu cầu lớp này, và GPT giữ lại để tương thích với trọng số đã huấn luyện trước.
- **B.** Vì lm_head chia sẻ trọng số với ma trận embedding nên cần chuẩn hóa để hai ma trận có cùng thang đo trước khi tính logits trên vocabulary.
- **C.** Vì prenorm đặt layer norm trước attention và FFN nên đầu ra block cuối chưa được chuẩn hóa; cần một layer norm phụ ngay dưới language modeling head. (đáp án đúng)
- **D.** Vì softmax của lm_head cần đầu vào có trung bình 0 và phương sai 1 để tránh tràn số khi tính exp trên một vocabulary lớn hàng chục nghìn token.

**Đáp án: C**

**Giải thích:** SLP3: "at the very end of the last (highest) transformer block, there is a single extra layer norm that is run on the last h_i of each token stream (just below the language model head layer)", và chú thích 2 nói kiến trúc phổ biến nhất là prenorm, còn postnorm của Vaswani et al. (2017) đặt layer norm sau attention và FFN; "having the layer norm beforehand works better, but does require this one extra layer at the end." (SLP3 mục 7.2, tr. 188)

## Câu 10 (Trắc nghiệm)

Theo SLP3 mục 7.5, khi dùng weight tying, ma trận ánh xạ từ đầu ra lớp cuối h (shape [1 × d]) sang logits có shape gì, và vì sao được gọi là unembedding?

- **A.** [d × |V|], là E^T, vì nó ánh xạ ngược từ embedding [1 × d] về vector điểm trên vocabulary [1 × |V|], đảo chiều với bước embedding. (đáp án đúng)
- **B.** [|V| × d], vì chính E được dùng lại nguyên dạng để ánh xạ one-hot sang embedding lần thứ hai ở phía đầu ra của mạng.
- **C.** [d × d], vì nó chiếu đầu ra lớp cuối về không gian embedding trước khi so sánh cosine với từng hàng của E.
- **D.** [N × |V|], vì nó tạo logits cho toàn bộ N vị trí trong cửa sổ ngữ cảnh cùng lúc chỉ trong một phép nhân ma trận duy nhất.

**Đáp án: A**

**Giải thích:** SLP3 viết ở đầu vào ma trận embedding [|V| × d] ánh xạ one-hot [1 × |V|] sang embedding [1 × d]; ở language modeling head, "E^T, the transpose of the embedding matrix (of shape [d × |V|]) is used to map back from an embedding (shape [1 × d]) to a vector over the vocabulary (shape [1 × |V|])", nên "We therefore sometimes call the transpose E^T the unembedding layer"; u = h E^T, y = softmax(u) (công thức 7.47, 7.48). (SLP3 mục 7.5, tr. 195)

## Câu 11 (Trắc nghiệm)

Figure 7.21 của SLP3 dùng vocabulary 4 token với logits all = 1.2, the = 0.9, your = 0.1, that = -0.5. Xác suất của "all" thay đổi thế nào khi temperature τ giảm từ 1 xuống 0.5 rồi 0.1?

- **A.** Tăng từ .44 lên .50 rồi .55, vì chia logits cho τ chỉ dịch chuyển nhẹ phân phối về phía token có logit cao nhất.
- **B.** Tăng từ .44 lên .59 rồi .95, vì chia logits cho τ < 1 đưa giá trị lớn hơn vào softmax, đẩy phân phối về phía greedy decoding. (đáp án đúng)
- **C.** Giảm từ .44 xuống .33 rồi .25, vì chia logits cho τ nhỏ làm phân phối tiến về phân phối đều trên 4 token.
- **D.** Giữ nguyên .44 ở cả ba giá trị, vì temperature chỉ đổi thứ hạng tương đối giữa các token chứ không đổi xác suất.

**Đáp án: B**

**Giải thích:** SLP3: "τ = 1 is the normal softmax, and we can see how setting τ = 0.5 increases the probability of the top candidate from .44 to .59. Setting τ = 0.1 increases the probability of the top candidate to .95, getting us close to greedy decoding." Ngược lại τ = 10 và 100 cho .27 và .25, tiến về phân phối đều (high-temperature sampling). Trong code, đây là logits / temperature trước softmax trong hàm generate. (SLP3 mục 7.6.3, tr. 200)

## Câu 12 (Trắc nghiệm)

Theo UDL mục 12.7.3, masked self-attention đem lại hệ quả gì về tính toán khi decoder sinh văn bản từng token?

- **A.** Có thể sinh mọi token của câu trong một lần forward duy nhất mà không cần lặp, vì mask đã tách các vị trí độc lập với nhau.
- **B.** Mỗi token mới đòi hỏi tính lại toàn bộ embedding của các token trước, vì attention weight của chúng thay đổi khi chuỗi dài thêm.
- **C.** Các embedding ở vị trí trước không phụ thuộc token sau, nên phần lớn tính toán trước đó có thể được dùng lại khi sinh token kế tiếp. (đáp án đúng)
- **D.** Số phép tính giảm đúng một nửa vì ma trận attention chỉ còn tam giác dưới cần tính, bất kể chuỗi dài bao nhiêu.

**Đáp án: C**

**Giải thích:** Prince viết: "The computation can be made quite efficient as prior embeddings do not depend on subsequent ones due to the masked self-attention. Hence, much of the earlier computation can be recycled as we generate subsequent tokens." Đây là cơ sở của KV cache mà bạn gặp ở Tuần 12. Việc sinh vẫn phải lặp: chuỗi mở rộng được đưa lại vào decoder để lấy phân phối cho token tiếp theo. (UDL mục 12.7.3, tr. 224)

## Câu 13 (Trắc nghiệm)

UDL mục 12.7.4 nêu cấu hình của GPT3. Phát biểu nào đúng theo Prince, và hãy tự kiểm tra số head nhân chiều mỗi head có khớp chiều embedding theo quy ước D/H của mục 12.3.3 không?

- **A.** 96 lớp transformer, chiều embedding 12288, 128 head với chiều query/key/value 96, huấn luyện trên 2048 tỷ token.
- **B.** 96 lớp transformer, chiều embedding 4096, 32 head với chiều query/key/value 128, huấn luyện trên 300 tỷ token.
- **C.** 48 lớp transformer, chiều embedding 12288, 96 head với chiều query/key/value 64, huấn luyện trên 175 tỷ token.
- **D.** 96 lớp transformer, chiều embedding 12288, 96 head với chiều query/key/value 128, huấn luyện trên 300 tỷ token. (đáp án đúng)

**Đáp án: D**

**Giải thích:** Prince: "In GPT3, the sequence lengths are 2048 tokens long, and the total batch size is 3.2 million tokens. There are 96 transformer layers ..., each processing a word embedding of size 12288. There are 96 heads in the self-attention layers, and the value, query, and key dimension is 128. It is trained with 300 billion tokens and contains 175 billion parameters." Kiểm tra: 96 × 128 = 12288, đúng quy ước ở mục 12.3.3 rằng value, query, key có kích cỡ D/H khi có H head. (UDL mục 12.7.4, tr. 224)

## Câu 14 (Tự luận)

SLP3 mục 7.6.2 kết luận "greedy decoding is too boring, and random sampling is too random". Hãy giải thích vấn đề của từng phương pháp theo SLP3, và nêu ba phương pháp sampling được đề xuất để đứng giữa hai cực này.

**Trả lời mẫu:** Greedy decoding luôn chọn token có xác suất cao nhất nên văn bản sinh ra rất dễ đoán, chung chung và thường lặp lại; nó còn hoàn toàn xác định, cùng ngữ cảnh và cùng model thì luôn cho cùng chuỗi. Random sampling chọn token theo đúng xác suất của model, nhưng phần đuôi phân phối có rất nhiều token xác suất thấp; tuy từng token hiếm, tổng của chúng chiếm một phần không nhỏ nên chúng được chọn đủ thường xuyên để tạo ra câu kỳ quặc. Ba phương pháp sửa random sampling: temperature sampling, top-k sampling và top-p (nucleus) sampling.

**Giải thích:** SLP3 về greedy: "because the tokens it chooses are (by definition) extremely predictable, the resulting text is generic and often quite repetitive ... greedy decoding is so predictable that it is deterministic" (tr. 197). Về random sampling: "there are many odd, low-probability tokens in the tail of the distribution. Even though each one is low-probability, the sum of these rare tokens constitutes a non-trivial portion of the distribution. As a result, these tokens get chosen often enough to result in weird sentences being generated", và "There are three standard sampling methods ... Temperature sampling, top-k, and top-p." (SLP3 mục 7.6.2, tr. 198)

## Câu 15 (Tự luận)

SLP3 mục 7.2 mô tả transformer bằng ẩn dụ residual stream (Elhage et al. 2021). Hãy giải thích ẩn dụ này, thành phần nào duy nhất đọc thông tin từ stream của token khác, và nội dung của stream thay đổi thế nào từ block thấp đến block cao trong một GPT 12 lớp được train dự đoán token kế tiếp.

**Trả lời mẫu:** Residual stream xem việc xử lý token i qua các block là một dòng biểu diễn d chiều cho vị trí i: bắt đầu bằng embedding, các thành phần (layer norm rồi attention, layer norm rồi FFN) đọc từ dòng và cộng đầu ra của mình trở lại dòng. Chỉ multi-head attention lấy thông tin từ các residual stream của token khác; Elhage et al. cho thấy có thể xem attention head như đang chuyển thông tin từ stream của token lân cận vào stream hiện tại (Figure 7.8), nên attention là thành phần token-mixing. Ở các block đầu, stream chủ yếu biểu diễn token hiện tại; ở các block cao nhất, stream thường biểu diễn token kế tiếp, vì ở cuối cùng nó được huấn luyện để dự đoán token đó.

**Giải thích:** SLP3: "the various components read their input from the residual stream and add their output back into the stream" (tr. 184); "the only component that takes as input information from other tokens (other residual streams) is multi-head attention" và Elhage et al. (2021) "show that we can view attention heads as literally moving information from the residual stream of a neighboring token into the current stream" (tr. 187). Về nội dung theo độ sâu: "At the earlier transformer blocks, the residual stream is representing the current token. At the highest transformer blocks, the residual stream is usually representing the following token, since at the very end it's being trained to predict the next token." (SLP3 mục 7.2, tr. 188)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Top-p (nucleus) sampling khác top-k ở điểm nào theo Jurafsky và Martin, và vì sao điểm đó quan trọng khi ngữ cảnh đổi?

- **A.** Top-p chỉ dùng khi temperature bằng 1
- **B.** Top-p là greedy với p = 1
- **C.** Top-k giữ k token cố định còn top-p giữ tập nhỏ nhất chiếm p khối xác suất, nên số ứng viên tự co giãn theo hình dạng phân phối trong từng ngữ cảnh (đáp án đúng)
- **D.** Top-p luôn chọn nhiều token hơn top-k

**Đáp án: C**

**Giải thích:** SLP3 mục 7.6.4 (trang 200): k cố định là điểm yếu vì có ngữ cảnh 10 token đầu chiếm gần hết khối xác suất, có ngữ cảnh phân phối phẳng.

## Nâng cao 2 (Tự luận)

Vì sao khi kiểm tra kiến trúc GPT bằng cách load trọng số GPT-2 rồi sinh text, nên bắt đầu bằng greedy decoding thay vì sampling?

**Trả lời mẫu:** Greedy loại bỏ biến ngẫu nhiên của sampling: nếu output vô nghĩa ở greedy thì lỗi nhiều khả năng nằm ở kiến trúc hoặc mapping trọng số, không ở tham số sampling. Đây là suy luận thực hành của người viết, dựa trên việc greedy là hàm xác định của logits (SLP3 mục 7.6, trang 196).

**Giải thích:** Sau khi greedy ra text mạch lạc, mới bật temperature và top-p để so phong cách.
