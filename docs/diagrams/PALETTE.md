# Diagram palette

Stage coloring for README infographics (original assets).

| Token | Hex | Meaning |
|-------|-----|---------|
| data | `#0d9488` | Data / Token |
| model | `#2563eb` | Model / Phase 1 |
| train | `#d97706` | Pretrain / SFT |
| align | `#e11d48` | Alignment / cloud branch |
| eval | `#16a34a` | Eval / Serve / stay local |
| rag | `#0891b2` | RAG |
| agent | `#9333ea` | Agent |
| graph | `#4f46e5` | Graph / Phase 3 |

Motion: các SVG gốc dùng SMIL (`animate` / `animateMotion`). Khả năng hiển thị chuyển động phụ thuộc trình đọc và bộ xử lý ảnh; bố cục đứng yên vẫn phải đọc được.

Regenerate: `python docs/diagrams/_gen_svgs.py`

## Bộ diagram cho lịch chính

- `08-learning-journey.svg`: năm chặng, số tuần lấy từ `curriculum.json`; có bản dọc cho màn hình nhỏ.
- `09-cornloop.svg`: vòng nhiệm vụ, vòng học, vòng kiểm soát; G1/G2/G3 riêng.
- `10-candidate-lifecycle.svg`: quarantine, eval, duyệt đúng bản, dùng trong scope và rollback/revoke.

Mỗi hình có bản `-static.svg` không chuyển động. SVG mới không dùng JavaScript hay tài nguyên ngoài; có title/desc và `prefers-reduced-motion`. Luồng chuyển động là minh họa khái niệm, không phải tiến độ hay kết quả agent. Các hình 01–07 giữ nguyên.

Sinh bộ mới: `python3 docs/diagrams/_gen_motion_diagrams.py`.

Mở [gallery](index.html) để xem và bật/tắt chuyển động. Dùng bản static khi trình đọc không hỗ trợ motion; không cam kết mọi trình đọc Markdown phát animation.

Màu tiếp tục theo các stage gốc: teal cho nền, blue cho model, cyan cho retrieval, purple cho agent/control, gold cho learning, green cho thay đổi được kiểm. Chữ đứng yên; motion chỉ chạy trên tuyến liên kết. Nguồn thiết kế: [curriculum](../../curriculum.json), [CornLoop](../../modules/research-contracts.md), [promotion](../../modules/promotion-and-revocation.md).
