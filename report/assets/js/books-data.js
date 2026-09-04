/* Kệ sách nền tảng, window.BOOKS_DATA
   Đồng bộ với docs/books/README.md (license kiểm ngày 2026-09-04). PDF chỉ nằm local, không có trong repo. */
window.BOOKS_DATA = [
  {
    title: "Mathematics for Machine Learning", author: "Deisenroth, Faisal, Ong · 2020 · Cambridge University Press",
    url: "https://mml-book.github.io/", weeks: [1, 2, 3], verified: true,
    license: "PDF miễn phí trên trang sách; bản quyền ghi \"personal use only, not for re-distribution\". Chỉ trích dẫn.",
    read: [
      {week: 1, what: "Ch.2 Linear Algebra (2.4-2.7), Ch.3 Analytic Geometry (3.1, 3.2, 3.4, 3.8), Ch.4 Matrix Decompositions (4.2, 4.5, 4.6). Trang 22-134."},
      {week: 2, what: "Ch.5 Vector Calculus (5.2, 5.3, 5.6), Ch.6 Probability (6.1, 6.3, 6.4, 6.5), Ch.7 Optimization (7.1, 7.3). Trang 141-246."},
      {week: 3, what: "Ch.8 When Models Meet Data (8.1, 8.2, 8.6), Ch.9 Linear Regression (9.2.1). Trang 251-293."}
    ]
  },
  {
    title: "Machine Learning cơ bản", author: "Vũ Hữu Tiệp · bản 27/03/2018",
    url: "https://github.com/tiepvupsu/ebookMLCB", weeks: [1, 2, 3], verified: true,
    license: "CC BY-SA 4.0 theo file LICENSE.md của repo ebookMLCB.",
    read: [
      {week: 1, what: "Ch.1 Ôn tập đại số tuyến tính (1.3, 1.11, 1.13, 1.14). Trang 13-28."},
      {week: 2, what: "Ch.2 Giải tích ma trận (2.1, 2.6), Ch.3 Ôn tập xác suất, Ch.4 MLE và MAP, Ch.12 Gradient descent. Trang 30-63, 140-155."},
      {week: 3, what: "Ch.5 Các khái niệm cơ bản, Ch.7 Linear regression, Ch.8 Overfitting, Ch.14 Logistic regression. Trang 64-100, 165-179."}
    ]
  },
  {
    title: "Deep Learning cơ bản (v2)", author: "Nguyễn Thanh Tuấn · 2019, cập nhật 08/2020",
    url: "https://nttuan8.com/", weeks: [2, 3], verified: false,
    license: "PDF chỉ ghi \"Copyright © 2019 Nguyễn Thanh Tuấn\"; trang sách trả 404 khi kiểm. Dùng đối chiếu cách diễn đạt tiếng Việt.",
    read: [
      {week: 2, what: "3.3 Thuật toán gradient descent, giải thích trực quan trên y = x². Trang 50-55."},
      {week: 3, what: "12.3 Bias và variance. Trang 181-183."}
    ]
  },
  {
    title: "Elementary Probability for Applications (v2.4)", author: "Rick Durrett · 2021",
    url: "https://sites.math.duke.edu/~rtd/EP4A/EP4A.html", weeks: [2], verified: false,
    license: "\"Copyright 2020, All rights reserved\"; tác giả tự đăng bản beta miễn phí, trang không nêu điều khoản.",
    read: [
      {week: 2, what: "1.1.1 tiên đề xác suất (tr. 4), 1.4 biến ngẫu nhiên và kỳ vọng (tr. 15), 4.4 luật số lớn (Thm 4.7, tr. 93), 4.5 định lý giới hạn trung tâm (Thm 4.9, tr. 95), 5.3 công thức Bayes (tr. 118)."}
    ]
  },
  {
    title: "Probability: Theory and Examples (5th ed.)", author: "Rick Durrett · 2019",
    url: "https://sites.math.duke.edu/~rtd/PTE/pte.html", weeks: [2], verified: false,
    license: "\"Copyright 2019, All rights reserved\"; tác giả tự đăng. Mức measure theory, chỉ tra khi cần định nghĩa chặt.",
    read: [{week: 2, what: "Ch.1 Measure Theory, chỉ tra cứu. Trang 1-42."}]
  },
  {
    title: "Advanced Data Analysis from an Elementary Point of View", author: "Cosma Rohilla Shalizi · bản nháp, hợp đồng với Cambridge University Press",
    url: "https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/", weeks: [3], verified: false,
    license: "Trang ghi bản gần cuối \"will remain freely accessible here permanently\"; PDF ghi \"do not distribute without permission\".",
    read: [{week: 3, what: "3.2 Errors, In and Out of Sample; 3.3 Over-Fitting and Model Selection; 3.4 Cross-Validation. Trang 69-89. Thêm 11.2 Logistic Regression, tr. 257."}]
  },
  {
    title: "Understanding Machine Learning: From Theory to Algorithms", author: "Shai Shalev-Shwartz, Shai Ben-David · 2014 · Cambridge University Press",
    url: "https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning", weeks: [3], verified: true,
    license: "Chân trang PDF: \"Personal use only. Not for distribution. Do not post. Please link to ...\". Chỉ link theo yêu cầu tác giả.",
    read: [{week: 3, what: "2.1 A Formal Model (tr. 33), 2.2 ERM (eq. 2.2, tr. 35), 2.3 inductive bias, Def 3.1 PAC (tr. 43), 5.2 Error Decomposition (tr. 64), Def 6.5 VC-dimension (tr. 70), 11.2 Validation (tr. 146)."}]
  },
  {
    title: "Mathematical Analysis of Machine Learning Algorithms", author: "Tong Zhang · bản prepublication · Cambridge University Press",
    url: "https://tongzhang-ml.org/lt-book.html", weeks: [3], verified: true,
    license: "Trang ghi \"free to view and download for personal use only. Not for redistribution or commercial use.\"",
    read: [{week: 3, what: "1.1 Standard Model for Supervised Learning (eq. 1.1, tr. 2), 1.4 Basic Concepts in Generalization Analysis (tr. 5), 3.1 PAC Learning (tr. 29). Sau Tuần 8: 11.7 Double Descent (tr. 245)."}]
  },
  {
    title: "Machine learning with neural networks", author: "Bernhard Mehlig · 2021 · arXiv 1901.05639",
    url: "https://arxiv.org/abs/1901.05639", weeks: [3], verified: true,
    license: "arXiv non-exclusive distribution license (không phải CC); theo chính sách kệ paper thì chỉ link.",
    read: [{week: 3, what: "5.3 Gradient descent for linear units (tr. 79), 6.1 Chain rule and error backpropagation (tr. 91), 6.4 Overfitting and cross validation (tr. 101)."}]
  },
  {
    title: "The Principles of Deep Learning Theory", author: "Daniel A. Roberts, Sho Yaida, với Boris Hanin · 2021 · arXiv 2106.10165",
    url: "https://arxiv.org/abs/2106.10165", weeks: [3, 8], verified: true,
    license: "arXiv non-exclusive distribution license; chỉ link.",
    read: [
      {week: 3, what: "0.1 An Effective Theory Approach (tr. 2), đọc như cầu nối: vì sao lý thuyết học cổ điển chưa đủ cho mạng rất rộng."},
      {week: 8, what: "Ch.1 Pretraining (Gaussian integrals), Ch.2 Neural Networks, Ch.7 Gradient-Based Learning, sau khi đã chạy pretrain thật."}
    ]
  },
  {
    title: "Algorithmic Aspects of Machine Learning", author: "Ankur Moitra · Cambridge University Press",
    url: "https://people.csail.mit.edu/moitra/", weeks: [1, 17], verified: false,
    license: "Trang cá nhân chỉ ghi sách đã xuất bản và cho link PDF; không nêu điều khoản.",
    read: [
      {week: 1, what: "Ch.2 Nonnegative Matrix Factorization (đọc thêm). Trang 7-43."},
      {week: 17, what: "Ch.3-4 Tensor Decompositions, ứng dụng community detection."}
    ]
  },
  {
    title: "Deep Learning on Graphs", author: "Yao Ma, Jiliang Tang · 2021 · Cambridge University Press",
    url: "https://yaoma24.github.io/dlg_book/", weeks: [17], verified: true,
    license: "Trang ghi \"free to view and download for personal use only. Not for re-distribution, re-sale or use in derivative works.\"",
    read: [{week: 17, what: "Ch.2 Foundations of Graphs (2.2 biểu diễn, 2.3 degree, connectivity, centrality, 2.4 spectral graph theory), 10.7 GNN on Knowledge Graphs."}]
  },
  {
    title: "The State of Open Source AI (2023 Edition)", author: "Prem AI và cộng đồng đóng góp",
    url: "https://github.com/premAI-io/state-of-open-source-ai", weeks: [11, 12], verified: true,
    license: "CC-BY-4.0 cho văn bản, Apache-2.0 cho code (file LICENCE). Số liệu là ảnh chụp năm 2023.",
    read: [{week: 11, what: "Ch.1 Licences (1.3 Meaning of \"Open\"), Ch.2 Evaluation & Datasets: bối cảnh licence model mở khi chọn base model để fine-tune."}]
  }
  ,

  {
    title: "Speech and Language Processing (3rd ed. draft)", author: "Daniel Jurafsky, James H. Martin · bản nháp 19/08/2026",
    url: "https://web.stanford.edu/~jurafsky/slp3/", weeks: [3, 6, 7, 8, 9, 10, 13, 14, 15], verified: true,
    license: "PDF ghi \"Copyright ©2026. All rights reserved. Draft\"; trang sách cho phép dùng bản nháp trong lớp học. Không có license mở tường minh, chỉ link.",
    read: [
      {week: 3, what: "Ch.4 Logistic Regression: 4.5 cross-entropy loss (tr. 101), 4.6 gradient descent (tr. 103), 4.10 test sets và cross-validation (tr. 115)."},
      {week: 6, what: "2.4 Byte-Pair Encoding (tr. 42), 5.4 Cosine similarity (tr. 134), 7.1 Attention (tr. 179), 7.4 token và positional embedding (tr. 191)."},
      {week: 7, what: "7.2 Transformer Blocks (tr. 184), 7.5 LM head (tr. 193), 7.6 Decoding (tr. 196)."},
      {week: 8, what: "3.3 Perplexity (tr. 76), 3.7 perplexity và entropy (tr. 85), 7.7 Pretraining Transformer LLMs (tr. 201)."},
      {week: 9, what: "8.1 Instruction Tuning (tr. 210), 8.2 Parameter Efficient Fine Tuning (tr. 213)."},
      {week: 10, what: "8.3 Learning from Preferences (tr. 215), 8.4 Alignment via Preference-Based Learning (tr. 219)."},
      {week: 13, what: "11.1 IR (tr. 254), 11.3 dense vectors và vocabulary mismatch (tr. 264), 11.4 RAG (tr. 267)."},
      {week: 14, what: "11.2 Evaluation of IR systems (tr. 261)."},
      {week: 15, what: "1.8 Agents (tr. 24)."}
    ]
  },
  {
    title: "Foundations of Large Language Models", author: "Tong Xiao, Jingbo Zhu · 2025 · arXiv 2501.09223",
    url: "https://arxiv.org/abs/2501.09223", weeks: [8, 10, 11, 12, 15], verified: false,
    license: "Trang arXiv ghi CC BY 4.0 nhưng trang bản quyền trong PDF ghi CC BY-NC 4.0; hai nguồn mâu thuẫn nên coi là NC, chỉ link.",
    read: [
      {week: 8, what: "2.2 Training at Scale: data preparation, scaling laws (tr. 56)."},
      {week: 10, what: "4.3 RLHF (tr. 172), 4.4.2 Direct Preference Optimization (tr. 193)."},
      {week: 11, what: "5.2 Efficient Inference Techniques: quantization, pruning (tr. 222)."},
      {week: 12, what: "5.1 Prefilling and Decoding (tr. 204), 2.3.3.1 Fixed-size KV Cache."},
      {week: 15, what: "3.1 General Prompt Design (tr. 97), 3.2 Advanced Prompting Methods."}
    ]
  },
  {
    title: "Deep Learning", author: "Ian Goodfellow, Yoshua Bengio, Aaron Courville · 2016 · MIT Press",
    url: "https://www.deeplearningbook.org/", weeks: [4, 5, 8], verified: true,
    license: "Trang sách: bản online miễn phí vĩnh viễn; hợp đồng với MIT Press không cho phát hành PDF. Đọc HTML, trích theo chương và mục.",
    read: [
      {week: 4, what: "Ch.6 Deep Feedforward Networks; Ch.5 Machine Learning Basics (đối chiếu Tuần 3)."},
      {week: 5, what: "6.5 Back-Propagation and Other Differentiation Algorithms."},
      {week: 8, what: "Ch.8 Optimization for Training Deep Models; Ch.3 Probability and Information Theory."}
    ]
  },
  {
    title: "Understanding Deep Learning", author: "Simon J. D. Prince · MIT Press · PDF 02/09/2026 (release v5.0.3)",
    url: "https://udlbook.github.io/udlbook/", weeks: [4, 5, 6, 7, 8], verified: true,
    license: "Trang bản quyền PDF: \"This work is subject to a Creative Commons CC-BY-NC-ND license. (C) MIT Press.\" Chỉ link.",
    read: [
      {week: 4, what: "5.7 Cross-entropy loss (tr. 71); Ch.6 Fitting models: 6.1 GD (tr. 77), 6.2 SGD (tr. 83), 6.4 Adam (tr. 88)."},
      {week: 5, what: "7.4 Backpropagation algorithm (tr. 103), 7.5 Parameter initialization (tr. 107)."},
      {week: 6, what: "12.2 Dot-product self-attention (tr. 208), 12.3 Extensions (tr. 213)."},
      {week: 7, what: "12.4 Transformer layers (tr. 215), 12.7 Decoder model example: GPT3 (tr. 222)."},
      {week: 8, what: "Ch.9 Regularization: 9.2 Implicit regularization (tr. 141)."}
    ]
  },
  {
    title: "Probabilistic Machine Learning: An Introduction", author: "Kevin P. Murphy · 2022 · MIT Press",
    url: "https://probml.github.io/pml-book/book1.html", weeks: [2, 3], verified: true,
    license: "Draft PDF 2025-04-18, CC-BY-NC-ND (trang sách và chân trang PDF). Chỉ link.",
    read: [
      {week: 2, what: "6.1 Entropy (eq. 6.1, tr. 207), 6.2 Relative entropy / KL divergence (tr. 213)."},
      {week: 3, what: "4.3 Empirical risk minimization (eq. 4.60, tr. 115); Ch.10 Logistic Regression (tr. 339)."}
    ]
  },
  {
    title: "Pattern Recognition and Machine Learning", author: "Christopher M. Bishop · 2006 · Springer",
    url: "https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/", weeks: [2, 3, 5], verified: false,
    license: "PDF ghi \"© 2006 Springer ... All rights reserved\"; Microsoft Research đăng công khai. Điều khoản cho phép đăng chưa xác minh. Chỉ link.",
    read: [
      {week: 2, what: "1.6 Information Theory (tr. 48), 1.6.1 relative entropy (tr. 55)."},
      {week: 3, what: "4.3.2 Logistic regression (eq. 4.87, tr. 205), 4.3.4 multiclass (tr. 209)."},
      {week: 5, what: "5.3 Error Backpropagation."}
    ]
  },
  {
    title: "Convex Optimization", author: "Stephen Boyd, Lieven Vandenberghe · 2004 · Cambridge University Press",
    url: "https://web.stanford.edu/~boyd/cvxbook/", weeks: [2], verified: true,
    license: "Trang sách: bản quyền thuộc Cambridge University Press, được phép để sách trên web. Chỉ link.",
    read: [{week: 2, what: "3.1.1 Definition of convex function (eq. 3.1, tr. 67); 1.3 Convex optimization."}]
  },
  {
    title: "Introduction to Information Retrieval", author: "Manning, Raghavan, Schütze · 2008 · Cambridge University Press",
    url: "https://nlp.stanford.edu/IR-book/information-retrieval-book.html", weeks: [13, 14], verified: true,
    license: "PDF là \"Online edition (c) 2009 Cambridge UP\", nhà xuất bản cho đăng bản online. Chỉ link.",
    read: [
      {week: 13, what: "6.2.2 Tf-idf weighting (tr. 118), 6.3 vector space model (tr. 120)."},
      {week: 14, what: "11.4.3 Okapi BM25 (tr. 232), 8.3-8.4 Evaluation of unranked and ranked retrieval (tr. 155-158)."}
    ]
  },
  {
    title: "Reinforcement Learning: An Introduction (2nd ed.)", author: "Richard S. Sutton, Andrew G. Barto · 2018 · MIT Press",
    url: "http://incompleteideas.net/book/the-book-2nd.html", weeks: [10], verified: true,
    license: "Trang bản quyền PDF: CC BY-NC-ND 2.0. Chỉ link.",
    read: [{week: 10, what: "3.1 Agent-Environment Interface (tr. 47), 13.1 Policy Approximation (softmax policy eq. 13.2, tr. 322), 13.3 REINFORCE (tr. 326)."}]
  },
  {
    title: "Information Theory, Inference, and Learning Algorithms", author: "David J. C. MacKay · 2003 · Cambridge University Press",
    url: "http://www.inference.org.uk/mackay/itila/book.html", weeks: [2, 8], verified: false,
    license: "Trang sách: bản quyền Cambridge University Press, tác giả đăng PDF miễn phí. Điều khoản tái phân phối chưa xác minh. Chỉ link.",
    read: [
      {week: 2, what: "2.4 Entropy of an ensemble (eq. 2.35, tr. 32), relative entropy và Gibbs' inequality (eq. 2.45-2.46, tr. 34)."},
      {week: 8, what: "Ch.4 The Source Coding Theorem: nối perplexity với bits per byte."}
    ]
  },
  {
    title: "The Little Book of Deep Learning", author: "François Fleuret · 2023",
    url: "https://fleuret.org/francois/lbdl.html", weeks: [4, 6, 8, 9, 11], verified: true,
    license: "Trang sách: \"distributed under a non-commercial Creative Commons license\". Chỉ link.",
    read: [
      {week: 4, what: "3.1 Losses (tr. 25): cross-entropy từ logit."},
      {week: 6, what: "4.8 Attention layers (tr. 89), 4.9 Token embedding, 4.10 Positional encoding."},
      {week: 8, what: "3.7 The benefits of scale (tr. 51), dẫn Kaplan et al. 2020."},
      {week: 9, what: "8.3 Adapters (tr. 155): LoRA là phương pháp thống trị."},
      {week: 11, what: "8.2 Quantization (tr. 154)."}
    ]
  },
  {
    title: "Neural Networks and Deep Learning", author: "Michael Nielsen · 2015",
    url: "http://neuralnetworksanddeeplearning.com/", weeks: [5], verified: true,
    license: "CC BY-NC 3.0 (trang about). Sách HTML, trích theo chương.",
    read: [{week: 5, what: "Ch.2 How the backpropagation algorithm works: bốn phương trình backprop, đối chiếu với micrograd."}]
  }
];
