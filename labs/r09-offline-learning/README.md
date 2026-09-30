# R09: Học tham số offline và giữ năng lực cũ

Thuộc CornAgents.AI · [tuần 33](../../Week-33/README.md) · Tài liệu: [research-contracts](../../modules/research-contracts.md) · [specifications](../specifications.md) · [controlled-learning](../../modules/controlled-learning.md).

## Mục tiêu và cơ chế

SFT/LoRA/DPO cần dữ liệu được phép dùng, nhãn có tiêu chí và lineage. So base/candidate trên nhóm mới, nhóm cũ và ngoài phạm vi.

## Đầu vào

[fixtures.json](fixtures.json) là ví dụ **giả lập công khai**, chỉ dùng tìm lỗi kỹ thuật. Không có dữ liệu khách hàng, secret, hidden test hoặc kết quả LLM thật.

## Thứ tự thực hành

1. Đọc [lab.yaml](lab.yaml), viết protocol và dự đoán outcome.
2. Điền [starter.py](starter.py). Không sửa expected answer/tests để làm bài xanh.
3. Tự kiểm starter trên fixture và thêm phản ví dụ. [reference.py](reference.py) là lời giải offline để đối chiếu sau khi đã tự làm.
4. Chạy public tests của reference từ repo root:

```bash
python3 -m unittest discover -s labs/r09-offline-learning/tests -v
```

5. Điền [report_template.md](report_template.md) bằng output thật. Kiểm student starter riêng; test reference pass không xác nhận student starter đã hoàn thành.

## Gây lỗi và tiêu chí qua môn

CPU low-rank toy minh họa W+A×B, không phải adapter LLM được fine-tune. Replay không chứng minh live-model gain.

Làm R09: kiểm low-rank update nhỏ và rollback weights; lập data card/preference rubric. Nhánh live-model chỉ chạy khi có runtime, license, dataset và budget rõ.

**AI-off:** DPO preference chọn văn phong tự tin có đảm bảo factuality không?

## Phạm vi code tham chiếu

Reference triển khai một phép kiểm nhỏ dùng thư viện chuẩn. Không gọi model, không train adapter LLM, không bảo vệ process/secret thật, không triển khai agent nghiên cứu hoặc phát hành production. Gọi đúng nhãn offline fixture/CPU toy. Toàn bộ R09 theo đặc tả chuyên gia cần protocol, bài biến thể và thực nghiệm riêng ngoài các ví dụ này.
