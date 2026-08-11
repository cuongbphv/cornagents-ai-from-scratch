# Retrospective — Nối Capstone về Phase 1 Internals (deliverable Tuần 15)

> Viết bằng lời mình. Mục đích: chứng minh bạn hiểu *vì sao* hệ thống hoạt động, nối kiến thức from-scratch (Phase 1) với ứng dụng (Phase 2–3).

## 1. Tôi đã build gì

- Capstone: ______
- Thành phần: RAG (______) + agents (______) + model (______)

## 2. Nối về internals (trả lời bằng lời mình)

- **Attention/transformer** (Tuần 3–4): hiểu biết này giúp tôi quyết định gì ở capstone? (vd. context window, vì sao chunk size quan trọng) ______
- **Pretraining/cross-entropy** (Tuần 5): vì sao model "biết" những gì nó biết, và giới hạn ở đâu? ______
- **Fine-tuning/alignment** (Tuần 6–8): khi nào fine-tune thắng prompting? Tôi đã chọn thế nào? ______
- **RAG vs fine-tune**: tôi quyết định dùng cái nào cho phần nào, vì sao? ______

## 3. Quyết định kiến trúc & đánh đổi

- Vì sao chọn Claude làm brain + (model nào) cho sub-task? ______
- Human-in-the-loop đặt ở đâu và vì sao? ______

## 4. Điều học được lớn nhất

1. ______
2. ______
3. ______

## 5. Bước tiếp theo (sau roadmap)

- Đào sâu: ______ (vd. reasoning model — sách Raschka full 28/07/2026; repo `reasoning-from-scratch`)
- Mở rộng CornAgents.AI: ______

---
*Tiêu chí tự đánh giá xuyên suốt:* nếu giải thích được mọi thành phần cho Claude bằng lời mình → bạn đã thực sự nắm.
