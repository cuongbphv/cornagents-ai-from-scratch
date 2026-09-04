# Tuần 7, Đáp án & Giải thích: Lắp ráp & chạy mô hình GPT

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

LayerNorm trong transformer chuẩn hoá theo chiều nào?

- **A.** Theo chiều batch (như BatchNorm)
- **B.** Theo chiều feature/embedding của từng token (last dim) (đáp án đúng)
- **C.** Theo chiều sequence
- **D.** Theo toàn bộ tensor

**Đáp án: B**

**Giải thích:** LayerNorm chuẩn hoá theo feature của mỗi token độc lập (không phụ thuộc batch) → ổn định, hợp với độ dài chuỗi thay đổi.

## Câu 2 (Tự luận)

Pre-LN + residual: x = x + Sublayer(LN(x)). Vì sao thiết kế này giúp train mạng sâu?

**Trả lời mẫu:** Residual tạo một 'đường cao tốc' để gradient chảy thẳng về các lớp đầu mà không bị nhân nhỏ dần qua nhiều lớp (chống vanishing gradient). Đặt LayerNorm TRƯỚC sublayer (pre-LN) giữ đầu vào mỗi sublayer ở thang đo ổn định, làm việc xếp chồng hàng chục block ổn định hơn so với post-LN. Nhờ vậy có thể train transformer rất sâu.

**Giải thích:** Ngoài vai trò shortcut gradient, residual còn cho phép mỗi block tinh chỉnh dần biểu diễn (residual stream).

## Câu 3 (Trắc nghiệm)

Feed-forward network (FFN) trong block GPT-2 mở rộng chiều ẩn lên khoảng mấy lần d_model?

- **A.** 2 lần
- **B.** 4 lần (đáp án đúng)
- **C.** 8 lần
- **D.** Không mở rộng

**Đáp án: B**

**Giải thích:** FFN: Linear(d → 4d) → GELU → Linear(4d → d). Hệ số 4× là chuẩn của GPT-2.

## Câu 4 (Trắc nghiệm)

GPT-2 small có khoảng bao nhiêu tham số (với emb_dim=768, n_layers=12, n_heads=12)?

- **A.** ~50M
- **B.** ~124M (đáp án đúng)
- **C.** ~350M
- **D.** ~1.5B

**Đáp án: B**

**Giải thích:** ~124M. Verify số tham số là cách kiểm tra nhanh kiến trúc đã ghép đúng.

## Câu 5 (Tự luận)

[Nâng cao] RMSNorm khác LayerNorm ở điểm nào, vì sao model hiện đại chuộng nó?

**Trả lời mẫu:** RMSNorm bỏ bước trừ mean và bỏ bias β; chỉ chia cho căn của trung bình bình phương rồi nhân γ: x / sqrt(mean(x^2) + eps) · γ. Ít phép tính hơn LayerNorm nhưng ổn định tương đương, nên Llama/Qwen dùng để rẻ và nhanh hơn ở quy mô lớn.

**Giải thích:** Xem mục A2 trong advanced_topics_vi.md.

## Câu 6 (Trắc nghiệm)

[Nâng cao] SwiGLU FFN của Llama/Qwen thay thế phần nào của GPT-2?

- **A.** Thay attention
- **B.** Thay FFN GELU-4× bằng một FFN có cổng (gated) dùng SiLU, ~2/3·4d chiều ẩn (đáp án đúng)
- **C.** Thay LayerNorm
- **D.** Thay positional embedding

**Đáp án: B**

**Giải thích:** SwiGLU = (SiLU(x W_gate) ⊙ x W_up) W_down; có 3 ma trận nên giảm chiều ẩn để giữ số tham số tương đương.

## Câu 7 (Trắc nghiệm)

[Nâng cao] Trong một lớp Mixture-of-Experts (MoE), 'router' làm gì?

- **A.** Chọn top-k expert (FFN con) cho mỗi token, chỉ kích hoạt số ít expert (đáp án đúng)
- **B.** Định tuyến gradient ngược
- **C.** Chọn GPU để chạy
- **D.** Sắp xếp token theo độ dài

**Đáp án: A**

**Giải thích:** Router gán mỗi token cho top-k experts → tổng tham số lớn nhưng tham số active mỗi token nhỏ; cần lo load balancing. Qwen3-MoE, gpt-oss, DeepSeek dùng MoE.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Top-p (nucleus) sampling khác top-k ở điểm nào theo Jurafsky và Martin, và vì sao điểm đó quan trọng khi ngữ cảnh đổi?

- **A.** Top-p luôn chọn nhiều token hơn top-k
- **B.** Top-k giữ k token cố định còn top-p giữ tập nhỏ nhất chiếm p khối xác suất, nên số ứng viên tự co giãn theo hình dạng phân phối trong từng ngữ cảnh (đáp án đúng)
- **C.** Top-p chỉ dùng khi temperature bằng 1
- **D.** Top-p là greedy với p = 1

**Đáp án: B**

**Giải thích:** SLP3 mục 7.6.4 (trang 200): k cố định là điểm yếu vì có ngữ cảnh 10 token đầu chiếm gần hết khối xác suất, có ngữ cảnh phân phối phẳng.

## Nâng cao 2 (Tự luận)

Vì sao khi kiểm tra kiến trúc GPT bằng cách load trọng số GPT-2 rồi sinh text, nên bắt đầu bằng greedy decoding thay vì sampling?

**Trả lời mẫu:** Greedy loại bỏ biến ngẫu nhiên của sampling: nếu output vô nghĩa ở greedy thì lỗi nhiều khả năng nằm ở kiến trúc hoặc mapping trọng số, không ở tham số sampling. Đây là suy luận thực hành của người viết, dựa trên việc greedy là hàm xác định của logits (SLP3 mục 7.6, trang 196).

**Giải thích:** Sau khi greedy ra text mạch lạc, mới bật temperature và top-p để so phong cách.
