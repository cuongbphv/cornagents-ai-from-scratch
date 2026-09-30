# Lộ trình CornAgents.AI: Từ nền tảng LLM đến nghiên cứu và học có kiểm soát

> Dự án học thuật, nghiên cứu cá nhân, không thương mại hóa. Chỉ sử dụng nguồn và dữ liệu phù hợp [quy tắc của repo](../CLAUDE.md); không dùng tài liệu nội bộ ngân hàng, dữ liệu khách hàng hay credentials thật.

**Cập nhật:** 30/09/2026 (UTC+7). **Vào học:** [mục lục từng tuần](../ENTRYPOINTS.md) · [tài liệu chương trình](../docs/curriculum/README.md).

**Trạng thái:** lịch chính đã có 36 bộ tài liệu, starter, protocol, mẫu báo cáo và quiz. [Mục lục bài học](../ENTRYPOINTS.md) dẫn đúng thư mục; [tri thức tích hợp](../modules/README.md) và [12 lab](../labs/README.md) dẫn về mục nguồn. Bản tham chiếu lab đã được kiểm bằng fixture công khai; bài làm người học, live-model, CornBench đại diện và runtime production chưa được xác nhận.

## Tóm tắt nhanh (TL;DR)

- Đường học chính: **24 tuần nền tảng (core) + 12 tuần nghiên cứu mở rộng (extension)**. Nhịp **10–12 giờ/tuần** là giả định phân bổ trong mục 8.1 của nguồn, không phải thời lượng đã đo hay lời hứa hoàn thành.
- Giữ **fast-track 18 tuần** dựa trên thư mục hiện có cho người đã có nền tảng học máy và kỹ thuật hệ thống. Sau fast-track vẫn cần bổ sung phần thiếu và đạt tiêu chí năng lực của phần nền tảng trước khi vào extension; không quy đổi chỉ bằng số tuần.
- Người chưa lập trình có thể chuẩn bị **4–6 tuần** theo đề xuất của nguồn: Python, Git, terminal, JSON/HTTP, SQL và test. Tự đánh giá bằng [prerequisites_vi.md](prerequisites_vi.md); các số tuần trong file đó vẫn thuộc fast-track.
- Đích học tập là hiểu cơ chế, nghiên cứu có bằng chứng và đề xuất cải tiến có thể kiểm tra. Agent không tự sửa quyền, tiêu chuẩn đánh giá hay tự duyệt phát hành.

## Các phát hiện chính

**Một đường học liền mạch từ cơ chế đến hệ thống.** Toán, autograd, tokenizer, attention, tiny Transformer, SFT/LoRA và retrieval vẫn là phần lõi. Một demo chạy được cần đi cùng nguồn dữ liệu, phép đo, lỗi đã gặp và giới hạn kết luận.

**Tách ba cửa theo mục 3.4 của nguồn:** G1 (AI-off) kiểm tra người học tự giải thích và sửa phần lõi; G2 (AI-on) kiểm tra kết quả hệ thống; G3 kiểm tra bằng chứng của bản cải tiến trước khi thay bản đang dùng. Điểm cửa này không bù cho lỗi cửa khác. Thí nghiệm không cải thiện vẫn có thể đạt môn nếu phương pháp và báo cáo đúng; bản cải tiến đó chưa được đưa vào sử dụng.

**Sửa cách hiểu ở roadmap cũ theo mục 1.1 và 6.3 của nguồn:** validation dùng để chọn cấu hình, test độc lập dùng để đánh giá bản đã đóng băng; DPO không bắt buộc reward model riêng; RAG có thể retrieval lặp; graph cần so với baseline; mức bộ nhớ phải đo cho toàn workload. Không giữ các giá cloud, tốc độ máy hoặc cam kết model vừa bộ nhớ khi chưa có phép đo tương ứng.

**Cách đọc nguồn:** mỗi tuần dẫn tài liệu theo chủ đề và phần thực hành tương ứng. URL sơ cấp được tập hợp trong [catalog nguồn](../docs/papers/research_learning_sources.md); tài liệu thiết kế không thay kết quả đo. Các ví dụ lịch sử giữ giới hạn riêng, không dùng làm điểm của agent.

## Chi tiết

Mỗi tuần dưới đây giữ cùng nhịp đọc: **mục tiêu → nguồn → thực hành → sản phẩm → tự kiểm**. Mở bài tuần để xem starter, protocol, quiz và mẫu báo cáo.

Các thuật ngữ xuyên suốt: **baseline** là bản đối chứng; **candidate** là bản đề xuất cải tiến; **held-out** là tập giữ riêng để đánh giá; **quarantine** là vùng chờ kiểm chứng; **retention** đo khả năng giữ năng lực cũ. “Đóng băng” nghĩa là cố định phiên bản trước đánh giá, không sửa rồi dùng lại bằng chứng của bản trước.

### Cách dùng AI làm bạn học (lồng xuyên suốt mọi tuần)

Theo nhịp **Dự đoán → Tự triển khai → Gây lỗi → Đo → Sửa → Chuyển giao** ở mục 8.1 của nguồn: tự làm phần lõi trước, dùng AI để đề nghị phản biện và bài biến thể, rồi đối chiếu bằng code/nguồn. Lưu phiên bản, cấu hình và output thực; không coi nhận xét của AI là nhãn đúng.

Trước mỗi bài, viết câu hỏi, dữ liệu được phép dùng, ngân sách, bản đối chứng, chỉ số đánh giá, điều kiện dừng và kết quả nào sẽ bác bỏ giả thuyết. Chỉ đi tiếp khi đã có sản phẩm và bằng chứng tương ứng. Khi thiếu nguồn hoặc nhãn, ghi “chưa đủ bằng chứng”.

![Bản đồ năm chặng của lịch chính 36 tuần](../docs/diagrams/08-learning-journey.svg)

*Hình minh họa đường học; motion không biểu thị kết quả thực tế.*

### PHASE 0: Nền toán và phép đo (tuần 1–4)

**Tuần 1: Môi trường học và phạm vi nhiệm vụ.**

- **Mục tiêu:** Bắt đầu bằng một nhiệm vụ nhỏ có đầu vào, đầu ra và điều kiện hoàn thành rõ. Task contract ghi công cụ được phép, nguồn bị loại và ngân sách; agent không tự đổi nhiệm vụ.
- **Nguồn học:** [schedule](../docs/curriculum/schedule.md) · [runtime-boundaries](../modules/runtime-boundaries.md).
- **Thực hành:** Tạo môi trường Python, ghi phiên bản thực tế, thiết kế task đọc một fixture JSON; lưu manifest có nguồn, cấu hình và lệnh chạy. Dùng dữ liệu giả lập, không chép secrets.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 1](../tracks/core-24/Week-01/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Agent tìm thấy nguồn hữu ích ngoài allowlist. Có được tự đọc để hoàn thành nhanh hơn không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 2: Bản đối chứng và phép đánh giá đầu tiên.**

- **Mục tiêu:** Định nghĩa outcome trước khi tối ưu. Với bài toán có quy tắc rõ, dùng rules/search/code không LLM làm bản đối chứng B0.
- **Nguồn học:** [statistical-reliability](../modules/statistical-reliability.md) · [schedule](../docs/curriculum/schedule.md) · [DESIGN](../benchmarks/cornbench_vi_rl/DESIGN.md).
- **Thực hành:** Lập fixture đúng/sai và rubric cho parser số nguyên có đơn vị. Chạy bản đối chứng, lưu từng input, expected và output; báo toàn bộ task kể cả từ chối.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 2](../tracks/core-24/Week-02/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Không có task nào được nhận xử lý: accepted risk có bằng 0 không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 3: Đại số tuyến tính qua code.**

- **Mục tiêu:** Xem ma trận như ánh xạ tuyến tính. Xác định chiều đầu vào/đầu ra trước khi nhân; phép chiếu và xấp xỉ hạng thấp là nền cho regression và low-rank update.
- **Nguồn học:** [controlled-learning](../modules/controlled-learning.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-01/README.md](../Week-01/README.md) · [Week-01/02_linear_algebra_lab.py](../Week-01/02_linear_algebra_lab.py).
- **Thực hành:** Tái sử dụng lab NumPy ở Week-01. Tự tính phép chiếu, kiểm phần dư trực giao và so nghiệm bằng một cách độc lập. Lưu seed và tolerance.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 3](../tracks/core-24/Week-03/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Vì sao shape đúng chưa đủ để xác nhận một phép chiếu đúng?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 4: Đạo hàm, xác suất và gradient check.**

- **Mục tiêu:** Gradient check so đạo hàm tự tính với sai phân số trên một hàm nhỏ. Sampling unit và giả định độc lập phải được nêu khi chuyển từ ví dụ tính toán sang kết luận thống kê.
- **Nguồn học:** [statistical-reliability](../modules/statistical-reliability.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-02/README.md](../Week-02/README.md) · [Week-02/02_calculus_probability_lab.py](../Week-02/02_calculus_probability_lab.py) · [Week-03/README.md](../Week-03/README.md).
- **Thực hành:** Tự tính gradient logistic regression, kiểm bằng sai phân trung tâm; chia dữ liệu train/validation/test theo vai trò. Giải thích nguồn sai số số học.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 4](../tracks/core-24/Week-04/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Có nên chọn learning rate bằng điểm test rồi báo điểm test là đánh giá độc lập?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

### PHASE 1: Deep Internals: hiểu nội tại LLM (tuần 5–14)

**Tuần 5: Autograd và backprop từ đầu.**

- **Mục tiêu:** Autograd tích lũy đạo hàm theo graph tính toán. Tự viết một lõi nhỏ giúp đối chiếu chain rule với gradient reference thay vì chỉ nhìn loss giảm.
- **Nguồn học:** [controlled-learning](../modules/controlled-learning.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-04/README.md](../Week-04/README.md) · [Week-05/README.md](../Week-05/README.md) · [Week-05/02_micrograd.py](../Week-05/02_micrograd.py).
- **Thực hành:** Làm micrograd skeleton hiện có; kiểm gradient cho biểu thức có nhánh dùng chung và so với sai phân số. Vẽ graph trước khi gọi backward.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 5](../tracks/core-24/Week-05/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Một biến được dùng ở hai nhánh: gradient tại biến đó được cộng hay ghi đè?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 6: Training loop và overfit có chủ ý.**

- **Mục tiêu:** Training loss, validation loss và kết quả test trả lời các câu hỏi khác nhau. Tạo overfit trên tập nhỏ để kiểm loop, sau đó đánh giá khả năng khái quát.
- **Nguồn học:** [controlled-learning](../modules/controlled-learning.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-04/05_train_mlp.py](../Week-04/05_train_mlp.py) · [Week-03/02_erm_lab.py](../Week-03/02_erm_lab.py).
- **Thực hành:** Chạy MLP nhỏ, cố ý overfit một tập nhỏ, lưu loss train/validation theo bước. Thử một thay đổi mỗi lần và báo kết quả âm.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 6](../tracks/core-24/Week-06/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Vì sao overfit một batch có ích nhưng không phải kết quả cuối?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 7: Tokenizer, BPE và Unicode tiếng Việt.**

- **Mục tiêu:** Tokenizer là một hợp đồng chuyển đổi input. Round-trip, normalization và cách xử lý bytes/Unicode cần được kiểm riêng trên văn bản tiếng Việt.
- **Nguồn học:** [controlled-learning](../modules/controlled-learning.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-06/README.md](../Week-06/README.md).
- **Thực hành:** Viết bộ fixture gồm tiếng Việt có dấu, dấu kết hợp, ký tự lạ và khoảng trắng. Kiểm encode/decode; ghi chính sách normalization và giữ raw input.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 7](../tracks/core-24/Week-07/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Round-trip pass có chứng minh tokenizer phù hợp mọi tài liệu không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 8: Causal attention và dịch nhãn.**

- **Mục tiêu:** Causal mask hạn chế thông tin tương lai trong attention. Label shift phải làm khớp input ở vị trí hiện tại với target kế tiếp.
- **Nguồn học:** [controlled-learning](../modules/controlled-learning.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-06/02_multihead_attention.py](../Week-06/02_multihead_attention.py).
- **Thực hành:** Sửa attention skeleton, gây lỗi bằng cách bỏ mask; thay token tương lai và kiểm đầu ra ở vị trí trước đó. Viết một test dịch nhãn trên chuỗi ngắn.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 8](../tracks/core-24/Week-08/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Test nào mạnh hơn chỉ kiểm shape để phát hiện lỗi causal mask?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 9: Tiny Transformer và các khối kiến trúc.**

- **Mục tiêu:** Triển khai model nhỏ đủ để kiểm embedding, normalization, residual và attention. RoPE/normalization được học qua một biến thể nhỏ có reference.
- **Nguồn học:** [controlled-learning](../modules/controlled-learning.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-07/README.md](../Week-07/README.md) · [Week-00/advanced_topics_vi.md](../Week-00/advanced_topics_vi.md).
- **Thực hành:** Lắp tiny Transformer, kiểm shape và loss trên fixture nhỏ. Chọn một khối normalization/position để so bản tham chiếu; ghi rõ weights tự train hay tải.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 9](../tracks/core-24/Week-09/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Generate từ weights tải về cho phép kết luận đã tự huấn luyện từ đầu không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 10: KV cache và báo cáo tài nguyên.**

- **Mục tiêu:** Cache parity so đầu ra có và không có KV cache dưới cùng model/input. Profiler ghi bộ nhớ và thời gian theo workload thực.
- **Nguồn học:** [controlled-learning](../modules/controlled-learning.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-07/README.md](../Week-07/README.md) · [Week-12/03_hardware_decision.md](../Week-12/03_hardware_decision.md).
- **Thực hành:** Kiểm cached/uncached logits trong tolerance định trước; đo peak memory, context, dtype và throughput. Không chép benchmark máy khác vào báo cáo của mình.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 10](../tracks/core-24/Week-10/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Khi cached logits khác reference, có nên tăng tolerance đến khi pass?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 11: Nguồn dữ liệu, dedup và chia tập.**

- **Mục tiêu:** Dataset card ghi nguồn, quyền sử dụng, phiên bản và cách lấy mẫu. Chia theo nguồn/template/thời gian khi thích hợp để tránh gần trùng giữa development và confirmation.
- **Nguồn học:** [evidence-and-memory](../modules/evidence-and-memory.md) · [statistical-reliability](../modules/statistical-reliability.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-08/README.md](../Week-08/README.md) · [docs/datasets/README.md](../docs/datasets/README.md).
- **Thực hành:** Tạo manifest của corpus giả lập có hai bản gần trùng, nhóm theo nguồn trước khi chia tập. Ghi quyền đọc và quyền train riêng; không dùng dữ liệu chưa xác minh license.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 11](../tracks/core-24/Week-11/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Chia hai chunk từ cùng tài liệu sang train và test có làm chúng độc lập không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 12: Training dynamics và thí nghiệm tách ảnh hưởng.**

- **Mục tiêu:** Giữ baseline và các biến không nghiên cứu cố định; ablation bỏ hoặc đổi một thành phần để kiểm vai trò của nó. Lưu cả run lỗi và run không cải thiện.
- **Nguồn học:** [controlled-learning](../modules/controlled-learning.md) · [schedule](../docs/curriculum/schedule.md) · [research-methods](../modules/research-methods.md). Tài liệu tái sử dụng: [Week-08/04_loss_analysis.md](../Week-08/04_loss_analysis.md) · [Week-08/README.md](../Week-08/README.md).
- **Thực hành:** Train tiny model theo budget tự đặt trước, so một thay đổi như lịch LR. Lưu code/data/config/seed, loss, thời gian và lỗi của toàn bộ lượt chạy.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 12](../tracks/core-24/Week-12/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Kết quả âm có phải lý do xóa run khỏi báo cáo không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 13: SFT và LoRA ở quy mô nhỏ.**

- **Mục tiêu:** SFT học từ target; LoRA dùng tham số hiệu chỉnh hạng thấp. Nguồn/nhãn phải được review trước khi dữ liệu trở thành training target.
- **Nguồn học:** [schedule](../docs/curriculum/schedule.md) · [controlled-learning](../modules/controlled-learning.md). Tài liệu tái sử dụng: [Week-09/README.md](../Week-09/README.md) · [Week-11/README.md](../Week-11/README.md).
- **Thực hành:** So full update với low-rank update trên model nhỏ; ghi dataset card, phân tách train/test và retention trên task cũ. Chọn quy mô sau smoke test.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 13](../tracks/core-24/Week-13/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Loss train giảm và format đẹp hơn có đủ để đưa adapter vào dùng không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 14: Preference learning và DPO.**

- **Mục tiêu:** DPO tối ưu theo cặp chosen/rejected mà không bắt buộc học reward model riêng. Ý nghĩa preference phụ thuộc tiêu chí gán nhãn.
- **Nguồn học:** [controlled-learning](../modules/controlled-learning.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-10/README.md](../Week-10/README.md) · [Week-10/03_dpo_skeleton.py](../Week-10/03_dpo_skeleton.py).
- **Thực hành:** Tự viết DPO loss toy, giải thích reference policy và tiêu chí chọn cặp. Dùng fixture để phân biệt câu trôi chảy với câu có outcome đúng.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 14](../tracks/core-24/Week-14/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** DPO, GRPO và RLVR có phải ba bước bắt buộc liên tiếp không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

### PHASE 2: Ứng dụng: retrieval, tài liệu và serving (tuần 15–18)

**Tuần 15: Hybrid retrieval và reranking.**

- **Mục tiêu:** BM25 và dense retrieval cung cấp các tín hiệu khác nhau; fusion/reranking cần được so với baseline trên cùng nguồn và task.
- **Nguồn học:** [controlled-learning](../modules/controlled-learning.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-13/README.md](../Week-13/README.md) · [Week-14/README.md](../Week-14/README.md).
- **Thực hành:** Chọn corpus công khai được phép dùng hoặc giả lập; so retrieval baseline với fusion dưới budget rõ. Kiểm recall và lỗi nguồn ở từng query.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 15](../tracks/core-24/Week-15/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Candidate retrieval tốt hơn nhưng corpus cũng lớn hơn: đã xác nhận lợi ích riêng của fusion chưa?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 16: Bằng chứng, phiên bản và context.**

- **Mục tiêu:** Evidence ledger nối mỗi claim với source span, snapshot, thời điểm hiệu lực và quyền đọc. Nguồn tồn tại khác với nguồn thực sự hỗ trợ claim.
- **Nguồn học:** [evidence-and-memory](../modules/evidence-and-memory.md) · [controlled-learning](../modules/controlled-learning.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-14/README.md](../Week-14/README.md).
- **Thực hành:** Lập bảng claim–evidence–counterevidence với nguồn giả lập cũ/mới và bản sao. Lọc quyền trước khi trả context; ghi phần chưa đủ nguồn.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 16](../tracks/core-24/Week-16/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Ba URL đều chép một thông cáo thì có ba xác nhận độc lập không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 17: Document AI và số/đơn vị tiếng Việt.**

- **Mục tiêu:** Trích xuất cần giữ raw span và vị trí/đơn vị của nguồn. Parser chỉ tính khi input nằm trong grammar và schema đã hỗ trợ.
- **Nguồn học:** [schedule](../docs/curriculum/schedule.md) · [DESIGN](../benchmarks/cornbench_vi_rl/DESIGN.md) · [document-ai](../modules/document-ai.md). Tài liệu tái sử dụng: [Week-13/README.md](../Week-13/README.md).
- **Thực hành:** Tự viết parser số nguyên có đơn vị tường minh, thử thiếu đơn vị và dấu OCR. Xuất raw span, normalized value và lý do từ chối; so với fixture.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 17](../tracks/core-24/Week-17/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Bảng chỉ ghi 12, không còn header đơn vị: có được đoán là triệu đồng không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 18: Serving, phiên bản và chi phí thực.**

- **Mục tiêu:** Tách replay fixtures khỏi live-model evaluation. Mỗi kết quả inference cần biết model revision, config, input scope và tài nguyên đã dùng.
- **Nguồn học:** [schedule](../docs/curriculum/schedule.md) · [runtime-boundaries](../modules/runtime-boundaries.md). Tài liệu tái sử dụng: [Week-12/README.md](../Week-12/README.md).
- **Thực hành:** Xây adapter interface cho fake/local model, đo latency của đúng workload, ghi toàn bộ retry. Không cần API trả phí để hoàn thành bài offline.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 18](../tracks/core-24/Week-18/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Fake model replay pass có thể ghi là benchmark LLM thật không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

### PHASE 3: Agent và capstone nền (tuần 19–24)

**Tuần 19: Hợp đồng công cụ và agent có giới hạn.**

- **Mục tiêu:** Tool schema kiểm hình dạng; executor phải kiểm thêm semantics, quyền hiện tại và ngân sách. Model đề nghị hành động nhưng không tự cấp capability.
- **Nguồn học:** [research-contracts](../modules/research-contracts.md) · [runtime-boundaries](../modules/runtime-boundaries.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-15/README.md](../Week-15/README.md) · [labs/r01-research-contract/README.md](../labs/r01-research-contract/README.md).
- **Thực hành:** Dùng R01/R10 reference offline; tạo schema cho read_fixture, từ chối tool không có trong contract. Viết starter executor chỉ hỗ trợ công cụ giả lập.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 19](../Week-19/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** JSON đúng schema nhưng action ngoài scope có được chạy không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 20: Deny tests, sandbox và thu hồi quyền.**

- **Mục tiêu:** Biên quyền cần nằm ngoài worker. Sau resume phải kiểm lại quyền hiện tại và expiry, không sống lại capability cũ từ checkpoint.
- **Nguồn học:** [research-contracts](../modules/research-contracts.md) · [runtime-boundaries](../modules/runtime-boundaries.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-15/README.md](../Week-15/README.md) · [labs/r03-governed-memory/README.md](../labs/r03-governed-memory/README.md).
- **Thực hành:** Dùng fixtures hai tenant, quyền hết hạn và thu hồi giữa hai bước; viết deny tests cho read/write. Vẽ biên process/credential cần có khi triển khai thật.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 20](../Week-20/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Tại sao thư mục evaluator riêng vẫn chưa đủ bảo vệ đáp án?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 21: Checkpoint, idempotency và recovery.**

- **Mục tiêu:** Checkpoint giữ state của workflow; idempotency và reconciliation xử lý tác động bên ngoài. Crash sau write trước ack là tình huống riêng cần kiểm.
- **Nguồn học:** [runtime-boundaries](../modules/runtime-boundaries.md) · [schedule](../docs/curriculum/schedule.md). Tài liệu tái sử dụng: [Week-16/README.md](../Week-16/README.md) · [labs/r10-durable-research/README.md](../labs/r10-durable-research/README.md).
- **Thực hành:** Chạy DurableToy với ack bị mất, event trùng, payload đổi cùng key và quyền bị revoke. Viết event timeline và cách reconcile; không dùng service thật.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 21](../Week-21/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Checkpoint mới nhất không có ack: có chắc thao tác chưa xảy ra không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 22: Bộ đánh giá được bảo vệ.**

- **Mục tiêu:** Evaluator độc lập trước hết ở quyền sửa, dữ liệu và quy trình. Candidate gửi immutable digest; hidden answers và credential của evaluator không nằm trong workspace worker.
- **Nguồn học:** [statistical-reliability](../modules/statistical-reliability.md) · [schedule](../docs/curriculum/schedule.md) · [runtime-boundaries](../modules/runtime-boundaries.md) · [implementation](../docs/curriculum/implementation.md). Tài liệu tái sử dụng: [Week-16/README.md](../Week-16/README.md) · [labs/r08-evaluator-boundary/README.md](../labs/r08-evaluator-boundary/README.md).
- **Thực hành:** Làm R08 toy digest-mismatch, lập sơ đồ service evaluator riêng và query budget; phân biệt fixture tests công khai với confirmation thật ngoài workspace.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 22](../Week-22/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Giữ answer file kín nhưng chọn prompt theo pass/fail lặp có còn test độc lập không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 23: Capstone nền và mini research.**

- **Mục tiêu:** Chọn một workflow hẹp có outcome kiểm được. Định nghĩa baseline, metric, non-compensable constraints và giả thuyết trước thử nghiệm.
- **Nguồn học:** [research-contracts](../modules/research-contracts.md) · [schedule](../docs/curriculum/schedule.md) · [DESIGN](../benchmarks/cornbench_vi_rl/DESIGN.md). Tài liệu tái sử dụng: [Week-18/README.md](../Week-18/README.md) · [labs/r12-cornbench-learning/README.md](../labs/r12-cornbench-learning/README.md).
- **Thực hành:** Tạo protocol cho parser/retrieval tiếng Việt, chạy B0 và B1/B2 phù hợp; giữ mọi failure và báo nguồn, chi phí, outcome.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 23](../Week-23/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Candidate tăng success nhưng có một vi phạm quyền xác nhận được thì xử lý thế nào?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 24: Bảo vệ năng lực và điều kiện vào nghiên cứu.**

- **Mục tiêu:** G1 kiểm người học tự giải thích/sửa phần lõi; G2 kiểm hệ thống; G3 xét candidate. Ba cửa tách nhau, không lấy artifact AI sinh để suy ra học viên hiểu.
- **Nguồn học:** [research-contracts](../modules/research-contracts.md) · [schedule](../docs/curriculum/schedule.md) · [graduation-and-maintenance](../modules/graduation-and-maintenance.md). Tài liệu tái sử dụng: [Week-18/README.md](../Week-18/README.md) · [labs/r11-promotion/README.md](../labs/r11-promotion/README.md).
- **Thực hành:** Tự sửa một lỗi biến thể không dùng AI; trình bày report của tuần 23; đóng băng candidate và lập quyết định reject/insufficient/promote với scope giả lập.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 24](../Week-24/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Thí nghiệm không có gain có thể đạt môn nghiên cứu không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

### PHASE 4: Nghiên cứu và học có kiểm soát (tuần 25–36)

**Tuần 25: Từ câu hỏi rộng thành phạm vi nghiên cứu.**

- **Mục tiêu:** Tách câu hỏi, scope, thời gian nguồn, công cụ, ngân sách và điều kiện hoàn thành. Gắn claim_kind: source_fact, computed, inference hoặc hypothesis.
- **Nguồn học:** [research-contracts](../modules/research-contracts.md) · [evidence-and-memory](../modules/evidence-and-memory.md) · [specifications](../labs/specifications.md).
- **Thực hành:** Làm R01: viết contract và ledger cho câu hỏi parser tiếng Việt; fixture có hai bản sao cùng xuất xứ. Phân loại phát biểu và ghi giới hạn từng claim.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 25](../Week-25/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Nguồn chưa trả được toàn văn thì có được nói đã tích hợp từng chi tiết không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 26: Nghiên cứu lặp, phản chứng và điều kiện dừng.**

- **Mục tiêu:** Mỗi query phải nhằm kiểm câu hỏi trong contract. Vòng nghiên cứu ghi support/counterevidence và dừng khi hết budget hoặc không còn phép kiểm hợp lệ.
- **Nguồn học:** [research-contracts](../modules/research-contracts.md) · [evidence-and-memory](../modules/evidence-and-memory.md) · [specifications](../labs/specifications.md).
- **Thực hành:** Làm R02: xử lý nguồn cũ/mới/mâu thuẫn; ghi query nào thêm evidence. Thử hết budget, query drift và nguồn không trả đáp án.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 26](../Week-26/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Tại sao nguồn hỗ trợ và nguồn phản bác cần giữ cùng báo cáo?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 27: Bộ nhớ có nguồn, thời hạn và quyền đọc.**

- **Mục tiêu:** Tách fact, episode và procedural lesson. Worker đề nghị; review mới chuyển từ quarantine sang active có phạm vi. Đọc phải kiểm trạng thái, tenant và thời hạn.
- **Nguồn học:** [runtime-boundaries](../modules/runtime-boundaries.md) · [evidence-and-memory](../modules/evidence-and-memory.md) · [specifications](../labs/specifications.md).
- **Thực hành:** Làm R03: hai tenant giả lập, nguồn bị revoke và summary hai tầng; kiểm không trả text/citation ngoài quyền. Vẽ lineage và ghi phần code toy chưa mô phỏng.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 27](../Week-27/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Xóa entry khỏi memory có đồng nghĩa đã unlearn dữ liệu khỏi model train trước đó không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 28: Học từ lỗi bằng bài học có điều kiện.**

- **Mục tiêu:** Reflexion là phản hồi ngôn ngữ và episodic memory, không tự cập nhật weights. Lesson phải có điều kiện áp dụng, phản ví dụ và cách xử lý ngoài scope.
- **Nguồn học:** [research-contracts](../modules/research-contracts.md) · [evidence-and-memory](../modules/evidence-and-memory.md) · [controlled-learning](../modules/controlled-learning.md) · [specifications](../labs/specifications.md).
- **Thực hành:** Làm R04: so parser rule/bộ nhớ lesson trên trường có grammar; kiểm đổi đơn vị và thiếu header. Thiết kế nhánh Reflexion live riêng; reference offline không gọi LLM.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 28](../Week-28/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Lesson “luôn dùng parser” sai ở trường hợp nào trong lab?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 29: Tìm bản cải tiến prompt và kỹ năng.**

- **Mục tiêu:** Tìm candidate trên development; chỉ thay phần allowlist. Đóng băng finalist trước confirmation. Prompt/skill optimization là L2, khác học tham số L3.
- **Nguồn học:** [controlled-learning](../modules/controlled-learning.md) · [specifications](../labs/specifications.md).
- **Thực hành:** Làm R05: random search baseline trên fixture; ghi lineage và rejected candidates. Tạo candidate cố thêm quyền và xác nhận bị từ chối.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 29](../Week-29/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Tự chọn một prompt bằng tay có thể gọi là đã tái lập GEPA không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 30: Thiết kế và chọn thí nghiệm.**

- **Mục tiêu:** Đặt objective, metric, tổng budget và stopping rule trước. Random search/ablation là baseline; BO chỉ thử khi evaluator đắt và objective thích hợp.
- **Nguồn học:** [controlled-learning](../modules/controlled-learning.md) · [specifications](../labs/specifications.md) · [research-methods](../modules/research-methods.md).
- **Thực hành:** Làm R06: giữ model/corpus, thay một cấu hình; runner dừng trước khi vượt budget. Lưu run fail, tiêu chí chọn và tổng chi phí.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 30](../Week-30/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Có được dừng ngay khi thấy một kết quả đẹp rồi bỏ run thất bại không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 31: Hiệu chỉnh, risk–coverage và cận thống kê.**

- **Mục tiêu:** Coverage=A/N; accepted risk=E/A khi A>0. Chọn threshold trên calibration rồi cố định; cận nhị thức dùng cho policy và mẫu phù hợp, không cho một câu trả lời cụ thể.
- **Nguồn học:** [statistical-reliability](../modules/statistical-reliability.md) · [specifications](../labs/specifications.md).
- **Thực hành:** Làm R07: no-data, zero-error, một lỗi và retry trùng task; giải thích giả định. So công thức zero-error với reference; ghi rõ CP toy không kiểm representativeness.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 31](../Week-31/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Không thấy lỗi trong mẫu có chứng minh tỷ lệ lỗi thật bằng 0 không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 32: Bảo vệ evaluator và dữ liệu xác nhận.**

- **Mục tiêu:** Confirmation kiểm một finalist đã cố định. Regression công khai giữ hành vi đã biết nhưng có thể overfit, không thay cohort confirmation mới.
- **Nguồn học:** [runtime-boundaries](../modules/runtime-boundaries.md) · [statistical-reliability](../modules/statistical-reliability.md) · [specifications](../labs/specifications.md).
- **Thực hành:** Làm R08: tính digest, sửa một tham số và kiểm từ chối. Thiết kế process/credential tách biệt và sổ query budget; diễn tập contamination bằng trace chứa nhãn.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 32](../Week-32/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Sửa candidate sau khi có report tốt rồi giữ report cũ có hợp lệ không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 33: Học tham số offline và giữ năng lực cũ.**

- **Mục tiêu:** SFT/LoRA/DPO cần dữ liệu được phép dùng, nhãn có tiêu chí và lineage. So base/candidate trên nhóm mới, nhóm cũ và ngoài phạm vi.
- **Nguồn học:** [research-contracts](../modules/research-contracts.md) · [specifications](../labs/specifications.md) · [controlled-learning](../modules/controlled-learning.md).
- **Thực hành:** Làm R09: kiểm low-rank update nhỏ và rollback weights; lập data card/preference rubric. Nhánh live-model chỉ chạy khi có runtime, license, dataset và budget rõ.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 33](../Week-33/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** DPO preference chọn văn phong tự tin có đảm bảo factuality không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 34: Chạy dài với quota, hủy và recovery.**

- **Mục tiêu:** Worker con tiêu cùng quota nhiệm vụ mẹ; hủy cần lan tới mọi worker/subprocess/retry. Resume vẫn kiểm quyền hiện hành.
- **Nguồn học:** [runtime-boundaries](../modules/runtime-boundaries.md) · [specifications](../labs/specifications.md).
- **Thực hành:** Làm R10: ack mất sau write, duplicate event, key reused, unknown outcome, cancel và revoke. Reference chỉ có in-memory toy, chưa có supervisor process thật.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 34](../Week-34/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Worker con có được tạo budget mới để tiếp tục khi quota mẹ hết không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 35: Duyệt đúng bản cải tiến, shadow và rollback.**

- **Mục tiêu:** Evidence và approval gắn đúng digest, policy/model/corpus/memory snapshot, scope và expiry. Shadow không tác động quyết định thực; canary cần phạm vi/tác động đã duyệt.
- **Nguồn học:** [runtime-boundaries](../modules/runtime-boundaries.md) · [specifications](../labs/specifications.md) · [promotion-and-revocation](../modules/promotion-and-revocation.md).
- **Thực hành:** Làm R11: promote đúng digest, sửa artifact sau eval, scope thiếu, violation và rollback. Viết release package; thử trong mô phỏng, không deploy production.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 35](../Week-35/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Tại sao rollback và revoke cần hai quyết định riêng?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

**Tuần 36: CornBench-VI: học qua nhiều vòng và báo cáo tái lập.**

- **Mục tiêu:** Capstone gồm frozen baseline, một cơ chế học và nhiều cohort mới. Chấm G1/G2/G3 riêng; báo gain, retention, risk–coverage và tổng chi phí kể cả kết quả âm.
- **Nguồn học:** [specifications](../labs/specifications.md) · [DESIGN](../benchmarks/cornbench_vi_rl/DESIGN.md) · [research-methods](../modules/research-methods.md) · [graduation-and-maintenance](../modules/graduation-and-maintenance.md).
- **Thực hành:** Làm R12 và H1: đăng ký protocol, chia development/confirmation/retention theo family; chạy baseline/lesson ablation. Reference parser replay chỉ kiểm fixture; nộp report giới hạn và lệnh tái lập.
- **Sản phẩm:** code/artifact, protocol và output thực trong [bài tuần 36](../Week-36/README.md); báo cáo cả lỗi và giới hạn.
- **Tự kiểm không dùng AI:** Candidate không cải thiện nhưng thí nghiệm đúng có được hạ ngưỡng để tốt nghiệp không?
- **Thời lượng và máy:** 10–12 giờ là giả định phân bổ; CPU/toy trước, đo tài nguyên nếu chạy model thật.

### Fast-track 18 tuần: giữ thư mục, bổ sung theo năng lực

**Số tuần của đường rút gọn khác số tuần của đường học chính.** Bảng là quy đổi nội dung đề xuất, không xác nhận tương đương toàn bộ. Chi tiết core ở các bảng trên mới là mục tiêu của đường chính.

| Thư mục hiện có | Nội dung tái sử dụng | Vùng core liên quan | Phần cần bổ sung |
|---|---|---|---|
| Week-01–03 | Toán, xác suất, ML NumPy | 3–4; nền cho 11–12 | Contract, baseline và eval đầu tiên của 1–2 |
| Week-04–05 | PyTorch, backprop, MLP | 5–6 | So gradient với bản tham chiếu, bài biến thể không dùng AI |
| Week-06–07 | Tokenizer, attention, GPT | 7–10 | Unicode, label shift, cache parity, profiler |
| Week-08 | Pretraining | 11–12 | Dedup, split theo nguồn, data card và ablation |
| Week-09–12 | SFT, alignment, QLoRA/MLX, inference | 13–14; một phần 17–18 | DPO toy, data lineage, retention; đo tài nguyên thay ước lượng cũ |
| Week-13–14 | RAG và evaluation | 15–18 | Evidence span, số/đơn vị, Document AI, báo cáo cả kết quả âm |
| Week-15–16 | Agent, MCP, SDLC | 19–22 | Enforcement ngoài model, quota/cancel/revoke, crash/retry, protected evaluator |
| Week-17–18 | Graph và capstone | 23–24; graph tùy chọn | Bản đối chứng không graph, protocol với tập giữ riêng, G1/G2; chưa thay thế R01–R12 |

Dùng [README từng tuần](../Week-01/README.md) để mở bài hiện có. Quiz, ghi chú và portal fast-track chưa được audit toàn bộ trong lần cập nhật roadmap này; đối chiếu các sửa đổi học thuật nêu trên khi học. [Bản tiếng Anh](plan_llm_from_scratch_en.md) vẫn mô tả lịch cũ, chưa đồng bộ với lịch điều chỉnh.

## Đánh giá tổng thể và cách chọn độ sâu

Phần nền cần chắc để phần tự học có thể kiểm chứng. Những điểm dưới giúp chọn độ sâu và biết lúc nào cần thêm bằng chứng; chưa phải đánh giá hiệu năng agent.

| Góc nhìn | Điểm mạnh của thiết kế | Phần cần bằng chứng trước khi kết luận | Điều chỉnh trong đường học |
|---|---|---|---|
| Học thuật | Giữ toán, tự triển khai, phản ví dụ và G1 | Chưa đo mức phù hợp của thời lượng với từng người học | 24 tuần nền, bài riêng từng tuần; thời lượng ghi là giả định |
| Nghiên cứu | Có baseline, giả thuyết bác bỏ được và tập giữ riêng | H1 chưa có kết quả; tính mới chưa được xác nhận | Protocol H1, ablation, confirmation và retention trước khi báo gain |
| Dữ liệu | Evidence span, lineage, quarantine và thu hồi dữ liệu dẫn xuất | Fixture development chưa đại diện dữ liệu thực | Tách nguồn/tenant/thời gian; báo thiếu bằng chứng và giữ raw input |
| Kỹ thuật hệ thống | Quyền/budget nằm ngoài model; eval và duyệt tách riêng | Toy in-memory chưa chứng minh isolation, recovery hoặc cancellation của process thật | Bài failure/revoke/digest; reference offline có giới hạn rõ |
| Thống kê | Báo risk cùng coverage và điều kiện của cận | Thiếu task độc lập và confirmation thì chưa có bảo đảm chất lượng | R07, protocol tách tập, mẫu số rõ; không lấy retry làm mẫu mới |

Từ các điểm trên, lịch 36 tuần hợp lý như một khung học có sản phẩm kiểm được. Nó chưa chứng minh CornAgents.AI tự cải tiến hiệu quả hoặc đủ điều kiện production. Bước tiếp theo của người học là thực hiện protocol và thu output thực; không đổi trạng thái chỉ vì đã có tài liệu hoặc demo.

## Khuyến nghị

1. Chọn đường học bằng bài đầu vào, không nhảy cóc chỉ vì đã gọi được API. Giữ phần tự triển khai và giải thích phản ví dụ.
2. Triển khai theo phụ thuộc ở tài liệu chương trình mục 17.3: scope/mapping → contract và bounded runner → evidence ledger và eval protocol → memory quarantine → baseline lesson và protected evaluator → candidate search → promotion/shadow/rollback → CornBench-VI pilot. Đây là thứ tự đề xuất, chưa phải backlog đã hoàn thành.
3. Bắt đầu nghiên cứu bằng **H1: bài học có điều kiện và phản ví dụ** trên parser số/đơn vị hoặc retrieval tiếng Việt (tài liệu chương trình, mục 15). So sánh bộ nhớ trải nghiệm, bản tóm tắt cùng độ dài và bài học dưới ngân sách tương đương. Chỉ gọi là giả thuyết; chưa có bằng chứng nó thắng.
4. Chọn một runtime và state machine đơn giản trước. Mở graph, multi-agent, optimizer nâng cao hoặc adapter lớn khi baseline và evaluator cho thấy cần thử.
5. Với mỗi paper, nộp một báo cáo kèm bằng chứng: bản đã đọc, giả định, phần tái lập, cấu hình, sai khác, kết quả và quyết định áp dụng. Không gọi baseline lấy cảm hứng là tái lập đầy đủ.

## Cảnh báo (Caveats)

- **Chưa có số liệu chất lượng live-model của CornAgents trong roadmap này.** CornBench-VI R&L là benchmark đề xuất. Không điền accuracy, learning gain, retention hoặc cost từ paper hay ví dụ giả lập.
- **Phép đo phải có mẫu số:** báo task success trên toàn bộ task, accepted risk cùng coverage, lỗi evidence/quyền, retention, thời gian người sửa và toàn bộ chi phí fail/retry/search. Nếu không nhận task nào, accepted risk chưa đo được; không ghi 0% lỗi.
- **Tách dữ liệu theo vai trò:** development/training, calibration, independent confirmation, regression/retention, future/shift cohort. Tránh gần trùng nguồn/template; không tối ưu lặp bằng phản hồi hidden test.
- **Cận thống kê có điều kiện.** Ví dụ Phụ lục A của tài liệu chương trình không phải benchmark agent hoặc quyền deploy. Không lấy một ngưỡng accuracy để mở quyền; không tự đặt ngưỡng an toàn cho nghiệp vụ ngân hàng.
- **Phần cứng và giá:** dùng smoke test/profiler, đo peak memory, throughput và tổng thời gian trên cấu hình thực. Chưa có benchmark máy trong lần cập nhật này, nên không cam kết model vừa RAM/VRAM hay giữ giá thuê cũ. Bộ nhớ cần tính cả activations, optimizer, gradients, KV cache và runtime overhead theo workload.
- **Phát hành:** evidence phải gắn đúng digest, corpus/memory snapshot, policy/evaluator version và scope. Shadow, canary, rollback là nội dung lab; không tự chuyển sang dữ liệu hay thao tác production.
- **Trạng thái:** `designed` là có đặc tả; `implemented` cần code/fixtures; `validated` cần log kiểm định đúng phạm vi. Tick checklist không tự chứng minh hai trạng thái sau.

## Danh sách nguồn hợp nhất / Tech Stack

**Tra cứu trong repo:** [Phân bổ chương trình](../docs/curriculum/schedule.md), [tri thức theo chủ đề](../modules/README.md), [đặc tả R01–R12](../labs/specifications.md), [CornBench-VI](../benchmarks/cornbench_vi_rl/DESIGN.md), [promotion và rollback](../modules/promotion-and-revocation.md). Số mục trong các tài liệu được giữ để đối chiếu chéo.

**Nguồn sơ cấp:** [catalog nghiên cứu](../docs/papers/research_learning_sources.md) giữ tên, URL và giới hạn sử dụng từng nguồn. Không tự nhận đã đọc toàn văn hoặc tái lập mọi công trình; xác minh paper/docs theo phiên bản khi làm bài.

Nguồn nền giữ tại [kệ sách](../docs/books/README.md), [kệ paper](../docs/papers/README.md), [advanced topics](advanced_topics_vi.md) và nguồn của từng tuần. Catalog lịch sử không thay việc kiểm lại license khi dùng dữ liệu/model/code.

**Stack đề xuất theo tài liệu chương trình mục 10:** Python/NumPy/PyTorch; pytest/unittest, type checking và dependency lock; Pydantic hoặc JSON Schema; state machine Python trước, LangGraph khi cần persistence; SQLite local; retrieval BM25/dense/fusion; scripts và manifest cho experiments. MCP, DSPy/GEPA, PostgreSQL, graph và adapter là lựa chọn theo lab, không phải danh sách phải cài hết. Không khóa điều kiện tốt nghiệp vào model thương mại hoặc preview API.

## Tài liệu đã tích hợp và cách kiểm lại

Lịch chính: [36 bài học](../ENTRYPOINTS.md). Tuần 1–18 dùng `tracks/core-24/Week-XX`; tuần 19–36 dùng `Week-XX` ở gốc. Mỗi tuần có nguyên lý, phản ví dụ, bài tập, protocol, báo cáo trống và quiz. H1 nằm ở [protocol nghiên cứu](../research/hypotheses/H1.md), chưa có kết quả thực nghiệm.

Chạy `python3 scripts/run_learning_checks.py` từ gốc repo. [Báo cáo](../evaluation/offline_check_report.json) hiện ghi 23 test đạt với 44 tình huống fixture giả lập công khai, chỉ kiểm code tham chiếu offline và công thức số. Không quy đổi kết quả đó thành chất lượng agent, tính đại diện benchmark hay năng lực người học. Công cụ sinh bài giữ nguyên starter/protocol/report đã tồn tại để bảo toàn bài làm.
