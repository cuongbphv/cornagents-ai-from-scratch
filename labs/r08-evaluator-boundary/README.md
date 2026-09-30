# R08: Bảo vệ evaluator và dữ liệu xác nhận

Thuộc CornAgents.AI · [tuần 32](../../Week-32/README.md) · Tài liệu: [runtime-boundaries](../../modules/runtime-boundaries.md) · [statistical-reliability](../../modules/statistical-reliability.md) · [specifications](../specifications.md).

## Mục tiêu và cơ chế

Confirmation kiểm một finalist đã cố định. Regression công khai giữ hành vi đã biết nhưng có thể overfit, không thay cohort confirmation mới.

## Đầu vào

[fixtures.json](fixtures.json) là ví dụ **giả lập công khai**, chỉ dùng tìm lỗi kỹ thuật. Không có dữ liệu khách hàng, secret, hidden test hoặc kết quả LLM thật.

## Thứ tự thực hành

1. Đọc [lab.yaml](lab.yaml), viết protocol và dự đoán outcome.
2. Điền [starter.py](starter.py). Không sửa expected answer/tests để làm bài xanh.
3. Tự kiểm starter trên fixture và thêm phản ví dụ. [reference.py](reference.py) là lời giải offline để đối chiếu sau khi đã tự làm.
4. Chạy public tests của reference từ repo root:

```bash
python3 -m unittest discover -s labs/r08-evaluator-boundary/tests -v
```

5. Điền [report_template.md](report_template.md) bằng output thật. Kiểm student starter riêng; test reference pass không xác nhận student starter đã hoàn thành.

## Gây lỗi và tiêu chí qua môn

Thay artifact sau khi được duyệt làm evidence mismatch. Đáp án kín nằm ngoài repo public/worker; fixture công khai của bài này không phải hidden test thật.

Làm R08: tính digest, sửa một tham số và kiểm từ chối. Thiết kế process/credential tách biệt và sổ query budget; diễn tập contamination bằng trace chứa nhãn.

**AI-off:** Sửa candidate sau khi có report tốt rồi giữ report cũ có hợp lệ không?

## Phạm vi code tham chiếu

Reference triển khai một phép kiểm nhỏ dùng thư viện chuẩn. Không gọi model, không train adapter LLM, không bảo vệ process/secret thật, không triển khai agent nghiên cứu hoặc phát hành production. Gọi đúng nhãn offline fixture/CPU toy. Toàn bộ R08 theo đặc tả chuyên gia cần protocol, bài biến thể và thực nghiệm riêng ngoài các ví dụ này.
