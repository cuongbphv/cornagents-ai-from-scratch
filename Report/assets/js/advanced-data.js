/* Kiến thức nâng cao (gap analysis) — window.ADVANCED_TOPICS
   Đồng bộ với Week-00/advanced_topics_vi.md. Dùng chung class .know (formula/code/kt). */
window.ADVANCED_TOPICS = [
  {
    id: "arch", ix: "A", title: "Kiến trúc hiện đại: GPT-2 → Llama/Qwen", week: "Tuần 3–4",
    desc: "Những thứ model 2024–25 dùng mà GPT-2 (2019) không có.",
    body: `
      <p>GPT-2 dùng <b>absolute positional embedding</b>, <b>LayerNorm</b>, <b>GELU-FFN 4×</b>, <b>MHA</b>, có bias. Llama 3 / Qwen3 đổi gần như tất cả:</p>
      <h5>A1 · RoPE (Rotary Positional Embeddings)</h5>
      <p>Thay vì <i>cộng</i> vector vị trí, RoPE <b>xoay</b> Q,K theo góc tỉ lệ vị trí (tần số \\(\\theta_i = 10000^{-2i/d}\\)). Hệ quả: \\(q_m\\cdot k_n\\) chỉ phụ thuộc khoảng cách tương đối \\((m-n)\\) → tổng quát hoá tốt hơn, nền của mở rộng context (YaRN).</p>
      <h5>A2 · RMSNorm (thay LayerNorm)</h5>
      <div class="formula">\\( \\text{RMSNorm}(x)=\\dfrac{x}{\\sqrt{\\frac{1}{d}\\sum_i x_i^2+\\epsilon}}\\cdot\\gamma \\)</div>
      <p>Bỏ trừ mean & bias → rẻ hơn, ổn định tương đương.</p>
      <h5>A3 · SwiGLU FFN (thay GELU-FFN)</h5>
      <div class="formula">\\( \\text{SwiGLU}(x)=\\big(\\text{SiLU}(xW_{gate})\\odot xW_{up}\\big)W_{down} \\)</div>
      <p>FFN có cổng; 3 ma trận nên chiều ẩn ≈ ⅔·4d để giữ số tham số.</p>
      <h5>A4 · GQA / MQA</h5>
      <p>Các nhóm head chia sẻ chung K,V → <b>giảm KV cache</b>. MQA = chung 1 K,V; GQA = theo nhóm (Llama/Qwen). MLA (A5, DeepSeek) nén K,V xuống vector tiềm ẩn chiều thấp.</p>
      <h5>A6 · Sliding Window · A7 · MoE</h5>
      <p>Sliding window: chỉ attend \\(w\\) token gần nhất → chi phí tuyến tính. MoE: nhiều FFN "expert" + router chọn top-k → tổng tham số lớn nhưng <b>active</b> mỗi token nhỏ (Qwen3-MoE, gpt-oss, DeepSeek).</p>
      <div class="tagrow"><span class="kt">RoPE</span><span class="kt">RMSNorm</span><span class="kt">SwiGLU</span><span class="kt">GQA/MQA</span><span class="kt">MLA</span><span class="kt">MoE</span></div>
      <p style="margin-top:8px;font-size:12.5px;color:var(--txt-faint)">Nguồn: rasbt <i>Bonus Material</i> (Llama 3 & Qwen3 from scratch, gpt-oss); nanochat <code>gpt.py</code>.</p>`
  },
  {
    id: "infer", ix: "B", title: "Tối ưu inference", week: "Tuần 4 & 8",
    desc: "Sinh text nhanh & rẻ.",
    body: `
      <h5>B1 · KV Cache (bắt buộc hiểu)</h5>
      <p>Khi sinh tự hồi quy, lưu lại K,V của token đã sinh → mỗi bước chỉ tính cho token mới (\\(O(n)\\) thay vì \\(O(n^2)\\)). Bộ nhớ KV cache ∝ \\(n_{layers}\\cdot n_{kv\\_heads}\\cdot d_{head}\\cdot\\)seq — nút thắt VRAM khi context dài (rất liên quan giới hạn 8GB).</p>
      <h5>B2 · Sampling</h5>
      <ul>
        <li><b>Temperature</b> \\(T\\): chia logits cho \\(T\\); \\(T\\) nhỏ hơn 1 → an toàn, lớn hơn 1 → sáng tạo.</li>
        <li><b>Top-k</b>: lấy mẫu trong k token cao nhất.</li>
        <li><b>Top-p (nucleus)</b>: tập nhỏ nhất có tổng xác suất ≥ p.</li>
      </ul>
      <h5>B3 · Speculative decoding</h5>
      <p>Model "nháp" nhỏ đề xuất nhiều token, model lớn verify song song → nhanh hơn, không đổi phân phối.</p>
      <h5>B4 · Quantization internals (sâu hơn Tuần 8)</h5>
      <ul>
        <li><b>NF4</b> (QLoRA): 4-bit "normal float" cho trọng số ~Gaussian; chỉ quantize base.</li>
        <li><b>GPTQ</b> (per-layer, Hessian) · <b>AWQ</b> (bảo vệ kênh salient).</li>
        <li><b>GGUF</b> = <i>định dạng file</i> llama.cpp (Q4_K_M…), không phải thuật toán — thứ Ollama/LM Studio load.</li>
      </ul>
      <div class="tagrow"><span class="kt">KV cache</span><span class="kt">top-p</span><span class="kt">NF4</span><span class="kt">GPTQ/AWQ</span><span class="kt">GGUF</span></div>`
  },
  {
    id: "scale-attn", ix: "C", title: "Attention ở quy mô lớn", week: "Tuần 3",
    desc: "Vì sao context dài đắt, và FlashAttention.",
    body: `
      <h5>C1 · Độ phức tạp \\(O(n^2)\\)</h5>
      <p>Ma trận score \\((\\text{seq}\\times\\text{seq})\\) → bộ nhớ/tính toán tăng bình phương theo độ dài. Đây là rào cản context dài.</p>
      <h5>C2 · FlashAttention (khái niệm)</h5>
      <p>Không vật chất hoá ma trận \\(n\\times n\\) trong HBM: <b>tiling</b> Q,K,V, tính softmax kiểu streaming trong SRAM, cộng dồn → <b>cùng kết quả toán học, giảm I/O bộ nhớ</b>. PyTorch gói qua <code>F.scaled_dot_product_attention</code>.</p>
      <div class="tagrow"><span class="kt">O(n²)</span><span class="kt">tiling</span><span class="kt">FlashAttention</span><span class="kt">SDPA</span></div>
      <p style="margin-top:8px;font-size:12.5px;color:var(--txt-faint)">Nguồn: Giles part 14 (complexity at scale).</p>`
  },
  {
    id: "dynamics", ix: "D", title: "Training dynamics — 'Interventions' của Giles", week: "Tuần 5",
    desc: "Giles train 7+ model 3090, đo từng can thiệp (32a–32m).",
    body: `
      <ul>
        <li><b>Gradient clipping</b> (32b): giảm loss-spike, cải thiện nhẹ.</li>
        <li><b>Bỏ dropout</b> (32c): pretrain 1-epoch data lớn → <b>bỏ dropout tốt hơn</b> (dropout hợp fine-tune data nhỏ).</li>
        <li><b>Attention bias</b> (32d): thêm bias Q/K/V <b>không giúp</b> → modern bỏ bias.</li>
        <li><b>LR</b> (32e): warmup → cosine; siêu tham số nhạy nhất.</li>
        <li><b>Weight decay</b> (32f ~0.1) · <b>Weight tying</b> (32g): modern lớn thường không tie.</li>
        <li><b>Noise/variance</b> (32i): nhiều "cải thiện" nằm trong <b>nhiễu</b> — phải chạy nhiều seed. <i>Bài học phương pháp luận quan trọng nhất.</i></li>
        <li><b>Gradient accumulation</b> (32k): chìa khoá đạt effective batch lớn trên 8GB.</li>
      </ul>
      <h5>D1 · Optimizer: AdamW vs Muon</h5>
      <p><b>Muon</b> (nanochat) orthogonalize update cho ma trận 2D (Newton-Schulz) → pretrain nhanh hơn; embedding/head vẫn AdamW.</p>
      <h5>D2 · Mixed precision</h5>
      <p>bf16 (Ampere+), fp16 (cần GradScaler), fp8 (Hopper). nanochat quản lý dtype tường minh qua <code>COMPUTE_DTYPE</code> thay autocast.</p>
      <div class="tagrow"><span class="kt">grad clip</span><span class="kt">no-dropout</span><span class="kt">Muon</span><span class="kt">bf16/fp8</span><span class="kt">grad accum</span></div>`
  },
  {
    id: "tokenizer", ix: "E", title: "Train BPE tokenizer from scratch", week: "Tuần 3",
    desc: "Roadmap chỉ DÙNG tiktoken — bước sâu hơn là TỰ train.",
    body: `
      <ol style="margin-left:18px;color:var(--txt-dim);font-size:13.5px;line-height:1.8">
        <li>Bắt đầu byte-level (256 token) → không bao giờ OOV.</li>
        <li>Lặp: đếm cặp kề nhau nhiều nhất → <b>merge</b> → tới <code>vocab_size</code>.</li>
        <li>Dùng <b>regex split</b> kiểu GPT-4 tách số/chữ/khoảng trắng.</li>
        <li>Đánh giá: <b>compression rate</b> = bytes/token (cao = nén tốt).</li>
      </ol>
      <p>Hiểu tokenizer giải thích "đếm r trong strawberry", toán nhiều chữ số, lỗi khoảng trắng.</p>
      <div class="tagrow"><span class="kt">byte-level BPE</span><span class="kt">merge</span><span class="kt">compression rate</span></div>
      <p style="margin-top:8px;font-size:12.5px;color:var(--txt-faint)">Nguồn: nanochat <code>tok_train.py</code>/<code>tok_eval.py</code>; rasbt "BPE from scratch".</p>`
  },
  {
    id: "scale", ix: "F", title: "Scale & Parallelism", week: "Tuần 5",
    desc: "Khi 1 GPU không đủ.",
    body: `
      <ul>
        <li><b>DDP</b> (Data Parallel): nhân bản model, mỗi GPU một phần batch, <b>all-reduce</b> gradient. Giles part 29 dùng 8×A100.</li>
        <li><b>TP</b> (Tensor Parallel): chia <i>trong</i> một lớp qua nhiều GPU.</li>
        <li><b>PP</b> (Pipeline Parallel): chia <i>theo lớp</i> thành stage.</li>
        <li><b>ZeRO / FSDP</b>: shard optimizer/gradient/param để giảm bộ nhớ.</li>
        <li><b>MFU</b>: % FLOP lý thuyết dùng được — thước đo hiệu quả train.</li>
      </ul>
      <p>Với bạn (1×8GB): chủ yếu <b>gradient accumulation</b> ở local; DDP khi thuê multi-GPU cloud.</p>
      <div class="tagrow"><span class="kt">DDP</span><span class="kt">TP/PP</span><span class="kt">ZeRO/FSDP</span><span class="kt">MFU</span></div>`
  },
  {
    id: "align", ix: "G", title: "Alignment & Reasoning đầy đủ", week: "Tuần 6–7",
    desc: "Base → aligned reasoning model.",
    body: `
      <div class="formula" style="font-family:'JetBrains Mono';font-size:12.5px;border-left-color:var(--p3)">Pretrain → <b>Midtrain</b> → SFT → Reward Model → PPO/DPO → <b>GRPO/RLVR</b></div>
      <ul>
        <li><b>Midtrain</b> (nanochat): bước <i>không có</i> trong sách Raschka — dạy format hội thoại, special tokens, tool use.</li>
        <li><b>Reward Model</b>: chấm điểm ưu tiên cặp output (FareedKhan implement from scratch).</li>
        <li><b>DPO</b>: tối ưu trực tiếp từ cặp (chosen, rejected), bỏ RM/PPO.</li>
        <li><b>GRPO/RLVR</b>: bỏ critic, chuẩn hoá reward theo nhóm sample; RLVR = reward <b>kiểm chứng được</b> (toán đúng/sai, test pass) → nền reasoning (o1/R1-style).</li>
        <li><b>Tool-use RL</b> (nanochat): model học gọi Python để tính/đếm, reward khi đúng.</li>
      </ul>
      <div class="tagrow"><span class="kt">midtrain</span><span class="kt">RM</span><span class="kt">DPO</span><span class="kt">GRPO</span><span class="kt">RLVR</span><span class="kt">tool-use RL</span></div>
      <p style="margin-top:8px;font-size:12.5px;color:var(--txt-faint)">Nguồn: FareedKhan <code>src/post_training</code>; Raschka <code>reasoning-from-scratch</code>; nanochat <code>chat_rl.py</code>.</p>`
  },
  {
    id: "eval", ix: "H", title: "Evaluation đúng cách", week: "Tuần 5, 8, 11, 15",
    desc: "Đừng tin một chỉ số duy nhất.",
    body: `
      <ul>
        <li><b>Perplexity</b> \\(=e^{L}\\): phụ thuộc vocab/tokenizer → khó so chéo.</li>
        <li><b>Bits-per-byte (bpb)</b>: chuẩn hoá về byte → <b>so sánh được</b> giữa tokenizer. nanochat dùng val_bpb.</li>
        <li><b>CORE (DCLM)</b>: tổ hợp benchmark; nanochat đo "time-to-GPT-2" (GPT-2 = 0.2565).</li>
        <li><b>Benchmark</b>: MMLU (kiến thức), ARC (khoa học), GSM8K (toán), HumanEval (code).</li>
        <li><b>LLM-as-judge</b> (Giles 30): tiện nhưng bẫy (thiên vị độ dài/vị trí); <b>loss thấp ≠ hữu ích hơn</b>.</li>
      </ul>
      <div class="tagrow"><span class="kt">perplexity</span><span class="kt">bits-per-byte</span><span class="kt">CORE/DCLM</span><span class="kt">MMLU/GSM8K</span><span class="kt">LLM-as-judge</span></div>`
  }
];
