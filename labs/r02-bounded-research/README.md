# R02: Nghiên cứu lặp, phản chứng và điều kiện dừng

Thuộc CornAgents.AI · [tuần 26](../../Week-26/README.md) · Tài liệu: [research-contracts](../../modules/research-contracts.md) · [evidence-and-memory](../../modules/evidence-and-memory.md) · [specifications](../specifications.md).

## Mục tiêu và cơ chế

Mỗi query phải nhằm kiểm câu hỏi trong contract. Vòng nghiên cứu ghi support/counterevidence và dừng khi hết budget hoặc không còn phép kiểm hợp lệ.

## Đầu vào

[fixtures.json](fixtures.json) là ví dụ **giả lập công khai**, chỉ dùng tìm lỗi kỹ thuật. Không có dữ liệu khách hàng, secret, hidden test hoặc kết quả LLM thật.

## Thứ tự thực hành

1. Đọc [lab.yaml](lab.yaml), viết protocol và dự đoán outcome.
2. Điền [starter.py](starter.py). Không sửa expected answer/tests để làm bài xanh.
3. Tự kiểm starter trên fixture và thêm phản ví dụ. [reference.py](reference.py) là lời giải offline để đối chiếu sau khi đã tự làm.
4. Chạy public tests của reference từ repo root:

```bash
python3 -m unittest discover -s labs/r02-bounded-research/tests -v
```

5. Điền [report_template.md](report_template.md) bằng output thật. Kiểm student starter riêng; test reference pass không xác nhận student starter đã hoàn thành.

## Gây lỗi và tiêu chí qua môn

Hết budget nhưng chưa đủ evidence là incomplete/uncertain, không đổi nhãn thành successful.

Làm R02: xử lý nguồn cũ/mới/mâu thuẫn; ghi query nào thêm evidence. Thử hết budget, query drift và nguồn không trả đáp án.

**AI-off:** Tại sao nguồn hỗ trợ và nguồn phản bác cần giữ cùng báo cáo?

## Phạm vi code tham chiếu

Reference triển khai một phép kiểm nhỏ dùng thư viện chuẩn. Không gọi model, không train adapter LLM, không bảo vệ process/secret thật, không triển khai agent nghiên cứu hoặc phát hành production. Gọi đúng nhãn offline fixture/CPU toy. Toàn bộ R02 theo đặc tả chuyên gia cần protocol, bài biến thể và thực nghiệm riêng ngoài các ví dụ này.
