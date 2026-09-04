# Appendix: Advanced Topics (Gap Analysis)

> **Why this file exists.** Phases 1 and 2 of the roadmap (Weeks 4-18) build a GPT-2-class model, a 2019 architecture, and then move on to applications. The open models people use today (Llama 3, Qwen3, Mistral, DeepSeek) have replaced almost every GPT-2 component, and modern training repos (nanoGPT, nanochat, FareedKhan) contain training, inference and evaluation techniques that a minimal GPT-2 does not have. This file explains each gap in enough depth to read the original paper and the code, with a concrete source for every claim.
>
> **How to use it.** Do not read it in one pass. Each week, open the sections anchored in the table below; each week's README has an "Advanced additions" block pointing back here. Section codes (A1, B4, I5...) are stable so weeks can reference them. Vietnamese version: [advanced_topics_vi.md](advanced_topics_vi.md).
>
> **Source convention.** Every sourced claim is followed by (author, arXiv id, section) or (repo, file). Quoted text is verbatim from PDFs or code read on 2026-09-04. The author's own reasoning starts with `[Inference]`; anything not checked starts with `[Unverified]`.

**Contents**

- [A. Modern architecture: from GPT-2 to Llama, Qwen, Mistral, DeepSeek](#a-modern-architecture)
- [B. Inference optimization](#b-inference-optimization)
- [C. Attention at scale](#c-attention-at-scale)
- [D. Training dynamics](#d-training-dynamics)
- [E. Tokenizer: training BPE from scratch](#e-tokenizer-training-bpe-from-scratch)
- [F. Scale and parallelism](#f-scale-and-parallelism)
- [G. Alignment and reasoning](#g-alignment-and-reasoning)
- [H. Evaluation](#h-evaluation)
- [I. Agentic and Graph Engineering (Phase 3)](#i-agentic-and-graph-engineering)
- [J. Production inference serving: vLLM and PagedAttention](#j-production-inference-serving-vllm-and-pagedattention)
- [K. Test-time compute and reasoning models](#k-test-time-compute-and-reasoning-models)
- [L. Multimodal and VLM overview](#l-multimodal-and-vlm-overview)

---

## Navigation: which week reads which section

The first five weeks deliberately have no sections: Weeks 1-3 are math and learning theory, Weeks 4-5 are PyTorch and autograd. Every topic below assumes you have already written attention yourself.

| Week | Sections | Why now |
|---|---|---|
| 1-5 | *(none)* | Math, PyTorch, autograd. Read the books by page in `../docs/books/README.md`. |
| 6: Attention from scratch | A1-A6, C1-C2, E | Right after coding multi-head attention is when RoPE, GQA and MLA are easiest to compare with your own code. |
| 7: Assembling GPT | A7, B1, B2 | Right after generating text: understand the KV cache and sampling on your own code. |
| 8: Pretraining | D, D1-D2, F, H (bpb, CORE) | You are running a real training loop; the interventions now mean something. |
| 9: Instruction fine-tuning | G (pipeline diagram only) | Place your instruction FT as the SFT step of the larger pipeline. |
| 10: Alignment | G (full), K | The alignment week. K is the inference side of the same reasoning problem that GRPO solves on the training side. |
| 11: QLoRA | B4, H | If you turn on the 4-bit flag you should know how NF4, GPTQ and AWQ differ, and how to evaluate base versus fine-tuned. |
| 12: Mac, MLX, local inference | B1, B3, B4 (GGUF), J | Real serving: the KV cache is the VRAM bottleneck, GGUF is the format you load. J shows how serving many users differs from serving one. |
| 13: RAG pipeline | B2 | Temperature and top-p decide whether a RAG answer fabricates. |
| 14: Advanced RAG, RAGAS | H (full) | You are measuring quality; know the LLM-as-judge pitfalls before trusting numbers. |
| 15: Agentic foundations | I1, I2 | The five engineering layers and the ratchet loop are the week's content. |
| 16: Agent graph for the SDLC | I2, I3 | Which pattern, when to split roles, at what cost. |
| 17: Graph Engineering | I3, I4 | Scale, storage and monitoring of the KG pipeline you just built. |
| 18: Capstone | H, I4, I5 | Evaluation, complexity budget and production checklist before shipping. |
| Further reading, not tied to a week | L | Multimodal is outside the hands-on scope of the roadmap; read it at concept level when someone asks about scanned documents. |

Sections A to H are depth for Phases 1-2 (model internals). Section I is depth for Phase 3, taken from the two PDFs in [`../docs/`](../docs/) and Anthropic's documentation. Sections J to L are later extensions: serving for many users, test-time compute, and multimodal at concept level.

---

## A. Modern architecture

> **Week** 6-7. **Sources:** RoFormer (Su et al., arXiv 2104.09864); RMSNorm (Zhang and Sennrich, arXiv 1910.07467); GLU Variants (Shazeer, arXiv 2002.05202); GQA (Ainslie et al., arXiv 2305.13245); DeepSeek-V2 (arXiv 2405.04434); Mistral 7B (arXiv 2310.06825); Switch Transformer (Fedus, Zoph, Shazeer, arXiv 2101.03961, JMLR 2022, CC BY 4.0); Mixtral (arXiv 2401.04088); Llama 3 (arXiv 2407.21783, section 3.2); `nanochat/gpt.py` (karpathy/nanochat, MIT). All read on 2026-09-04.

The GPT-2 you assemble in Week 7 has learned positional embeddings added to the token embedding, LayerNorm, a two-layer FFN with GELU and a 4d hidden size, multi-head attention with separate Q, K, V per head, and bias in the Linear layers. The table summarizes what changed; the subsections explain why.

| Component | GPT-2 (2019) | Open models 2023-2025 | Source for the right column |
|---|---|---|---|
| Position | Learned absolute embedding | RoPE, rotating Q and K by position | RoFormer; Llama 3 section 3.2 |
| Normalization | LayerNorm (subtract mean, divide by std, bias) | RMSNorm, no mean subtraction, no bias | RMSNorm paper; `nanochat/gpt.py` uses `F.rms_norm` |
| FFN | Linear, GELU, Linear, hidden 4d | SwiGLU (gated), hidden size reduced to keep parameter count | Shazeer 2020 |
| Attention | MHA | GQA (Llama 3, Mistral, nanochat), MLA (DeepSeek-V2) | GQA paper; Llama 3; Mistral Table 1; DeepSeek-V2 |
| Linear bias | Yes | Removed | `nanochat/gpt.py` (`bias=False`); `nanoGPT/train.py` (`bias = False`) |
| Attention span | Full context | Optional sliding window | Mistral 7B |
| Density | Dense | Optional MoE | Switch; Mixtral; DeepSeek-V2 |

### A1. RoPE: Rotary Position Embedding

GPT-2 encodes position by adding a learned vector for each absolute position to the token embedding. Two weaknesses: the model only knows positions seen in training, and the attention score between two tokens has no way to depend only on their distance.

RoFormer proposes Rotary Position Embedding for exactly these two points. Per the abstract, RoPE "encodes the absolute position with a rotation matrix and meanwhile incorporates the explicit relative position dependency in self-attention formulation" (Su et al., arXiv 2104.09864, abstract). Mechanism: split the query and key vectors into pairs of dimensions (2i, 2i+1), treat each pair as a complex number, and rotate it by the angle m·θ_i, where m is the token position and θ_i the frequency of pair i. Following Vaswani et al., the paper sets θ_i = 10000^(−2i/d) (section 3.4.3 and the long-term decay discussion). When computing q_m · k_n, the two rotations by mθ_i and nθ_i combine into a single rotation by (m−n)θ_i, so the dot product depends only on the relative distance m−n. The paper also proves long-term decay: with this choice of θ_i the dot product decays as the distance grows (RoFormer section 3.4.3).

Three practical consequences. First, RoPE applies to Q and K inside attention, not to V and not to the embedding; the header of `nanochat/gpt.py` says "rotary embeddings (and no positional embeddings)" and `apply_rotary_emb(x, cos, sin)` is called on q and k. Second, because position is encoded as an angle, the base frequency can be changed to stretch context: Llama 3 states "We increase the RoPE base frequency hyperparameter to 500,000" (arXiv 2407.21783, section 3.2), versus 10000 in the original paper. Third, Jurafsky and Martin place RoPE in their section on transformer input embeddings (SLP3 section 7.4, page 191), so this is textbook material now, not a trick.

When implementing in Week 6: write a function taking (B, T, H, D) plus precomputed cos and sin tables for all positions; test it by rotating q at position 5 and k at position 2, then comparing the dot product with the case of positions 8 and 5. The two must match to machine precision.

#### A1.1. Context extension with RoPE: Position Interpolation, NTK-aware scaling, YaRN

> **Sources:** Position Interpolation, Chen et al. 2023 (arXiv [2306.15595](https://arxiv.org/abs/2306.15595), abstract looked up 2026-08-16); YaRN, Peng et al. 2023 (arXiv [2309.00071](https://arxiv.org/abs/2309.00071), abstract and full-text HTML looked up 2026-08-16).

Plain extrapolation fails for a simple reason. The model has only ever seen rotation angles m·θ_i with m inside the training length (for example 0-4095). Pushing m far beyond that range sends attention into angles it has never met; the PI abstract describes extrapolation as something that "may lead to catastrophically high attention scores that completely ruin the self-attention mechanism".

There are three levels of fix, and all of them turn on the question of what to rescale.

Position Interpolation (PI) rescales the position. It linearly compresses the position index m to m·L/L' (L the training length, L' the new length) so that every new position falls back inside the range of angles seen in training: interpolation instead of extrapolation. The PI abstract reports extending LLaMA to 32768 tokens with fine-tuning of under 1000 steps, and that the upper bound of interpolation is smaller than that of extrapolation by "~600×". The drawback, pointed out by the YaRN paper, is that compressing every dimension uniformly loses the high-frequency components, "it removes the high frequency components of RoPE", which blurs the ability to tell apart tokens that are close together.

NTK-aware scaling rescales the frequencies, that is the base, and does so non-uniformly. Instead of compressing every dimension by the same factor s, it changes the base b to b·s^(d/(d−2)); the YaRN full text says "we spread out the interpolation pressure across multiple dimensions by scaling high frequencies less and low frequencies more", so the high-frequency dimensions stay almost unchanged to keep local detail while the low-frequency dimensions are compressed heavily to cover the long context.

YaRN combines NTK-by-parts (interpolation chosen per dimension, based on the ratio of wavelength to context: high-frequency dimensions are left alone and only low-frequency dimensions are interpolated) with attention temperature scaling (an extra temperature t multiplied into the attention softmax, with sqrt(1/t) = 0.1 ln s + 1). The YaRN abstract states that it needs "10x less tokens and 2.5x less training steps than previous methods" to reach the same context extension.

The three sit on one axis: PI pulls positions back into the trained range; NTK-aware scaling pulls frequencies, and pulls them unevenly across dimensions; YaRN makes that selection per dimension and then patches the softmax. All three are cheap because they do not change the architecture: only the computation of the RoPE angle changes, with or without a small amount of fine-tuning.

### A2. RMSNorm

LayerNorm normalizes by subtracting the mean, dividing by the standard deviation, then scaling by γ and shifting by β. Zhang and Sennrich hypothesize that the mean subtraction is redundant: "we hypothesize that re-centering invariance in LayerNorm is dispensable and propose root mean square layer normalization, or RMSNorm" (arXiv 1910.07467, abstract). RMSNorm divides the vector by the root of the mean of its squared components and multiplies by γ:

$$ \text{RMSNorm}(x) = \frac{x}{\sqrt{\tfrac{1}{d}\sum_i x_i^2 + \epsilon}} \cdot \gamma $$

The paper reports that RMSNorm "achieves comparable performance against LayerNorm but reduces the running time by 7%∼64% on different models" (abstract). The figure depends on 2019 models and hardware, so do not expect the same ratio on your machine; what matters is the qualitative conclusion that dropping mean-centering does not hurt quality and is cheaper.

nanochat goes one step further: `norm(x)` calls `F.rms_norm(x, (x.size(-1),))` and the header says "no learnable params in rmsnorm", that is, γ is dropped too. That is that repo's decision, not the paper's conclusion; the Llama code in HF transformers still has γ.

### A3. SwiGLU FFN

The original Transformer FFN is two matrix multiplications around a nonlinearity, FFN(x) = max(0, xW₁)W₂, and GPT-2 replaces ReLU with GELU. Shazeer replaces the "Linear then activation" pair with a Gated Linear Unit: the component-wise product of two linear projections, one of which passes through an activation. With Swish as the activation we get SwiGLU(x) = Swish_β(xW) ⊗ (xV) (arXiv 2002.05202, eq. 5), and the full FFN is (Swish(xW) ⊗ xV)W₂. The paper concludes that some GLU variants "yield quality improvements over the typically-used ReLU or GELU activations" (abstract).

Because a GLU-style FFN has three matrices instead of two, Shazeer keeps parameter count and compute constant by shrinking the number of hidden units d_ff (section 3: "we reduce the number of hidden units d_ff"). That is why Llama-style configs have an FFN hidden size smaller than 4d; Mistral 7B lists hidden_dim 14336 with d = 4096, i.e. 3.5d (Mistral 7B, Table 1). nanochat chooses differently, using a "relu^2 activation in MLP" (`gpt.py` header); both are engineering choices you can measure, with no single right answer.

### A4. GQA and MQA: sharing K, V to shrink the KV cache

The decoding bottleneck is memory bandwidth, not arithmetic. Ainslie et al. open GQA with that observation: "Autoregressive decoder inference is a severe bottleneck for Transformer models due to the memory bandwidth overhead from loading decoder weights and all attention keys and values at every decoding step" (arXiv 2305.13245, section 1). Shazeer's 2019 multi-query attention (MQA) shrinks K and V by giving every query head one shared key head and one shared value head, but it "can lead to quality degradation and training instability" (same section).

GQA is the midpoint: split the query heads into g groups, each sharing one K, V pair. The paper describes it as "an interpolation between multi-head and multi-query attention with single key and value heads per subgroup of query heads" and reports that "uptrained GQA achieves quality close to multi-head attention while being almost as fast as multi-query attention" (section 1). The paper also proposes uptraining, converting an existing MHA checkpoint to MQA/GQA by mean-pooling the K, V projection matrices and training further with 5% of the original pretraining compute (abstract and section 2.1).

Three models you will meet use GQA: Llama 3 uses "grouped query attention (GQA; Ainslie et al. (2023)) with 8 key-value heads" (arXiv 2407.21783, section 3.2); Mistral 7B has n_heads 32 and n_kv_heads 8 (Table 1); nanochat has `n_kv_head` in `GPTConfig` with the assertion `n_head % n_kv_head == 0`, and `c_k`, `c_v` project to `n_kv_head * head_dim` dimensions (`gpt.py`). When implementing: K and V have fewer heads than Q, and before computing attention scores you repeat each K, V head for the g query heads in its group.

### A5. MLA: Multi-head Latent Attention (DeepSeek-V2)

MLA takes a different route from GQA: instead of reducing the number of K, V heads, it compresses the K and V of all heads into a low-dimensional latent vector with "low-rank key-value joint compression" (DeepSeek-V2, arXiv 2405.04434, section 2.1.2), caches only that compressed vector, and projects back to full K, V when computing attention. Because the projection is linear it can be folded into the Q and output matrices, so the added cost is small. The paper reports that, compared with DeepSeek 67B, DeepSeek-V2 "reduces the KV cache by 93.3%, and boosts the maximum generation throughput to 5.76 times" (abstract). The model has 236B total parameters, 21B activated per token, and a 128K context (abstract).

Link to Week 1: the low-rank compression here is the same SVD intuition as section 7 of Week 1, applied to a sequence's K, V matrices instead of a weight matrix as in LoRA. You do not need to implement MLA in this roadmap; you need to recognize the same mathematical idea appearing a third time.

### A6. Sliding window attention

Full attention costs O(n²) in sequence length (section C1). Mistral 7B brings it to O(n·W) with sliding window attention: "The hidden state in position i of the layer k, h_i, attends to all hidden states from the previous layer with positions between i − W and i" (arXiv 2310.06825, section 2). Information farther than W still arrives through stacking: after k layers a position "can access tokens from the input layer at a distance of up to W × k tokens"; with W = 4096 over 32 layers the paper states "a theoretical attention span of approximately 131K tokens" (same section). A fixed window also enables a rolling buffer cache: the cache holds only W K, V pairs, the pair for step i goes to slot i mod W, so once i exceeds W the cache overwrites and stops growing; at 32k tokens the paper says this "reduces the cache memory usage by 8x, without impacting the model quality" (section 2, Rolling Buffer Cache). Xiao and Zhu present the same idea as a fixed-size KV cache with a window of the n_c most recent pairs (*Foundations of LLMs*, section 2.3.3.1, page 72).

#### A6.1. Attention sinks and StreamingLLM: why the first few tokens are special

> **Source:** StreamingLLM, Xiao et al. 2023, *Efficient Streaming Language Models with Attention Sinks* (arXiv [2309.17453](https://arxiv.org/abs/2309.17453), abstract looked up 2026-08-16).

A naive sliding window has one breaking point: once a long conversation exceeds the cache size and the first tokens are evicted from the KV cache, quality collapses; the abstract describes window attention failing "when the text length surpasses the cache size". The paper's finding is that simply keeping the KV of the initial tokens "will largely recover the performance of window attention", even though those tokens carry no semantic importance. The paper names this phenomenon the attention sink: the initial tokens absorb an unusually large share of attention.

[Inference] An intuitive explanation (based on the argument in the paper, not in the abstract): softmax forces the attention weights to sum to 1, so when a head has nowhere it needs to look it still has to put its weight somewhere, and the most stable place is the first positions, because every later token sees them under causal attention. Evicting them from the cache removes the outlet the model has learned to rely on.

The StreamingLLM recipe is window plus sink: the KV cache holds a few sink tokens from the start of the sequence, kept permanently, plus a sliding window of the w most recent tokens, with no fine-tuning needed. Per the abstract, this lets a model trained with a finite attention window "generalize to infinite sequence lengths without any fine-tuning", running to "4 million tokens and more", up to 22.2× faster than the sliding-window-with-recomputation baseline. The paper also notes that adding a placeholder token as a dedicated sink from pretraining onward improves streaming further. A note on scope: this is a streaming and cache-memory technique, not a "real" context extension; the model still does not remember content that has fallen out of the window (unlike A1.1, where the model does attend over the whole long context).

### A7. Mixture of Experts

MoE replaces the dense FFN with several FFNs (experts) and a router that picks experts per token. Switch Transformer states the benefit and the price: the result is a sparsely activated model with a very large parameter count but constant compute per token, and adoption has been hindered by "complexity, communication costs, and training instability" (Fedus, Zoph, Shazeer, arXiv 2101.03961, abstract). Switch's main contribution is simplified routing: "route to only a single expert" (k = 1), which the paper shows "preserves model quality, reduces routing computation and performs better" (section 2.1); and an auxiliary load balancing loss added to the main loss to avoid piling tokens onto a few experts (section 2.2, "A Differentiable Load Balancing Loss").

Two open models give concrete numbers. Mixtral 8x7B: each layer has 8 FFNs, the router picks 2 per token, so "each token has access to 47B parameters, but only uses 13B active parameters during inference" (arXiv 2401.04088, abstract). DeepSeek-V2: 236B total, 21B activated (arXiv 2405.04434, abstract). When reading an MoE parameter count, always ask for both numbers, total and active; VRAM to load depends on the first, speed on the second.

---

## B. Inference optimization

> **Week** 7 (B1, B2), 11 (B4), 12 (B1, B3, B4), 13 (B2). **Sources:** SLP3 section 7.6 (Jurafsky and Martin, draft of 2026-08-19); *Foundations of LLMs* (Xiao and Zhu, arXiv 2501.09223) sections 2.3.3, 5.1, 5.2; Fleuret, *The Little Book of Deep Learning* section 8.2; Leviathan, Kalman, Matias (arXiv 2211.17192); QLoRA (Dettmers et al., arXiv 2305.14314, PDF in `../docs/papers/`); GPTQ (Frantar et al., arXiv 2210.17323); AWQ (Lin et al., arXiv 2306.00978); `nanochat/engine.py`.

### B1. KV cache

Autoregressive generation adds one token per step. Recomputing K and V for the whole sequence at every step costs O(n) projections per step and O(n²) overall; the KV cache stores K, V for processed tokens, so each step computes K, V only for the new token and attends into the cache. Xiao and Zhu describe inference as therefore splitting into two phases, prefilling that computes the cache for the prompt and decoding that generates tokens attending into the cache (*Foundations of LLMs*, section 5.1.2, page 207).

The price is memory. Cache size scales with the number of layers, number of K, V heads, head dimension, sequence length and bytes per element, doubled for K and V:

$$ \text{KV cache} \approx 2 \cdot n_{\text{layers}} \cdot n_{\text{kv\_heads}} \cdot d_{\text{head}} \cdot n_{\text{tokens}} \cdot \text{bytes} $$

`[Inference]` This formula is a direct count of stored elements; it explains why GQA (fewer n_kv_heads), MLA (smaller stored dimension) and sliding windows (bounded n_tokens) all target the same product. On an 8GB card this is the number to compute before choosing a context length in Week 12. Leviathan et al. note the underlying fact: "inference from large models is often not bottlenecked on arithmetic operations, but rather on memory bandwidth and communication" (arXiv 2211.17192, section 1); Fleuret says the same for single-stream inference (*Little Book*, section 8.2, page 154).

### B2. Sampling

Given a distribution over the vocabulary, how you pick a token decides the style of the output. Jurafsky and Martin describe greedy as picking the most probable token; top-k truncates the distribution to the k most probable tokens, renormalizes and samples, with k = 1 equal to greedy; its weakness is that k is fixed while the shape of the distribution changes with context. Top-p, or nucleus sampling after Holtzman et al. 2020, keeps the smallest set of tokens covering p of the probability mass, so the candidate pool adapts (SLP3 section 7.6.4, page 200). Temperature divides logits by T before the softmax: T below 1 sharpens, T above 1 flattens.

For RAG in Week 13: `[Inference]` answers should stay close to the documents, so prefer low temperature and moderate top-p; but this is a hyperparameter to measure with the Week 14 eval set, not a rule.

### B3. Speculative decoding

Idea: a small model proposes several tokens and the large model verifies them in parallel in a single pass. Leviathan, Kalman and Matias base this on two observations: hard tasks "often include easier subtasks that can be approximated well by more efficient models", and with speculative execution and a new sampling method "we can make exact decoding from the large models faster ... without changing the distribution" (arXiv 2211.17192, abstract). They report a 2 to 3 times speedup on T5-XXL "with identical outputs" (abstract). This is a serving-side technique; what you need to know is that it does not change the output distribution, unlike quantization.

### B4. Quantization

Week 11 turns on a 4-bit flag. Underneath are four different things commonly lumped together as "quantization":

NF4 is QLoRA's data type: "4-bit NormalFloat (NF4), a new data type that is information theoretically optimal for normally distributed weights" (Dettmers et al., arXiv 2305.14314, abstract), together with double quantization (quantizing the quantization constants) and paged optimizers. QLoRA "backpropagates gradients through a frozen, 4-bit quantized pretrained language model into Low Rank Adapters" and allows fine-tuning a 65B model on a single 48GB GPU (abstract). So the base is quantized and frozen; the adapter stays in higher precision because it is being trained.

GPTQ is post-training quantization, "a new one-shot weight quantization method based on approximate second-order information", quantizing a 175B model "in approximately four GPU hours, reducing the bitwidth down to 3 or 4 bits per weight, with negligible accuracy degradation" (Frantar et al., arXiv 2210.17323, abstract).

AWQ starts from the observation that "not all weights in an LLM are equally important. Protecting only 1% salient weights can greatly reduce quantization error", and to find the salient channels "we should refer to the activation distribution, not weights"; instead of mixed precision, AWQ scales those channels and needs no backpropagation (Lin et al., arXiv 2306.00978, abstract).

GGUF is not an algorithm but the file format of the llama.cpp project, the thing Ollama and LM Studio load in Week 12; Fleuret mentions llama.cpp as a post-training quantization framework for consumer hardware (*Little Book*, section 8.2, page 154). `[Unverified]` in this session: the table of GGUF quantization level names (Q4_K_M, Q8_0...), check the llama.cpp docs when exporting.

Why 4-bit works: Fleuret explains that activations are sums of many terms so quantization error is averaged out, and "models quantized down to 6 or 4 bits per parameter exhibit remarkable performance" (section 8.2, page 154). The right measurement is the perplexity of the quantized model versus the original on the same held-out set (section H).

---

## C. Attention at scale

> **Week** 6. **Sources:** FlashAttention (Dao et al., arXiv 2205.14135); PyTorch docs for `torch.nn.functional.scaled_dot_product_attention`.

### C1. Why O(n²)

The score matrix QKᵀ is n × n for n tokens. Dao et al. open with: "the time and memory complexity of self-attention are quadratic in sequence length" (arXiv 2205.14135, abstract). This is the root of every technique in section A6 (bounding n), A4 and A5 (shrinking K, V), and C2 (changing memory use without changing the result).

### C2. FlashAttention

Many approximate attention methods reduce compute but "often do not achieve wall-clock speedup". Dao et al. argue the missing principle is IO-awareness, "accounting for reads and writes between levels of GPU memory", and propose FlashAttention, "an IO-aware exact attention algorithm that uses tiling to reduce the number of memory reads/writes between GPU high bandwidth memory (HBM) and GPU on-chip SRAM" (abstract). The word exact matters: the math is unchanged, only the order of computation and where intermediates live. The paper reports a 15% end-to-end speedup on BERT-large at length 512 versus the MLPerf 1.1 record and 3x on GPT-2 at length 1K (abstract).

In PyTorch, `F.scaled_dot_product_attention` selects a backend (flash among them) when dtype and hardware allow; in Week 6 you write attention by hand to understand it, then compare outputs with this function to verify.

---

## D. Training dynamics

> **Week** 8. **Sources:** `nanoGPT/train.py` (karpathy/nanoGPT, MIT; read 2026-09-04); `nanochat/optim.py`, `nanochat/common.py`, nanochat README; modded-nanogpt (KellerJordan/modded-nanogpt, MIT).

The interventions below all appear in `nanoGPT/train.py`, with defaults read from the code:

| Intervention | Default in `train.py` | Role |
|---|---|---|
| Gradient clipping | `grad_clip = 1.0` | Clip gradient norm to stop loss spikes |
| Dropout | `dropout = 0.0`, comment "for pretraining 0 is good, for finetuning try 0.1+" | Single-epoch pretraining on large data needs little of this regularization |
| Bias | `bias = False` | Remove bias in LayerNorm and Linear |
| Learning rate | `learning_rate = 6e-4`, `warmup_iters = 2000`, `decay_lr = True`, `min_lr = 6e-5` with comment "should be ~= learning_rate/10 per Chinchilla" | Warmup then decay; LR is the most sensitive hyperparameter |
| Weight decay | `weight_decay = 1e-1` | Regularize matrix weights |
| Adam β₂ | `beta2 = 0.95` | Lower than Adam's 0.999 default |
| Mixed precision | `dtype = 'bfloat16'` if supported, else `'float16'` which "will auto implement a GradScaler" | Faster and lighter on VRAM |
| Gradient accumulation | `gradient_accumulation_steps = 5 * 8`, comment "used to simulate larger batch sizes" | The key for an 8GB card: a large effective batch on small VRAM |

Weight tying (sharing the embedding and unembedding matrix) lives in `nanoGPT/model.py`, line `self.transformer.wte.weight = self.lm_head.weight`, cited in Week 7. The most important methodological lesson of this section is not in the config: `[Inference]` many "improvements" from changing one hyperparameter fall within the noise between runs with different seeds; unless you run at least two seeds you do not know whether you saw signal or noise.

### D1. Optimizers: AdamW and Muon

AdamW is the default in nanoGPT. nanochat uses a combined optimizer: "Usually the embeddings and scalars go into AdamW, and the matrix parameters go into Muon" (`nanochat/optim.py`, module docstring). Muon is "adapted and simplified from modded-nanogpt" (MIT) and uses a "Newton-Schulz iteration to compute the zeroth power / orthogonalization of G", that is, the matrix update is orthogonalized before being applied; the file also mentions the alternative "Polar Express Sign Method for orthogonalization" and a "NorMuon variance reduction" that rescales columns after orthogonalization (same file). You do not need to implement Muon; you need to know why it applies only to 2-D matrices (orthogonalization only makes sense for matrices) and why embeddings still use AdamW.

### D2. Mixed precision and dtype

bf16 is the default on Ampere and newer GPUs; fp16 needs a GradScaler against underflow (comment in `train.py`). nanochat manages dtype explicitly through `COMPUTE_DTYPE` in `common.py` (imported by `optim.py`), and the leaderboard in the nanochat README lists the second-ranked run as "d26 slightly undertrained +fp8" (README, Time-to-GPT-2 Leaderboard), so fp8 is already usable in the speedrun on H100. On a 3070 Ti you only have bf16 or fp16.

---

## E. Tokenizer: training BPE from scratch

> **Week** 6. **Sources:** SLP3 section 2.4 (page 42); Sennrich et al. 2015 (arXiv 1508.07909, PDF in `../docs/papers/`); `nanochat/tokenizer.py`, `scripts/tok_train.py`, `scripts/tok_eval.py`; karpathy/minbpe (MIT).

The roadmap uses a prebuilt tiktoken encoding. The deeper step is training your own BPE tokenizer, and the reason is not only academic: the Week 6 experiment shows the `gpt2` vocabulary spends many tokens on Vietnamese because it has no merges for accented sequences. Jurafsky and Martin define tokenization as "the process of segmenting the running input text into tokens" and explain why morpheme-sized units are chosen in a data-driven way (SLP3 section 2.4, page 42). Sennrich et al.'s original BPE starts from characters, repeatedly counts the most frequent adjacent pair and merges it into a new symbol until the merge budget is used (arXiv 1508.07909, section 3.2). The byte-level version starts from 256 bytes so it never sees an out-of-vocabulary token; a regex split (GPT-2, GPT-4 style) separates digits, letters and whitespace before merging so merges do not cross meaningless boundaries.

How to measure a tokenizer: compression, bytes per token on a representative corpus, and fertility, tokens per word. nanochat has `scripts/tok_train.py` and `scripts/tok_eval.py` for these two jobs (file list in the repo). For your project, measure on a sample of Vietnamese legal text before deciding which tokenizer to use in Week 11.

---

## F. Scale and parallelism

> **Week** 8. **Sources:** PyTorch docs on DistributedDataParallel and FullyShardedDataParallel; Xiao and Zhu, *Foundations of LLMs* section 2.2.3 Distributed Training (page 60); Hugging Face Ultra-Scale Playbook (official HF documentation; `[Unverified]` in this session because the page content did not load).

There are four axes for splitting training when one GPU is not enough. Data parallelism replicates the model on each GPU, each GPU processes part of the batch, and gradients are combined with all-reduce; this is the first level to know and how nanoGPT runs multi-GPU via `torchrun`. Tensor parallelism splits one matrix multiplication within a layer across GPUs, for models that do not fit one card. Pipeline parallelism splits the model by layers into sequential stages. ZeRO or FSDP sharding splits optimizer state, gradients and parameters across GPUs to reduce per-card memory. Xiao and Zhu discuss these under Distributed Training in their chapter on training at scale (*Foundations of LLMs*, section 2.2.3, page 60).

With a single 8GB GPU the technique you actually use is gradient accumulation (section D); data parallelism appears only when renting a multi-GPU node for the pretraining run. When reading the log of a distributed run, two numbers to understand are throughput (tokens per second) and the fraction of theoretical hardware FLOPs actually used, usually called MFU; `[Inference]` low MFU usually points to a data or communication bottleneck, not to compute.

### F1. ZeRO stages 1/2/3: sharding one kind of state at a time

DDP has a memory limitation: every GPU holds a full copy of the model state, parameters plus gradients plus optimizer states (with mixed-precision AdamW the optimizer states are usually the heaviest part). ZeRO (Zero Redundancy Optimizer; Rajbhandari et al. 2019, arXiv 1910.02054, checked 2026-09-04) removes that redundancy step by step in three cumulative stages, each sharding one more kind of state across N_d GPUs (memory-reduction figures taken from the paper, looked up 2026-08-16):

1. Stage 1, P_os, shards the optimizer states (each GPU holds 1/N_d); the paper: "4x memory reduction, same communication volume as DP", that is, about 4× less memory with unchanged communication.
2. Stage 2, P_os+g, additionally shards the gradients (reduce-scatter to the GPU responsible for updating the corresponding slice of parameters); the paper: "8x memory reduction, same communication volume as DP".
3. Stage 3, P_os+g+p, shards the parameters as well: each GPU keeps only its own shard, and whichever layer the forward or backward pass needs is broadcast or gathered just in time and then released; the paper: memory falls linearly with N_d, in exchange for a "~50% increase in communication volume". This is the only stage that breaks the "model must fit on one GPU" limit.

The higher the stage, the more memory is saved and the more communication it costs, so pick the lowest stage that lets the model fit on the machine.

### F2. FSDP: ZeRO-3 style in PyTorch

FSDP (FullyShardedDataParallel) is how PyTorch integrates the ZeRO idea into core: the official docs ([docs.pytorch.org/docs/stable/fsdp.html](https://docs.pytorch.org/docs/stable/fsdp.html), looked up 2026-08-16) describe `ShardingStrategy.FULL_SHARD` as "Parameters, gradients, and optimizer states are sharded", the ZeRO-3 shape; `SHARD_GRAD_OP` shards only gradients and optimizer states (the ZeRO-2 shape; the docs even have a variant named `_HYBRID_SHARD_ZERO2`); `NO_SHARD` behaves like DDP. Moving from DDP to FSDP is therefore not a change of framework, only a change in the strategy for spreading state across GPUs.

As for hands-on work, the repo owner confirmed on 2026-08-16 that renting cloud GPUs is an option, and the DDP/FSDP hands-on has been added to the Week 8 extension (renting a 2×GPU machine); see the extension block in the Week 8 README. Locally, on one 8GB GPU, the main tool remains gradient accumulation (section D); F1 and F2 are what you run for real on the rented machine.

---

## G. Alignment and reasoning

> **Week** 9 (diagram) and 10 (full). **Sources:** SLP3 sections 8.1-8.4 (pages 210-223); Sutton and Barto, *RL: An Introduction* sections 3.1, 13.1, 13.3; Xiao and Zhu, *Foundations of LLMs* sections 4.3-4.4; DPO (Rafailov et al., arXiv 2305.18290, PDF in `../docs/papers/`); DeepSeekMath (Shao et al., arXiv 2402.03300); FareedKhan-dev/train-llm-from-scratch `src/post_training/`; nanochat `scripts/chat_sft.py`, `scripts/chat_rl.py`.

The pipeline from a base model to a model that converses and reasons:

```
Pretrain → SFT → Reward Model → PPO or DPO → GRPO / RLVR
```

Pretraining is next-token prediction (Week 8). SFT, or instruction tuning, is supervised learning on instruction and response pairs with the same cross-entropy objective (SLP3 section 8.1, page 210; Week 9). From here on it is learning from preferences.

**Reward model.** Instead of writing down what a good answer is, people compare pairs of outputs, and a scoring model is trained so the chosen output scores higher than the rejected one (SLP3 section 8.3, page 215; FoLLM section 4.3.2). Xiao and Zhu give the reason for the detour: "often, humans themselves cannot precisely express their own preferences" (*Foundations of LLMs*, section 4.3, page 172).

**PPO in RLHF.** SLP3 states that current alignment methods "are based on a Reinforcement Learning (RL) framework (Sutton and Barto, 1998)" (section 8.4, page 219). The policy is the LLM, actions are tokens, reward comes from the reward model, and a KL constraint keeps the policy near the reference model. FoLLM writes the objective in advantage form: U(τ; θ) = Σ_t log π_θ(a_t|s_t) A(s_t, a_t), with the advantage estimated by a TD error and a value function trained with the reward model (section 4.3.3, eq. 4.39, page 182). The Week 10 theory notes trace the path from Sutton and Barto's REINFORCE to this formula.

**DPO.** Rafailov et al. introduce "a new parameterization of the reward model in RLHF that enables extraction of the corresponding optimal policy in closed form, allowing us to solve the standard RLHF problem with only a simple classification loss"; DPO "is stable, performant, and computationally lightweight, eliminating the need for sampling from the LM during fine-tuning" (arXiv 2305.18290, abstract). The loss formula is in Week 10.

**GRPO and RLVR.** DeepSeekMath introduces GRPO as a PPO variant: "GRPO foregoes the critic model, instead estimating the baseline from group scores, significantly reducing training resources" (Shao et al., arXiv 2402.03300, section 1). That is, for each prompt a group of outputs is sampled and rewards are normalized within the group to form the advantage, with no value network. The paper reports GSM8K rising from 82.9% to 88.2% in the RL phase (same section). RLVR is the name used when the reward is machine-checkable, a correct math answer or passing tests; the DeepSeek-R1 paper on the paper shelf is the large-scale example.

**Midtraining.** `[Unverified]` Some modern pipelines insert a stage between pretraining and SFT to teach chat format and special tokens; in the nanochat file list read on 2026-09-04 there are `chat_sft.py` and `chat_rl.py` but I did not see a script named midtrain, so I do not assert how nanochat names this step.

Code to compare against: FareedKhan's `src/post_training/` has SFT, reward model, PPO, DPO and GRPO in plain PyTorch. When reading, find three places: where log π_θ(a_t|s_t) is computed, where the advantage is computed (from a critic in PPO, from the group in GRPO), and where the KL to the reference model is kept.

---

## H. Evaluation

> **Week** 8, 11, 14, 18. **Sources:** SLP3 sections 3.3, 3.7, 1.9, 11.6; nanochat README (Time-to-GPT-2 Leaderboard); `nanochat/core_eval.py`, `nanochat/loss_eval.py`; Zheng et al., "Judging LLM-as-a-Judge" (arXiv 2306.05685); IR-book chapter 8.

**Perplexity and bits per byte.** Perplexity is a function of per-token cross-entropy, normalized by length (SLP3 section 3.3, page 76; section 3.7, page 85). Because it is per token it depends on the tokenizer: two models with different vocabularies cannot compare perplexities. Bits per byte divides the same information by the number of bytes of text instead of tokens, so it compares across models; nanochat reports `val_bpb` on its leaderboard instead of raw loss (nanochat README), and `nanochat/loss_eval.py` computes it. This is the number to use when comparing your Week 8 run to GPT-2.

**CORE.** nanochat measures "time to GPT-2" with the CORE score from the DCLM paper: "The GPT-2 CORE score is 0.256525" and the original GPT-2 checkpoint sits in row 0 of the leaderboard with CORE 0.2565 (nanochat README, Time-to-GPT-2 Leaderboard); `nanochat/core_eval.py` "Evaluates base model CORE score (DCLM paper)" (README, directory tree). Familiar benchmarks such as MMLU, ARC, GSM8K and HumanEval are knowledge, science, math and code questions; SLP3 notes that accuracy on an unseen test set is the basic measure and that large benchmarks are usually question sets (section 1.9, page 25).

**LLM-as-judge.** Zheng et al. list the limitations of using an LLM to grade: "position, verbosity, and self-enhancement biases, as well as limited reasoning ability", while showing that strong judges like GPT-4 reach "over 80% agreement" with humans, the same level as human-human agreement (arXiv 2306.05685, abstract). Two lessons: usable, but check position bias by swapping the order of the two answers, and never trust a single number. The "Judging the Judges" paper on the shelf re-measures this with 13 judges.

**For RAG.** Precision and recall over the retrieved set, and the precision-recall curve for ranked results (IR-book sections 8.3-8.4, pages 155-158); exact match and token F1 for answers (SLP3 section 11.6, page 271). RAGAS in Week 14 is the LLM-graded version of these measures.

---

## I. Agentic and Graph Engineering

> **Week** 15-18. **Sources:** [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf), [`../docs/Graph-Engineering-Athropic-Playbook.pdf`](../docs/Graph-Engineering-Athropic-Playbook.pdf), [`../docs/5-layers-multi-agent.jpg`](../docs/5-layers-multi-agent.jpg); Anthropic, *Building Effective AI Agents* and *How we built our multi-agent research system* (anthropic.com/engineering, read 2026-09-04); SLP3 section 1.8.

Phases 1-2 ask how the model works. Phase 3 asks where to put memory and evaluation, because that is the bottleneck when many model calls are composed into a system.

### I1. Five engineering layers

The diagram in `docs/5-layers-multi-agent.jpg` stacks five layers, each wrapping the previous: prompt (the message: role, instructions, examples, format), context (the memory: what goes into the window), harness (the machine: gather, act, verify, with retries), loop (the system: run, check budget and progress, decide to continue or stop), graph (the organization: many agents with shared memory). The value of the layering is diagnostic: malformed output is a layer 1 problem; the model not knowing what it needs to know is layer 2; nobody checking results is layer 3; running forever is layer 4; agents repeating each other's work is layer 5. Jurafsky and Martin give the base definition at the lowest layer: an agent is an LLM that can act by calling other programs, and "The technical difference is only that the set of actions in the world are added to the set of possible tokens to generate" (SLP3 section 1.8, page 24).

### I2. From loop to swarm

Each architecture externalizes one bottleneck out of the model: a loop externalizes iteration and evaluation; a chain externalizes task order; a swarm externalizes parallel search and role specialization; a DAG externalizes experiment lineage; a knowledge graph externalizes shared facts, provenance and cross-session memory (Karpathy-Loop PDF, section on architectures).

The canonical example is Karpathy's ratchet loop in autoresearch: inspect, propose, apply, evaluate, keep if the metric improves, revert otherwise. The PDF puts the core code at "roughly 630 lines" and notes an extended run "executed about 700 experiments in two days" (Karpathy-Loop PDF, section I.B). Four conditions make such a loop meaningful: measurable output, reversible actions, a short horizon for dense feedback, and a bounded environment. Without the first the agent optimizes the wrong thing; without the second one error corrupts the whole state.

`program.md` is how the loop is "programmed" in natural language: it declares which files may change, the metric and its direction, the budget, commit and revert rules, and when to escalate to a human. The PDF frames this as the step to Software 3.0 in Karpathy's phrase (PDF reference [9]). One distinction that is often blurred: the commit DAG answers "what changed, which experiment is the parent", the knowledge graph answers "which entities exist, how they relate, which source backs them"; the PDF advises against introducing a knowledge graph merely because you can.

### I3. Five workflow patterns and the cost of multi-agent

Anthropic distinguishes workflows, "Systems where LLMs and tools are orchestrated through predefined code paths", from agents, "Systems where LLMs dynamically direct their own processes and tool usage", and concludes from work with many teams: "the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns" (*Building Effective AI Agents*). Five patterns: prompt chaining (sequential steps, each processing the previous output), routing (classify input then send it to a specialized branch), parallelization (run in parallel then aggregate, including sectioning and voting), orchestrator-workers (a central model decomposes, delegates to workers, synthesizes), evaluator-optimizer (one side generates, the other evaluates and gives feedback, in a loop).

The cost is measured. In its post on the multi-agent research system, Anthropic reports that the system with Claude Opus 4 as lead and Claude Sonnet 4 subagents "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval", while "agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats", and "token usage by itself explains 80% of the variance" in performance (*How we built our multi-agent research system*). Design consequence: split roles when the problem has many independent directions and specialization adds signal, and always define the reducer before fanning out.

The Karpathy-Loop PDF describes dynamic workflows, in which the model generates the orchestration script and spawns sub-agents with fresh context, with a "hard cap of 1,000 per workflow" (PDF, dynamic workflows section); the abstraction boundary moves up but the designer still defines the objective, file scope, output contract, permissions, verification policy, budget and rollback rule. `[Inference]` Tasks that need one continuous line of thought, such as architecture design or writing a long document, usually get worse when split into isolated units; and parallel workers can share the same mistake if they share the same prompt and evidence, so reviewers need different prompts and evidence.

### I4. Knowledge graphs at production scale

The Week 17 pipeline runs on a few documents, in memory. The Playbook in `docs/` describes what to add when moving to thousands of documents.

Resolution cannot put every entity into one prompt. The Playbook uses blocking: group candidates by cheap signals (shared name tokens, Jaccard over tokens, rules) into blocks, then let the model arbitrate within a block; the pipeline runs unchanged on blocks of 50 to 100 candidates, and the combination is "blocking plus expensive LLM arbitration within blocks" (Playbook, scaling section). This is the general principle: the model for the part that needs judgment, deterministic logic for everything else.

Storage: NetworkX is enough for a notebook; at scale the Playbook names two paths, a graph database or "three Postgres tables" with path queries "implemented as recursive CTEs", and stresses that this choice leaves the extraction and resolution code unchanged (Playbook, storage section). Two failure modes the Playbook warns about: silent loss, where "a raw name left out of every cluster silently vanishes from" the results, so every name must land in a cluster even a singleton; and false merges, which wrongly join two entities and contaminate every downstream query, so resolution must keep aliases and evidence and be reversible. For monitoring, the Playbook names extraction rate, the number of entities and relations extracted per document, as the first signal for detecting a corpus drifting out of domain, and cautions that precision 1.00 is not automatically good: "Perfect precision (1.00) means the extractor is conservative" (Playbook, evaluation section). Read the rest of the monitoring section and pick the signals that fit your system.

### I5. Production discipline

A complexity budget is declared before each run: number of model calls, sub-agents, concurrent workers, wall-clock, tokens, cost, retries, and the minimum evidence required to finalize. When the budget runs out, return the best artifact so far with the list of unresolved issues and the reason for stopping; never hide a partial failure behind a fluent answer (Karpathy-Loop PDF, section VII). Metric gaming is the structural risk of every ratchet: the loop only improves what it can see, so it may lower validation loss while raising inference cost or overfitting the eval set; keep secondary constraints.

Six questions for choosing an architecture, per the PDF's decision framework: can success be verified, if not do not start with autonomy; are the steps stable, if so chain; are subtasks independent, if so parallelize; must alternative branches be kept, if so a DAG; must facts outlive a run, if so persist a graph instead of relying on the transcript; can you afford the cost and latency, set the budget before adding workers.

The final measure, quoted from the Karpathy-Loop PDF:

> *Every important output can be traced to an objective, a plan, an artifact, a source, a graph path, an evaluator decision, and a bounded execution record.*

When that sentence holds for your system, loops, swarms, DAGs and knowledge graphs are composable mechanisms. When it does not, adding agents only adds opacity. This is the sentence you test against in Week 18.

---

## J. Production inference serving: vLLM and PagedAttention

> **Week** 12 (after running local inference with Ollama/MLX). **Sources:** the vLLM paper, Kwon et al. 2023, *Efficient Memory Management for Large Language Model Serving with PagedAttention* (arXiv [2309.06180](https://arxiv.org/abs/2309.06180), abstract looked up 2026-08-16); the official README of [vllm-project/vllm](https://github.com/vllm-project/vllm) (Apache 2.0, looked up 2026-08-16).

In Week 12 you serve a model to one user, yourself. Production serving is a different problem: many concurrent requests, and GPUs are expensive so they must run at full load. The two vLLM techniques below solve that problem, and both revolve around the KV cache from B1.

### J1. PagedAttention: paging the KV cache like virtual memory

The problem is that the naive way to allocate the KV cache reserves one contiguous block of memory for the maximum length of each request, which wastes a great deal because (a) requests are usually much shorter than the maximum and (b) memory fragments between requests. The vLLM paper borrows from operating-system virtual memory: cut the KV cache into fixed-size blocks, allocate blocks on demand, and keep a logical-to-physical mapping table so the blocks of one sequence can be scattered. Per the abstract (looked up 2026-08-16), this reduces KV cache waste and raises throughput 2-4× over serving systems of the same period at the same latency level.

Do not confuse this with QLoRA's "paged optimizers" (Week 11). The two share the word "paged" but are entirely different: paged optimizers (Dettmers et al., arXiv [2305.14314](https://arxiv.org/abs/2305.14314), abstract looked up 2026-08-16) move optimizer state back and forth between GPU and CPU RAM to "manage memory spikes" during training; PagedAttention pages the KV cache inside VRAM during inference and serving. One is training-side, the other serving-side.

### J2. Continuous batching: throughput versus latency

Static batching gathers N requests into one batch and runs until the whole batch finishes before accepting new requests, so short requests wait for long ones and the GPU sits idle for nothing. Continuous batching (vLLM README: "continuous batching of incoming requests", looked up 2026-08-16) works at each decode step: a request that finishes leaves the batch and a new request takes the free slot immediately, so the GPU stays full. In exchange, continuous batching optimizes throughput (tokens per second for the whole system), while the latency of an individual request may rise slightly because it shares the GPU with other requests. Configure according to which one you prioritize.

### J3. Compared with Ollama / LM Studio

Ollama and LM Studio (llama.cpp backend) are optimized for single-user local use: load a GGUF, one request at a time, running on consumer CPU or GPU, exactly what you need in Week 12. vLLM is optimized for multi-user serving on a GPU server: PagedAttention and continuous batching only pay off when there are many concurrent requests. [Inference] For this roadmap you do not need to stand up a real vLLM; what to carry away is the way of asking the question: when someone says "serve the model to the whole team", you know the problem has shifted from "is there enough VRAM" (B1) to "is the GPU running at full load" (J2) and "is the KV cache being wasted" (J1).

## K. Test-time compute and reasoning models

> **Week** 10 (right after G, GRPO/RLVR). **Sources:** self-consistency, Wang et al. 2022 (arXiv [2203.11171](https://arxiv.org/abs/2203.11171)); s1, Muennighoff et al. 2025 (arXiv [2501.19393](https://arxiv.org/abs/2501.19393)); DeepSeek-R1 (arXiv [2501.12948](https://arxiv.org/abs/2501.12948): already in [`../docs/papers/README.md`](../docs/papers/README.md), anchored to Week 10). All abstracts looked up 2026-08-16.

Week 10 teaches the training-side axis: pour compute into training (RM, DPO, GRPO) so the model gets better. The second axis is inference-side: spend extra compute at inference time, with the same model, to get a better answer. The two axes complement each other, and reasoning models are where they meet.

### K1. CoT sampling and self-consistency

Instead of greedily decoding one chain of reasoning (chain-of-thought), sample several reasoning chains (temperature above 0) and vote on the final answer; the abstract of Wang et al. describes a method that "samples a diverse set of reasoning paths instead of only taking the greedy one, and then selects the most consistent answer". The condition for applying it is that the final answer must be machine-comparable (a number, a multiple-choice answer), the same family of conditions as RLVR.

### K2. Best-of-N with a verifier

Generate N answers, have a verifier score them, and keep the highest-scoring one. The verifier can be a reward model (the very RM from G and Week 10, used at inference instead of training) or a deterministic verifier (run the tests, compare the result). Compared with K1: self-consistency votes by majority, best-of-N trusts a single judge.

### K3. Budget forcing (s1)

This is direct control over how much "thinking" a reasoning model does: the s1 abstract describes "budget forcing to control test-time compute by forcefully terminating the model's thinking process or lengthening it", that is, cutting off early or forcing more thought, and the abstract reports that this lets their 32B model surpass o1-preview on competition math benchmarks (looked up 2026-08-16). Test-time compute is thus a controllable axis, not a black box.

### K4. DeepSeek-R1: where the two axes meet

The R1 abstract states that reasoning ability "can be incentivized through pure reinforcement learning (RL), obviating the need for human-labeled reasoning trajectories", which is the GRPO/RLVR of section G run at real scale. One way to read R1: RLVR (training-side) trains the model to generate long reasoning chains on its own, that is, it moves test-time compute inside the model instead of building an external scaffold as in K1 and K2. After R1 the two axes are no longer separate: train so the model knows how to think long, then regulate how long it thinks with a budget (K3).

## L. Multimodal and VLM overview

> **Week** none; further reading, outside the hands-on scope of the roadmap (this roadmap is text-only). **Sources:** CLIP, Radford et al. 2021 (arXiv [2103.00020](https://arxiv.org/abs/2103.00020)); LLaVA, Liu et al. 2023 (arXiv [2304.08485](https://arxiv.org/abs/2304.08485)). Abstracts looked up 2026-08-16.

Real banking documents contain scanned tables, stamps and signatures, so sooner or later someone will ask why you do not use a model that can read images. This section gives you enough vocabulary to answer that question, and no more.

### L1. CLIP: contrastive pretraining

Train two encoders (image and text) so that the embedding of an image and the embedding of its correct caption are close while wrong pairs are far apart (contrastive). The abstract: trained on 400 million (image, text) pairs collected from the internet, and the model transfers zero-shot to many tasks through natural-language prompts (looked up 2026-08-16). CLIP provides a shared embedding space for images and text. [Inference] That is the foundation of most later VLMs; LLaVA in L2 is one example.

### L2. The common VLM architecture: vision encoder, projector, LLM

The LLaVA recipe (abstract: "connects a vision encoder and LLM"): take a pretrained vision encoder (usually the image side of CLIP), then a projector (a learned projection) maps the image features into a sequence of "visual tokens" living in the LLM's embedding space, and the LLM reads the mixed sequence of image tokens and text tokens as usual. [Inference] The appeal of this recipe is that it reuses two separately trained models and learns only the connecting layer in between, far cheaper than training multimodal from scratch; that is why it is widespread.

### L3. Why the OCR pipeline in the prerequisites is NOT multimodal modelling

The OCR pipeline goes from image to text (a deterministic OCR step) to a model that sees only text. In a VLM the image representation goes straight into the model, with no transcription step. The consequences differ: OCR loses layout, figures and stamps, but it is simple, every step can be debugged, and everything downstream (RAG, KG) remains the text problem you have already learned; a VLM keeps the visual information but drags in an entirely different training and evaluation stack. [Inference] For this academic project on one 8GB GPU, OCR-then-text is the right choice; a VLM is worth considering only when visual information (the position of a signature, a complex table structure) genuinely decides the answer.

---

## Priorities if time is short

Must: KV cache (B1), RoPE (A1), RMSNorm and SwiGLU (A2, A3), GQA (A4), gradient accumulation (D), bits per byte (H); for Phase 3: the five layers (I1), the four ratchet-loop conditions (I2), the complexity budget (I5). Should: MoE (A7), quantization internals (B4), Muon (D1), the full alignment pipeline (G), BPE training (E), the five workflow patterns (I3), blocking and incremental updates for KGs (I4). Later: MLA (A5), sliding window (A6), speculative decoding (B3), tensor and pipeline parallelism (F), large-scale dynamic workflows (I3). Nice to have, after G and B1: production serving with vLLM (J) and test-time compute (K); read when needed: the multimodal overview (L).
