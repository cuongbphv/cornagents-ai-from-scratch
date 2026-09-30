# R12: CornBench-VI: học qua nhiều vòng và báo cáo tái lập

Thuộc CornAgents.AI · [tuần 36](../../Week-36/README.md) · Tài liệu: [specifications](../specifications.md) · [DESIGN](../../benchmarks/cornbench_vi_rl/DESIGN.md) · [research-methods](../../modules/research-methods.md) · [graduation-and-maintenance](../../modules/graduation-and-maintenance.md).

## Mục tiêu và cơ chế

Capstone gồm frozen baseline, một cơ chế học và nhiều cohort mới. Chấm G1/G2/G3 riêng; báo gain, retention, risk–coverage và tổng chi phí kể cả kết quả âm.

## Đầu vào

[fixtures.json](fixtures.json) là ví dụ **giả lập công khai**, chỉ dùng tìm lỗi kỹ thuật. Không có dữ liệu khách hàng, secret, hidden test hoặc kết quả LLM thật.

## Thứ tự thực hành

1. Đọc [lab.yaml](lab.yaml), viết protocol và dự đoán outcome.
2. Điền [starter.py](starter.py). Không sửa expected answer/tests để làm bài xanh.
3. Tự kiểm starter trên fixture và thêm phản ví dụ. [reference.py](reference.py) là lời giải offline để đối chiếu sau khi đã tự làm.
4. Chạy public tests của reference từ repo root:

```bash
python3 -m unittest discover -s labs/r12-cornbench-learning/tests -v
```

5. Điền [report_template.md](report_template.md) bằng output thật. Kiểm student starter riêng; test reference pass không xác nhận student starter đã hoàn thành.

## Gây lỗi và tiêu chí qua môn

Fixture vài task dùng tìm lỗi kỹ thuật, không phải benchmark đã xuất bản hay bằng chứng accuracy của agent. H1 chưa được xác nhận tốt hơn.

Làm R12 và H1: đăng ký protocol, chia development/confirmation/retention theo family; chạy baseline/lesson ablation. Reference parser replay chỉ kiểm fixture; nộp report giới hạn và lệnh tái lập.

**AI-off:** Candidate không cải thiện nhưng thí nghiệm đúng có được hạ ngưỡng để tốt nghiệp không?

## Phạm vi code tham chiếu

Reference triển khai một phép kiểm nhỏ dùng thư viện chuẩn. Không gọi model, không train adapter LLM, không bảo vệ process/secret thật, không triển khai agent nghiên cứu hoặc phát hành production. Gọi đúng nhãn offline fixture/CPU toy. Toàn bộ R12 theo đặc tả chuyên gia cần protocol, bài biến thể và thực nghiệm riêng ngoài các ví dụ này.
