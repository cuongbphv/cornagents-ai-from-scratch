# Tuần 6, Quiz: Tokenization, embeddings, attention từ đầu

> Tự kiểm tra **trước** khi xem solution. Tổng **10** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Vì sao trong scaled dot-product attention ta chia cho sqrt(d_k)?

- **A.** Để score luôn dương
- **B.** Để chuẩn hoá vector về độ dài 1
- **C.** Để tiết kiệm bộ nhớ
- **D.** Để giữ phương sai của score ổn định, tránh softmax bão hoà làm gradient triệt tiêu

## Câu 2 (Tự luận)

Causal mask làm gì và cài đặt thế nào?

## Câu 3 (Trắc nghiệm)

Token embedding và positional embedding được kết hợp thế nào trong GPT-2?

- **A.** Nhân element-wise
- **B.** Chỉ dùng token embedding
- **C.** Nối (concatenate) lại
- **D.** Cộng vào nhau (cùng chiều d_model)

## Câu 4 (Trắc nghiệm)

Ma trận attention scores (trước khi nhân V) có shape nào với input (batch, seq, d)?

- **A.** (batch, d, d)
- **B.** (seq, seq)
- **C.** (batch, seq, d)
- **D.** (batch, seq, seq)

## Câu 5 (Tự luận)

[Nâng cao] RoPE khác với positional embedding tuyệt đối của GPT-2 thế nào?

## Câu 6 (Trắc nghiệm)

[Nâng cao] Mục đích chính của Grouped-Query Attention (GQA) so với Multi-Head Attention?

- **A.** Thay softmax bằng sigmoid
- **B.** Tăng số head để chính xác hơn
- **C.** Bỏ hoàn toàn key và value
- **D.** Cho các nhóm head chia sẻ chung K,V để GIẢM kích thước KV cache khi inference

## Câu 7 (Trắc nghiệm)

[Nâng cao] Độ phức tạp bộ nhớ/tính toán của self-attention thường (full) theo độ dài seq n là?

- **A.** O(1)
- **B.** O(n)
- **C.** O(n log n)
- **D.** O(n^2)

## Câu 8 (Tự luận)

Jurafsky và Martin (SLP3 mục 2.4) nói từ và morpheme có nghĩa ổn định nhưng khó định nghĩa hình thức, còn ký tự thì dễ định nghĩa nhưng quá nhỏ. BPE giải quyết mâu thuẫn này bằng cách nào, và vì sao việc chuẩn hóa đơn vị token lại cần cho perplexity?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

GQA (arXiv 2305.13245) là gì, và vì sao nó làm giảm KV cache nhưng không làm giảm số phép nhân trong QKᵀ?

- **A.** GQA chia query head thành g nhóm cùng chia sẻ một cặp K, V; cache chỉ lưu n_kv_head cặp nên nhỏ hơn, nhưng mỗi query head vẫn tính điểm với toàn bộ K của nhóm nên số phép nhân điểm attention không đổi
- **B.** GQA chỉ áp dụng khi train, không khi inference
- **C.** GQA bỏ hẳn value
- **D.** GQA giảm số query head

## Nâng cao 2 (Tự luận)

FlashAttention được gọi là exact attention. Nó thay đổi điều gì và không thay đổi điều gì so với cách bạn cài attention ở tuần này?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
