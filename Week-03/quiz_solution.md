# Tuần 3, Đáp án & Giải thích: Nền tảng ML và lý thuyết học

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Trong khung học thống kê của Shalev-Shwartz và Ben-David, learner được biết gì và không được biết gì?

- **A.** Biết phân phối D và hàm nhãn f, chỉ không biết tập test
- **B.** Biết mọi thứ trừ kích thước mẫu m
- **C.** Biết training data S gồm các cặp (x, y); không biết phân phối D sinh ra x và hàm gán nhãn f (đáp án đúng)
- **D.** Biết phân phối D nhưng không biết training data

**Đáp án: C**

**Giải thích:** UML mục 2.1 (trang 33) và câu ở trang 35: learner 'mù' với D và f, cách duy nhất tương tác với thế giới là qua training set. Vì thế lỗi thật L_D(h) không tính được, chỉ tính được lỗi trên mẫu.

## Câu 2 (Trắc nghiệm)

Empirical Risk Minimization trên toàn bộ các hàm có thể có thì dẫn đến hậu quả gì, và lý thuyết đề xuất cách khắc phục nào?

- **A.** Dẫn đến underfitting; khắc phục bằng cách tăng learning rate
- **B.** Không có hậu quả gì nếu dữ liệu đủ sạch
- **C.** Dẫn đến overfitting vì một hàm nhớ hết mẫu có lỗi mẫu bằng 0 nhưng lỗi thật cao; khắc phục bằng cách giới hạn trước lớp giả thuyết H, gọi là inductive bias (đáp án đúng)
- **D.** Dẫn đến chi phí tính toán cao; khắc phục bằng GPU

**Đáp án: C**

**Giải thích:** UML mục 2.2 định nghĩa empirical risk (eq. 2.2, trang 35) và mục 2.3 (trang 36) đưa ra ERM với inductive bias. Lab 02_erm_lab.py cho thấy đa thức bậc cao có train loss thấp nhất nhưng validation loss lớn.

## Câu 3 (Tự luận)

Hãy viết công thức tách lỗi của giả thuyết ERM thành approximation error và estimation error, rồi giải thích mỗi thành phần phụ thuộc vào điều gì.

**Trả lời mẫu:** L_D(h_S) = ε_app + ε_est, với ε_app = min over h in H của L_D(h) và ε_est = L_D(h_S) − ε_app (UML eq. 5.7, trang 64). Approximation error là lỗi nhỏ nhất đạt được trong lớp H, không phụ thuộc kích thước mẫu, chỉ phụ thuộc H; mở rộng H làm nó giảm. Estimation error là phần trả giá vì chỉ có mẫu hữu hạn; H càng lớn thì phần này càng dễ lớn. Cách nói bias và variance là phiên bản trực giác của cùng trade-off.

**Giải thích:** Đây là khung để đọc mọi loss curve về sau: train loss giảm mà validation loss tăng nghĩa là estimation error đang thắng.

## Câu 4 (Trắc nghiệm)

Trong định nghĩa PAC learnability, hai tham số ε và δ lần lượt mang ý nghĩa gì?

- **A.** ε là learning rate, δ là kích thước batch
- **B.** ε là số mẫu, δ là số chiều của dữ liệu
- **C.** ε là lỗi trên training set, δ là lỗi trên test set
- **D.** ε là độ chính xác cho phép của giả thuyết trả về (phần 'approximately correct'), δ là xác suất thất bại được chấp nhận (phần 'probably') (đáp án đúng)

**Đáp án: D**

**Giải thích:** UML Definition 3.1 (trang 43): với m ≥ m_H(ε, δ) mẫu i.i.d., thuật toán trả về h có lỗi thật không quá ε với xác suất ít nhất 1 − δ. Hai xấp xỉ này là không tránh được vì mẫu hữu hạn và ngẫu nhiên.

## Câu 5 (Trắc nghiệm)

Điều gì tuyệt đối không được làm với validation data, và vì sao?

- **A.** Không được vẽ đồ thị trên validation data vì tốn thời gian
- **B.** Không được để validation data nhỏ hơn 50% dữ liệu
- **C.** Không được dùng validation data để ước lượng hay chọn tham số model, vì khi đó ước lượng lỗi trên nó không còn độc lập và không còn là ước lượng không chệch của lỗi thật (đáp án đúng)
- **D.** Không được chia validation data ngẫu nhiên vì làm mất thứ tự thời gian

**Đáp án: C**

**Giải thích:** Shalizi mục 3.4 (trang 81): 'we absolutely, positively, cannot use any of the validation data in estimating the model.' UML mục 11.2 (trang 146) chỉ ra bound từ validation set độc lập chính xác hơn bound VC, nhưng chỉ khi nó thật sự độc lập.

## Câu 6 (Tự luận)

Logistic regression khác linear regression ở những điểm nào về đầu ra, hàm loss và cách giải, và vì sao có thể gọi nó là mạng neural một lớp?

**Trả lời mẫu:** Linear regression trả về số thực, dùng squared loss, và có nghiệm đóng bằng phép chiếu trực giao (MML Example 8.1, trang 259). Logistic regression đưa đầu ra qua sigmoid để thành xác suất trong (0, 1), dùng negative log-likelihood của Bernoulli tức binary cross-entropy, và không có nghiệm đóng nên phải dùng gradient descent với gradient Xᵀ(p − y)/n (Vũ Hữu Tiệp chương 14, trang 165). Nó là một lớp tuyến tính nối với một hàm kích hoạt phi tuyến và một loss, đúng cấu trúc tối giản của một mạng neural.

**Giải thích:** Tuần 4 viết lại đúng model này bằng nn.Linear và F.binary_cross_entropy trong PyTorch, rồi chồng thêm lớp để thành MLP.

## Câu 7 (Trắc nghiệm)

Hệ quả 2.3 trong UML cho lớp giả thuyết hữu hạn (giả định realizable): với m ≥ log(|H|/δ)/ε mẫu, ERM đạt lỗi thật ≤ ε với xác suất ≥ 1 − δ. Nếu bạn gấp đôi kích thước lớp giả thuyết |H| mà giữ ε, δ, số mẫu cần thiết thay đổi thế nào?

- **A.** Không thay đổi, vì bound chỉ phụ thuộc vào ε và δ, còn |H| bị triệt tiêu trong union bound.
- **B.** Tăng gấp đôi, vì số mẫu cần thiết tỉ lệ thuận với số giả thuyết mà thuật toán phải phân biệt.
- **C.** Tăng gấp bốn, vì lỗi ε xuất hiện bậc hai trong Hoeffding và |H| nhân đôi số sự kiện xấu.
- **D.** Tăng thêm một lượng cố định log(2)/ε, vì |H| chỉ xuất hiện trong logarit nên mở rộng lớp giả thuyết khá rẻ. (đáp án đúng)

**Đáp án: D**

**Giải thích:** Hệ quả 2.3: "let m be an integer that satisfies m ≥ log(|H|/δ)/ε. Then, for any labeling function f, and for any distribution D, for which the realizability assumption holds ... with probability of at least 1 − δ ... L_(D,f)(h_S) ≤ ε" (UML Hệ quả 2.3, tr. 40-41). Vì log(2|H|/δ) = log(|H|/δ) + log 2, số mẫu chỉ tăng thêm log(2)/ε. Chứng minh đi qua union bound trên tập giả thuyết xấu H_B và bất đẳng thức (1 − ε)ᵐ ≤ e^{−εm} (công thức 2.9), nên |H| xuất hiện dưới dạng hệ số |H|e^{−εm} rồi vào logarit (UML mục 2.3.1, công thức 2.6-2.9, tr. 39-40)

## Câu 8 (Trắc nghiệm)

Bất đẳng thức Hoeffding (UML Lemma 4.5) cho P[|(1/m)Σθᵢ − µ| > ε] ≤ 2 exp(−2mε²/(b − a)²). Muốn giảm sai số ε xuống còn một nửa với cùng độ tin cậy, kích thước mẫu m cần thay đổi bao nhiêu?

- **A.** Gấp đôi, vì ε và m xuất hiện đối xứng trong tích mε² nên chia đôi ε tương đương nhân đôi m.
- **B.** Gấp tám, vì ngoài mε² còn phải bù cho hệ số 2 phía trước hàm mũ.
- **C.** Không cần thay đổi, vì độ tin cậy 1 − δ đã cố định và Hoeffding không phụ thuộc vào ε.
- **D.** Gấp bốn, vì mũ chứa mε² nên để giữ nguyên mε² khi ε giảm một nửa thì m phải tăng bốn lần. (đáp án đúng)

**Đáp án: D**

**Giải thích:** Lemma 4.5 (Hoeffding's Inequality): với θ₁, ..., θₘ i.i.d., E[θᵢ] = µ và θᵢ ∈ [a, b], P[|(1/m)Σθᵢ − µ| > ε] ≤ 2 exp(−2mε²/(b − a)²) (UML Lemma 4.5, tr. 56). Vì bound phụ thuộc vào mε², chia đôi ε đòi m tăng gấp bốn; Hệ quả 4.6 cho cùng kết luận với sample complexity m_H^UC(ε, δ) ≤ ⌈log(2|H|/δ)/(2ε²)⌉ (UML mục 4.2, Hệ quả 4.6, tr. 57). Sách nhấn mạnh luật số lớn chỉ là kết quả tiệm cận, còn Hoeffding cho con số cụ thể với m hữu hạn, đúng điều cần khi ước lượng độ tin cậy của một eval set (UML mục 4.2, tr. 56)

## Câu 9 (Trắc nghiệm)

Định lý No-Free-Lunch (UML Định lý 5.1) nói gì, và hệ quả nào rút ra cho lớp giả thuyết gồm mọi hàm từ một miền X vô hạn vào {0, 1}?

- **A.** Với mọi learner A và m < |X|/2, tồn tại D có hàm f với L_D(f) = 0 nhưng P[L_D(A(S)) ≥ 1/8] ≥ 1/7, do đó lớp gồm mọi hàm trên X vô hạn không PAC learnable. (đáp án đúng)
- **B.** Mọi thuật toán học đều đạt lỗi tối thiểu trên mọi phân phối nếu m đủ lớn, do đó lớp gồm mọi hàm là PAC learnable ngay khi m ≥ |X|/2.
- **C.** Không thuật toán nào học được bất kỳ hàm nào nếu không biết trước phân phối D, do đó chỉ các lớp giả thuyết hữu hạn mới có thể PAC learnable.
- **D.** Với m ≥ |X|/2 mẫu mọi learner đều đạt lỗi ≤ 1/8 với xác suất ≥ 6/7, do đó VC-dimension của lớp gồm mọi hàm đúng bằng |X|/2.

**Đáp án: A**

**Giải thích:** Định lý 5.1: "Let A be any learning algorithm for the task of binary classification with respect to the 0 − 1 loss over a domain X. Let m be any number smaller than |X|/2 ... Then, there exists a distribution D over X × {0, 1} such that: 1. There exists a function f : X → {0, 1} with L_D(f) = 0. 2. With probability of at least 1/7 over the choice of S ∼ Dᵐ we have that L_D(A(S)) ≥ 1/8" (UML mục 5.1, Định lý 5.1, tr. 61). Hệ quả 5.2: "Let X be an infinite domain set and let H be the set of all functions from X to {0, 1}. Then, H is not PAC learnable" (UML mục 5.1.1, Hệ quả 5.2, tr. 63). Sách kết luận cần prior knowledge qua việc giới hạn lớp giả thuyết, tức inductive bias (UML mục 5.1.1, tr. 64)

## Câu 10 (Trắc nghiệm)

Theo UML Định nghĩa 6.5, VC-dimension của lớp giả thuyết H là gì, và VCdim của lớp hàm ngưỡng (threshold functions) trên R bằng bao nhiêu?

- **A.** VCdim là số tham số của mô hình; hàm ngưỡng có một tham số θ nên VCdim = 1, và mọi lớp có vô hạn giả thuyết đều có VCdim vô hạn.
- **B.** VCdim là số giả thuyết phân biệt trong H; hàm ngưỡng trên R có vô hạn giá trị θ nên VCdim vô hạn và lớp này không PAC learnable.
- **C.** VCdim là số mẫu tối thiểu để ERM không overfit; hàm ngưỡng cần đúng hai điểm để xác định θ nên VCdim = 2 với mọi phân phối D.
- **D.** VCdim là kích thước lớn nhất của một tập C ⊂ X mà H shatter được; hàm ngưỡng shatter mọi tập một điểm nhưng không tập hai điểm nào, nên VCdim = 1. (đáp án đúng)

**Đáp án: D**

**Giải thích:** Định nghĩa 6.5: "The VC-dimension of a hypothesis class H, denoted VCdim(H), is the maximal size of a set C ⊂ X that can be shattered by H. If H can shatter sets of arbitrarily large size we say that H has infinite VC-dimension". Mục 6.3.1 kết luận cho hàm ngưỡng: H shatter mọi C = {c₁} nên VCdim ≥ 1, nhưng với C = {c₁, c₂}, c₁ ≤ c₂ thì không shatter được, do đó VCdim(H) = 1. Định lý 6.6 nói lớp có VC-dimension vô hạn thì không PAC learnable; lớp vô hạn nhưng VCdim hữu hạn vẫn học được, nên VCdim không phải số tham số hay số giả thuyết (UML mục 6.2-6.3.1, Định nghĩa 6.5, Định lý 6.6, tr. 70)

## Câu 11 (Trắc nghiệm)

Bạn thử r = 200 cấu hình hyperparameter và chọn cấu hình có lỗi validation thấp nhất trên tập validation V gồm m_v mẫu. UML Định lý 11.2 cảnh báo điều gì về ước lượng lỗi thật của cấu hình được chọn?

- **A.** Bound phụ thuộc vào VC-dimension của mô hình gốc, nên với mạng neural lớn m_v phải ít nhất bằng số tham số thì ước lượng mới có ý nghĩa.
- **B.** Bound đúng đồng thời cho cả r giả thuyết với |H| = r trong logarit, nên thử quá nhiều cấu hình so với m_v sẽ dẫn đến overfitting chính validation set. (đáp án đúng)
- **C.** Không có vấn đề gì, vì validation set độc lập với training set nên lỗi validation là ước lượng không chệch cho mọi cấu hình, kể cả cấu hình được chọn sau cùng.
- **D.** Bound trở nên vô nghĩa ngay khi r > 1, vì Định lý 11.1 chỉ đúng cho một giả thuyết duy nhất được cố định trước khi lấy mẫu validation set.

**Đáp án: B**

**Giải thích:** Bài học cho Tuần 14: eval set RAG nhỏ mà quét hàng trăm cấu hình thì điểm tốt nhất bị thổi phồng. Định lý 11.2: với H = {h₁, ..., h_r} và validation set V kích thước m_v độc lập với H, với xác suất ≥ 1 − δ, ∀h ∈ H: |L_D(h) − L_V(h)| ≤ √(log(2|H|/δ)/(2m_v)). Sách nhận xét: "the error on the validation set approximates the true error as long as H is not too large. However, if we try too many methods (resulting in |H| that is large relative to the size of the validation set) then we're in danger of overfitting". Chọn cấu hình theo validation chính là áp dụng ERM_H trên validation set với lớp hữu hạn (UML mục 11.2.2, Định lý 11.2, tr. 147-148)

## Câu 12 (Trắc nghiệm)

Shalizi viết in-sample loss dưới dạng L(z_n, θ) = E[L(Z, θ)] + η_n(θ), với η_n(θ) là nhiễu lấy mẫu có kỳ vọng 0. Vì sao lỗi trên tập huấn luyện của mô hình được chọn θ̂_n lại lạc quan (optimistic) dù luật số lớn nói L(z_n, θ) → E[L(Z, θ)] cho từng θ?

- **A.** Vì tập huấn luyện luôn có nhiễu đo lường, nên kỳ vọng của η_n(θ) thực ra dương với mọi θ và phải trừ đi một hằng số hiệu chỉnh.
- **B.** Vì luật số lớn chỉ đúng khi loss là mean squared error; với negative log-likelihood, in-sample loss không hội tụ về risk thật dù n tăng.
- **C.** Vì η_n(θ) có kỳ vọng 0 với từng θ cố định, nhưng θ̂_n được chọn để cực tiểu E[L] + η_n nên nó thường là θ vừa tốt vừa may mắn (η_n < 0). (đáp án đúng)
- **D.** Vì luật số lớn chỉ áp dụng khi n → ∞, nên với mọi n hữu hạn in-sample loss của bất kỳ θ nào cũng lớn hơn risk thật của nó.

**Đáp án: C**

**Giải thích:** Shalizi: "the in-sample loss equals the risk plus sampling noise: L(z_n, θ) = E[L(Z, θ)] + η_n(θ)" (công thức 3.6) và "θ̂_n = argmin (E[L(Z, θ)] + η_n(θ)) ... we're almost surely going to end up picking a θ̂_n which was more or less lucky (η_n < 0) as well as good (E[L(Z, θ)] small). This is the reason why picking the model which best fits the data tends to exaggerate how well it will do in the future" (công thức 3.7). Sách nói lý thuyết học tiến xa hơn bằng các uniform laws of large numbers, tức kiểm soát max_θ |η_n(θ)|, đúng khung uniform convergence của UML Chương 4 (Shalizi mục 3.2, công thức 3.5-3.7, tr. 71-73)

## Câu 13 (Tự luận)

Tong Zhang phát biểu generalization bound dạng: với xác suất ≥ 1 − δ, test-loss ≤ training-loss + εₙ(δ). Hãy viết dạng này, giải thích vì sao ta cần nó khi chỉ quan sát được training error, rồi nêu điểm căng thẳng mà Zhang chỉ ra giữa lý thuyết cổ điển (hạn chế kích thước mô hình) và quan sát thực nghiệm ở mạng neural hiện đại. Điều này ảnh hưởng thế nào đến cách bạn đọc loss curve ở Tuần 8?

**Trả lời mẫu:** Dạng bound: E_{(X,Y)∼D} L(f(ŵ, X), Y) ≤ (1/n)Σᵢ L(f(ŵ, Xᵢ), Yᵢ) + εₙ(δ), với εₙ(δ) → 0 khi n → ∞; xác suất tính trên việc lấy mẫu ngẫu nhiên tập huấn luyện Sₙ. Ta cần nó vì test loss là kỳ vọng trên phân phối D không biết, chỉ training loss là quan sát được, nên bound cho phép suy test loss từ training loss cộng một khoản phụ thuộc n và độ phức tạp của lớp mô hình. Zhang lưu ý lý thuyết cổ điển coi hạn chế kích thước mô hình là kỹ thuật then chốt chống overfitting, nhưng với mạng neural hiện đại người ta quan sát mô hình lớn gần như luôn tốt hơn và hiện tượng benign overfitting: thuật toán với implicit bias phù hợp vẫn đạt test tốt dù fit hoàn toàn nhiễu; lý thuyết cho việc này chưa chín. Khi đọc loss curve Tuần 8, train loss thấp hơn validation loss là đúng dự đoán của bound, nhưng khoảng cách nhỏ không đủ để kết luận mô hình quá lớn hay quá nhỏ; cần nhìn validation loss thực tế thay vì chỉ dựa vào số tham số.

**Giải thích:** Công thức (1.2): "with probability at least 1 − δ ... E_{(X,Y)∼D} L(f(ŵ, X), Y) ≤ (1/n)Σ L(f(ŵ, Xᵢ), Yᵢ) + εₙ(δ)", cùng định nghĩa training-loss và test-loss ở mục 1.1 (Tong Zhang mục 1.1, công thức 1.1-1.2, tr. 2-3). Về căng thẳng lý thuyết: "the mathematical theory developed for limiting model size and preventing overfitting is the key classical technique ... However, in recent years, this classical view point has evolved due to the empirical observation in modern neural network models that large models nearly always perform better. For such models, one observes the so-called benign overfitting phenomenon ... the related theoretical results are less mature" (Tong Zhang mục 1.4, tr. 7). Hình 1.1 vẽ training error giảm đơn điệu còn test error có dạng chữ U theo độ phức tạp mô hình (Tong Zhang mục 1.4, Hình 1.1, tr. 6)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Shalev-Shwartz và Ben-David tách lỗi của giả thuyết ERM thành ε_app + ε_est. Khi bạn tăng hạng r của LoRA ở Tuần 11, thành phần nào của phân tích này có xu hướng thay đổi theo hướng nào?

- **A.** ε_app giảm vì lớp giả thuyết rộng hơn, còn ε_est có xu hướng tăng vì mẫu hữu hạn phải ước lượng nhiều tham số hơn (đáp án đúng)
- **B.** Không thành phần nào đổi vì LoRA không đổi lớp giả thuyết
- **C.** Cả hai đều giảm vì model mạnh hơn
- **D.** Chỉ ε_est giảm

**Đáp án: A**

**Giải thích:** UML mục 5.2 (trang 64): approximation error chỉ phụ thuộc H, estimation error là giá của mẫu hữu hạn. Tăng r mở rộng H. Kết quả thực nghiệm phụ thuộc dữ liệu; đây là khung để đọc, không phải dự đoán chắc.

## Nâng cao 2 (Tự luận)

Tại sao Shalev-Shwartz và Ben-David nói bound ước lượng từ validation set độc lập chính xác hơn bound từ VC-dimension, và cái giá của cách đó là gì?

**Trả lời mẫu:** Bound VC phụ thuộc VC-dimension d và kích thước mẫu m, còn bound từ validation set chỉ phụ thuộc kích thước m_v của validation set với sai số cỡ căn(log(2/δ)/(2m_v)), không phụ thuộc độ phức tạp của lớp giả thuyết (UML mục 11.2, trang 146-147). Cái giá là cần thêm mẫu độc lập ngoài mẫu đã dùng để train, và tuyệt đối không dùng validation data để ước lượng model (Shalizi mục 3.4, trang 81).

**Giải thích:** Đây là lý do mọi tuần eval về sau đều đòi held-out set riêng, kể cả eval set RAGAS ở Tuần 14.
