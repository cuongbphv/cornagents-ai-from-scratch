# Tuần 3, Quiz: Nền tảng ML và lý thuyết học

> Tự kiểm tra **trước** khi xem solution. Tổng **15** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Trong khung học thống kê của Shalev-Shwartz và Ben-David, learner được biết gì và không được biết gì?

- **A.** Biết phân phối D và hàm nhãn f, chỉ không biết tập test
- **B.** Biết mọi thứ trừ kích thước mẫu m
- **C.** Biết training data S gồm các cặp (x, y); không biết phân phối D sinh ra x và hàm gán nhãn f
- **D.** Biết phân phối D nhưng không biết training data

## Câu 2 (Trắc nghiệm)

Empirical Risk Minimization trên toàn bộ các hàm có thể có thì dẫn đến hậu quả gì, và lý thuyết đề xuất cách khắc phục nào?

- **A.** Dẫn đến underfitting; khắc phục bằng cách tăng learning rate
- **B.** Không có hậu quả gì nếu dữ liệu đủ sạch
- **C.** Dẫn đến overfitting vì một hàm nhớ hết mẫu có lỗi mẫu bằng 0 nhưng lỗi thật cao; khắc phục bằng cách giới hạn trước lớp giả thuyết H, gọi là inductive bias
- **D.** Dẫn đến chi phí tính toán cao; khắc phục bằng GPU

## Câu 3 (Tự luận)

Hãy viết công thức tách lỗi của giả thuyết ERM thành approximation error và estimation error, rồi giải thích mỗi thành phần phụ thuộc vào điều gì.

## Câu 4 (Trắc nghiệm)

Trong định nghĩa PAC learnability, hai tham số ε và δ lần lượt mang ý nghĩa gì?

- **A.** ε là learning rate, δ là kích thước batch
- **B.** ε là số mẫu, δ là số chiều của dữ liệu
- **C.** ε là lỗi trên training set, δ là lỗi trên test set
- **D.** ε là độ chính xác cho phép của giả thuyết trả về (phần 'approximately correct'), δ là xác suất thất bại được chấp nhận (phần 'probably')

## Câu 5 (Trắc nghiệm)

Điều gì tuyệt đối không được làm với validation data, và vì sao?

- **A.** Không được vẽ đồ thị trên validation data vì tốn thời gian
- **B.** Không được để validation data nhỏ hơn 50% dữ liệu
- **C.** Không được dùng validation data để ước lượng hay chọn tham số model, vì khi đó ước lượng lỗi trên nó không còn độc lập và không còn là ước lượng không chệch của lỗi thật
- **D.** Không được chia validation data ngẫu nhiên vì làm mất thứ tự thời gian

## Câu 6 (Tự luận)

Logistic regression khác linear regression ở những điểm nào về đầu ra, hàm loss và cách giải, và vì sao có thể gọi nó là mạng neural một lớp?

## Câu 7 (Trắc nghiệm)

Hệ quả 2.3 trong UML cho lớp giả thuyết hữu hạn (giả định realizable): với m ≥ log(|H|/δ)/ε mẫu, ERM đạt lỗi thật ≤ ε với xác suất ≥ 1 − δ. Nếu bạn gấp đôi kích thước lớp giả thuyết |H| mà giữ ε, δ, số mẫu cần thiết thay đổi thế nào?

- **A.** Không thay đổi, vì bound chỉ phụ thuộc vào ε và δ, còn |H| bị triệt tiêu trong union bound.
- **B.** Tăng gấp đôi, vì số mẫu cần thiết tỉ lệ thuận với số giả thuyết mà thuật toán phải phân biệt.
- **C.** Tăng gấp bốn, vì lỗi ε xuất hiện bậc hai trong Hoeffding và |H| nhân đôi số sự kiện xấu.
- **D.** Tăng thêm một lượng cố định log(2)/ε, vì |H| chỉ xuất hiện trong logarit nên mở rộng lớp giả thuyết khá rẻ.

## Câu 8 (Trắc nghiệm)

Bất đẳng thức Hoeffding (UML Lemma 4.5) cho P[|(1/m)Σθᵢ − µ| > ε] ≤ 2 exp(−2mε²/(b − a)²). Muốn giảm sai số ε xuống còn một nửa với cùng độ tin cậy, kích thước mẫu m cần thay đổi bao nhiêu?

- **A.** Gấp đôi, vì ε và m xuất hiện đối xứng trong tích mε² nên chia đôi ε tương đương nhân đôi m.
- **B.** Gấp tám, vì ngoài mε² còn phải bù cho hệ số 2 phía trước hàm mũ.
- **C.** Không cần thay đổi, vì độ tin cậy 1 − δ đã cố định và Hoeffding không phụ thuộc vào ε.
- **D.** Gấp bốn, vì mũ chứa mε² nên để giữ nguyên mε² khi ε giảm một nửa thì m phải tăng bốn lần.

## Câu 9 (Trắc nghiệm)

Định lý No-Free-Lunch (UML Định lý 5.1) nói gì, và hệ quả nào rút ra cho lớp giả thuyết gồm mọi hàm từ một miền X vô hạn vào {0, 1}?

- **A.** Với mọi learner A và m < |X|/2, tồn tại D có hàm f với L_D(f) = 0 nhưng P[L_D(A(S)) ≥ 1/8] ≥ 1/7, do đó lớp gồm mọi hàm trên X vô hạn không PAC learnable.
- **B.** Mọi thuật toán học đều đạt lỗi tối thiểu trên mọi phân phối nếu m đủ lớn, do đó lớp gồm mọi hàm là PAC learnable ngay khi m ≥ |X|/2.
- **C.** Không thuật toán nào học được bất kỳ hàm nào nếu không biết trước phân phối D, do đó chỉ các lớp giả thuyết hữu hạn mới có thể PAC learnable.
- **D.** Với m ≥ |X|/2 mẫu mọi learner đều đạt lỗi ≤ 1/8 với xác suất ≥ 6/7, do đó VC-dimension của lớp gồm mọi hàm đúng bằng |X|/2.

## Câu 10 (Trắc nghiệm)

Theo UML Định nghĩa 6.5, VC-dimension của lớp giả thuyết H là gì, và VCdim của lớp hàm ngưỡng (threshold functions) trên R bằng bao nhiêu?

- **A.** VCdim là số tham số của mô hình; hàm ngưỡng có một tham số θ nên VCdim = 1, và mọi lớp có vô hạn giả thuyết đều có VCdim vô hạn.
- **B.** VCdim là số giả thuyết phân biệt trong H; hàm ngưỡng trên R có vô hạn giá trị θ nên VCdim vô hạn và lớp này không PAC learnable.
- **C.** VCdim là số mẫu tối thiểu để ERM không overfit; hàm ngưỡng cần đúng hai điểm để xác định θ nên VCdim = 2 với mọi phân phối D.
- **D.** VCdim là kích thước lớn nhất của một tập C ⊂ X mà H shatter được; hàm ngưỡng shatter mọi tập một điểm nhưng không tập hai điểm nào, nên VCdim = 1.

## Câu 11 (Trắc nghiệm)

Bạn thử r = 200 cấu hình hyperparameter và chọn cấu hình có lỗi validation thấp nhất trên tập validation V gồm m_v mẫu. UML Định lý 11.2 cảnh báo điều gì về ước lượng lỗi thật của cấu hình được chọn?

- **A.** Bound phụ thuộc vào VC-dimension của mô hình gốc, nên với mạng neural lớn m_v phải ít nhất bằng số tham số thì ước lượng mới có ý nghĩa.
- **B.** Bound đúng đồng thời cho cả r giả thuyết với |H| = r trong logarit, nên thử quá nhiều cấu hình so với m_v sẽ dẫn đến overfitting chính validation set.
- **C.** Không có vấn đề gì, vì validation set độc lập với training set nên lỗi validation là ước lượng không chệch cho mọi cấu hình, kể cả cấu hình được chọn sau cùng.
- **D.** Bound trở nên vô nghĩa ngay khi r > 1, vì Định lý 11.1 chỉ đúng cho một giả thuyết duy nhất được cố định trước khi lấy mẫu validation set.

## Câu 12 (Trắc nghiệm)

Shalizi viết in-sample loss dưới dạng L(z_n, θ) = E[L(Z, θ)] + η_n(θ), với η_n(θ) là nhiễu lấy mẫu có kỳ vọng 0. Vì sao lỗi trên tập huấn luyện của mô hình được chọn θ̂_n lại lạc quan (optimistic) dù luật số lớn nói L(z_n, θ) → E[L(Z, θ)] cho từng θ?

- **A.** Vì tập huấn luyện luôn có nhiễu đo lường, nên kỳ vọng của η_n(θ) thực ra dương với mọi θ và phải trừ đi một hằng số hiệu chỉnh.
- **B.** Vì luật số lớn chỉ đúng khi loss là mean squared error; với negative log-likelihood, in-sample loss không hội tụ về risk thật dù n tăng.
- **C.** Vì η_n(θ) có kỳ vọng 0 với từng θ cố định, nhưng θ̂_n được chọn để cực tiểu E[L] + η_n nên nó thường là θ vừa tốt vừa may mắn (η_n < 0).
- **D.** Vì luật số lớn chỉ áp dụng khi n → ∞, nên với mọi n hữu hạn in-sample loss của bất kỳ θ nào cũng lớn hơn risk thật của nó.

## Câu 13 (Tự luận)

Tong Zhang phát biểu generalization bound dạng: với xác suất ≥ 1 − δ, test-loss ≤ training-loss + εₙ(δ). Hãy viết dạng này, giải thích vì sao ta cần nó khi chỉ quan sát được training error, rồi nêu điểm căng thẳng mà Zhang chỉ ra giữa lý thuyết cổ điển (hạn chế kích thước mô hình) và quan sát thực nghiệm ở mạng neural hiện đại. Điều này ảnh hưởng thế nào đến cách bạn đọc loss curve ở Tuần 8?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Shalev-Shwartz và Ben-David tách lỗi của giả thuyết ERM thành ε_app + ε_est. Khi bạn tăng hạng r của LoRA ở Tuần 11, thành phần nào của phân tích này có xu hướng thay đổi theo hướng nào?

- **A.** ε_app giảm vì lớp giả thuyết rộng hơn, còn ε_est có xu hướng tăng vì mẫu hữu hạn phải ước lượng nhiều tham số hơn
- **B.** Không thành phần nào đổi vì LoRA không đổi lớp giả thuyết
- **C.** Cả hai đều giảm vì model mạnh hơn
- **D.** Chỉ ε_est giảm

## Nâng cao 2 (Tự luận)

Tại sao Shalev-Shwartz và Ben-David nói bound ước lượng từ validation set độc lập chính xác hơn bound từ VC-dimension, và cái giá của cách đó là gì?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
