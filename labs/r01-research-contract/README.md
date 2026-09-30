# R01: Từ câu hỏi rộng thành phạm vi nghiên cứu

Thuộc CornAgents.AI · [tuần 25](../../Week-25/README.md) · Tài liệu: [research-contracts](../../modules/research-contracts.md) · [evidence-and-memory](../../modules/evidence-and-memory.md) · [specifications](../specifications.md).

## Mục tiêu và cơ chế

Tách câu hỏi, scope, thời gian nguồn, công cụ, ngân sách và điều kiện hoàn thành. Gắn claim_kind: source_fact, computed, inference hoặc hypothesis.

## Đầu vào

[fixtures.json](fixtures.json) là ví dụ **giả lập công khai**, chỉ dùng tìm lỗi kỹ thuật. Không có dữ liệu khách hàng, secret, hidden test hoặc kết quả LLM thật.

## Thứ tự thực hành

1. Đọc [lab.yaml](lab.yaml), viết protocol và dự đoán outcome.
2. Điền [starter.py](starter.py). Không sửa expected answer/tests để làm bài xanh.
3. Tự kiểm starter trên fixture và thêm phản ví dụ. [reference.py](reference.py) là lời giải offline để đối chiếu sau khi đã tự làm.
4. Chạy public tests của reference từ repo root:

```bash
python3 -m unittest discover -s labs/r01-research-contract/tests -v
```

5. Điền [report_template.md](report_template.md) bằng output thật. Kiểm student starter riêng; test reference pass không xác nhận student starter đã hoàn thành.

## Gây lỗi và tiêu chí qua môn

Không tự mở rộng sang một đề tài khác để dễ báo hoàn thành; bản đăng lại phải có origin cluster.

Làm R01: viết contract và ledger cho câu hỏi parser tiếng Việt; fixture có hai bản sao cùng xuất xứ. Phân loại phát biểu và ghi giới hạn từng claim.

**AI-off:** Nguồn chưa trả được toàn văn thì có được nói đã tích hợp từng chi tiết không?

## Phạm vi code tham chiếu

Reference triển khai một phép kiểm nhỏ dùng thư viện chuẩn. Không gọi model, không train adapter LLM, không bảo vệ process/secret thật, không triển khai agent nghiên cứu hoặc phát hành production. Gọi đúng nhãn offline fixture/CPU toy. Toàn bộ R01 theo đặc tả chuyên gia cần protocol, bài biến thể và thực nghiệm riêng ngoài các ví dụ này.
