# R03: Bộ nhớ có nguồn, thời hạn và quyền đọc

Thuộc CornAgents.AI · [tuần 27](../../Week-27/README.md) · Tài liệu: [runtime-boundaries](../../modules/runtime-boundaries.md) · [evidence-and-memory](../../modules/evidence-and-memory.md) · [specifications](../specifications.md).

## Mục tiêu và cơ chế

Tách fact, episode và procedural lesson. Worker đề nghị; review mới chuyển từ quarantine sang active có phạm vi. Đọc phải kiểm trạng thái, tenant và thời hạn.

## Đầu vào

[fixtures.json](fixtures.json) là ví dụ **giả lập công khai**, chỉ dùng tìm lỗi kỹ thuật. Không có dữ liệu khách hàng, secret, hidden test hoặc kết quả LLM thật.

## Thứ tự thực hành

1. Đọc [lab.yaml](lab.yaml), viết protocol và dự đoán outcome.
2. Điền [starter.py](starter.py). Không sửa expected answer/tests để làm bài xanh.
3. Tự kiểm starter trên fixture và thêm phản ví dụ. [reference.py](reference.py) là lời giải offline để đối chiếu sau khi đã tự làm.
4. Chạy public tests của reference từ repo root:

```bash
python3 -m unittest discover -s labs/r03-governed-memory/tests -v
```

5. Điền [report_template.md](report_template.md) bằng output thật. Kiểm student starter riêng; test reference pass không xác nhận student starter đã hoàn thành.

## Gây lỗi và tiêu chí qua môn

Thu hồi nguồn phải lần theo summary/cache/lesson dẫn xuất. Xóa vector không tự xóa ảnh hưởng đã học vào weights.

Làm R03: hai tenant giả lập, nguồn bị revoke và summary hai tầng; kiểm không trả text/citation ngoài quyền. Vẽ lineage và ghi phần code toy chưa mô phỏng.

**AI-off:** Xóa entry khỏi memory có đồng nghĩa đã unlearn dữ liệu khỏi model train trước đó không?

## Phạm vi code tham chiếu

Reference triển khai một phép kiểm nhỏ dùng thư viện chuẩn. Không gọi model, không train adapter LLM, không bảo vệ process/secret thật, không triển khai agent nghiên cứu hoặc phát hành production. Gọi đúng nhãn offline fixture/CPU toy. Toàn bộ R03 theo đặc tả chuyên gia cần protocol, bài biến thể và thực nghiệm riêng ngoài các ví dụ này.
