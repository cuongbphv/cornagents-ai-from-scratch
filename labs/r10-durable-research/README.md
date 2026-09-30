# R10: Chạy dài với quota, hủy và recovery

Thuộc CornAgents.AI · [tuần 34](../../Week-34/README.md) · Tài liệu: [runtime-boundaries](../../modules/runtime-boundaries.md) · [specifications](../specifications.md).

## Mục tiêu và cơ chế

Worker con tiêu cùng quota nhiệm vụ mẹ; hủy cần lan tới mọi worker/subprocess/retry. Resume vẫn kiểm quyền hiện hành.

## Đầu vào

[fixtures.json](fixtures.json) là ví dụ **giả lập công khai**, chỉ dùng tìm lỗi kỹ thuật. Không có dữ liệu khách hàng, secret, hidden test hoặc kết quả LLM thật.

## Thứ tự thực hành

1. Đọc [lab.yaml](lab.yaml), viết protocol và dự đoán outcome.
2. Điền [starter.py](starter.py). Không sửa expected answer/tests để làm bài xanh.
3. Tự kiểm starter trên fixture và thêm phản ví dụ. [reference.py](reference.py) là lời giải offline để đối chiếu sau khi đã tự làm.
4. Chạy public tests của reference từ repo root:

```bash
python3 -m unittest discover -s labs/r10-durable-research/tests -v
```

5. Điền [report_template.md](report_template.md) bằng output thật. Kiểm student starter riêng; test reference pass không xác nhận student starter đã hoàn thành.

## Gây lỗi và tiêu chí qua môn

Checkpoint không tạo exactly-once cho side effect. UNKNOWN_OUTCOME phải reconcile, không tự retry nhiều thao tác bù.

Làm R10: ack mất sau write, duplicate event, key reused, unknown outcome, cancel và revoke. Reference chỉ có in-memory toy, chưa có supervisor process thật.

**AI-off:** Worker con có được tạo budget mới để tiếp tục khi quota mẹ hết không?

## Phạm vi code tham chiếu

Reference triển khai một phép kiểm nhỏ dùng thư viện chuẩn. Không gọi model, không train adapter LLM, không bảo vệ process/secret thật, không triển khai agent nghiên cứu hoặc phát hành production. Gọi đúng nhãn offline fixture/CPU toy. Toàn bộ R10 theo đặc tả chuyên gia cần protocol, bài biến thể và thực nghiệm riêng ngoài các ví dụ này.
