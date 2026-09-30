# R04: Học từ lỗi bằng bài học có điều kiện

Thuộc CornAgents.AI · [tuần 28](../../Week-28/README.md) · Tài liệu: [research-contracts](../../modules/research-contracts.md) · [evidence-and-memory](../../modules/evidence-and-memory.md) · [controlled-learning](../../modules/controlled-learning.md) · [specifications](../specifications.md).

## Mục tiêu và cơ chế

Reflexion là phản hồi ngôn ngữ và episodic memory, không tự cập nhật weights. Lesson phải có điều kiện áp dụng, phản ví dụ và cách xử lý ngoài scope.

## Đầu vào

[fixtures.json](fixtures.json) là ví dụ **giả lập công khai**, chỉ dùng tìm lỗi kỹ thuật. Không có dữ liệu khách hàng, secret, hidden test hoặc kết quả LLM thật.

## Thứ tự thực hành

1. Đọc [lab.yaml](lab.yaml), viết protocol và dự đoán outcome.
2. Điền [starter.py](starter.py). Không sửa expected answer/tests để làm bài xanh.
3. Tự kiểm starter trên fixture và thêm phản ví dụ. [reference.py](reference.py) là lời giải offline để đối chiếu sau khi đã tự làm.
4. Chạy public tests của reference từ repo root:

```bash
python3 -m unittest discover -s labs/r04-conditional-lessons/tests -v
```

5. Điền [report_template.md](report_template.md) bằng output thật. Kiểm student starter riêng; test reference pass không xác nhận student starter đã hoàn thành.

## Gây lỗi và tiêu chí qua môn

Thắng khi retry cùng task có thể chỉ tận dụng đáp án cũ. Cần frozen baseline, transfer tasks và retention dưới budget khai báo.

Làm R04: so parser rule/bộ nhớ lesson trên trường có grammar; kiểm đổi đơn vị và thiếu header. Thiết kế nhánh Reflexion live riêng; reference offline không gọi LLM.

**AI-off:** Lesson “luôn dùng parser” sai ở trường hợp nào trong lab?

## Phạm vi code tham chiếu

Reference triển khai một phép kiểm nhỏ dùng thư viện chuẩn. Không gọi model, không train adapter LLM, không bảo vệ process/secret thật, không triển khai agent nghiên cứu hoặc phát hành production. Gọi đúng nhãn offline fixture/CPU toy. Toàn bộ R04 theo đặc tả chuyên gia cần protocol, bài biến thể và thực nghiệm riêng ngoài các ví dụ này.
