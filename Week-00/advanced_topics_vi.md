# Appendix: Kiến thức nâng cao (Gap Analysis)

> Phase 1 và 2 của lộ trình (Tuần 4-18) dựng một model cỡ GPT-2, kiến trúc năm 2019, rồi chuyển sang ứng dụng. Các model mở đang dùng hằng ngày (Llama 3, Qwen3, Mistral, DeepSeek) đã đổi gần hết các thành phần của GPT-2, và các repo huấn luyện hiện đại (nanoGPT, nanochat, FareedKhan) chứa một loạt kỹ thuật train, inference, eval mà bản GPT-2 tối giản không có. File này giải thích từng khoảng cách đó ở mức đủ để bạn đọc paper gốc và đọc code, kèm nguồn cụ thể cho từng khẳng định.
>
> Không đọc file này một lượt. Mỗi tuần mở đúng mục được neo trong bảng dưới; README từng tuần có block "Bổ sung nâng cao" trỏ ngược về đây. Mã mục (A1, B4, I5...) giữ cố định để các tuần tham chiếu được. Bản tiếng Anh: [advanced_topics_en.md](advanced_topics_en.md).
>
> Quy ước nguồn: mọi khẳng định có nguồn được ghi ngay sau câu, dạng (tác giả, arXiv id, mục) hoặc (repo, file). Câu trong ngoặc kép là trích nguyên văn từ PDF hoặc code đã đọc ngày 2026-09-04. Chỗ nào là suy luận của người viết thì mở đầu bằng `[Suy luận]`; chỗ nào chưa kiểm được thì `[Chưa xác minh]`.

**Mục lục**

- [A. Kiến trúc hiện đại: từ GPT-2 đến Llama, Qwen, Mistral, DeepSeek](#a-kiến-trúc-hiện-đại)
- [B. Tối ưu inference](#b-tối-ưu-inference)
- [C. Attention ở quy mô lớn](#c-attention-ở-quy-mô-lớn)
- [D. Training dynamics](#d-training-dynamics)
- [E. Tokenizer: train BPE from scratch](#e-tokenizer-train-bpe-from-scratch)
- [F. Scale và parallelism](#f-scale-và-parallelism)
- [G. Alignment và reasoning](#g-alignment-và-reasoning)
- [H. Evaluation](#h-evaluation)
- [I. Agentic và Graph Engineering (Phase 3)](#i-agentic-và-graph-engineering)
- [J. Inference serving production: vLLM và PagedAttention](#j-inference-serving-production-vllm-và-pagedattention)
- [K. Test-time compute và reasoning model](#k-test-time-compute-và-reasoning-model)
- [L. Multimodal và VLM tổng quan](#l-multimodal-và-vlm-tổng-quan)

---

## Bảng điều hướng: tuần nào đọc mục nào

Năm tuần đầu cố ý không có mục nào: Tuần 1-3 là nền toán và lý thuyết học, Tuần 4-5 là PyTorch và autograd. Mọi chủ đề dưới đây đều cần bạn đã tự viết attention trước đã.

| Tuần | Mục cần đọc | Vì sao đọc lúc này |
|---|---|---|
| 1-5 | *(không)* | Nền toán, PyTorch, autograd. Đọc sách theo trang trong `../docs/books/README.md`. |
| 6: Attention từ đầu | A1-A6, C1-C2, E | Vừa code multi-head attention xong là lúc so RoPE, GQA, MLA với bản của mình thấy rõ nhất. |
| 7: Lắp ráp GPT | A7, B1, B2 | Vừa sinh text xong: hiểu KV cache và sampling ngay trên code của mình. |
| 8: Pretraining | D, D1-D2, F, H (bpb, CORE) | Đang chạy train thật, các can thiệp vào loop mới có nghĩa. |
| 9: Instruction fine-tuning | G (chỉ sơ đồ pipeline) | Định vị instruction FT của bạn là bước SFT trong pipeline lớn. |
| 10: Alignment | G (đầy đủ), K | Tuần alignment. K là mặt inference của cùng bài toán reasoning mà GRPO giải ở mặt training. |
| 11: QLoRA | B4, H | Bật cờ 4-bit thì nên biết NF4, GPTQ, AWQ khác nhau chỗ nào; và cách eval base so với fine-tuned. |
| 12: Mac, MLX, local inference | B1, B3, B4 (GGUF), J | Serving thật: KV cache là nút thắt VRAM, GGUF là định dạng bạn load. J cho thấy serving nhiều người dùng khác gì serving một người. |
| 13: RAG pipeline | B2 | Temperature và top-p quyết định câu trả lời RAG có bịa hay không. |
| 14: Advanced RAG, RAGAS | H (đầy đủ) | Đang đo chất lượng, cần biết cạm bẫy LLM-as-judge trước khi tin số. |
| 15: Nền tảng agentic | I1, I2 | Năm tầng engineering và ratchet loop là nội dung chính của tuần. |
| 16: Agent graph SDLC | I2, I3 | Chọn pattern nào, khi nào tách vai, chi phí bao nhiêu. |
| 17: Graph Engineering | I3, I4 | Scale, storage, monitoring của KG pipeline vừa build. |
| 18: Capstone | H, I4, I5 | Eval, complexity budget, production checklist trước khi ship. |
| Đọc thêm, không neo tuần | L | Multimodal nằm ngoài phạm vi thực hành của lộ trình; đọc ở mức khái niệm khi có người hỏi về tài liệu scan. |

Mục A đến H là chiều sâu cho Phase 1-2 (model internals). Mục I là chiều sâu cho Phase 3, lấy từ hai PDF trong [`../docs/`](../docs/) và tài liệu Anthropic. Mục J đến L là phần mở rộng thêm sau: serving nhiều người dùng, test-time compute, và multimodal ở mức khái niệm.

---

## A. Kiến trúc hiện đại

> Học ở tuần 6-7. Nguồn: RoFormer (Su et al., arXiv 2104.09864); RMSNorm (Zhang và Sennrich, arXiv 1910.07467); GLU Variants (Shazeer, arXiv 2002.05202); GQA (Ainslie et al., arXiv 2305.13245); DeepSeek-V2 (arXiv 2405.04434); Mistral 7B (arXiv 2310.06825); Switch Transformer (Fedus, Zoph, Shazeer, arXiv 2101.03961, JMLR 2022, CC BY 4.0); Mixtral (arXiv 2401.04088); Llama 3 (arXiv 2407.21783, mục 3.2); code `nanochat/gpt.py` (repo karpathy/nanochat, MIT). Tất cả đọc ngày 2026-09-04.

GPT-2 mà bạn lắp ở Tuần 7 gồm: positional embedding học được và cộng vào token embedding, LayerNorm, FFN hai lớp với GELU và chiều ẩn 4d, multi-head attention với Q, K, V riêng cho mỗi head, và bias ở các lớp Linear. Bảng dưới tóm cái gì đã đổi; từng mục con giải thích vì sao.

| Thành phần | GPT-2 (2019) | Model mở 2023-2025 | Nguồn cho cột phải |
|---|---|---|---|
| Vị trí | Learned absolute embedding | RoPE, xoay Q và K theo vị trí | RoFormer; Llama 3 mục 3.2 |
| Normalization | LayerNorm (trừ mean, chia std, có bias) | RMSNorm, không trừ mean, không bias | RMSNorm paper; `nanochat/gpt.py` dùng `F.rms_norm` |
| FFN | Linear, GELU, Linear, ẩn 4d | SwiGLU (gated), ẩn thu lại để giữ số tham số | Shazeer 2020 |
| Attention | MHA | GQA (Llama 3, Mistral, nanochat), MLA (DeepSeek-V2) | GQA paper; Llama 3; Mistral Table 1; DeepSeek-V2 |
| Bias ở Linear | Có | Bỏ | `nanochat/gpt.py` (`bias=False`); `nanoGPT/train.py` (`bias = False`) |
| Phạm vi attention | Toàn bộ ngữ cảnh | Tùy chọn sliding window | Mistral 7B |
| Mật độ | Dense | Tùy chọn MoE | Switch; Mixtral; DeepSeek-V2 |

### A1. RoPE: Rotary Position Embedding

GPT-2 mã hóa vị trí bằng cách cộng một vector học được cho từng vị trí tuyệt đối vào embedding của token. Cách này có hai điểm yếu: model chỉ biết các vị trí đã thấy khi train, và điểm attention giữa hai token không có cách nào "chỉ" phụ thuộc khoảng cách giữa chúng.

RoFormer đề xuất Rotary Position Embedding để giải quyết đúng hai điểm đó. Theo tóm tắt của paper, RoPE "encodes the absolute position with a rotation matrix and meanwhile incorporates the explicit relative position dependency in self-attention formulation" (Su et al., arXiv 2104.09864, abstract). Cơ chế: chia vector query và key thành các cặp chiều (2i, 2i+1), coi mỗi cặp là một số phức, và xoay nó một góc m·θ_i, với m là vị trí token và θ_i là tần số của cặp chiều thứ i. Paper theo Vaswani et al. đặt θ_i = 10000^(−2i/d) (mục 3.4.3 và phần Long-term decay). Khi tính q_m · k_n, hai phép xoay góc mθ_i và nθ_i gộp thành một phép xoay góc (m−n)θ_i, nên tích vô hướng chỉ còn phụ thuộc khoảng cách tương đối m−n. Paper cũng chứng minh tính chất long-term decay: với cách chọn θ_i đó, tích vô hướng giảm dần khi khoảng cách tăng (RoFormer mục 3.4.3).

Ba hệ quả thực hành. Thứ nhất, RoPE áp lên Q và K bên trong attention, không áp lên V và không cộng vào embedding; trong `nanochat/gpt.py`, header file ghi rõ "rotary embeddings (and no positional embeddings)" và hàm `apply_rotary_emb(x, cos, sin)` được gọi trên q và k. Thứ hai, vì vị trí được mã hóa bằng góc quay, người ta có thể đổi tần số cơ sở để kéo dài ngữ cảnh: Llama 3 ghi "We increase the RoPE base frequency hyperparameter to 500,000" (arXiv 2407.21783, mục 3.2), thay cho 10000 của paper gốc. Thứ ba, Jurafsky và Martin xếp RoPE vào mục về input embedding của transformer (SLP3 mục 7.4, trang 191), tức đây đã là kiến thức giáo trình, không còn là mẹo.

Khi tự cài ở Tuần 6: viết một hàm nhận (B, T, H, D) và bảng cos, sin có sẵn cho mọi vị trí; kiểm bằng cách xoay q ở vị trí 5 và k ở vị trí 2, rồi so tích vô hướng với trường hợp vị trí 8 và 5. Hai tích phải bằng nhau tới sai số máy.

#### A1.1. Mở rộng context với RoPE: từ PI qua NTK-aware đến YaRN

> Nguồn: Position Interpolation, Chen et al. 2023 (arXiv [2306.15595](https://arxiv.org/abs/2306.15595), abstract tra 2026-08-16); YaRN, Peng et al. 2023 (arXiv [2309.00071](https://arxiv.org/abs/2309.00071), abstract + full text HTML tra 2026-08-16).

Extrapolation "trần" thất bại vì model chỉ từng thấy các góc quay \(m\theta_i\) với \(m\) trong độ dài train (vd. 0-4095). Cho \(m\) vượt xa mức đó là đưa attention vào vùng góc chưa từng gặp, abstract PI mô tả extrapolation "may lead to catastrophically high attention scores that completely ruin the self-attention mechanism" (điểm attention cao thảm hoạ, phá vỡ cơ chế self-attention).

Ba mức khắc phục, đều xoay quanh câu hỏi **"rescale cái gì"**.

Position Interpolation (PI) rescale *vị trí*. Nó nén tuyến tính chỉ số vị trí \(m \rightarrow m \cdot L/L'\) (\(L\) = độ dài train, \(L'\) = độ dài mới) để mọi vị trí mới rơi ngược vào dải góc đã train, nội suy thay vì ngoại suy. Abstract PI: mở rộng LLaMA lên **32768** token với fine-tune **dưới 1000 bước**, và cận trên của nội suy nhỏ hơn ngoại suy "~600×". Nhược điểm, như paper YaRN chỉ ra, là nén *đều mọi chiều* làm mất thành phần tần số cao, "it removes the high frequency components of RoPE", tức là làm mờ khả năng phân biệt các token *sát nhau*.

NTK-aware scaling rescale *tần số (base)*, và rescale không đều. Thay vì nén mọi chiều cùng hệ số \(s\), nó đổi base \(b \rightarrow b \cdot s^{d/(d-2)}\); full text YaRN: "we spread out the interpolation pressure across multiple dimensions by scaling high frequencies less and low frequencies more" (chiều tần số cao gần như giữ nguyên để không mất chi tiết cục bộ, chiều tần số thấp nén nhiều để phủ được context dài).

YaRN kết hợp **NTK-by-parts** (chọn nội suy theo *từng chiều*, dựa trên tỉ lệ bước sóng/context: chiều tần số cao giữ nguyên, chiều tần số thấp mới nội suy) với **attention temperature scaling** (nhân thêm nhiệt độ \(t\) vào softmax attention, \(\sqrt{1/t}=0.1\ln s + 1\)). Abstract YaRN: cần "10x less tokens and 2.5x less training steps than previous methods" để đạt cùng mức mở rộng context.

Ba cách nằm trên cùng một trục: PI kéo *vị trí* về vùng đã train; NTK-aware kéo *tần số*, và kéo không đều giữa các chiều; YaRN làm việc chọn lọc đó theo từng chiều rồi vá nốt phần softmax. Cả ba đều rẻ vì **không đổi kiến trúc**: chỉ đổi cách tính góc quay RoPE (± một lượng fine-tune nhỏ).

### A2. RMSNorm

LayerNorm chuẩn hóa bằng cách trừ trung bình rồi chia độ lệch chuẩn, sau đó nhân γ và cộng β. Zhang và Sennrich đặt giả thuyết rằng bước trừ trung bình là thừa: "we hypothesize that re-centering invariance in LayerNorm is dispensable and propose root mean square layer normalization, or RMSNorm" (arXiv 1910.07467, abstract). RMSNorm chia vector cho căn của trung bình bình phương các thành phần rồi nhân γ:

$$ \text{RMSNorm}(x) = \frac{x}{\sqrt{\tfrac{1}{d}\sum_i x_i^2 + \epsilon}} \cdot \gamma $$

Paper báo cáo RMSNorm "achieves comparable performance against LayerNorm but reduces the running time by 7%∼64% on different models" (abstract). Con số tùy model và phần cứng của năm 2019, nên đừng kỳ vọng đúng tỉ lệ đó trên máy bạn; điều đáng nhớ là kết luận định tính: bỏ mean-centering không hại chất lượng và rẻ hơn.

nanochat đi xa hơn một bước: `norm(x)` gọi `F.rms_norm(x, (x.size(-1),))` và header ghi "no learnable params in rmsnorm", tức bỏ luôn γ. Đây là quyết định của repo đó, không phải kết luận của paper; khi đọc code Llama trong HF transformers bạn sẽ thấy γ vẫn còn.

### A3. SwiGLU FFN

FFN của Transformer gốc là hai phép nhân ma trận kẹp một hàm phi tuyến: FFN(x) = max(0, xW₁)W₂, và GPT-2 thay ReLU bằng GELU. Shazeer thử thay cặp "Linear rồi activation" bằng Gated Linear Unit: tích theo từng thành phần của hai phép chiếu tuyến tính, một trong hai đi qua hàm kích hoạt. Với Swish làm hàm kích hoạt ta có SwiGLU(x) = Swish_β(xW) ⊗ (xV) (arXiv 2002.05202, eq. 5), và FFN đầy đủ là (Swish(xW) ⊗ xV)W₂. Paper kết luận một số biến thể GLU "yield quality improvements over the typically-used ReLU or GELU activations" (abstract).

Vì FFN kiểu GLU có ba ma trận thay cho hai, Shazeer giữ số tham số và lượng tính toán không đổi bằng cách giảm số đơn vị ẩn d_ff (mục 3 của paper: "we reduce the number of hidden units d_ff"). Đó là lý do trong config Llama, chiều ẩn FFN không phải 4d mà là một số nhỏ hơn; Mistral 7B ghi hidden_dim 14336 với d = 4096, tức 3,5d (Mistral 7B, Table 1). nanochat lại chọn hướng khác, dùng "relu^2 activation in MLP" (header `gpt.py`); cả hai đều là lựa chọn kỹ thuật có thể đo, không có câu trả lời duy nhất.

### A4. GQA và MQA: chia sẻ K, V để thu nhỏ KV cache

Điểm nghẽn của decoding không nằm ở phép nhân mà ở băng thông bộ nhớ. Ainslie et al. mở đầu GQA bằng nhận xét đó: "Autoregressive decoder inference is a severe bottleneck for Transformer models due to the memory bandwidth overhead from loading decoder weights and all attention keys and values at every decoding step" (arXiv 2305.13245, mục 1). Multi-query attention (MQA) của Shazeer 2019 giảm phần K, V bằng cách cho mọi query head dùng chung một key head và một value head, nhưng "can lead to quality degradation and training instability" (cùng mục).

GQA là điểm giữa: chia query head thành g nhóm, mỗi nhóm dùng chung một cặp K, V. Paper mô tả nó là "an interpolation between multi-head and multi-query attention with single key and value heads per subgroup of query heads" và báo "uptrained GQA achieves quality close to multi-head attention while being almost as fast as multi-query attention" (mục 1). Paper còn đề xuất uptraining, chuyển checkpoint MHA có sẵn sang MQA/GQA bằng cách mean-pool các ma trận chiếu K, V rồi train thêm với 5% compute của pretraining gốc (abstract và mục 2.1).

Ba model bạn sẽ gặp đều dùng GQA: Llama 3 dùng "grouped query attention (GQA; Ainslie et al. (2023)) with 8 key-value heads" (arXiv 2407.21783, mục 3.2); Mistral 7B có n_heads 32 và n_kv_heads 8 (Table 1); nanochat có `n_kv_head` trong `GPTConfig` với assert `n_head % n_kv_head == 0` và các lớp `c_k`, `c_v` chiếu ra `n_kv_head * head_dim` chiều (`gpt.py`). Khi tự cài: K và V có ít head hơn Q, và trước khi nhân điểm attention bạn lặp (repeat) mỗi K, V head cho g query head trong nhóm.

### A5. MLA: Multi-head Latent Attention (DeepSeek-V2)

MLA đi hướng khác GQA: thay vì giảm số head K, V, nó nén K và V của mọi head xuống một vector tiềm ẩn chiều thấp bằng "low-rank key-value joint compression" (DeepSeek-V2, arXiv 2405.04434, mục 2.1.2), chỉ lưu vector nén đó trong cache, và chiếu ngược ra K, V đầy đủ khi tính attention. Vì phép chiếu là tuyến tính, phần chiếu có thể gộp vào các ma trận Q và output, nên chi phí thêm nhỏ. Kết quả paper báo: so với DeepSeek 67B, DeepSeek-V2 "reduces the KV cache by 93.3%, and boosts the maximum generation throughput to 5.76 times" (abstract). Model có 236B tham số tổng, 21B kích hoạt mỗi token, ngữ cảnh 128K (abstract).

Nối với Tuần 1: nén hạng thấp ở đây là đúng trực giác SVD ở mục 7 của Tuần 1, áp cho ma trận K, V của một chuỗi thay cho ma trận trọng số như LoRA. Bạn không cần cài MLA trong lộ trình; cần nhận ra nó là cùng một ý toán học xuất hiện lần thứ ba.

### A6. Sliding window attention

Attention đầy đủ tốn O(n²) theo độ dài chuỗi (mục C1). Mistral 7B thu về O(n·W) bằng sliding window attention: "The hidden state in position i of the layer k, h_i, attends to all hidden states from the previous layer with positions between i − W and i" (arXiv 2310.06825, mục 2). Thông tin xa hơn W vẫn tới được nhờ xếp lớp: sau k lớp, một vị trí "can access tokens from the input layer at a distance of up to W × k tokens"; với W = 4096 ở 32 lớp, paper nêu "a theoretical attention span of approximately 131K tokens" (cùng mục). Cửa sổ cố định còn cho phép rolling buffer cache: cache chỉ giữ W cặp K, V, cặp ở bước i ghi vào ô i mod W, nên khi i vượt W thì cache ghi đè và không lớn thêm; paper ghi ở chuỗi 32k điều này "reduces the cache memory usage by 8x, without impacting the model quality" (mục 2, Rolling Buffer Cache). Xiao và Zhu trình bày cùng ý dưới tên fixed-size KV cache với cửa sổ n_c cặp gần nhất (*Foundations of LLMs*, mục 2.3.3.1, trang 72).

#### A6.1. Attention sinks & StreamingLLM: vì sao vài token đầu tiên "thiêng"

> Nguồn: StreamingLLM, Xiao et al. 2023, *Efficient Streaming Language Models with Attention Sinks* (arXiv [2309.17453](https://arxiv.org/abs/2309.17453), abstract tra 2026-08-16).

Cửa sổ trượt "ngây thơ" có một chỗ gãy: khi hội thoại dài vượt kích thước cache và các token *đầu tiên* bị đẩy khỏi KV cache, chất lượng sụp, abstract mô tả window attention thất bại "when the text length surpasses the cache size". Phát hiện của paper: chỉ cần **giữ lại KV của các token đầu tiên** là "will largely recover the performance of window attention", dù các token đó *không quan trọng về ngữ nghĩa*. Paper gọi hiện tượng này là **attention sink**: các token đầu hút một lượng attention lớn bất thường.

[Suy luận] Cách giải thích trực giác (dựa trên lập luận trong paper, không nằm trong abstract): softmax buộc tổng attention = 1, nên khi một head "không cần nhìn đâu cả" nó vẫn phải đổ trọng số đi đâu đó, và chỗ đổ ổn định nhất là các vị trí đầu tiên, vì *mọi* token về sau đều nhìn thấy chúng trong attention nhân quả. Rút chúng khỏi cache là rút mất "chỗ xả" mà model đã học cách dựa vào.

Công thức window + sink của StreamingLLM: KV cache = **vài token sink đầu chuỗi** (giữ cố định) **+ cửa sổ trượt \(w\) token gần nhất**: không cần fine-tune. Abstract: cách này cho model train với attention window hữu hạn "generalize to infinite sequence lengths without any fine-tuning", chạy tới "4 million tokens and more", nhanh hơn baseline sliding-window-có-tính-lại tới **22.2×**. Paper còn ghi nhận: thêm một placeholder token làm sink chuyên dụng ngay từ pretraining giúp streaming tốt hơn nữa. Lưu ý phạm vi: đây là kỹ thuật *streaming/bộ nhớ cache*, không phải mở rộng context "thật", model vẫn không nhớ nội dung đã rơi khỏi cửa sổ (khác với A1.1, nơi model thật sự attend được cả context dài).

### A7. Mixture of Experts

MoE thay FFN dày bằng nhiều FFN (expert) và một router chọn expert cho mỗi token. Switch Transformer tóm gọn lợi ích và cái giá: kết quả là một model kích hoạt thưa với số tham số rất lớn nhưng chi phí tính toán không đổi, và việc dùng rộng bị cản bởi "complexity, communication costs and training instability" (Fedus, Zoph, Shazeer, arXiv 2101.03961, abstract). Đóng góp chính của Switch là đơn giản hóa routing: "route to only a single expert" (k = 1), điều paper cho thấy "preserves model quality, reduces routing computation and performs better" (mục 2.1); và một auxiliary load balancing loss cộng vào loss chính để tránh dồn token vào ít expert (mục 2.2, "A Differentiable Load Balancing Loss").

Hai model mở cho thấy con số cụ thể. Mixtral 8x7B: mỗi lớp có 8 FFN, router chọn 2 cho mỗi token, nên "each token has access to 47B parameters, but only uses 13B active parameters during inference" (arXiv 2401.04088, abstract). DeepSeek-V2: 236B tổng, 21B kích hoạt (arXiv 2405.04434, abstract). Khi đọc số tham số của một model MoE, luôn hỏi hai con số: tổng và kích hoạt; VRAM để load phụ thuộc con số thứ nhất, tốc độ phụ thuộc con số thứ hai.

---

## B. Tối ưu inference

> Học ở tuần 7 (B1, B2), 11 (B4), 12 (B1, B3, B4), 13 (B2). Nguồn: SLP3 mục 7.6 (Jurafsky và Martin, bản nháp 19/08/2026); *Foundations of LLMs* (Xiao và Zhu, arXiv 2501.09223) mục 2.3.3, 5.1, 5.2; Fleuret, *The Little Book of Deep Learning* mục 8.2; Leviathan, Kalman, Matias (arXiv 2211.17192); QLoRA (Dettmers et al., arXiv 2305.14314, PDF trong `../docs/papers/`); GPTQ (Frantar et al., arXiv 2210.17323); AWQ (Lin et al., arXiv 2306.00978); `nanochat/engine.py`.

### B1. KV cache

Sinh text tự hồi quy thêm một token mỗi bước. Nếu bước nào cũng tính lại K và V cho toàn bộ chuỗi thì chi phí mỗi bước là O(n) phép chiếu và tổng cộng O(n²); KV cache lưu K, V của các token đã xử lý, nên mỗi bước chỉ tính K, V cho token mới và attend vào cache. Xiao và Zhu mô tả inference vì thế tách thành hai pha, prefilling tính cache cho prompt và decoding sinh từng token attend vào cache (*Foundations of LLMs*, mục 5.1.2, trang 207).

Cái giá là bộ nhớ. Kích thước cache tỉ lệ với số lớp, số head K, V, chiều head, độ dài chuỗi, và số byte mỗi phần tử, nhân đôi vì có cả K và V:

$$ \text{KV cache} \approx 2 \cdot n_{\text{layers}} \cdot n_{\text{kv\_heads}} \cdot d_{\text{head}} \cdot n_{\text{tokens}} \cdot \text{bytes} $$

`[Suy luận]` Công thức này là đếm trực tiếp số phần tử cần lưu; nó giải thích vì sao GQA (giảm n_kv_heads), MLA (giảm chiều lưu), và sliding window (chặn n_tokens) đều nhắm vào cùng một tích. Với card 8GB, đây là con số bạn nên tính trước khi chọn độ dài ngữ cảnh ở Tuần 12. Leviathan et al. nhắc điểm nền: "inference from large models is often not bottlenecked on arithmetic operations, but rather on memory bandwidth and communication" (arXiv 2211.17192, mục 1); Fleuret nói cùng ý cho single-stream inference (*Little Book*, mục 8.2, trang 154).

### B2. Sampling

Khi có phân phối trên vocab, cách chọn token quyết định phong cách đầu ra. Jurafsky và Martin mô tả greedy là chọn token xác suất lớn nhất; top-k cắt phân phối còn k token lớn nhất rồi chuẩn hóa lại và lấy mẫu, với k = 1 trùng greedy; điểm yếu là k cố định trong khi hình dạng phân phối đổi theo ngữ cảnh. Top-p, còn gọi nucleus sampling theo Holtzman et al. 2020, giữ tập token nhỏ nhất chiếm p phần khối xác suất, nên số ứng viên tự co giãn (SLP3 mục 7.6.4, trang 200). Temperature chia logits cho T trước softmax: T nhỏ hơn 1 làm phân phối nhọn, T lớn hơn 1 làm phẳng.

Cho RAG ở Tuần 13: `[Suy luận]` câu trả lời cần bám tài liệu nên ưu tiên temperature thấp và top-p vừa; nhưng đây là siêu tham số phải đo bằng eval set của Tuần 14, không phải quy tắc.

### B3. Speculative decoding

Ý tưởng: dùng một model nhỏ đề xuất nhiều token, rồi để model lớn kiểm song song trong một lần chạy. Leviathan, Kalman và Matias đặt ra hai quan sát nền: các tác vụ khó "often include easier subtasks that can be approximated well by more efficient models", và bằng speculative execution cùng một phép lấy mẫu mới "we can make exact decoding from the large models faster ... without changing the distribution" (arXiv 2211.17192, abstract). Họ báo tăng tốc 2 đến 3 lần trên T5-XXL "with identical outputs" (abstract). Đây là kỹ thuật phía serving; bạn chỉ cần nắm rằng nó không đổi phân phối đầu ra, khác với quantization.

### B4. Quantization

Tuần 11 bật cờ 4-bit. Bên dưới có bốn thứ khác nhau, hay bị gọi chung là "quantization":

NF4 là kiểu dữ liệu của QLoRA: "4-bit NormalFloat (NF4), a new data type that is information theoretically optimal for normally distributed weights" (Dettmers et al., arXiv 2305.14314, abstract), đi cùng double quantization (quantize cả các hằng số quantization) và paged optimizers. QLoRA "backpropagates gradients through a frozen, 4-bit quantized pretrained language model into Low Rank Adapters" và cho phép fine-tune model 65B trên một GPU 48GB (abstract). Vậy base bị quantize và đóng băng; adapter vẫn ở độ chính xác cao vì nó đang được train.

GPTQ là quantization sau huấn luyện, "a new one-shot weight quantization method based on approximate second-order information", quantize model 175B "in approximately four GPU hours, reducing the bitwidth down to 3 or 4 bits per weight, with negligible accuracy degradation" (Frantar et al., arXiv 2210.17323, abstract).

AWQ xuất phát từ quan sát "not all weights in an LLM are equally important. Protecting only 1% salient weights can greatly reduce quantization error", và để nhận ra kênh quan trọng "we should refer to the activation distribution, not weights"; thay vì trộn độ chính xác, AWQ nhân scale các kênh đó và không cần backpropagation (Lin et al., arXiv 2306.00978, abstract).

GGUF không phải thuật toán mà là định dạng file của dự án llama.cpp, thứ Ollama và LM Studio load ở Tuần 12; Fleuret nhắc llama.cpp là framework post-training quantization cho phần cứng tiêu dùng (*Little Book*, mục 8.2, trang 154). `[Chưa xác minh]` trong phiên này: bảng tên các mức quant trong GGUF (Q4_K_M, Q8_0...), hãy tra docs llama.cpp khi export.

Vì sao 4-bit chạy được: Fleuret giải thích activation là tổng của nhiều số hạng nên sai số quantization được trung bình hóa, và "models quantized down to 6 or 4 bits per parameter exhibit remarkable performance" (mục 8.2, trang 154). Cách đo đúng là perplexity của bản quantize so với bản gốc trên cùng held-out (mục H).

---

## C. Attention ở quy mô lớn

> Học ở tuần 6. Nguồn: FlashAttention (Dao et al., arXiv 2205.14135); PyTorch docs `torch.nn.functional.scaled_dot_product_attention`.

### C1. Vì sao O(n²)

Ma trận điểm QKᵀ có kích thước n × n với n là số token. Dao et al. mở đầu: "the time and memory complexity of self-attention are quadratic in sequence length" (arXiv 2205.14135, abstract). Đây là gốc của mọi kỹ thuật ở mục A6 (giới hạn n), A4 và A5 (giảm phần K, V), và C2 (đổi cách dùng bộ nhớ mà không đổi kết quả).

### C2. FlashAttention

Nhiều phương pháp attention xấp xỉ giảm số phép tính nhưng "often do not achieve wall-clock speedup". Dao et al. cho rằng nguyên lý thiếu là IO-awareness, "accounting for reads and writes between levels of GPU memory", và đề xuất FlashAttention, "an IO-aware exact attention algorithm that uses tiling to reduce the number of memory reads/writes between GPU high bandwidth memory (HBM) and GPU on-chip SRAM" (abstract). Chữ exact quan trọng: kết quả toán học không đổi, chỉ đổi thứ tự tính và nơi lưu tạm. Paper báo 15% tăng tốc đầu cuối trên BERT-large ở độ dài 512 so với kỷ lục MLPerf 1.1 và 3 lần trên GPT-2 ở độ dài 1K (abstract).

Trong PyTorch, `F.scaled_dot_product_attention` chọn backend (trong đó có flash) khi đủ điều kiện về dtype và phần cứng; ở Tuần 6 bạn viết attention thủ công để hiểu, rồi so output với hàm này để kiểm đúng.

---

## D. Training dynamics

> Học ở tuần 8. Nguồn: `nanoGPT/train.py` (repo karpathy/nanoGPT, MIT; đọc ngày 2026-09-04); `nanochat/optim.py`, `nanochat/common.py`, README nanochat; modded-nanogpt (repo KellerJordan/modded-nanogpt, MIT).

Các can thiệp dưới đây đều có trong `nanoGPT/train.py` với giá trị mặc định đọc được từ code:

| Can thiệp | Giá trị mặc định trong `train.py` | Vai trò |
|---|---|---|
| Gradient clipping | `grad_clip = 1.0` | Cắt norm gradient để chặn loss spike |
| Dropout | `dropout = 0.0`, comment "for pretraining 0 is good, for finetuning try 0.1+" | Pretraining một epoch trên dữ liệu lớn ít cần regularization kiểu này |
| Bias | `bias = False` | Bỏ bias trong LayerNorm và Linear |
| Learning rate | `learning_rate = 6e-4`, `warmup_iters = 2000`, `decay_lr = True`, `min_lr = 6e-5` với comment "should be ~= learning_rate/10 per Chinchilla" | Warmup rồi decay; LR là siêu tham số nhạy nhất |
| Weight decay | `weight_decay = 1e-1` | Regularize trọng số ma trận |
| Adam β₂ | `beta2 = 0.95` | Thấp hơn mặc định 0.999 của Adam |
| Mixed precision | `dtype = 'bfloat16'` nếu GPU hỗ trợ, ngược lại `'float16'` "will auto implement a GradScaler" | Nhanh và đỡ VRAM |
| Gradient accumulation | `gradient_accumulation_steps = 5 * 8`, comment "used to simulate larger batch sizes" | Chìa khóa cho card 8GB: effective batch lớn trên VRAM nhỏ |

Weight tying (chia sẻ ma trận embedding và unembedding) nằm trong `nanoGPT/model.py`, dòng `self.transformer.wte.weight = self.lm_head.weight`, đã dẫn ở Tuần 7. Bài học phương pháp luận quan trọng nhất của mục này không nằm trong config: `[Suy luận]` nhiều "cải thiện" khi thay đổi một siêu tham số nằm trong khoảng nhiễu giữa các lần chạy khác seed; nếu bạn không chạy ít nhất hai seed, bạn chưa biết mình thấy tín hiệu hay nhiễu.

### D1. Optimizer: AdamW và Muon

AdamW là mặc định trong nanoGPT. nanochat dùng một optimizer kết hợp: "Usually the embeddings and scalars go into AdamW, and the matrix parameters go into Muon" (`nanochat/optim.py`, docstring đầu file). Muon "adapted and simplified from modded-nanogpt" (MIT) và dùng "Newton-Schulz iteration to compute the zeroth power / orthogonalization of G", tức bản cập nhật ma trận được trực giao hóa trước khi áp; file còn nêu phương án thay thế "Polar Express Sign Method for orthogonalization" và "NorMuon variance reduction" điều chỉnh scale theo từng cột sau trực giao hóa (cùng file). Bạn không cần cài Muon; cần biết vì sao nó chỉ áp cho ma trận hai chiều (trực giao hóa chỉ có nghĩa với ma trận) và vì sao embedding vẫn dùng AdamW.

### D2. Mixed precision và dtype

bf16 là mặc định trên GPU Ampere trở lên; fp16 cần GradScaler chống underflow (comment trong `train.py`). nanochat quản lý dtype tường minh qua `COMPUTE_DTYPE` trong `common.py` (được import vào `optim.py`), và bảng leaderboard của README nanochat ghi lần chạy hạng 2 là "d26 slightly undertrained +fp8" (README, mục Time-to-GPT-2 Leaderboard), tức fp8 đã dùng được trong speedrun trên H100. Trên 3070 Ti bạn chỉ có bf16 hoặc fp16.

---

## E. Tokenizer: train BPE from scratch

> Học ở tuần 6. Nguồn: SLP3 mục 2.4 (trang 42); Sennrich et al. 2015 (arXiv 1508.07909, PDF trong `../docs/papers/`); `nanochat/tokenizer.py`, `scripts/tok_train.py`, `scripts/tok_eval.py`; repo karpathy/minbpe (MIT).

Lộ trình dùng tiktoken có sẵn. Bước sâu hơn là tự train một tokenizer BPE, và lý do không chỉ là học thuật: thí nghiệm ở Tuần 6 cho thấy vocab `gpt2` tốn nhiều token cho tiếng Việt vì không có merge nào cho các cụm có dấu. Jurafsky và Martin định nghĩa tokenization là "the process of segmenting the running input text into tokens" và giải thích vì sao chọn đơn vị cỡ morpheme theo cách data-driven (SLP3 mục 2.4, trang 42). Thuật toán BPE gốc của Sennrich et al. bắt đầu từ ký tự, lặp lại việc đếm cặp kề nhau xuất hiện nhiều nhất và gộp thành ký hiệu mới cho tới khi đủ số merge (arXiv 1508.07909, mục 3.2). Bản byte-level bắt đầu từ 256 byte nên không bao giờ gặp token ngoài vocab; regex split (kiểu GPT-2, GPT-4) tách số, chữ và khoảng trắng trước khi merge để merge không băng qua ranh giới vô nghĩa.

Cách đo tokenizer tốt hay không: compression, số byte mỗi token trên corpus đại diện, và fertility, số token mỗi từ. nanochat có `scripts/tok_train.py` và `scripts/tok_eval.py` cho hai việc này (danh sách file trong repo). Với dự án của bạn, hãy đo trên một mẫu văn bản pháp lý tiếng Việt trước khi quyết định dùng tokenizer nào ở Tuần 11.

---

## F. Scale và parallelism

> Học ở tuần 8. Nguồn: PyTorch docs về DistributedDataParallel và FullyShardedDataParallel; Xiao và Zhu, *Foundations of LLMs* mục 2.2.3 Distributed Training (trang 60); Hugging Face Ultra-Scale Playbook (tài liệu chính thức của HF; `[Chưa xác minh]` trong phiên này vì trang không tải được nội dung).

Có bốn trục để chia việc train khi một GPU không đủ. Data parallelism nhân bản model trên mỗi GPU, mỗi GPU xử lý một phần batch, rồi gộp gradient bằng all-reduce; đây là mức đầu tiên cần biết và là cách nanoGPT chạy multi-GPU qua `torchrun`. Tensor parallelism chia một phép nhân ma trận trong một lớp ra nhiều GPU, cho model không vừa một card. Pipeline parallelism chia model theo lớp thành các giai đoạn nối tiếp. Sharding kiểu ZeRO hay FSDP chia optimizer state, gradient và tham số qua các GPU để giảm bộ nhớ mỗi card. Xiao và Zhu bàn các kỹ thuật này dưới mục Distributed Training của chương về training at scale (*Foundations of LLMs*, mục 2.2.3, trang 60).

Với một GPU 8GB, kỹ thuật bạn dùng thật là gradient accumulation (mục D); data parallelism chỉ xuất hiện khi thuê node nhiều GPU cho lần pretrain. Khi đọc log của một lần chạy phân tán, hai con số cần hiểu là throughput (token mỗi giây) và tỉ lệ FLOP thực dùng so với FLOP lý thuyết của phần cứng, thường gọi là MFU; `[Suy luận]` MFU thấp thường báo hiệu nút thắt ở dữ liệu hoặc giao tiếp, không phải ở phép tính.

---

### F1. ZeRO stages 1/2/3: shard dần từng loại state

DDP có một hạn chế về bộ nhớ: mỗi GPU giữ **bản sao đầy đủ** của model state, params + gradients + optimizer states (với AdamW mixed-precision, optimizer states thường là phần *nặng nhất*). ZeRO (Zero Redundancy Optimizer; Rajbhandari et al. 2019, arXiv 1910.02054, kiểm 2026-09-04) xoá dần sự dư thừa đó, theo 3 stage *cộng dồn*, mỗi stage shard thêm một loại state qua \(N_d\) GPU (số liệu memory-reduction lấy từ paper, tra 2026-08-16):

1. Stage 1, \(P_{os}\), shard **optimizer states** (mỗi GPU giữ \(1/N_d\)); paper: "4x memory reduction, same communication volume as DP", giảm ~4× bộ nhớ, communication không đổi.
2. Stage 2, \(P_{os+g}\), shard thêm **gradients** (reduce-scatter về đúng GPU chịu trách nhiệm update phần param tương ứng); paper: "8x memory reduction, same communication volume as DP".
3. Stage 3, \(P_{os+g+p}\), shard nốt **parameters**: mỗi GPU chỉ giữ mảnh của mình, forward/backward cần lớp nào thì broadcast/gather lớp đó *đúng lúc* rồi thả ra; paper: memory giảm **tuyến tính theo \(N_d\)**, đổi lại "~50% increase in communication volume". Đây là stage duy nhất phá được giới hạn "model phải vừa 1 GPU".

Stage càng cao càng tiết kiệm bộ nhớ nhưng càng tốn communication, nên chọn stage thấp nhất đủ để model vừa máy.

### F2. FSDP: ZeRO-3-style trong PyTorch

**FSDP (FullyShardedDataParallel)** là cách PyTorch tích hợp ý tưởng ZeRO vào core: docs chính thức ([docs.pytorch.org/docs/stable/fsdp.html](https://docs.pytorch.org/docs/stable/fsdp.html), tra 2026-08-16) mô tả `ShardingStrategy.FULL_SHARD` là "Parameters, gradients, and optimizer states are sharded", đúng dáng ZeRO-3; `SHARD_GRAD_OP` chỉ shard gradient + optimizer states (dáng ZeRO-2, docs thậm chí có biến thể tên `_HYBRID_SHARD_ZERO2`); `NO_SHARD` thì hành xử như DDP. Nghĩa là chuyển từ DDP sang FSDP không phải đổi framework, chỉ đổi *chiến lược trải state lên GPU*.

Về kế hoạch hands-on, chủ repo xác nhận 2026-08-16 sẵn sàng thuê GPU cloud, DDP/FSDP hands-on đã được đưa vào Week-08 extension (thuê máy 2×GPU); xem block extension trong README Tuần 8. Ở local 1 GPU 8GB, công cụ chính vẫn là **gradient accumulation** (D); F1-F2 là thứ bạn chạy thật trên máy thuê.

---

## G. Alignment và reasoning

> Học ở tuần 9 (sơ đồ) và 10 (đầy đủ). Nguồn: SLP3 mục 8.1-8.4 (trang 210-223); Sutton và Barto, *RL: An Introduction* mục 3.1, 13.1, 13.3; Xiao và Zhu, *Foundations of LLMs* mục 4.3-4.4; DPO (Rafailov et al., arXiv 2305.18290, PDF trong `../docs/papers/`); DeepSeekMath (Shao et al., arXiv 2402.03300); repo FareedKhan-dev/train-llm-from-scratch `src/post_training/`; nanochat `scripts/chat_sft.py`, `scripts/chat_rl.py`.

Pipeline từ base model tới model biết hội thoại và suy luận:

```
Pretrain → SFT → Reward Model → PPO hoặc DPO → GRPO / RLVR
```

Pretrain là dự đoán token kế (Tuần 8). SFT, hay instruction tuning, là supervised learning trên cặp instruction và response với cùng objective cross-entropy (SLP3 mục 8.1, trang 210; Tuần 9). Từ đây trở đi là học từ sở thích.

Bước tiếp theo là reward model. Thay vì viết ra "câu trả lời tốt là gì", người ta cho người chấm so sánh cặp output, rồi train một model chấm điểm sao cho output được chọn có điểm cao hơn output bị loại (SLP3 mục 8.3, trang 215; FoLLM mục 4.3.2). Xiao và Zhu nêu lý do phải đi đường vòng: "often, humans themselves cannot precisely express their own preferences" (*Foundations of LLMs*, mục 4.3, trang 172).

Với PPO trong RLHF, SLP3 khẳng định các phương pháp alignment hiện nay "are based on a Reinforcement Learning (RL) framework (Sutton and Barto, 1998)" (mục 8.4, trang 219). Policy là LLM, action là token, reward từ reward model, và có thêm ràng buộc KL giữ policy gần model tham chiếu. FoLLM viết hàm mục tiêu dạng advantage: U(τ; θ) = Σ_t log π_θ(a_t|s_t) A(s_t, a_t), với advantage ước lượng bằng TD error và value function train nhờ reward model (mục 4.3.3, eq. 4.39, trang 182). Ghi chú lý thuyết Tuần 10 dẫn đường từ REINFORCE của Sutton và Barto tới công thức này.

Về DPO, Rafailov et al. giới thiệu "a new parameterization of the reward model in RLHF that enables extraction of the corresponding optimal policy in closed form, allowing us to solve the standard RLHF problem with only a simple classification loss"; DPO "is stable, performant, and computationally lightweight, eliminating the need for sampling from the LM during fine-tuning" (arXiv 2305.18290, abstract). Công thức loss đã có ở Tuần 10.

Về GRPO và RLVR, DeepSeekMath giới thiệu GRPO là biến thể của PPO: "GRPO foregoes the critic model, instead estimating the baseline from group scores, significantly reducing training resources" (Shao et al., arXiv 2402.03300, mục 1). Tức là với mỗi prompt sinh một nhóm output, chuẩn hóa reward trong nhóm để làm advantage, không cần value network. Paper báo trên GSM8K từ 82.9% lên 88.2% trong pha RL (cùng mục). RLVR là cách gọi khi reward là thứ kiểm được bằng máy, đáp án toán đúng hay sai, test code pass hay không; paper DeepSeek-R1 trong kệ paper là ví dụ ở quy mô lớn.

`[Chưa xác minh]` Về midtraining: một số pipeline hiện đại chèn một giai đoạn giữa pretrain và SFT để dạy định dạng hội thoại và special token; trong danh sách file của nanochat đọc ngày 2026-09-04 có `chat_sft.py` và `chat_rl.py` nhưng tôi không thấy script tên midtrain, nên không khẳng định cách nanochat gọi bước này.

Code để đối chiếu: `src/post_training/` của FareedKhan có SFT, reward model, PPO, DPO, GRPO bằng PyTorch thuần. Khi đọc, tìm ba chỗ: nơi tính log π_θ(a_t|s_t), nơi tính advantage (từ critic với PPO, từ nhóm với GRPO), và nơi giữ KL với model tham chiếu.

---

## H. Evaluation

> Học ở tuần 8, 11, 14, 18. Nguồn: SLP3 mục 3.3, 3.7, 1.9, 11.6; README nanochat (Time-to-GPT-2 Leaderboard); `nanochat/core_eval.py`, `nanochat/loss_eval.py`; Zheng et al., "Judging LLM-as-a-Judge" (arXiv 2306.05685); IR-book mục 8.

Perplexity là hàm của cross-entropy trên token, chuẩn hóa theo độ dài (SLP3 mục 3.3, trang 76; mục 3.7, trang 85). Vì tính trên token, nó phụ thuộc tokenizer: hai model với vocab khác nhau không so được perplexity với nhau. Bits per byte chia cùng lượng thông tin cho số byte của văn bản thay cho số token, nên so được chéo model; nanochat báo `val_bpb` trên leaderboard thay cho loss thô (README nanochat), và `nanochat/loss_eval.py` là nơi tính. Đây là con số nên dùng khi so lần chạy Tuần 8 với GPT-2.

nanochat đo "time to GPT-2" bằng CORE score theo paper DCLM: "The GPT-2 CORE score is 0.256525" và checkpoint GPT-2 gốc nằm ở hàng 0 của leaderboard với CORE 0.2565 (README nanochat, mục Time-to-GPT-2 Leaderboard); `nanochat/core_eval.py` "Evaluates base model CORE score (DCLM paper)" (README, cây thư mục). Các benchmark quen thuộc như MMLU, ARC, GSM8K, HumanEval là câu hỏi kiến thức, khoa học, toán, code; SLP3 nhắc accuracy trên test set chưa thấy là số đo cơ bản và các benchmark lớn thường dưới dạng câu hỏi (mục 1.9, trang 25).

Về LLM-as-judge, Zheng et al. liệt kê các hạn chế của việc dùng LLM chấm: "position, verbosity, and self-enhancement biases, as well as limited reasoning ability", đồng thời cho thấy judge mạnh như GPT-4 đạt "over 80% agreement" với người, ngang mức người đồng ý với nhau (arXiv 2306.05685, abstract). Hai bài học: dùng được, nhưng phải kiểm position bias bằng cách đảo thứ tự hai câu trả lời, và không tin một chỉ số duy nhất. Paper "Judging the Judges" trong kệ paper đo lại vấn đề này với 13 judge.

Cho RAG, precision và recall trên tập tài liệu lấy về, và precision-recall curve cho kết quả xếp hạng (IR-book mục 8.3-8.4, trang 155-158); exact match và token F1 cho câu trả lời (SLP3 mục 11.6, trang 271). RAGAS ở Tuần 14 là phiên bản dùng LLM chấm của các số đo này.

---

## I. Agentic và Graph Engineering

> Học ở tuần 15-18. Nguồn: [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf), [`../docs/Graph-Engineering-Athropic-Playbook.pdf`](../docs/Graph-Engineering-Athropic-Playbook.pdf), [`../docs/5-layers-multi-agent.jpg`](../docs/5-layers-multi-agent.jpg); Anthropic, *Building Effective AI Agents* và *How we built our multi-agent research system* (anthropic.com/engineering, đọc 2026-09-04); SLP3 mục 1.8.

Phase 1-2 hỏi model hoạt động thế nào. Phase 3 hỏi đặt bộ nhớ và đánh giá ở đâu, vì đó mới là nút thắt khi ghép nhiều lần gọi model thành một hệ thống.

### I1. Năm tầng engineering

Sơ đồ trong `docs/5-layers-multi-agent.jpg` xếp năm tầng, mỗi tầng bọc tầng trước: prompt (thông điệp: vai, chỉ dẫn, ví dụ, định dạng), context (bộ nhớ: chọn gì đưa vào cửa sổ), harness (cỗ máy: gather, act, verify, có retry), loop (hệ thống: chạy, kiểm budget và tiến độ, quyết định tiếp hay dừng), graph (tổ chức: nhiều agent với bộ nhớ chung). Giá trị của bảng phân tầng là chẩn đoán: output sai định dạng là lỗi tầng 1; model không biết thứ nó cần biết là tầng 2; không ai kiểm kết quả là tầng 3; chạy mãi không dừng là tầng 4; các agent lặp lại việc của nhau là tầng 5. Jurafsky và Martin cho định nghĩa nền ở tầng thấp nhất: agent là LLM có thể hành động bằng cách gọi chương trình khác, và "The technical difference is only that the set of actions in the world are added to the set of possible tokens to generate" (SLP3 mục 1.8, trang 24).

### I2. Từ loop đến swarm

Mỗi kiến trúc đưa một nút thắt ra ngoài model: loop đưa việc lặp và đánh giá ra ngoài; chain đưa thứ tự task; swarm đưa tìm kiếm song song và chuyên môn hóa vai; DAG đưa lineage của thí nghiệm; knowledge graph đưa facts chung, provenance và bộ nhớ xuyên phiên (PDF Karpathy-Loop, mục về các kiến trúc).

Ví dụ điển hình là ratchet loop của Karpathy trong autoresearch: inspect, propose, apply, evaluate, giữ nếu metric tốt lên, revert nếu không. PDF ghi lõi code "roughly 630 lines" và một lần chạy dài "executed about 700 experiments in two days" (PDF Karpathy-Loop, mục I.B). Bốn điều kiện để loop đó có nghĩa: output đo được, action đảo được, horizon ngắn để feedback dày, và môi trường hữu hạn. Thiếu điều kiện đầu, agent tối ưu thứ sai; thiếu điều kiện hai, một lỗi phá cả state.

`program.md` là cách viết "chương trình" cho loop bằng ngôn ngữ tự nhiên: khai báo file nào được sửa, metric và hướng tối ưu, budget, quy tắc commit và revert, khi nào gọi người. PDF gọi đây là bước sang Software 3.0 theo cách nói của Karpathy (tài liệu tham khảo [9] của PDF). Một phân biệt hay bị gộp: commit DAG trả lời "cái gì đã thay đổi, thí nghiệm nào là cha", knowledge graph trả lời "thực thể nào tồn tại, liên quan thế nào, nguồn nào chống lưng"; PDF khuyên không đưa knowledge graph vào chỉ vì có thể.

### I3. Năm workflow pattern và chi phí của multi-agent

Anthropic phân biệt workflow, "Systems where LLMs and tools are orchestrated through predefined code paths", với agent, "Systems where LLMs dynamically direct their own processes and tool usage", và kết luận sau khi làm việc với nhiều đội: "the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns" (*Building Effective AI Agents*). Năm pattern: prompt chaining (các bước nối tiếp, bước sau xử lý output bước trước), routing (phân loại input rồi chuyển tới nhánh chuyên biệt), parallelization (chạy song song rồi gộp, gồm sectioning và voting), orchestrator-workers (một model trung tâm chia việc, giao cho worker, tổng hợp), evaluator-optimizer (một bên sinh, một bên chấm và phản hồi, lặp).

Chi phí có số đo. Trong bài về hệ nghiên cứu đa agent, Anthropic báo hệ với Claude Opus 4 làm lead và Claude Sonnet 4 làm subagent "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval", đồng thời "agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats", và "token usage by itself explains 80% of the variance" trong hiệu năng (*How we built our multi-agent research system*). Hệ quả cho thiết kế: tách vai khi bài toán có nhiều hướng độc lập và chuyên môn hóa thêm tín hiệu, và luôn định nghĩa bước gộp (reducer) trước khi fan-out.

PDF Karpathy-Loop mô tả hướng dynamic workflows, trong đó model sinh script orchestration và spawn sub-agent với context tươi, có "hard cap of 1,000 per workflow" (PDF, mục về dynamic workflows); ranh giới trừu tượng dịch lên nhưng người thiết kế vẫn phải định nghĩa objective, phạm vi file, output contract, quyền, chính sách verification, budget và quy tắc rollback. `[Suy luận]` Task cần một mạch tư duy liền, như thiết kế kiến trúc hay viết một văn bản dài, thường tệ hơn khi bị chia thành đơn vị cô lập; và các worker song song có thể mắc cùng một lỗi nếu cùng prompt và cùng bằng chứng, nên reviewer cần prompt và bằng chứng khác.

### I4. Knowledge graph ở quy mô production

Pipeline Tuần 17 chạy trên vài tài liệu, in-memory. Playbook trong `docs/` mô tả điều cần thêm khi lên hàng nghìn tài liệu.

Resolution không thể nhét mọi thực thể vào một prompt. Playbook dùng blocking: gom ứng viên bằng tín hiệu rẻ (trùng token tên, Jaccard trên token, quy tắc) thành các block, rồi để model phân xử trong block; pipeline chạy nguyên trạng trên các block 50 đến 100 ứng viên, và cách kết hợp là "blocking plus expensive LLM arbitration within blocks" (Playbook, mục về scale). Đây là nguyên tắc chung: model cho phần cần phán xét, logic tất định cho phần còn lại.

Storage: NetworkX đủ cho notebook; lên quy mô, Playbook nêu hai đường, graph database hoặc "three Postgres tables" với truy vấn đường đi "implemented as recursive CTEs", và nhấn rằng lựa chọn này không đổi code extraction và resolution (Playbook, mục storage). Hai failure mode Playbook cảnh báo: silent loss, "a raw name left out of every cluster silently vanishes from" kết quả, nên mọi tên phải rơi vào một cluster kể cả cluster một phần tử; và false merge, gộp sai hai thực thể làm mọi truy vấn downstream nhiễm bẩn, nên resolution phải giữ alias, bằng chứng và đảo được. Về monitoring, Playbook nêu extraction rate, số thực thể và quan hệ trích được trên mỗi tài liệu, là tín hiệu đầu tiên để phát hiện corpus lệch domain; và nhắc rằng precision 1.00 chưa chắc tốt, "Perfect precision (1.00) means the extractor is conservative" (Playbook, mục evaluation). Các tín hiệu khác trong mục monitoring của Playbook bạn tự đọc và chọn theo hệ của mình.

### I5. Kỷ luật production

Complexity budget khai báo trước mỗi run: số lần gọi model, số sub-agent, số worker song song, thời gian, token, chi phí, số lần retry, và bằng chứng tối thiểu để được kết thúc. Hết budget thì trả artifact tốt nhất hiện có cùng danh sách việc chưa xử lý và lý do dừng; không che partial failure sau một câu trả lời trôi chảy (PDF Karpathy-Loop, mục VII). Metric bị game là rủi ro cấu trúc của mọi ratchet: loop chỉ cải thiện thứ nó thấy, nên có thể giảm val loss mà tăng chi phí inference hoặc overfit eval set; phải giữ ràng buộc phụ.

Sáu câu hỏi chọn kiến trúc, theo decision framework của PDF: thành công có kiểm được không, không thì đừng bắt đầu bằng autonomy; các bước có ổn định không, có thì chain; subtask có độc lập không, có thì parallelize; có cần giữ nhánh thay thế không, có thì DAG; facts có phải sống qua run không, có thì persist graph thay vì dựa vào transcript; có chịu được chi phí và latency không, đặt budget trước khi thêm worker.

Thước đo cuối cùng, trích PDF Karpathy-Loop:

> *Every important output can be traced to an objective, a plan, an artifact, a source, a graph path, an evaluator decision, and a bounded execution record.*

Khi câu đó đúng với hệ của bạn, loop, swarm, DAG và knowledge graph là các cơ chế ghép được với nhau. Khi nó sai, thêm agent chỉ tăng độ mờ đục. Đây là câu bạn tự kiểm ở Tuần 18.

---

## J. Inference serving production: vLLM và PagedAttention

> Học ở tuần 12 (sau khi đã chạy local inference với Ollama/MLX). Nguồn: paper vLLM, Kwon et al. 2023, *Efficient Memory Management for Large Language Model Serving with PagedAttention* (arXiv [2309.06180](https://arxiv.org/abs/2309.06180), abstract tra 2026-08-16); README chính thức của [vllm-project/vllm](https://github.com/vllm-project/vllm) (Apache 2.0, tra 2026-08-16).

Tuần 12 bạn serve model cho một người dùng, là chính bạn. Serving production là bài toán khác: nhiều request đồng thời, và GPU đắt nên phải chạy đầy tải. Hai kỹ thuật của vLLM dưới đây giải bài toán đó, và cả hai đều xoay quanh KV cache đã học ở B1.

### J1. PagedAttention: KV cache phân trang như virtual memory

Vấn đề: cách cấp phát KV cache "ngây thơ" là dành sẵn **một khối bộ nhớ liền mạch** cho độ dài tối đa của mỗi request, dẫn tới lãng phí lớn vì (a) request thường ngắn hơn nhiều mức tối đa, (b) phân mảnh giữa các request. Paper vLLM lấy cảm hứng từ **bộ nhớ ảo của hệ điều hành**: cắt KV cache thành các **block cố định**, cấp phát block khi cần, và một bảng ánh xạ từ logical sang physical cho phép các block của một chuỗi nằm rải rác. Theo abstract (tra 2026-08-16), cách này giảm lãng phí KV cache và tăng throughput **2-4×** so với các hệ serving cùng thời ở cùng mức latency.

Đừng nhầm với "paged optimizers" của QLoRA (Tuần 11). Hai thứ trùng chữ "paged" nhưng khác hẳn: paged optimizers (Dettmers et al., arXiv [2305.14314](https://arxiv.org/abs/2305.14314), abstract tra 2026-08-16) chuyển **optimizer state** qua lại giữa GPU và CPU RAM để "manage memory spikes" khi *training*; PagedAttention phân trang **KV cache** ngay trong VRAM khi *inference/serving*. Một cái là training-side, một cái là serving-side.

### J2. Continuous batching: throughput vs latency

Batching tĩnh: gom N request thành một batch, chạy đến khi **cả batch** xong mới nhận request mới, nên request ngắn phải chờ request dài, GPU rảnh rỗi vô ích. **Continuous batching** (README vLLM: "continuous batching of incoming requests", tra 2026-08-16): ở *mỗi bước decode*, request nào xong thì rời batch, request mới vào ngay chỗ trống, nên GPU luôn đầy. Đổi lại, continuous batching tối ưu throughput (token mỗi giây của cả hệ thống), còn latency của từng request có thể tăng nhẹ vì phải chia GPU với request khác. Cấu hình tùy bạn ưu tiên cái nào.

### J3. So với Ollama / LM Studio

Ollama/LM Studio (backend llama.cpp) tối ưu cho **single-user local**: load GGUF, một request một lúc, chạy được trên CPU/GPU consumer, đúng cái bạn cần ở Tuần 12. vLLM tối ưu cho **multi-user trên GPU server**: PagedAttention + continuous batching chỉ phát huy khi có nhiều request đồng thời. [Suy luận] Với lộ trình này bạn không cần dựng vLLM thật; cái cần mang theo là cách đặt câu hỏi: khi ai đó nói "serve model cho cả team", bạn biết bài toán đổi từ "VRAM có đủ không" (B1) sang "GPU có chạy đầy tải không" (J2) và "KV cache có lãng phí không" (J1).

## K. Test-time compute và reasoning model

> Học ở tuần 10 (ngay sau G, GRPO/RLVR). Nguồn: self-consistency, Wang et al. 2022 (arXiv [2203.11171](https://arxiv.org/abs/2203.11171)); s1, Muennighoff et al. 2025 (arXiv [2501.19393](https://arxiv.org/abs/2501.19393)); DeepSeek-R1 (arXiv [2501.12948](https://arxiv.org/abs/2501.12948): đã có trong [`../docs/papers/README.md`](../docs/papers/README.md), neo Tuần 10). Tất cả abstract tra 2026-08-16.

Tuần 10 dạy trục training-side: đổ compute vào lúc huấn luyện (RM, DPO, GRPO) để model tốt hơn. Trục thứ hai là inference-side: chi thêm compute lúc suy luận cho cùng một model để ra đáp án tốt hơn. Hai trục bổ sung nhau, và reasoning model là chỗ chúng gặp nhau.

### K1. CoT sampling + self-consistency

Thay vì decode greedy một chuỗi suy luận (chain-of-thought), **sample nhiều chuỗi suy luận** (temperature > 0) rồi **vote đáp án cuối**: abstract của Wang et al.: "samples a diverse set of reasoning paths instead of only taking the greedy one, and then selects the most consistent answer". Điều kiện áp dụng: đáp án cuối phải **so sánh được bằng máy** (con số, đáp án trắc nghiệm): cùng họ điều kiện với RLVR.

### K2. Best-of-N + verifier

Sinh N câu trả lời, cho một **verifier** chấm, giữ câu điểm cao nhất. Verifier có thể là Reward Model (đúng RM bạn học ở G/Tuần 10, dùng ở inference thay vì training) hoặc verifier tất định (chạy test, so đáp số). So với K1: self-consistency vote theo *đa số*, best-of-N tin *một giám khảo*.

### K3. Budget forcing (s1)

Kiểm soát trực tiếp lượng "thinking" của reasoning model: abstract s1 mô tả "budget forcing to control test-time compute by forcefully terminating the model's thinking process or lengthening it", tức là cắt sớm hoặc ép nghĩ thêm, và abstract báo cáo cách này giúp model 32B của họ vượt o1-preview trên benchmark toán thi đấu (tra 2026-08-16). Nghĩa là test-time compute là một trục có thể điều khiển, không phải hộp đen.

### K4. DeepSeek-R1: nơi hai trục gặp nhau

Abstract R1: khả năng reasoning "can be incentivized through pure reinforcement learning (RL), obviating the need for human-labeled reasoning trajectories", chính là GRPO/RLVR của G chạy ở quy mô thật. Có thể đọc R1 như sau: RLVR (training-side) huấn luyện model tự sinh chuỗi suy luận dài, tức là đưa test-time compute vào trong model thay vì dựng scaffold bên ngoài như K1 và K2. Sau R1, hai trục không còn tách rời: train để model *biết* nghĩ dài, rồi điều tiết *nghĩ bao lâu* bằng budget (K3).

## L. Multimodal và VLM tổng quan

> Không neo tuần, **đọc thêm, ngoài phạm vi hands-on của lộ trình** (lộ trình này thuần text). Nguồn: CLIP, Radford et al. 2021 (arXiv [2103.00020](https://arxiv.org/abs/2103.00020)); LLaVA, Liu et al. 2023 (arXiv [2304.08485](https://arxiv.org/abs/2304.08485)). Abstract tra 2026-08-16.

Tài liệu ngân hàng thật có bảng scan, con dấu và chữ ký, nên sớm muộn sẽ có người hỏi vì sao không dùng model đọc được ảnh. Mục này cho đủ vốn từ để trả lời câu đó, không hơn.

### L1. CLIP: contrastive pretraining

Train **hai encoder** (ảnh và text) sao cho embedding của một ảnh và caption *đúng* của nó gần nhau, còn các cặp *sai* xa nhau (contrastive). Abstract: train trên **400 triệu cặp (ảnh, text)** thu từ internet, và model transfer zero-shot sang nhiều task qua prompt ngôn ngữ tự nhiên (tra 2026-08-16). CLIP cho một không gian embedding chung cho ảnh và text. [Suy luận] Đó là nền của phần lớn VLM sau này; LLaVA ở L2 là một ví dụ.

### L2. Kiến trúc VLM phổ biến: vision encoder + projector + LLM

Công thức LLaVA (abstract: "connects a vision encoder and LLM"): lấy **vision encoder** đã train sẵn (thường là phía ảnh của CLIP), nối vào một **projector** (phép chiếu học được) map đặc trưng ảnh thành chuỗi "token thị giác" nằm trong không gian embedding của LLM, rồi LLM đọc chuỗi trộn [token ảnh + token text] như thường. [Suy luận] Cái hay của công thức này là *tái dùng* hai model đã train riêng, chỉ học lớp nối ở giữa, rẻ hơn nhiều so với train multimodal from scratch; đó là lý do nó phổ biến.

### L3. Vì sao OCR pipeline ở prerequisites KHÔNG phải multimodal modeling

OCR pipeline đi từ ảnh sang *text* (bước OCR tất định), rồi model **chỉ thấy text**. VLM: biểu diễn ảnh đi **thẳng vào model**, không qua bước chuyển chữ. Khác biệt hệ quả: OCR làm mất layout/hình/con dấu nhưng đơn giản, debug được từng bước, và mọi thứ downstream (RAG, KG) vẫn là bài text bạn đã học; VLM giữ được thông tin thị giác nhưng kéo theo cả một stack train/eval khác. [Suy luận] Với dự án học thuật 1-GPU-8GB này, OCR-rồi-text là lựa chọn đúng; VLM chỉ đáng cân nhắc khi thông tin *thị giác* (vị trí chữ ký, cấu trúc bảng phức tạp) thật sự quyết định đáp án.

## Ưu tiên nếu thời gian hẹp

Bắt buộc: KV cache (B1), RoPE (A1), RMSNorm và SwiGLU (A2, A3), GQA (A4), gradient accumulation (D), bits per byte (H); với Phase 3: năm tầng (I1), bốn điều kiện của ratchet loop (I2), complexity budget (I5). Nên có: MoE (A7), quantization internals (B4), Muon (D1), pipeline alignment đầy đủ (G), train BPE (E), năm workflow pattern (I3), blocking và incremental update cho KG (I4). Để dành: MLA (A5), sliding window (A6), speculative decoding (B3), tensor và pipeline parallelism (F), dynamic workflows quy mô lớn (I3). Nên có, sau G và B1: serving production với vLLM (J) và test-time compute (K); đọc khi cần: tổng quan multimodal (L).
