# R11: Duyệt đúng bản cải tiến, shadow và rollback

Thuộc CornAgents.AI · [tuần 35](../../Week-35/README.md) · Tài liệu: [runtime-boundaries](../../modules/runtime-boundaries.md) · [specifications](../specifications.md) · [promotion-and-revocation](../../modules/promotion-and-revocation.md).

## Mục tiêu và cơ chế

Evidence và approval gắn đúng digest, policy/model/corpus/memory snapshot, scope và expiry. Shadow không tác động quyết định thực; canary cần phạm vi/tác động đã duyệt.

## Đầu vào

[fixtures.json](fixtures.json) là ví dụ **giả lập công khai**, chỉ dùng tìm lỗi kỹ thuật. Không có dữ liệu khách hàng, secret, hidden test hoặc kết quả LLM thật.

## Thứ tự thực hành

1. Đọc [lab.yaml](lab.yaml), viết protocol và dự đoán outcome.
2. Điền [starter.py](starter.py). Không sửa expected answer/tests để làm bài xanh.
3. Tự kiểm starter trên fixture và thêm phản ví dụ. [reference.py](reference.py) là lời giải offline để đối chiếu sau khi đã tự làm.
4. Chạy public tests của reference từ repo root:

```bash
python3 -m unittest discover -s labs/r11-promotion/tests -v
```

5. Điền [report_template.md](report_template.md) bằng output thật. Kiểm student starter riêng; test reference pass không xác nhận student starter đã hoàn thành.

## Gây lỗi và tiêu chí qua môn

Rollback đổi bản đang dùng; revoke cấm dùng quyền/nguồn/candidate. Rollback không tự đảo một side effect bên ngoài.

Làm R11: promote đúng digest, sửa artifact sau eval, scope thiếu, violation và rollback. Viết release package; thử trong mô phỏng, không deploy production.

**AI-off:** Tại sao rollback và revoke cần hai quyết định riêng?

## Phạm vi code tham chiếu

Reference triển khai một phép kiểm nhỏ dùng thư viện chuẩn. Không gọi model, không train adapter LLM, không bảo vệ process/secret thật, không triển khai agent nghiên cứu hoặc phát hành production. Gọi đúng nhãn offline fixture/CPU toy. Toàn bộ R11 theo đặc tả chuyên gia cần protocol, bài biến thể và thực nghiệm riêng ngoài các ví dụ này.
