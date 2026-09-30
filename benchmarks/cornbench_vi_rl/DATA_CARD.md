# CornBench-VI — hồ sơ dữ liệu thực hành

**Trạng thái:** fixture development giả lập; benchmark agent đầy đủ chưa được chạy hoặc xuất bản.

## Nguồn và quyền

Các chuỗi số/đơn vị và expected output ở `development/parser_cases.json` được viết cho bài thực hành trong repo. Không trích từ tài liệu ngân hàng hoặc dữ liệu cá nhân. Không có output model vendor làm target training.

## Phạm vi

Parser số nguyên không âm với đơn vị tường minh trong grammar được code hỗ trợ. Missing unit trả AMBIGUOUS. Các ví dụ chỉ phục vụ kiểm logic, không đại diện phân phối tài liệu tiếng Việt.

## Chia tập

File hiện có là development công khai; không phải hidden confirmation. Trước nghiên cứu H1, người học phải tạo manifest tách development, calibration, confirmation, retention và future/shift theo nguồn/task family; answer confirmation nằm ngoài workspace/repo public.

## Nhãn và bất đồng

Nhãn do người viết fixture đặt, được reference tests đối chiếu theo grammar. Chưa có review độc lập dataset đại diện, chưa đủ điều kiện suy tỷ lệ lỗi agent. Fixture nhãn sai được đưa vào tests để minh họa evaluator có thể phát hiện mismatch, không xác nhận mọi nhãn đều đúng.

## Kết quả và giới hạn

Không có score CornAgents.AI trong data card. Replay parser chỉ báo outcome của fixture. Không dùng kết quả đó thay accuracy/learning gain của model thật; không coi biến thể cùng template là task độc lập.
