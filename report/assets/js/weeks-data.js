/* Dữ liệu tuần + phase (trích từ report gốc). window.PHASES, window.WEEKS_DATA */
window.PHASES = [
  {id:0, no:"PHASE 0", name:"Nền tảng toán & ML", weeks:"Tuần 1-3", cls:"p0",
   desc:"Ba tuần dựng nền từ kệ sách giáo trình: đại số tuyến tính và hình học giải tích; giải tích vector, xác suất, tối ưu hóa; rồi khung học thống kê (ERM, generalization, bias-variance, PAC, validation). Không có PyTorch, chỉ NumPy."},
  {id:1, no:"PHASE 1", name:"Deep Internals", weeks:"Tuần 4-10", cls:"p1",
   desc:"Hiểu sâu nội tại: PyTorch, backprop, attention từ đầu, lắp ráp GPT-2, pretraining, instruction fine-tuning, và alignment (tách 2 tuần cho đỡ dồn)."},
  {id:2, no:"PHASE 2", name:"Applied, RAG & Fine-Tuning", weeks:"Tuần 11-14", cls:"p2",
   desc:"Chuyển sang tooling production: QLoRA trên 3070 Ti, MLX trên Mac, RAG pipeline end-to-end, advanced RAG + đánh giá RAGAS."},
  {id:3, no:"PHASE 3", name:"Agentic SDLC, CornAgents.AI", weeks:"Tuần 15-18", cls:"p3",
   desc:"Xây framework agentic-SDLC cá nhân: 5 tầng engineering, Claude Agent SDK + MCP + LangGraph/CrewAI, multi-agent workflow, Graph Engineering (knowledge graph làm shared memory), capstone Finance Banking."}
];

window.WEEKS_DATA = [
 {
  n:1, phase:0, title:"Đại số tuyến tính và hình học giải tích", dur:"~10-12 giờ", hw:"Bất kỳ (NumPy)",
  obj:["Đọc phép nhân ma trận như phép biến đổi không gian và suy ra chiều kết quả không cần chạy code","Giải thích vì sao dot product đo độ cùng hướng và cosine similarity là góc giữa hai vector","Tính nghiệm least squares bằng phép chiếu trực giao, kiểm phần dư trực giao với không gian cột","Nêu ý nghĩa trị riêng, giá trị kỳ dị, xấp xỉ hạng thấp, nối sang câu hỏi vì sao LoRA chỉ cần hạng r nhỏ"],
  src:["<b>Mathematics for Machine Learning</b>, Ch.2 Linear Algebra, Ch.3 Analytic Geometry, Ch.4 Matrix Decompositions (tr. 22-134)","<b>Machine Learning cơ bản</b> (Vũ Hữu Tiệp): Ch.1 Ôn tập đại số tuyến tính (tr. 13-28)","Catalog chương và trang: <code>docs/books/README.md</code>"],
  deliver:"Cheat sheet một trang tự viết (<code>03_cheat_sheet.md</code>) với bốn mục ánh xạ tuyến tính, dot product và góc, phép chiếu, SVD; cộng hai bài tập NumPy (least squares bằng phép chiếu, hai hướng chính từ ma trận Gram) có output.",
  know:`<h5>Ma trận là ánh xạ tuyến tính</h5>
   <p>Nhân ma trận là hợp hai ánh xạ nên không giao hoán (MML 2.7, tr. 48). Xoay 90° rồi kéo dãn trục x đưa [1, 0] thành [0, 1]; làm ngược thứ tự thì ra [0, 2]. <code>nn.Linear</code> ở Tuần 4 và W_Q, W_K, W_V ở Tuần 6 đều là ánh xạ kiểu này.</p>
   <h5>Góc và trực giao</h5>
   <div class="formula">\\( \\cos\\omega=\\dfrac{\\langle x,y\\rangle}{\\|x\\|\\,\\|y\\|} \\)</div>
   <p>MML Ex 3.6 (tr. 77): x = [1, 1], y = [1, 2] cho cos ω = 3/√10, góc ≈ 18°. Đây là attention score q·k của Tuần 6 và cosine similarity trong RAG Tuần 13.</p>
   <h5>Phép chiếu và least squares</h5>
   <div class="formula">\\( \\hat{x}=(A^{\\top}A)^{-1}A^{\\top}b,\\qquad A^{\\top}(b-A\\hat{x})=0 \\)</div>
   <h5>SVD và xấp xỉ hạng thấp</h5>
   <p>A = UΣVᵀ tồn tại cho mọi ma trận (MML Thm 4.22, tr. 119). Giữ k giá trị kỳ dị lớn nhất là xấp xỉ hạng k tốt nhất (Eckart-Young, Thm 4.25, tr. 131). Ma trận 6×5 hạng 2 cộng nhiễu 0.01 có giá trị kỳ dị [4.98, 2.17, 0.02, 0.02, 0.005]. LoRA (Tuần 9, 11) đặt cược vào đúng trực giác này.</p>
   <div class="tagrow"><span class="kt">linear map</span><span class="kt">rank</span><span class="kt">norm</span><span class="kt">cosine</span><span class="kt">projection</span><span class="kt">eigen</span><span class="kt">SVD</span></div>`,
  check:["Đọc 01_theory_notes.md mục 1-3 (ánh xạ tuyến tính, chiều, hạng)","Đọc MML 2.4-2.7 khi cần chứng minh đầy đủ","Đọc 01_theory_notes.md mục 4-5 (norm, góc, phép chiếu)","Đọc MML 3.1, 3.2, 3.4, 3.8","Đọc 01_theory_notes.md mục 6-7 (trị riêng, SVD, xấp xỉ hạng thấp)","Đọc MML 4.2, 4.5, 4.6","Chạy hết 02_linear_algebra_lab.py, đoán trước rồi chạy","Bài tập 1: least squares bằng phép chiếu","Bài tập 2: hai hướng chính từ ma trận Gram, so với np.linalg.svd","Viết 03_cheat_sheet.md bằng lời mình","Tự kiểm tra: giải thích cho Claude vì sao cosine similarity là góc và vì sao SVD cho xấp xỉ hạng thấp tốt nhất"]
 },
 {
  n:2, phase:0, title:"Giải tích vector, xác suất, tối ưu hóa", dur:"~12-14 giờ", hw:"Bất kỳ (NumPy)",
  obj:["Tính gradient hàm nhiều biến bằng tay và kiểm lại bằng sai phân số","Phát biểu chain rule dạng Jacobian và chỉ ra nó là toàn bộ ý tưởng của backprop","Dùng đúng tiên đề xác suất, sum rule, product rule, Bayes trên bài toán đếm được","Giải thích luật số lớn và CLT bằng mô phỏng, nối sang loss trên batch là ước lượng của loss kỳ vọng","Chỉ ra cross-entropy là negative log-likelihood; tự cài gradient descent và thấy step size quyết định hội tụ"],
  src:["<b>MML</b>, Ch.5 Vector Calculus, Ch.6 Probability, Ch.7 Optimization (tr. 141-246)","<b>Durrett</b>, Elementary Probability for Applications, 1.1.1, 4.4, 4.5, 5.3","<b>Vũ Hữu Tiệp</b>, Ch.2, 3, 4, 12; <b>Nguyễn Thanh Tuấn</b>, 3.3 gradient descent","Sách mở: <b>MacKay</b> 2.4 entropy, KL; <b>Murphy</b> 6.1-6.2; <b>Boyd</b> 3.1.1 convex"],
  deliver:"<code>03_gradient_descent.py</code> tự điền đạo hàm và bước cập nhật, kèm output và câu trả lời hai câu hỏi (điểm khởi đầu, step size); cheat sheet <code>04_cheat_sheet.md</code>.",
  know:`<h5>Gradient và chain rule</h5>
   <p>MML Ex 5.7 (tr. 147): f = x₁²x₂ + x₁x₂³ có gradient [12, 13] tại (1, 2); sai phân trung tâm khớp tới 1e-9 (Vũ Hữu Tiệp 2.6, tr. 36). Jacobian của Ax là A, nên backward của Linear chỉ là nhân với Wᵀ.</p>
   <h5>Xác suất</h5>
   <p>Ba tiên đề (Durrett 1.1.1, tr. 4); pmf, pdf, cdf tách rõ ở MML Table 6.1 (tr. 183). Bayes: bệnh 1%, nhạy 95%, dương tính giả 5% cho P(bệnh | dương) ≈ 0.16, không phải 90%.</p>
   <div class="formula">\\( \\bar X_n\\to\\mu,\\quad \\mathrm{var}(\\bar X_n)=\\sigma^2/n,\\qquad \\dfrac{S_n-n\\mu}{\\sigma\\sqrt n}\\to N(0,1) \\)</div>
   <p>Loss trên batch là trung bình mẫu như X̄ₙ; batch nhỏ thì loss curve nhấp nhô hơn.</p>
   <h5>MLE và gradient descent</h5>
   <p>Cross-entropy là negative log-likelihood (Vũ Hữu Tiệp 4.2, tr. 53). Gradient descent x ← x − γ∇f: điểm khởi đầu quyết định rơi vào cực tiểu nào (MML Fig 7.2, tr. 227); trên x², lr 0.1 hội tụ, lr 1.1 phân kỳ.</p>
   <div class="tagrow"><span class="kt">gradient</span><span class="kt">chain rule</span><span class="kt">gradcheck</span><span class="kt">Bayes</span><span class="kt">LLN</span><span class="kt">CLT</span><span class="kt">MLE</span><span class="kt">step size</span></div>`,
  check:["Đọc 01_theory_notes.md phần A (đạo hàm, gradient, chain rule, Jacobian)","Đọc MML 5.2, 5.3; Vũ Hữu Tiệp 2.6","Chạy gradcheck, chain, jacobian trong lab","Đọc 01_theory_notes.md phần B (tiên đề, Bayes, LLN, CLT)","Đọc Durrett 1.1.1, 4.4, 4.5, 5.3; MML Table 6.1","Chạy lln, clt, bayes; tự làm bài Bayes với số của mình","Đọc 01_theory_notes.md phần C (MLE, gradient descent, step size, convex)","Đọc MML 7.1; Vũ Hữu Tiệp Ch.12","Chạy mle trong lab","Điền TODO trong 03_gradient_descent.py và trả lời hai câu hỏi","Viết 04_cheat_sheet.md bằng lời mình","Tự kiểm tra: giải thích cho Claude vì sao cross-entropy là negative log-likelihood"]
 },
 {
  n:3, phase:0, title:"Nền tảng ML và lý thuyết học", dur:"~12-14 giờ", hw:"Bất kỳ (NumPy)",
  obj:["Phát biểu khung học thống kê: X, Y, D không biết, mẫu S, giả thuyết h, L_D(h) và L_S(h)","Giải thích ERM và vì sao ERM không giới hạn lớp giả thuyết thì overfit","Tách lỗi thành approximation và estimation error, nối sang bias và variance","Nhận diện định nghĩa PAC learnability và VC-dimension","Dùng đúng train, validation, test; tự code linear và logistic regression bằng NumPy"],
  src:["<b>Shalev-Shwartz & Ben-David</b>, Understanding Machine Learning, 2.1-2.3, Def 3.1, 5.2, Def 6.5, 11.2","<b>Tong Zhang</b>, 1.1, 1.4, 3.1; <b>MML</b>, Ch.8, 9.2.1","<b>Shalizi</b>, 3.2-3.4; <b>Mehlig</b>, 5.3, 6.1, 6.4; <b>Vũ Hữu Tiệp</b>, Ch.5, 7, 8, 14","Sách mở: <b>Murphy</b> 4.3 ERM; <b>Bishop</b> 4.3.2 logistic regression; <b>SLP3</b> ch.4"],
  deliver:"<code>02_erm_lab.py</code> và <code>04_logistic_regression_numpy.py</code> chạy được kèm output; <code>03_learning_theory_notes.md</code> với năm khái niệm ERM, overfitting, error decomposition, PAC, validation viết bằng lời mình.",
  know:`<h5>Khung học thống kê và ERM</h5>
   <p>Learner chỉ thấy mẫu S, không thấy D và f (UML 2.1, tr. 33). Empirical risk L_S(h) là tỉ lệ sai trên mẫu (UML eq. 2.2, tr. 35); ERM chọn h làm nó nhỏ nhất, và phải giới hạn lớp H trước để không overfit (UML 2.3).</p>
   <h5>Tách lỗi</h5>
   <div class="formula">\\( L_D(h_S)=\\varepsilon_{app}+\\varepsilon_{est},\\quad \\varepsilon_{app}=\\min_{h\\in H}L_D(h) \\)</div>
   <p>Approximation error chỉ phụ thuộc H; estimation error là giá của mẫu hữu hạn (UML 5.2, tr. 64). Bias và variance là cách nói trực giác của cùng trade-off.</p>
   <h5>PAC và VC</h5>
   <p>PAC: đúng đến ε với xác suất 1 − δ khi có đủ m_H(ε, δ) mẫu (UML Def 3.1, tr. 43). VC-dimension: tập lớn nhất H shatter được; vô hạn thì không học được (UML Def 6.5, Thm 6.6, tr. 70).</p>
   <h5>Validation</h5>
   <p>"We absolutely, positively, cannot use any of the validation data in estimating the model" (Shalizi 3.4, tr. 81). Train khớp tham số, validation chọn model, test chạm một lần cuối.</p>
   <div class="tagrow"><span class="kt">ERM</span><span class="kt">inductive bias</span><span class="kt">overfitting</span><span class="kt">bias-variance</span><span class="kt">PAC</span><span class="kt">VC-dim</span><span class="kt">hold-out</span><span class="kt">logistic regression</span></div>`,
  check:["Đọc 01_theory_notes.md mục 1-2 (khung học thống kê, ERM)","Đọc UML 2.1-2.3 và Tong Zhang 1.1","Đọc 01_theory_notes.md mục 3 (error decomposition, bias và variance)","Đọc UML 5.2; Nguyễn Thanh Tuấn 12.3","Đọc 01_theory_notes.md mục 4 (PAC, VC-dimension)","Đọc 01_theory_notes.md mục 5 (validation); Shalizi 3.4","Điền và chạy 02_erm_lab.py, ghi câu trả lời vào 03_learning_theory_notes.md","Điền 04_logistic_regression_numpy.py, gradcheck lệch dưới 1e-6, rồi train","Đọc 01_theory_notes.md mục 6-7 (hai model cổ điển, cầu nối sang deep learning)","Hoàn thành 03_learning_theory_notes.md","Tự kiểm tra: giải thích cho Claude vì sao không được chọn model bằng test set"]
 },
 {
  n:4, phase:1, title:"PyTorch core: từ NumPy sang tensor, autograd, training loop", dur:"~10-12 giờ", hw:"RTX 3070 Ti / Mac MPS",
  obj:["Chuyển mọi phép toán NumPy của Phase 0 sang tensor; thêm device và dtype","Hiểu autograd làm gì thay cho gradient viết tay ở Tuần 2-3, và vì sao grad cộng dồn","Nhận ra softmax là pmf và cross-entropy là NLL (Tuần 2), dùng đúng nn.CrossEntropyLoss với logits","Thành thạo nn.Module, optimizer, training loop 5 bước","Viết lại logistic regression Tuần 3 bằng PyTorch, rồi chồng lớp ẩn thành MLP","Xác nhận GPU (torch.cuda.is_available()) / Mac MPS"],
  src:["<b>PyTorch tutorials</b>, Learn the Basics / 60 Minute Blitz","<b>PyTorch docs</b>, Tensor, autograd, nn.Module","Ghi chú Tuần 1-3 để mở lại khi công thức chưa rõ; MML 5.6 về backprop và autodiff","Sách mở: <b>UDL</b> 5.7 cross-entropy, ch.6 optimizers; <b>Fleuret</b> 3.1 losses"],
  deliver:"<code>05_train_mlp.py</code> ba phần: held-out split, logistic regression PyTorch (gradient autograd khớp gradient tay Tuần 3), MLP thắng trên two moons + một câu giải thích; cheat sheet <code>03_math_cheat_sheet.md</code> nối công thức Phase 0 với API PyTorch.",
  know:`<h5>Từ NumPy sang PyTorch: cùng toán, đổi công cụ</h5>
   <p>Tuần 1-3 bạn nhân ma trận, tính gradient tay, viết NLL và gradient descent bằng NumPy. Tuần này <code>torch.tensor</code> thay <code>np.array</code>, <code>loss.backward()</code> thay hàm <code>grad</code> tự viết, <code>optimizer.step()</code> thay <code>w -= lr*grad</code>. Thứ mới duy nhất: PyTorch ghi đồ thị tính toán để đi ngược, và vì thế grad cộng dồn nên cần <code>zero_grad()</code>.</p>
   <h5>Nền toán cho LLM (ôn, đã học Tuần 1-2)</h5>
   <p><b>Dot product</b> đo độ "giống hướng" giữa hai vector, chính là nền của attention score (query · key):</p>
   <div class="formula">\\( \\mathbf{a}\\cdot\\mathbf{b}=\\sum_i a_i b_i \\)</div>
   <p><b>Nhân ma trận</b> <code>C = A@B</code> với <code>A:(m×k)</code>, <code>B:(k×n)</code> → <code>C:(m×n)</code>; một <code>nn.Linear(in,out)</code> thực chất là <code>y = x@Wᵀ + b</code>.</p>
   <h5>Gradient descent & chain rule</h5>
   <div class="formula">\\( w \\leftarrow w - \\eta\\,\\frac{\\partial L}{\\partial w}, \\qquad \\frac{\\partial L}{\\partial w}=\\frac{\\partial L}{\\partial g}\\cdot\\frac{\\partial g}{\\partial w} \\)</div>
   <p>Backprop = áp dụng chain rule lan ngược qua từng layer, nhân dồn các đạo hàm cục bộ.</p>
   <h5>Softmax & cross-entropy</h5>
   <div class="formula">\\( \\text{softmax}(z)_i=\\dfrac{e^{z_i}}{\\sum_j e^{z_j}}, \\quad L_{CE}=-\\sum_i y_i\\log\\hat{y}_i \\)</div>
   <div class="tagrow"><span class="kt">tensor</span><span class="kt">autograd</span><span class="kt">broadcasting</span><span class="kt">softmax</span><span class="kt">cross-entropy</span></div>`,
  check:["Đọc bảng 'Bạn đến đây với gì' trong README; mở lại mục Tuần 1-3 còn mơ hồ","(Tùy chọn) Làm 00_math_bridge.md nếu ký hiệu toán còn lạ","Làm PyTorch tutorial Learn the Basics","Đọc docs autograd + nn.Module","Chạy 01_check_gpu.py → xác nhận CUDA/MPS","Đọc 02_theory_notes.md, chạy lại được mọi snippet","05_train_mlp.py phần 2: logistic regression PyTorch, gradient autograd khớp gradient tay Tuần 3","05_train_mlp.py phần 3: MLP, accuracy held-out cao hơn logistic regression","Viết một câu giải thích vì sao MLP thắng (lớp giả thuyết, Tuần 3)","Hoàn thành 03_math_cheat_sheet.md: công thức, tuần đã học, API PyTorch","Tự kiểm tra: giải thích cho Claude loss.backward() thay cho gì và vì sao zero_grad()"]
 },
 {
  n:5, phase:1, title:"Backprop từ đầu + mental model Transformer", dur:"~12-15 giờ", hw:"3070 Ti / Mac (workload nhẹ)",
  obj:["Mở hộp đen loss.backward() của Tuần 4: tự build autograd engine (micrograd) bằng chain rule Tuần 2","Kiểm micrograd bằng sai phân trung tâm (Tuần 2) rồi mới so PyTorch","Dựng mental model transformer & attention trước khi code","Hiểu vì sao attention permutation-equivariant & cần positional info"],
  src:["Repo mở <b>karpathy/micrograd</b> + <b>karpathy/makemore</b>","<b>The Annotated Transformer</b> (Harvard NLP)","Paper gốc, <b>Attention Is All You Need</b>","Sách mở: <b>UDL</b> 7.4 backprop; <b>Nielsen</b> ch.2; <b>Bishop</b> 5.3"],
  deliver:"Repo <b>micrograd</b> của riêng bạn (<code>02_micrograd.py</code>) + gradient khớp PyTorch; bài viết giải thích permutation-equivariance (<code>05_attention_writeup.md</code>).",
  know:`<h5>Autograd engine, micrograd</h5>
   <p>Mỗi <code>Value</code> lưu <code>data</code>, <code>grad</code>, và một hàm <code>_backward</code>. Forward dựng computation graph; <code>backward()</code> duyệt ngược theo thứ tự topo, áp chain rule. Ví dụ local gradient:</p>
   <div class="formula">\\( z=x\\,y \\Rightarrow \\frac{\\partial z}{\\partial x}=y,\\;\\frac{\\partial z}{\\partial y}=x; \\quad \\tanh'(x)=1-\\tanh^2(x) \\)</div>
   <h5>Vì sao attention "mù" thứ tự</h5>
   <p>Score giữa token i và j chỉ là <code>qᵢ·kⱼ</code>, không chứa thông tin vị trí. <b>Permutation-equivariant</b>: hoán vị input → output hoán vị theo đúng cách đó. Vì <code>W_Q,W_K,W_V</code> dùng chung cho mọi vị trí, model không phân biệt "chó cắn người" vs "người cắn chó" nếu không thêm <b>positional encoding</b>.</p>
   <div class="tagrow"><span class="kt">computation graph</span><span class="kt">topological order</span><span class="kt">chain rule</span><span class="kt">permutation-equivariant</span><span class="kt">positional encoding</span></div>`,
  check:["Đọc 01_theory_notes.md, chạy lại được mọi snippet","Đọc code repo karpathy/micrograd + tự code lại","Tự viết 02_micrograd.py: Value với +, *, tanh/relu, backward()","Kiểm micrograd bằng sai phân trung tâm của Tuần 2 (không cần PyTorch)","Kiểm tra gradient khớp PyTorch (03_check_grad.py)","Đọc repo karpathy/makemore: bigram → MLP","Tự code bigram model (đếm + neural net 1 layer)","Mở rộng makemore lên MLP (Bengio 2003)","Đọc The Annotated Transformer (mental model)","Viết 05_attention_writeup.md → Claude review","Tự kiểm tra: vẽ computation graph + giải thích backward"]
 },
 {
  n:6, phase:1, title:"Tokenization, embeddings, attention từ đầu", dur:"~12-15 giờ (crux khái niệm)", hw:"RTX 3070 Ti",
  obj:["Hiểu & code BPE / data loading, token + positional embeddings","Tự code self-attention → causal → multi-head từng bước"],
  src:["Paper BPE (arXiv 1508.07909) + repo <b>tiktoken</b>/<b>minbpe</b>","<b>nanoGPT</b> model.py, tham chiếu attention","<b>The Annotated Transformer</b> (Harvard NLP)","Sách mở: <b>SLP3</b> 2.4 BPE, 5.4 cosine, 7.1 attention, 7.4 embeddings; <b>UDL</b> 12.2"],
  deliver:"<code>02_multihead_attention.py</code> tự viết, <b>pass shape test</b> (<code>03_test_attention.py</code>) + ghi chú Claude review.",
  know:`<h5>Scaled dot-product attention</h5>
   <div class="formula">\\( \\text{Attention}(Q,K,V)=\\text{softmax}\\!\\left(\\dfrac{QK^{\\top}}{\\sqrt{d_k}}\\right)V \\)</div>
   <p>Chia <code>√dₖ</code> để chống score quá lớn làm softmax bão hòa (gradient triệt tiêu).</p>
   <h5>Causal mask</h5>
   <p>Đặt tam giác trên = <code>-∞</code> trước softmax → token chỉ "nhìn" về quá khứ, đảm bảo tính tự hồi quy.</p>
   <h5>Mốc shape cần nhớ</h5>
   <ul><li>Input embeddings: <code>(batch, seq, d_in)</code></li><li>Q/K/V: <code>(batch, seq, d_out)</code></li><li>Attention scores: <code>(batch, seq, seq)</code></li><li>Multi-head: <code>(batch, heads, seq, head_dim)</code> → gộp <code>(batch, seq, d_out)</code></li></ul>
   <div class="tagrow"><span class="kt">BPE</span><span class="kt">token+pos emb</span><span class="kt">QKV</span><span class="kt">causal mask</span><span class="kt">multi-head</span></div>`,
  check:["Đọc 01_theory_notes.md, chạy lại được mọi snippet","Học BPE (tiktoken), data loader, sliding window","Hiểu token vs positional embedding (cộng vào nhau)","Code simplified self-attention (không trainable)","Code scaled dot-product với W_Q,W_K,W_V trainable","Thêm causal mask (tam giác trên = -inf) + dropout","Mở rộng lên multi-head (chia d_out hoặc stack)","Chạy 03_test_attention.py → shape đúng","Dán code cho Claude review so với nanoGPT"]
 },
 {
  n:7, phase:1, title:"Lắp ráp & chạy mô hình GPT", dur:"~10-12 giờ", hw:"3070 Ti (inference 124M gọn trong 8GB)",
  obj:["Build đầy đủ kiến trúc GPT-2: LayerNorm, GELU FFN, residual, transformer block","Sinh text (ban đầu từ model chưa train)"],
  src:["<b>nanoGPT</b>, model.py + from_pretrained (tham chiếu chính)","Paper <b>GPT-2</b>; LayerNorm (1607.06450), GELU (1606.08415)","Sách mở: <b>SLP3</b> 7.2 Transformer Blocks, 7.5 LM head, 7.6 Decoding; <b>UDL</b> 12.7"],
  deliver:"Mô hình GPT sinh <b>text mạch lạc</b> từ trọng số GPT-2 OpenAI đã load → xác nhận kiến trúc đúng.",
  know:`<h5>Config GPT-2 small (124M)</h5>
   <ul><li><code>vocab_size=50257</code>, <code>context_length=1024</code></li><li><code>emb_dim=768</code>, <code>n_heads=12</code>, <code>n_layers=12</code></li><li><code>drop_rate=0.1</code>, <code>qkv_bias=True</code></li></ul>
   <h5>Các khối lõi</h5>
   <p><b>LayerNorm</b> chuẩn hóa theo feature rồi scale γ + shift β:</p>
   <div class="formula">\\( \\hat{x}=\\dfrac{x-\\mu}{\\sqrt{\\sigma^2+\\epsilon}}\\cdot\\gamma+\\beta \\)</div>
   <p><b>FFN</b>: <code>Linear → GELU → Linear</code> (mở rộng 4×). <b>Pre-LN + residual</b>: <code>x = x + Sublayer(LN(x))</code> giúp gradient ổn định khi xếp chồng nhiều block.</p>
   <div class="tagrow"><span class="kt">LayerNorm</span><span class="kt">GELU</span><span class="kt">FFN 4×</span><span class="kt">residual</span><span class="kt">pre-LN</span><span class="kt">weight loading</span></div>`,
  check:["Đọc 01_theory_notes.md, chạy lại được mọi snippet","Code LayerNorm từ đầu (mean/var, γ scale + β shift)","Code GELU activation","Code FeedForward (Linear→GELU→Linear, 4×)","Ghép MultiHeadAttention vào TransformerBlock + residual + pre-LN","Lắp GPTModel: tok emb + pos emb → N blocks → final LN → out head","Verify số tham số ≈ 124M","Load trọng số GPT-2 OpenAI, map đúng tên layer","Sinh text mạch lạc → xác nhận kiến trúc","Claude review phần load weights (dễ sai mapping)"]
 },
 {
  n:8, phase:1, title:"Pretraining: training loop + 1 lần chạy GPT-2 thật", dur:"~12-15 giờ + thời gian train", hw:"Local 3070 Ti (validate) · Cloud (run thật ~$15-35)",
  obj:["Hiểu pretraining loop, cross-entropy/perplexity, LR scheduling, checkpointing","Thực sự pretrain một model nhỏ"],
  src:["<b>nanoGPT</b> train.py (clipping, LR decay, mixed precision, grad accum)","<b>Karpathy</b> llm.c reproduce GPT-2 (Discussion #481)","<b>HF</b> Ultra-Scale Playbook","Sách mở: <b>SLP3</b> 3.3 perplexity, 7.7 pretraining; <b>Foundations of LLMs</b> 2.2; <b>Fleuret</b> 3.7 scale"],
  deliver:"Checkpoint base-model nhỏ + write-up <b>so sánh loss curve</b> với GPT-2 gốc (<code>04_loss_analysis.md</code>) + pipeline lọc và khử trùng lặp dữ liệu kiểu FineWeb (<code>05_data_dedup.py</code>).",
  know:`<h5>Loss & perplexity</h5>
   <div class="formula">\\( L=-\\dfrac{1}{N}\\sum_t \\log p_\\theta(x_t\\mid x_{<t}), \\quad \\text{PPL}=e^{L} \\)</div>
   <p>GPT-2 gốc đạt val loss ≈ <b>3.5</b>, dùng làm mốc so sánh cho lần chạy của bạn.</p>
   <h5>LR schedule & tricks</h5>
   <p>Warmup tuyến tính → cosine decay. Cộng thêm: gradient clipping, mixed precision (autocast), grad accumulation để đạt effective batch lớn (~524,288 tokens/update kiểu Karpathy), weight tying, weight decay.</p>
   <h5>Bộ nhớ 8GB</h5>
   <p><code>PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True</code> + gradient checkpointing + micro-batch 1-2 + seq ≤1024.</p>
   <p><b>Trigger lên cloud:</b> khi run local dự kiến &gt; ~24h.</p>
   <div class="tagrow"><span class="kt">cross-entropy</span><span class="kt">perplexity</span><span class="kt">warmup+cosine</span><span class="kt">grad accumulation</span><span class="kt">mixed precision</span><span class="kt">checkpointing</span></div>`,
  check:["Đọc 01_theory_notes.md, chạy lại được mọi snippet","Code training loop: batch→logits→CE loss→backward→step","Thêm train/val split + đánh giá loss định kỳ","Thêm LR warmup + cosine decay","Thêm gradient clipping + mixed precision + grad accumulation","Thêm checkpointing (model + optimizer + step)","Smoke test local trên text public-domain nhỏ, loss giảm","Chọn cloud provider + chuẩn bị FineWeb-Edu sample","Chạy pretrain thật trên cloud → lưu checkpoint","Vẽ loss curve, so GPT-2 gốc (~3.5) → 04_loss_analysis.md"]
 },
 {
  n:9, phase:1, title:"Instruction fine-tuning (classification + LoRA)", dur:"~10-12 giờ", hw:"3070 Ti (model nhỏ, LoRA)",
  obj:["Fine-tune classification (ch.6) & instruction-following (ch.7)","Áp dụng LoRA (Appendix E): so sánh với full fine-tuning"],
  src:["Paper <b>LoRA</b> (2106.09685) + <b>InstructGPT</b> (2203.02155)","<b>HF PEFT</b> docs; FareedKhan phần SFT","Sách mở: <b>SLP3</b> 8.1 instruction tuning, 8.2 PEFT; <b>Fleuret</b> 8.3 adapters"],
  deliver:"Mini-model instruction-following chat được + ghi chú so sánh <b>full FT vs LoRA</b>.",
  know:`<h5>Classification head (ch.6)</h5>
   <p>Thay output head (vocab_size) bằng một head nhỏ số lớp = số nhãn; thường chỉ train head + vài layer cuối, dùng hidden state của token cuối.</p>
   <h5>Instruction fine-tuning (ch.7)</h5>
   <p>Dataset cặp (instruction, response) theo Alpaca-style template; <b>mask phần prompt khỏi loss</b> (label = -100) để model học sinh response chứ không học lặp lại đề bài. Cùng cross-entropy như pretraining, thứ đổi là phân phối dữ liệu và hành vi đích.</p>
   <h5>LoRA, fine-tune hiệu quả</h5>
   <p>Thay vì update toàn bộ W, học hai ma trận thấp hạng: <code>W' = W + BA</code> với <code>rank(BA)=r ≪ d</code> → ít tham số, tiết kiệm VRAM. Là nền của QLoRA (Tuần 11).</p>
   <div class="tagrow"><span class="kt">classification head</span><span class="kt">Alpaca template</span><span class="kt">loss masking</span><span class="kt">LoRA</span></div>`,
  check:["Đọc 01_theory_notes.md, chạy lại được mọi snippet","ch.6: chuẩn bị dataset classification (spam) + sửa head","ch.6: fine-tune classifier, đo accuracy train/val/test","ch.7: format instruction dataset (Alpaca-style)","ch.7: instruction fine-tune + sinh phản hồi","Áp dụng LoRA (Appendix E): so full FT vs LoRA","Chat thử với mini-model → ghi ví dụ"]
 },
 {
  n:10, phase:1, title:"Nhập môn alignment: SFT → RM → DPO/PPO → GRPO", dur:"~10-12 giờ", hw:"3070 Ti (scaled-down) · Cloud (full PPO/GRPO)",
  obj:["Hiểu pipeline alignment SFT→RM→PPO/DPO→GRPO (khái niệm)","Chạy ≥1 stage alignment from scratch (SFT hoặc DPO)"],
  src:["<b>FareedKhan-dev</b> src/post_training (SFT/RM/PPO/DPO/GRPO pure PyTorch)","Paper <b>DPO</b> (2305.18290) + <b>DeepSeekMath/GRPO</b> (2402.03300)","Sách mở: <b>SLP3</b> 8.3-8.4; <b>Sutton & Barto</b> 3.1, 13.1, 13.3; <b>Foundations of LLMs</b> 4.3 RLHF, 4.4.2 DPO"],
  deliver:"Log/checkpoint 1 stage alignment đã chạy + ghi chú phân biệt <b>SFT vs DPO vs GRPO</b> (<code>02_alignment_notes.md</code>) + loss DPO tự code qua kiểm tra toy (<code>03_dpo_skeleton.py</code>).",
  know:`<h5>So sánh các stage alignment</h5>
   <ul><li><b>SFT</b>: học bắt chước phản hồi tốt (supervised).</li><li><b>Reward Model</b>: học chấm điểm ưu tiên giữa các cặp output.</li><li><b>DPO</b>: tối ưu trực tiếp từ cặp (chosen, rejected), bỏ qua RM/PPO:</li></ul>
   <div class="formula">\\( L_{DPO}=-\\log\\sigma\\!\\Big(\\beta\\log\\tfrac{\\pi_\\theta(y_w|x)}{\\pi_{ref}(y_w|x)}-\\beta\\log\\tfrac{\\pi_\\theta(y_l|x)}{\\pi_{ref}(y_l|x)}\\Big) \\)</div>
   <p><b>GRPO/PPO</b>: RL tối ưu reward, GRPO dùng nhóm sample thay critic, nền của reasoning model (RLVR = reward kiểm chứng được).</p>
   <h5>Vai trò của KL / reference policy</h5>
   <p>Giữ policy mới không trôi xa bản SFT, chống reward hacking và mất khả năng ngôn ngữ chung.</p>
   <div class="tagrow"><span class="kt">SFT</span><span class="kt">reward model</span><span class="kt">DPO</span><span class="kt">PPO</span><span class="kt">GRPO</span><span class="kt">RLVR</span></div>`,
  check:["Đọc 01_theory_notes.md, tự tính lại được ví dụ loss","Vẽ lại pipeline: Pretrain → (Midtrain) → SFT → RM → PPO/DPO → GRPO/RLVR","Đọc FareedKhan src/post_training, hiểu SFT/RM/DPO","Hiểu loss Reward Model (log-sigmoid hiệu score)","Hiểu vì sao DPO bỏ được RM riêng + dạng loss DPO","Hiểu GRPO group-relative + vì sao hợp RLVR","Chạy MỘT stage alignment (SFT hoặc DPO) scaled-down","Viết 02_alignment_notes.md: SFT vs DPO vs GRPO","So phản hồi trước/sau stage đã chạy → ghi ví dụ"]
 },
 {
  n:11, phase:2, title:"QLoRA fine-tuning thực tế (Unsloth)", dur:"~10-12 giờ", hw:"RTX 3070 Ti / Colab T4 15GB",
  obj:["Fine-tune model 7B-8B thật với 4-bit QLoRA trên 8GB","Hiểu LoRA hyperparams (r, α, target modules) trong thực tế"],
  src:["<b>Unsloth</b> docs (Fine-tuning & LoRA Hyperparameters Guide)","<b>HF</b> PEFT + TRL (SFTTrainer)","<b>NVIDIA</b>, Fine-Tune LLMs on RTX GPUs With Unsloth","Sách mở: <b>Fleuret</b> 8.2 quantization, 8.3 adapters; <b>Foundations of LLMs</b> 5.2"],
  deliver:"Adapter 7B/8B đã fine-tune + <b>eval so base vs fine-tuned</b> trên held-out (<code>03_eval_notes.md</code>).",
  know:`<h5>QLoRA = quantize 4-bit + LoRA</h5>
   <p>Base model nén xuống NF4 4-bit (đóng băng), chỉ train adapter LoRA ở bf16 → 7B vừa ~5GB VRAM.</p>
   <h5>Config cho 8GB</h5>
   <ul><li><code>load_in_4bit=True</code>, <code>batch_size=1-2</code>, <code>seq_len≤1024</code></li><li><code>gradient_checkpointing=True</code></li><li><code>r=16</code>, <code>lora_alpha=16</code>, target tất cả attention + MLP projections</li></ul>
   <h5>Bảng VRAM (Unsloth)</h5>
   <ul><li>7B QLoRA ≈ 5GB · 8B ≈ 6GB → <b>fits</b></li><li>11B ≈ 7.5GB (ở rìa) · 14B ≈ 8.5GB (vượt 8GB)</li></ul>
   <p><b>Threshold:</b> fine-tune &gt;24h hoặc OOM ở batch 1 → chuyển 4090/A100 thuê.</p>
   <div class="tagrow"><span class="kt">QLoRA</span><span class="kt">NF4 4-bit</span><span class="kt">PEFT</span><span class="kt">SFTTrainer</span><span class="kt">GGUF export</span></div>`,
  check:["Đọc 01_theory_notes.md, giải thích được vì sao 8GB fine-tune được 8B","Cài Unsloth + dependencies (CUDA khớp)","Chọn base model (Llama 3.1 8B / Qwen2.5 7B) 4-bit","Chuẩn bị dataset 500-1,000 mẫu (domain Finance Banking)","Cấu hình LoRA (r=16, α=16, target all proj) + SFTTrainer","Smoke test vài step → không OOM, loss giảm","Chạy full run + lưu adapter","Merge adapter + export GGUF (cho Tuần 12)","Eval base vs fine-tuned trên held-out → 03_eval_notes.md"]
 },
 {
  n:12, phase:2, title:"Fine-tuning Mac/MLX + local inference stack", dur:"~8-10 giờ", hw:"MacBook Pro 24GB (unified memory)",
  obj:["Fine-tune 7B-8B với LoRA/QLoRA bằng MLX trên Mac","Dựng local inference stack (Ollama + LM Studio)"],
  src:["<b>mlx-lm</b> docs + mlx_lm.lora","Tùy chọn: MLX LoRA Studio, mlx-tune","<b>Ollama</b>, <b>LM Studio</b>, llama.cpp","Sách mở: <b>Foundations of LLMs</b> 5.1 prefill/decode, 2.3.3.1 KV cache"],
  deliver:"Local inference stack hoạt động + model MLX fine-tune + ghi chú <b>Mac vs 3070 Ti vs cloud</b> (<code>03_hardware_decision.md</code>).",
  know:`<h5>Vì sao Mac cho fine-tuning lớn hơn</h5>
   <p><b>Unified memory 24GB</b> cho phép fine-tune tới ~13-14B (QLoRA ~14-18GB working): vượt giới hạn 8GB của 3070 Ti, đổi lại tốc độ chậm hơn ~2-4× so với NVIDIA.</p>
   <h5>Luồng MLX</h5>
   <ul><li><code>mlx_lm.lora --model ... --train --data ... --iters 500</code></li><li><code>mlx_lm.fuse --model ... --adapter-path ...</code></li><li>Serve qua Ollama (Modelfile) hoặc LM Studio (GGUF & MLX)</li></ul>
   <h5>Phân vai phần cứng</h5>
   <ul><li><b>3070 Ti</b>: QLoRA 7B-8B nhanh, code from-scratch</li><li><b>Mac 24GB</b>: model 13-14B, chạy yên tĩnh local</li><li><b>Cloud</b>: full fine-tune / iterate nhanh</li></ul>
   <div class="tagrow"><span class="kt">MLX</span><span class="kt">unified memory</span><span class="kt">fuse adapter</span><span class="kt">Ollama</span><span class="kt">LM Studio</span></div>`,
  check:["Đọc 01_theory_notes.md, chốt bộ 10 prompt song ngữ trước khi fine-tune","Cài mlx-lm (pip install mlx-lm) trên Mac","Tải model MLX-format (HF mlx-community/...)","LoRA fine-tune: mlx_lm.lora --train --iters 500","Fuse adapter: mlx_lm.fuse","Cài Ollama + Modelfile cho GGUF (Tuần 11) / MLX","Cài LM Studio, load model, test chat","So tốc độ Mac vs 3070 Ti cùng prompt","Viết 03_hardware_decision.md"]
 },
 {
  n:13, phase:2, title:"Xây dựng RAG pipeline end-to-end", dur:"~12 giờ", hw:"Mac / 3070 Ti (embeddings nhẹ)",
  obj:["Build baseline RAG đầy đủ trên corpus tài liệu nghiệp vụ Finance Banking của bạn"],
  src:["Paper gốc <b>RAG</b> (2005.11401)","<b>LlamaIndex</b> + <b>LangChain</b> docs (tutorial RAG chính thức)","GitHub: <b>NirDiamant/RAG_Techniques</b>","Sách mở: <b>SLP3</b> 11.1, 11.3, 11.4 RAG; <b>IR-book</b> 6.2.2 tf-idf, 6.3"],
  deliver:"App RAG trả lời được câu hỏi trên tài liệu Finance Banking của bạn.",
  know:`<h5>Pipeline RAG cơ bản</h5>
   <p><code>Load PDF → chunk → embed → vector store → retrieve top-k → generate</code></p>
   <ul><li><b>Chunking</b>: RecursiveCharacterTextSplitter, size ~800, overlap ~100</li><li><b>Embedding</b>: BGE / e5 / nomic (local) hoặc OpenAI</li><li><b>Vector store</b>: Chroma (dev), pgvector/Qdrant (production)</li><li><b>Generate</b>: Ollama local (Tuần 12) hoặc Claude</li></ul>
   <h5>Retrieval = nearest neighbor theo cosine</h5>
   <div class="formula">\\( \\text{sim}(q,d)=\\dfrac{\\mathbf{q}\\cdot\\mathbf{d}}{\\|\\mathbf{q}\\|\\,\\|\\mathbf{d}\\|} \\)</div>
   <p><b>Anchor:</b> corpus, dataset fine-tune & capstone nên đều là tài liệu nghiệp vụ Finance Banking (giữ tổng quát, không gắn sản phẩm cụ thể): điểm khác biệt của bạn.</p>
   <div class="tagrow"><span class="kt">chunking</span><span class="kt">embeddings</span><span class="kt">Chroma</span><span class="kt">top-k retrieval</span><span class="kt">grounding</span></div>`,
  check:["Đọc 01_theory_notes.md, chạy lại được mọi snippet","Thu thập corpus (PDF tài liệu nghiệp vụ nội bộ) vào data/","Load + parse PDF (PyPDF / Unstructured)","Chunk: RecursiveCharacterTextSplitter (~800, overlap ~100)","Chọn embedding model (BGE/e5/nomic): local","Index vào Chroma (persist xuống đĩa)","Retrieve top-k + lắp prompt context","Generate bằng Ollama (Tuần 12) hoặc Claude","Test 10 câu hỏi domain → kiểm tra grounding","Lưu baseline để so sánh sau khi thêm rerank"]
 },
 {
  n:14, phase:2, title:"Advanced RAG + đánh giá (RAGAS)", dur:"~10-12 giờ", hw:"Local (cross-encoder chạy ổn)",
  obj:["Thêm hybrid search (BM25 + vector) và reranker","Đánh giá định lượng với RAGAS; wire tracing (Langfuse/LangSmith)"],
  src:["<b>RAGAS</b> docs (precision/recall, faithfulness, relevancy)","<b>Langfuse</b> (open source, tracing, LLM-as-judge)","<b>BGE cross-encoder</b> reranker (mã nguồn mở)","Tùy chọn: GraphRAG (Microsoft, repo mở)","Sách mở: <b>IR-book</b> 11.4.3 BM25, 8.3-8.4 evaluation; <b>SLP3</b> 11.2"],
  deliver:"Báo cáo eval RAGAS cho thấy <b>cải thiện relevancy đo được</b> nhờ reranking + pipeline đã trace (<code>03_ragas_report.md</code>).",
  know:`<h5>Hybrid retrieval + rerank</h5>
   <p><b>BM25</b> (lexical) + <b>vector</b> (semantic) kết hợp bằng reciprocal rank fusion → bù điểm yếu của nhau. Sau đó <b>cross-encoder reranker</b> chấm lại top-N để xếp hạng tinh.</p>
   <h5>Bốn metric RAGAS</h5>
   <ul><li><b>Context precision / recall</b>: chất lượng đoạn retrieve được</li><li><b>Faithfulness</b>: câu trả lời có bám context không (chống hallucination)</li><li><b>Answer relevancy</b>: trả lời có đúng trọng tâm câu hỏi</li></ul>
   <h5>Observability</h5>
   <p>Langfuse/LangSmith trace từng bước retrieval → generate, dùng LLM-as-judge để chấm tự động; đo before/after khi thêm rerank.</p>
   <div class="tagrow"><span class="kt">BM25</span><span class="kt">RRF</span><span class="kt">cross-encoder</span><span class="kt">faithfulness</span><span class="kt">tracing</span></div>`,
  check:["Đọc 01_theory_notes.md, tự tính lại được ví dụ RRF","Thêm BM25 retriever (rank_bm25) song song vector","Kết hợp (EnsembleRetriever / reciprocal rank fusion)","Thêm reranker (BGE cross-encoder) trên top-N","Tạo eval set ~20-30 cặp (câu hỏi, ground-truth)","Đo RAGAS: precision/recall, faithfulness, relevancy","So baseline (Tuần 13) vs hybrid+rerank → bảng số","Wire Langfuse/LangSmith tracing","Viết 03_ragas_report.md"]
 },
 {
  n:15, phase:3, title:"Nền tảng agentic: 5 tầng engineering, Claude Agent SDK, MCP", dur:"~12 giờ", hw:"Bất kỳ (API/orchestration)",
  obj:["Nắm 5 tầng: Prompt → Context → Harness → Loop → Graph engineering","Hiểu agent loop, tools, subagents, MCP","Build reflective loop đầu tiên (kiểu Karpathy autoresearch)","Chọn orchestration layer cho CornAgents.AI"],
  src:["<b>Claude Agent SDK</b> docs + Building agents","<b>Model Context Protocol</b> docs (200+ servers)","<code>docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf</code> (mục II, VI.A-B)","<code>docs/5-layers-multi-agent.jpg</code>","<b>LangGraph</b> + <b>CrewAI</b> docs (AutoGen thay thế)","Sách mở: <b>Foundations of LLMs</b> 3.1-3.2 prompting; <b>SLP3</b> 1.8 Agents"],
  deliver:"Single agent + kết nối MCP hoạt động + reflective loop chạy được + sơ đồ kiến trúc CornAgents.AI 1 trang (<code>03_cornagents_architecture.md</code>).",
  know:`<h5>5 tầng engineering</h5>
   <p><b>Prompt</b> (the message) → <b>Context</b> (the memory) → <b>Harness</b> (the machine: gather-act-verify) → <b>Loop</b> (the system: run-check-decide) → <b>Graph</b> (the organization). Mỗi tầng bọc tầng trước; model là commodity, hệ thống quanh nó là engineering.</p>
   <h5>Agent loop</h5>
   <p><code>perceive → reason (LLM) → chọn tool → execute → quan sát kết quả → lặp</code> cho tới khi đạt mục tiêu, trả structured output.</p>
   <h5>Karpathy ratchet loop, 4 điều kiện</h5>
   <p>(1) output <b>verifiable</b>; (2) action <b>reversible</b>; (3) horizon <b>ngắn</b>; (4) environment <b>bounded</b>. Thiếu một cái là loop hỏng.</p>
   <h5>MCP, Model Context Protocol</h5>
   <p>Chuẩn kết nối model ↔ tool/data qua server/client (GitHub, Postgres, Slack, filesystem...). Tách "bộ não" khỏi nguồn dữ liệu.</p>
   <ul><li><b>LangGraph</b>: stateful, auditable → ưu tiên cho regulated finance</li><li><b>CrewAI</b>: prototype nhanh theo role</li></ul>
   <p><b>Metering:</b> từ 15/06/2026 headless Agent SDK trên Pro/Max rút từ pool token tuần riêng.</p>
   <div class="tagrow"><span class="kt">5 layers</span><span class="kt">agent loop</span><span class="kt">ratchet loop</span><span class="kt">MCP</span><span class="kt">LangGraph</span><span class="kt">HITL</span></div>`,
  check:["Đọc 01_theory_notes.md, tự vẽ lại agent loop + 5 tầng","Xem docs/5-layers-multi-agent.jpg, tự vẽ lại 5 tầng bằng lời mình","Đọc Claude Agent SDK docs, agent loop + tool use","Đọc MCP docs, server/client, transport","Build single agent: đọc repo → chạy 1 tool → structured output","Kết nối 1 MCP server (filesystem hoặc GitHub)","Build reflective loop: gen → eval → revise → stop rule","Hiểu 4 điều kiện của ratchet loop (verifiable/reversible/short/bounded)","So sánh LangGraph vs CrewAI cho nhu cầu của bạn","Chọn stack + lý do (regulated → LangGraph)","Vẽ 03_cornagents_architecture.md (sơ đồ + tool boundaries + HITL)"]
 },
 {
  n:16, phase:3, title:"Map LLM vào SDLC; build agent graph CornAgents.AI", dur:"~12-15 giờ", hw:"Bất kỳ (orchestration + API)",
  obj:["Nắm 5 workflow patterns của Anthropic + decision framework 6 câu hỏi","Thiết kế agent chuyên biệt cho requirements→design→code→review→test→docs","Thêm human-in-the-loop gates + artifact contracts"],
  src:["<code>docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf</code> (mục IV patterns, VIII decision framework)","Agentic SDLC: CodeRabbit, Sonar (AC/DC), GlobalLogic (VelocityAI)","Ví dụ code-review của Claude Agent SDK"],
  deliver:"Workflow multi-agent: requirement → <b>stories + design note + tests</b>, có human gate (<code>03_agent_design.md</code>).",
  know:`<h5>5 workflow patterns (Anthropic)</h5>
   <ul><li><b>Prompt Chaining</b>: các bước cố định nối tiếp</li><li><b>Routing</b>: phân loại input → prompt/model chuyên biệt</li><li><b>Parallelization</b>: các call độc lập chạy song song</li><li><b>Orchestrator-Workers</b>: model trung tâm phân rã & giao việc</li><li><b>Evaluator-Optimizer</b>: một bên sinh, một bên chấm theo tiêu chí, lặp</li></ul>
   <h5>Map agent ↔ stage SDLC</h5>
   <ul><li><b>Requirements Analyst</b> (thế mạnh BA): feature request Finance Banking → user story + acceptance criteria, grounded bởi RAG (Tuần 13-14) trên tài liệu nghiệp vụ nội bộ</li><li><b>Code Review agent</b>: đọc diff/PR → criterion-level defects (không "looks good")</li><li><b>Test-Generation agent</b>: từ story/code → sinh test case</li></ul>
   <h5>Nguyên tắc thiết kế</h5>
   <ul><li><b>Least-privilege</b>: mỗi agent chỉ có quyền tool tối thiểu</li><li><b>Human-in-the-loop gate</b> giữa các stage để duyệt</li><li><b>Artifact contract</b>: mỗi handoff là artifact có schema (không phải prose)</li></ul>
   <p>Lưu ý chi phí: multi-agent hơn single agent ở task đa hướng nhưng tốn 10-15× token, cần reducer + budget rõ.</p>
   <div class="tagrow"><span class="kt">5 patterns</span><span class="kt">requirements agent</span><span class="kt">code review</span><span class="kt">test-gen</span><span class="kt">artifact contract</span><span class="kt">HITL gate</span></div>`,
  check:["Đọc 01_theory_notes.md, kể được 5 patterns + ví dụ artifact contract","Đọc mục IV + VIII Karpathy-Loop PDF, 5 patterns + 6 câu hỏi","Map từng stage SDLC ↔ loại agent + pattern + I/O rõ ràng","Agent 1, Requirements Analyst: request → stories + AC (RAG)","Agent 2, Code Review: đọc diff/PR → criterion-level defects","Agent 3, Test-Gen: từ story/code → test case","Định nghĩa artifact contract (schema) cho từng handoff","Nối thành graph (LangGraph state / CrewAI crew)","Thêm human approval gate giữa các stage","Scope tool least-privilege cho từng agent","Chạy thử 1 requirement Finance Banking end-to-end","Ghi 03_agent_design.md"]
 },
 {
  n:17, phase:3, title:"Graph Engineering: Knowledge Graph làm shared memory", dur:"~10-12 giờ", hw:"Bất kỳ (API: Haiku + Sonnet, chi phí thấp)",
  obj:["Xây KG pipeline 4 bước bằng Claude API: extract → resolve → assemble → query","Hiểu 3 vai trò của graph: shared memory, grounding layer, persistent world model","Phân biệt RAG (single-hop) vs Knowledge Graph (multi-hop): bổ trợ nhau","Chạy evaluation feedback loop vs mini gold set"],
  src:["<code>docs/Graph-Engineering-Athropic-Playbook.pdf</code> (pipeline + prompts + eval)","<code>docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf</code> (Loop → Graph)","<b>Anthropic</b> Knowledge Graph Construction Cookbook","<b>NetworkX</b> docs (MultiDiGraph)"],
  deliver:"<code>02_kg_pipeline.py</code> chạy trên corpus của bạn + so sánh grounded vs ungrounded + precision/recall vs gold set (<code>03_graph_notes.md</code>).",
  know:`<h5>Pipeline 4 bước</h5>
   <p><code>Extraction (Haiku + structured outputs) → Resolution (Sonnet cluster) → Assembly (NetworkX MultiDiGraph) → Querying (subgraph k=2 + grounded answer)</code>. Pydantic schema là "training data" duy nhất, đổi domain = đổi schema, không cần label lại.</p>
   <h5>3 vai trò trong multi-agent</h5>
   <ul><li><b>Shared memory</b> (orchestrator-workers): worker đọc/ghi graph, window của orchestrator không phình</li><li><b>Grounding layer</b> (evaluator-optimizer): fact-check claim theo edge có provenance</li><li><b>Persistent world model</b>: "the agent forgets, the graph does not"</li></ul>
   <h5>RAG vs KG</h5>
   <p>RAG: retrieve theo tương đồng, tốt cho single-hop. KG: entity chung = node tường minh nối các tài liệu, multi-hop reasoning bất kể surface form. Dùng cùng nhau.</p>
   <h5>Nguyên tắc chất lượng</h5>
   <ul><li>Descriptions là chìa khoá resolution</li><li>Precision &gt; recall (entity sai lan truyền qua multi-hop)</li><li>Provenance trên mọi edge</li><li>Evaluation feedback loop = "graph autoresearch"</li></ul>
   <div class="tagrow"><span class="kt">structured outputs</span><span class="kt">entity resolution</span><span class="kt">provenance</span><span class="kt">multi-hop</span><span class="kt">grounded answer</span><span class="kt">gold set</span></div>`,
  check:["Đọc 01_theory_notes.md, chạy lại được demo NetworkX","Đọc 2 PDF trong docs/ + ảnh 5 layers","Định nghĩa Pydantic schema: Entity(name, type, description), Relation(s, p, o)","Viết extraction prompt (precision-first: only central entities)","Extraction bằng Haiku trên 5-10 tài liệu domain","Resolution bằng Sonnet: cluster theo type, descriptions làm ngữ cảnh","Assembly: NetworkX MultiDiGraph, edge mang predicate + source_doc","Diagnostics: connected components, degree distribution, edges/nodes","Query: serialize k-hop subgraph (k=2) → grounded answer cite edges","So sánh grounded vs ungrounded trên 3-5 câu hỏi multi-hop","Lập mini gold set + đo precision/recall → tune prompt → đo lại","Cắm graph vào workflow Tuần 16 (shared memory + grounding)","Viết 03_graph_notes.md"]
 },
 {
  n:18, phase:3, title:"Capstone + evaluation/observability", dur:"~12-15 giờ", hw:"Local (sub-model) · API (agent brain)",
  obj:["Ship 1 workflow CornAgents.AI end-to-end, polished, gắn domain, và đánh giá nó"],
  src:["<b>Langfuse/LangSmith</b> (tracing + eval agent)","<b>promptfoo</b> / LLM-as-judge","<code>docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf</code> (mục VII eval + production checklist)","Hiểu biết Phase 1-2 để chọn model"],
  deliver:"Capstone CornAgents.AI demo được + báo cáo evaluation (<code>02_eval_rubric.md</code>) + retrospective nối về Phase 1 (<code>03_retrospective.md</code>).",
  know:`<h5>Use case khuyến nghị</h5>
   <p><b>Spec-to-stories + automated review</b> cho một feature Finance Banking (chọn nghiệp vụ bạn thạo, giữ tổng quát). Kết hợp <b>RAG</b> (grounding) + <b>knowledge graph Tuần 17</b> (shared memory + fact-check) + <b>agents</b> (workflow) + tùy chọn <b>model fine-tuned</b> cho sub-task phân loại hẹp.</p>
   <h5>Chọn model thông minh</h5>
   <p>Claude làm "brain" của agent; một model 7B fine-tuned local (Tuần 11/12) cho sub-task hẹp → tối ưu chi phí/độ trễ.</p>
   <h5>Complexity budget + metric</h5>
   <ul><li>Khai báo trước: max calls, max sub-agents, max tokens/cost, max retries</li><li><b>Success rate</b>: tỉ lệ hoàn thành đúng yêu cầu</li><li><b>Human-override rate</b>: tần suất người phải sửa</li><li><b>Groundedness</b>: bám tài liệu nguồn (chống bịa)</li></ul>
   <p>Thước đo hệ thống đáng tin: <i>"Every important output can be traced to an objective, a plan, an artifact, a source, a graph path, an evaluator decision, and a bounded execution record."</i></p>
   <p>🎓 Đây là mục tiêu thật của cả roadmap, nối ngược về internals Phase 1 để hiểu <i>vì sao</i> nó hoạt động.</p>
   <div class="tagrow"><span class="kt">capstone</span><span class="kt">RAG+KG+agents</span><span class="kt">complexity budget</span><span class="kt">groundedness</span><span class="kt">retrospective</span></div>`,
  check:["Đọc 01_theory_notes.md, điền được assembly map của chính mình","Chốt 1 use case Finance Banking (spec-to-stories + review, giữ tổng quát)","Ghép RAG (Tuần 13-14) + agents (Tuần 16) + KG (Tuần 17) thành 1 luồng","(Tùy chọn) cắm model fine-tuned (Tuần 11/12) cho sub-task","Khai báo complexity budget trước khi chạy","Instrument tracing (Langfuse/LangSmith)","Viết eval rubric → 02_eval_rubric.md","Đo: success rate, human-override rate, groundedness","Kiểm tra 'every output can be traced...' với demo","Demo end-to-end (script / video ngắn)","Viết 03_retrospective.md (nối về Phase 1)"]
 }
];
