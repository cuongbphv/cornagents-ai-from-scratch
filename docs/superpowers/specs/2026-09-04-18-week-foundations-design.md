# Thiết kế: mở lộ trình lên 18 tuần với Phase 0 nền tảng toán và ML

Ngày viết: 2026-09-04. Người duyệt: chủ repo (đã chọn phương án "chèn đầu, đổi số" trong phiên làm việc).

## Vấn đề

Lộ trình 15 tuần cũ bắt đầu thẳng ở "toán nền + PyTorch" trong một tuần, rồi vào backprop và attention. Phần toán và phần nền ML (ERM, generalization, bias-variance, PAC) chỉ được nhắc lướt trong `Week-00/prerequisites_vi.md`. Chủ repo đã tải về thư mục `books/` gồm 13 cuốn sách toán, xác suất, lý thuyết học máy và deep learning để làm nguồn trích dẫn có trang.

## Quyết định

1. Thêm ba tuần nền tảng ở đầu lộ trình, gọi là Phase 0. Thứ tự theo đúng cấu trúc của các sách toán trong kho (MML: đại số tuyến tính, hình học giải tích, phân rã ma trận, giải tích vector, xác suất, tối ưu, rồi mới tới ML; Vũ Hữu Tiệp: đại số tuyến tính, giải tích ma trận, xác suất, MLE/MAP, rồi các khái niệm ML):
   - Tuần 1: đại số tuyến tính và hình học giải tích.
   - Tuần 2: giải tích vector, xác suất, tối ưu hóa.
   - Tuần 3: nền tảng ML và lý thuyết học (ERM, generalization, bias-variance, PAC, validation).
2. Mọi tuần cũ đổi số cộng 3 (Tuần 1 cũ thành Tuần 4, Tuần 15 cũ thành Tuần 18). Thư mục `Week-XX`, id quiz, dữ liệu portal, sơ đồ SVG, nhật ký học và mọi tham chiếu "Tuần N" trong văn bản đổi theo bằng script (`scripts/` không lưu script này; nó là việc một lần).
3. Phase 1, 2, 3 giữ tên và giữ số. Phase mới mang số 0 để không phải đổi tên trong toàn bộ văn bản.
4. File PDF trong `books/` chỉ giữ local (đã thêm vào `.gitignore`). Repo chỉ chứa catalog `docs/books/README.md` ghi tên sách, tác giả, link tải chính thức, tình trạng license tại ngày tra cứu, và bảng map chương sang tuần. Nội dung sách được trích dẫn tự do trong ghi chú lý thuyết, luôn kèm tên sách, mục và số trang in.
5. Report HTML (`report/`) thêm Phase 0 vào dashboard, bộ lọc, dữ liệu tuần, và thêm một mục "Kệ sách" liệt kê catalog.
6. Toàn bộ câu văn, comment, câu hỏi quiz mới được viết thành câu hoàn chỉnh, rõ nghĩa, qua bước soát bằng skill humanizer.

## Ngoài phạm vi

- Không viết lại nội dung các tuần cũ ngoài việc đổi số và vài câu nối sang Tuần 1–3.
- Không thêm chủ đề nâng cao mới vào `advanced_topics_vi.md`.
- Không commit PDF sách.

## Kiểm chứng

- `python scripts/generate_quiz.py` chạy xong 18/18 tuần.
- `python docs/diagrams/_gen_svgs.py` sinh lại SVG với bốn phase.
- `grep` không còn tham chiếu `Week-01..03` cũ lẫn với tuần mới; không còn "15 tuần".
- Mở `report/index.html` thấy 18 tuần, 4 phase, mục kệ sách.
