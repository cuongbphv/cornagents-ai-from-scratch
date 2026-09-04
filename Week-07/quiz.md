# Tuần 7, Quiz: Lắp ráp & chạy mô hình GPT

> Tự kiểm tra **trước** khi xem solution. Tổng **9** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
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
