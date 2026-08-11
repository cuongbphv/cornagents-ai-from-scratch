# Vì sao attention permutation-equivariant và cần positional info

> Deliverable Tuần 2. **Viết bằng lời của bạn**, sau đó dán cho Claude review.
> Dưới đây là khung gợi ý + câu hỏi dẫn dắt. Đừng để trống — viết nháp rồi sửa.

## 1. Định nghĩa: equivariant vs invariant

- **Permutation-invariant**: đổi thứ tự input → output KHÔNG đổi (vd. sum, mean).
- **Permutation-equivariant**: đổi thứ tự input → output đổi theo ĐÚNG cách hoán vị đó.

TODO: Viết lại 2 định nghĩa trên bằng lời mình + 1 ví dụ đời thường cho mỗi loại.

## 2. Vì sao self-attention permutation-equivariant

Cho chuỗi token `x₁..xₙ`. Mỗi token sinh query/key/value qua các ma trận chung `W_Q, W_K, W_V` (giống nhau cho mọi vị trí). Attention score giữa i và j chỉ là dot product `qᵢ · kⱼ`, KHÔNG chứa thông tin về **vị trí** i hay j.

→ Nếu hoán vị thứ tự token đầu vào, tập các score y hệt, chỉ bị đánh số lại; output cũng bị hoán vị tương ứng → **equivariant**.

TODO trả lời:
- Vì sao việc `W_Q, W_K, W_V` dùng chung cho mọi vị trí dẫn tới equivariance? ______
- Nếu đổi chỗ token 1 và token 5, output tại vị trí tương ứng thay đổi ra sao? ______

## 3. Hệ quả: model "mù" thứ tự nếu không thêm gì

Với ngôn ngữ, thứ tự mang nghĩa: "chó cắn người" ≠ "người cắn chó". Nhưng attention thuần không phân biệt được hai chuỗi này nếu chúng chỉ khác thứ tự.

TODO: Cho 1 ví dụ tiếng Việt mà đổi thứ tự từ làm đổi nghĩa, và giải thích vì sao attention thuần xử lý sai. ______

## 4. Giải pháp: positional encoding/embedding

Tiêm thông tin vị trí vào input để phá vỡ tính equivariance một cách có kiểm soát:
- **Sinusoidal** (paper gốc "Attention Is All You Need").
- **Learned positional embeddings** (GPT-2 — sẽ gặp ở Tuần 3–4).
- **RoPE** (rotary) — phổ biến ở các model hiện đại.

TODO:
- Positional info được CỘNG vào hay nối vào embedding? (kiểm tra với GPT-2) ______
- Vì sao thêm vị trí làm attention không còn permutation-equivariant nữa? ______
- (Nâng cao) RoPE khác learned positional embedding ở chỗ nào? ______

## 5. Tóm tắt 3 câu (viết sau cùng)

1. ______
2. ______
3. ______

---
*Checklist trước khi gửi Claude review:* đã viết bằng lời mình ✓ · có ví dụ cụ thể ✓ · trả lời hết các TODO ✓
