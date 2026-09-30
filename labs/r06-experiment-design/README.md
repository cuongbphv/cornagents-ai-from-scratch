# R06: Thiết kế và chọn thí nghiệm

Thuộc CornAgents.AI · [tuần 30](../../Week-30/README.md) · Tài liệu: [controlled-learning](../../modules/controlled-learning.md) · [specifications](../specifications.md) · [research-methods](../../modules/research-methods.md).

## Mục tiêu và cơ chế

Đặt objective, metric, tổng budget và stopping rule trước. Random search/ablation là baseline; BO chỉ thử khi evaluator đắt và objective thích hợp.

## Đầu vào

[fixtures.json](fixtures.json) là ví dụ **giả lập công khai**, chỉ dùng tìm lỗi kỹ thuật. Không có dữ liệu khách hàng, secret, hidden test hoặc kết quả LLM thật.

## Thứ tự thực hành

1. Đọc [lab.yaml](lab.yaml), viết protocol và dự đoán outcome.
2. Điền [starter.py](starter.py). Không sửa expected answer/tests để làm bài xanh.
3. Tự kiểm starter trên fixture và thêm phản ví dụ. [reference.py](reference.py) là lời giải offline để đối chiếu sau khi đã tự làm.
4. Chạy public tests của reference từ repo root:

```bash
python3 -m unittest discover -s labs/r06-experiment-design/tests -v
```

5. Điền [report_template.md](report_template.md) bằng output thật. Kiểm student starter riêng; test reference pass không xác nhận student starter đã hoàn thành.

## Gây lỗi và tiêu chí qua môn

Gain ước đoán bằng lời của LLM chưa phải acquisition score đã hiệu chỉnh. Tính cả run fail và chi phí chọn thí nghiệm.

Làm R06: giữ model/corpus, thay một cấu hình; runner dừng trước khi vượt budget. Lưu run fail, tiêu chí chọn và tổng chi phí.

**AI-off:** Có được dừng ngay khi thấy một kết quả đẹp rồi bỏ run thất bại không?

## Phạm vi code tham chiếu

Reference triển khai một phép kiểm nhỏ dùng thư viện chuẩn. Không gọi model, không train adapter LLM, không bảo vệ process/secret thật, không triển khai agent nghiên cứu hoặc phát hành production. Gọi đúng nhãn offline fixture/CPU toy. Toàn bộ R06 theo đặc tả chuyên gia cần protocol, bài biến thể và thực nghiệm riêng ngoài các ví dụ này.
