# Retrospective: Nối Capstone về Phase 1 Internals (deliverable Tuần 18)

> Viết bằng lời mình. Mục đích: chứng minh bạn hiểu *vì sao* hệ thống hoạt động, nối kiến thức from-scratch (Phase 1) với ứng dụng (Phase 2-3).

## 1. Tôi đã build gì

- Capstone: ______
- Thành phần: RAG (______) + agents (______) + model (______)

## 2. Nối về internals (trả lời bằng lời mình)

- Hiểu biết về attention/transformer (Tuần 6-7) giúp tôi quyết định gì ở capstone? (vd. context window, vì sao chunk size quan trọng) ______
- Từ pretraining/cross-entropy (Tuần 8), vì sao model "biết" những gì nó biết, và giới hạn ở đâu? ______
- Từ fine-tuning/alignment (Tuần 9-11), khi nào fine-tune thắng prompting? Tôi đã chọn thế nào? ______
- Giữa RAG và fine-tune, tôi quyết định dùng cái nào cho phần nào, vì sao? ______

## 3. Quyết định kiến trúc & đánh đổi

- Vì sao chọn Claude làm brain + (model nào) cho sub-task? ______
- Human-in-the-loop đặt ở đâu và vì sao? ______

## 4. Điều học được lớn nhất

1. ______
2. ______
3. ______

## 5. Bước tiếp theo (sau roadmap)

- Đào sâu: ______ (vd. reasoning model, paper DeepSeekMath/GRPO, nanochat `chat_rl.py`)
- Mở rộng CornAgents.AI: ______

---
*Tiêu chí tự đánh giá xuyên suốt:* nếu giải thích được mọi thành phần cho Claude bằng lời mình thì bạn đã thực sự nắm.
