# Protocol đánh giá độc lập

Tài liệu: [phép đo](../../modules/statistical-reliability.md), [benchmark](../../benchmarks/cornbench_vi_rl/DESIGN.md) và [promotion](../../modules/promotion-and-revocation.md). File này là mẫu quy trình, không phải test set đã được kiểm định.

1. Chốt outcome, loss, sampling unit, dependence assumptions, scope và budget trước.
2. Phát triển trên development, chọn threshold trên calibration; giữ confirmation riêng theo family/nguồn/thời gian.
3. Đóng băng finalist, code/model/prompt/config/corpus/memory/evaluator versions và digest.
4. Evaluator do maintainer quản lý ngoài worker, hidden answers không mount vào candidate. Fixture công khai của repo không thay bước này.
5. Ghi số task, accepted, lỗi, coverage, cận/giả định và retention; lưu toàn bộ fail và bất đồng nhãn.
6. Thử nhiều candidate/lặp feedback phải có protocol phù hợp; không coi Bonferroni chữa được contamination.
7. Bằng chứng gắn đúng artifact/scope/expiry; người có thẩm quyền quyết định. Thiếu dữ liệu thì INSUFFICIENT_EVIDENCE; cổng thống kê không cấp quyền triển khai.
