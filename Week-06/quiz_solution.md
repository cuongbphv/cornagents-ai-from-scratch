# Tuần 6, Đáp án & Giải thích: Tokenization, embeddings, attention từ đầu

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Vì sao trong scaled dot-product attention ta chia cho sqrt(d_k)?

- **A.** Để score luôn dương
- **B.** Để chuẩn hoá vector về độ dài 1
- **C.** Để tiết kiệm bộ nhớ
- **D.** Để giữ phương sai của score ổn định, tránh softmax bão hoà làm gradient triệt tiêu (đáp án đúng)

**Đáp án: D**

**Giải thích:** Dot product của hai vector d_k chiều có phương sai ~d_k; không chia, score quá lớn đẩy softmax về one-hot → gradient ~0, khó học.

## Câu 2 (Tự luận)

Causal mask làm gì và cài đặt thế nào?

**Trả lời mẫu:** Causal (masked) attention làm cho token chỉ 'nhìn' về quá khứ, không thấy token tương lai, bắt buộc cho mô hình tự hồi quy. Cài đặt: đặt phần tam giác TRÊN của ma trận score = -vô cực (hoặc -1e9) TRƯỚC khi softmax; sau softmax các vị trí đó thành ~0, nên token i không attend tới token j>i.

**Giải thích:** Nếu để token thấy tương lai, model 'gian lận' lúc train và vô dụng lúc generate.

## Câu 3 (Trắc nghiệm)

Token embedding và positional embedding được kết hợp thế nào trong GPT-2?

- **A.** Nhân element-wise
- **B.** Chỉ dùng token embedding
- **C.** Nối (concatenate) lại
- **D.** Cộng vào nhau (cùng chiều d_model) (đáp án đúng)

**Đáp án: D**

**Giải thích:** GPT-2 cộng token embedding và positional embedding (cùng shape) → một vector vừa mang nghĩa token vừa mang vị trí.

## Câu 4 (Trắc nghiệm)

Ma trận attention scores (trước khi nhân V) có shape nào với input (batch, seq, d)?

- **A.** (batch, d, d)
- **B.** (seq, seq)
- **C.** (batch, seq, d)
- **D.** (batch, seq, seq) (đáp án đúng)

**Đáp án: D**

**Giải thích:** Score[i,j] = q_i·k_j cho mọi cặp token → (batch, seq, seq). Chính shape (seq×seq) này gây độ phức tạp O(n^2).

## Câu 5 (Tự luận)

[Nâng cao] RoPE khác với positional embedding tuyệt đối của GPT-2 thế nào?

**Trả lời mẫu:** GPT-2 CỘNG một vector vị trí học được vào embedding. RoPE thay vào đó XOAY các cặp chiều của Q và K một góc tỉ lệ với vị trí token, áp dụng ngay trong attention (không lên V). Hệ quả: tích q_m·k_n chỉ phụ thuộc khoảng cách tương đối (m-n), không phụ thuộc vị trí tuyệt đối → tổng quát hoá tốt hơn ra ngoài độ dài đã train và là nền cho mở rộng context (NTK/YaRN). Llama 3, Qwen3 dùng RoPE.

**Giải thích:** Xem mục A1 trong advanced_topics_vi.md.

## Câu 6 (Trắc nghiệm)

[Nâng cao] Mục đích chính của Grouped-Query Attention (GQA) so với Multi-Head Attention?

- **A.** Thay softmax bằng sigmoid
- **B.** Tăng số head để chính xác hơn
- **C.** Bỏ hoàn toàn key và value
- **D.** Cho các nhóm head chia sẻ chung K,V để GIẢM kích thước KV cache khi inference (đáp án đúng)

**Đáp án: D**

**Giải thích:** GQA gom head thành nhóm dùng chung K,V → KV cache nhỏ hơn → sinh text dài rẻ hơn về bộ nhớ; trung dung giữa MHA và MQA.

## Câu 7 (Trắc nghiệm)

[Nâng cao] Độ phức tạp bộ nhớ/tính toán của self-attention thường (full) theo độ dài seq n là?

- **A.** O(1)
- **B.** O(n)
- **C.** O(n log n)
- **D.** O(n^2) (đáp án đúng)

**Đáp án: D**

**Giải thích:** Ma trận score n×n → O(n^2). Đây là động lực cho sliding-window, MLA, và FlashAttention (tiling, không vật chất hoá ma trận n×n).

## Câu 8 (Tự luận)

Jurafsky và Martin (SLP3 mục 2.4) nói từ và morpheme có nghĩa ổn định nhưng khó định nghĩa hình thức, còn ký tự thì dễ định nghĩa nhưng quá nhỏ. BPE giải quyết mâu thuẫn này bằng cách nào, và vì sao việc chuẩn hóa đơn vị token lại cần cho perplexity?

**Trả lời mẫu:** BPE học đơn vị token từ dữ liệu bằng cách gộp dần các cặp ký tự hay đi cùng nhau, nên đơn vị thu được thường cỡ morpheme hoặc từ với từ phổ biến, và rơi về ký tự với từ hiếm. Chuẩn hóa đơn vị cần vì perplexity tính trên mỗi token, chuẩn hóa theo độ dài chuỗi; hai model tokenize khác nhau thì số token khác nhau và perplexity không so được với nhau.

**Giải thích:** SLP3 trang 42 nói rõ tokenization là để 'different algorithms and systems can agree on simple questions' như độ dài văn bản, và perplexity 'assume that all texts have a fixed' đơn vị. Đây là lý do mục H nâng cao đề xuất bits per byte để so model khác tokenizer.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

GQA (arXiv 2305.13245) là gì, và vì sao nó làm giảm KV cache nhưng không làm giảm số phép nhân trong QKᵀ?

- **A.** GQA chia query head thành g nhóm cùng chia sẻ một cặp K, V; cache chỉ lưu n_kv_head cặp nên nhỏ hơn, nhưng mỗi query head vẫn tính điểm với toàn bộ K của nhóm nên số phép nhân điểm attention không đổi (đáp án đúng)
- **B.** GQA chỉ áp dụng khi train, không khi inference
- **C.** GQA bỏ hẳn value
- **D.** GQA giảm số query head

**Đáp án: A**

**Giải thích:** Paper mô tả GQA là 'an interpolation between multi-head and multi-query attention with single key and value heads per subgroup of query heads'. Llama 3 dùng 8 KV head (arXiv 2407.21783 mục 3.2).

## Nâng cao 2 (Tự luận)

FlashAttention được gọi là exact attention. Nó thay đổi điều gì và không thay đổi điều gì so với cách bạn cài attention ở tuần này?

**Trả lời mẫu:** Nó không đổi kết quả toán học: cùng softmax(QKᵀ/√d)V. Nó đổi cách dùng bộ nhớ: chia Q, K, V thành khối (tiling), tính softmax theo kiểu streaming trong SRAM của GPU, không vật chất hóa ma trận n×n trong HBM, nên giảm số lần đọc ghi bộ nhớ (Dao et al., arXiv 2205.14135, abstract: 'an IO-aware exact attention algorithm that uses tiling'). Trong PyTorch, F.scaled_dot_product_attention chọn backend flash khi đủ điều kiện.

**Giải thích:** Kiểm bằng cách so output attention thủ công của bạn với F.scaled_dot_product_attention trên cùng input, sai lệch phải ở mức sai số số học.
