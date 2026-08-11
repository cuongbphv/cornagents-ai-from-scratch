# Tuần 3 — Đáp án & Giải thích: Tokenization, embeddings, attention từ đầu

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Vì sao trong scaled dot-product attention ta chia cho sqrt(d_k)?

- **A.** Để tiết kiệm bộ nhớ
- **B.** Để chuẩn hoá vector về độ dài 1
- **C.** Để giữ phương sai của score ổn định, tránh softmax bão hoà làm gradient triệt tiêu ✅
- **D.** Để score luôn dương

**Đáp án: C**

**Giải thích:** Dot product của hai vector d_k chiều có phương sai ~d_k; không chia, score quá lớn đẩy softmax về one-hot → gradient ~0, khó học.

## Câu 2 (Tự luận)

Causal mask làm gì và cài đặt thế nào?

**Trả lời mẫu:** Causal (masked) attention đảm bảo token chỉ 'nhìn' về quá khứ, không thấy token tương lai — bắt buộc cho mô hình tự hồi quy. Cài đặt: đặt phần tam giác TRÊN của ma trận score = -vô cực (hoặc -1e9) TRƯỚC khi softmax; sau softmax các vị trí đó thành ~0, nên token i không attend tới token j>i.

**Giải thích:** Nếu để token thấy tương lai, model 'gian lận' lúc train và vô dụng lúc generate.

## Câu 3 (Trắc nghiệm)

Token embedding và positional embedding được kết hợp thế nào trong GPT-2?

- **A.** Nối (concatenate) lại
- **B.** Cộng vào nhau (cùng chiều d_model) ✅
- **C.** Nhân element-wise
- **D.** Chỉ dùng token embedding

**Đáp án: B**

**Giải thích:** GPT-2 cộng token embedding và positional embedding (cùng shape) → một vector vừa mang nghĩa token vừa mang vị trí.

## Câu 4 (Trắc nghiệm)

Ma trận attention scores (trước khi nhân V) có shape nào với input (batch, seq, d)?

- **A.** (batch, seq, d)
- **B.** (batch, seq, seq) ✅
- **C.** (batch, d, d)
- **D.** (seq, seq)

**Đáp án: B**

**Giải thích:** Score[i,j] = q_i·k_j cho mọi cặp token → (batch, seq, seq). Chính shape (seq×seq) này gây độ phức tạp O(n^2).

## Câu 5 (Tự luận)

[Nâng cao] RoPE khác với positional embedding tuyệt đối của GPT-2 thế nào?

**Trả lời mẫu:** GPT-2 CỘNG một vector vị trí học được vào embedding. RoPE thay vào đó XOAY các cặp chiều của Q và K một góc tỉ lệ với vị trí token, áp dụng ngay trong attention (không lên V). Hệ quả: tích q_m·k_n chỉ phụ thuộc khoảng cách tương đối (m-n), không phụ thuộc vị trí tuyệt đối → tổng quát hoá tốt hơn ra ngoài độ dài đã train và là nền cho mở rộng context (NTK/YaRN). Llama 3, Qwen3 dùng RoPE.

**Giải thích:** Xem mục A1 trong advanced_topics_vi.md.

## Câu 6 (Trắc nghiệm)

[Nâng cao] Mục đích chính của Grouped-Query Attention (GQA) so với Multi-Head Attention?

- **A.** Tăng số head để chính xác hơn
- **B.** Cho các nhóm head chia sẻ chung K,V để GIẢM kích thước KV cache khi inference ✅
- **C.** Bỏ hoàn toàn key và value
- **D.** Thay softmax bằng sigmoid

**Đáp án: B**

**Giải thích:** GQA gom head thành nhóm dùng chung K,V → KV cache nhỏ hơn → sinh text dài rẻ hơn về bộ nhớ; trung dung giữa MHA và MQA.

## Câu 7 (Trắc nghiệm)

[Nâng cao] Độ phức tạp bộ nhớ/tính toán của self-attention thường (full) theo độ dài seq n là?

- **A.** O(n)
- **B.** O(n log n)
- **C.** O(n^2) ✅
- **D.** O(1)

**Đáp án: C**

**Giải thích:** Ma trận score n×n → O(n^2). Đây là động lực cho sliding-window, MLA, và FlashAttention (tiling, không vật chất hoá ma trận n×n).
