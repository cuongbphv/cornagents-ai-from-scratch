# R05: Tìm bản cải tiến prompt và kỹ năng

Thuộc CornAgents.AI · [tuần 29](../../Week-29/README.md) · Tài liệu: [controlled-learning](../../modules/controlled-learning.md) · [specifications](../specifications.md).

## Mục tiêu và cơ chế

Tìm candidate trên development; chỉ thay phần allowlist. Đóng băng finalist trước confirmation. Prompt/skill optimization là L2, khác học tham số L3.

## Đầu vào

[fixtures.json](fixtures.json) là ví dụ **giả lập công khai**, chỉ dùng tìm lỗi kỹ thuật. Không có dữ liệu khách hàng, secret, hidden test hoặc kết quả LLM thật.

## Thứ tự thực hành

1. Đọc [lab.yaml](lab.yaml), viết protocol và dự đoán outcome.
2. Điền [starter.py](starter.py). Không sửa expected answer/tests để làm bài xanh.
3. Tự kiểm starter trên fixture và thêm phản ví dụ. [reference.py](reference.py) là lời giải offline để đối chiếu sau khi đã tự làm.
4. Chạy public tests của reference từ repo root:

```bash
python3 -m unittest discover -s labs/r05-candidate-search/tests -v
```

5. Điền [report_template.md](report_template.md) bằng output thật. Kiểm student starter riêng; test reference pass không xác nhận student starter đã hoàn thành.

## Gây lỗi và tiêu chí qua môn

Không cho candidate đọc hidden answers, sửa grader hoặc thêm quyền tool. GEPA/DSPy là lựa chọn tái lập riêng, không gắn nhãn cho search thủ công.

Làm R05: random search baseline trên fixture; ghi lineage và rejected candidates. Tạo candidate cố thêm quyền và xác nhận bị từ chối.

**AI-off:** Tự chọn một prompt bằng tay có thể gọi là đã tái lập GEPA không?

## Phạm vi code tham chiếu

Reference triển khai một phép kiểm nhỏ dùng thư viện chuẩn. Không gọi model, không train adapter LLM, không bảo vệ process/secret thật, không triển khai agent nghiên cứu hoặc phát hành production. Gọi đúng nhãn offline fixture/CPU toy. Toàn bộ R05 theo đặc tả chuyên gia cần protocol, bài biến thể và thực nghiệm riêng ngoài các ví dụ này.
