# Graph Engineering — Ghi chú (deliverable Tuần 14)

> Điền sau khi chạy `kg_pipeline.py` trên corpus Finance Banking của bạn. Điền các chỗ ______.

## 1. Corpus & schema

- Tài liệu đã dùng (5–10): ______
- Entity types cho domain: ______ (vd. REGULATION, DOCUMENT, PROCESS, PERSON, ORGANIZATION)
- Số entities/relations extract được theo từng tài liệu: ______

## 2. Resolution

- Số surface forms → số canonical entities (compression ratio): ______
- Ví dụ merge đúng mà string similarity sẽ bỏ lỡ (kiểu "Edwin Aldrin" → "Buzz Aldrin"): ______
- Có case over-merge (hai thứ khác nhau bị gộp)? Xử lý thế nào? ______

## 3. Graph diagnostics

| Chỉ số | Giá trị | Đọc thế nào |
|---|---|---|
| Weakly connected components | ______ | 1 = resolution tốt; nhiều = còn đảo rời |
| Hub nodes (degree cao nhất) | ______ | Thường là entity "buộc" cả corpus |
| Edges / nodes ratio | ______ | <1.0 thưa; ~1.0–2.0 khoẻ; >2.0 rất kết nối |

## 4. Grounded vs ungrounded

| Câu hỏi multi-hop | Ungrounded answer | Grounded answer (cite edges) | Nhận xét |
|---|---|---|---|
| ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ |

- TODO: vì sao trên private corpus chỉ grounded answer là dùng được? ______

## 5. Evaluation feedback loop

- Gold set: ______ entities, ______ relations (từ tài liệu nào: ______)
- Vòng 1: precision ______ / recall ______ / F1 ______
- Thay đổi prompt đã thử: ______
- Vòng 2: precision ______ / recall ______ / F1 ______
- TODO: trade-off precision vs recall của câu "extract only entities central to the document" — bạn chọn phía nào, vì sao? ______

## 6. Cắm vào CornAgents.AI

- Agent nào GHI vào graph: ______
- Agent nào ĐỌC/fact-check theo graph: ______
- Một ví dụ evaluator bắt được claim không có edge chống lưng: ______

## 7. Tóm tắt 3 câu

1. ______
2. ______
3. ______

---
*Nhắc lại từ docs:* "Every important output can be traced to an objective, a plan, an artifact, a source, a graph path, an evaluator decision, and a bounded execution record." — khi câu này sai, thêm agent chỉ tăng độ mờ đục.
