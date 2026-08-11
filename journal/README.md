# Nhật ký tự học (Learning Journal)

Mỗi tuần một file, đặt tên theo tuần lộ trình + tuần lịch: `W08_2026-08-17.md` (Tuần 8 của lộ trình, bắt đầu ngày 17/08/2026). Copy từ [TEMPLATE_week.md](TEMPLATE_week.md).

## Nguyên tắc ghi chép (theo Reality Filter của repo)

1. **Không có bằng chứng thì không tick "Done".** Mỗi kết quả phải kèm ít nhất một loại evidence: lệnh đã chạy + output thật, commit hash, đường dẫn file artifact, hoặc số liệu đo được.
2. **Số liệu phải kèm ngày đo và cách đo** (lệnh, script, dataset, seed nếu có). Số nhớ mang máng → ghi `[Chưa xác minh]`.
3. **Ghi cả thất bại**: OOM, loss không giảm, kết quả tệ hơn baseline — đây là dữ liệu quý nhất khi nhìn lại.
4. **Evidence lưu tại chỗ**: output dài thì lưu vào `journal/evidence/W08/` và link tới, không paste 500 dòng vào nhật ký.
5. Ghi bằng thì quá khứ, sự việc đã xảy ra — không ghi dự định như thể đã làm.

## Cấu trúc thư mục

```
journal/
├── README.md            ← file này
├── TEMPLATE_week.md     ← template copy mỗi tuần
├── W08_2026-08-17.md    ← ví dụ file tuần
└── evidence/
    └── W08/             ← log, screenshot, kết quả eval của tuần 8
```
