# R07: Hiệu chỉnh, risk–coverage và cận thống kê

Thuộc CornAgents.AI · [tuần 31](../../Week-31/README.md) · Tài liệu: [statistical-reliability](../../modules/statistical-reliability.md) · [specifications](../specifications.md).

## Mục tiêu và cơ chế

Coverage=A/N; accepted risk=E/A khi A>0. Chọn threshold trên calibration rồi cố định; cận nhị thức dùng cho policy và mẫu phù hợp, không cho một câu trả lời cụ thể.

## Đầu vào

[fixtures.json](fixtures.json) là ví dụ **giả lập công khai**, chỉ dùng tìm lỗi kỹ thuật. Không có dữ liệu khách hàng, secret, hidden test hoặc kết quả LLM thật.

## Thứ tự thực hành

1. Đọc [lab.yaml](lab.yaml), viết protocol và dự đoán outcome.
2. Điền [starter.py](starter.py). Không sửa expected answer/tests để làm bài xanh.
3. Tự kiểm starter trên fixture và thêm phản ví dụ. [reference.py](reference.py) là lời giải offline để đối chiếu sau khi đã tự làm.
4. Chạy public tests của reference từ repo root:

```bash
python3 -m unittest discover -s labs/r07-risk-coverage/tests -v
```

5. Điền [report_template.md](report_template.md) bằng output thật. Kiểm student starter riêng; test reference pass không xác nhận student starter đã hoàn thành.

## Gây lỗi và tiêu chí qua môn

Model tự nói chắc 95% không phải xác suất đã hiệu chỉnh. CP pass chỉ là cổng thống kê, không cấp quyền deploy; nhiều candidate cần protocol khác.

Làm R07: no-data, zero-error, một lỗi và retry trùng task; giải thích giả định. So công thức zero-error với reference; ghi rõ CP toy không kiểm representativeness.

**AI-off:** Không thấy lỗi trong mẫu có chứng minh tỷ lệ lỗi thật bằng 0 không?

## Phạm vi code tham chiếu

Reference triển khai một phép kiểm nhỏ dùng thư viện chuẩn. Không gọi model, không train adapter LLM, không bảo vệ process/secret thật, không triển khai agent nghiên cứu hoặc phát hành production. Gọi đúng nhãn offline fixture/CPU toy. Toàn bộ R07 theo đặc tả chuyên gia cần protocol, bài biến thể và thực nghiệm riêng ngoài các ví dụ này.
