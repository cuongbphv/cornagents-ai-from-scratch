# Lý thuyết Tuần 12: MLX trên Mac + local inference stack

> Đọc trước khi chạy các lệnh trong [`02_mlx_commands.md`](02_mlx_commands.md). Tuần này chạy trên Mac, các số liệu không kiểm chứng được từ máy Windows này đều ghi rõ; nguồn cuối file (xác minh 2026-08-11).

---

## 1. Unified memory: vì sao Mac 24GB "chứa" được model mà 8GB VRAM không chứa nổi

Kiến trúc Apple Silicon: CPU và GPU **dùng chung một vùng RAM**: không có "VRAM rời". Hệ quả bằng số học byte (tự kiểm): model 13B ở 4-bit ≈ 6.5 GB trọng số + working memory fine-tune → nằm trong 24 GB unified, nhưng vượt xa 8 GB của 3070 Ti. Trade-off: băng thông/throughput thấp hơn GPU rời, README ước "~2-4× chậm hơn NVIDIA"; [Chưa xác minh] con số này với chính hai máy của bạn, đo thật ở mục 4 chính là deliverable.

## 2. MLX fine-tune flow: 3 lệnh, cùng bản chất với Tuần 11

`mlx-lm` (repo `ml-explore/mlx-lm`, MIT, xác minh 2026-08-11, có tài liệu LoRA riêng `mlx_lm/LORA.md`):

```
1. Tải model MLX-format:   HF repo mlx-community/<model>
2. LoRA train:             mlx_lm.lora --model <m> --train --data <d> --iters 500
3. Fuse adapter:           mlx_lm.fuse --model <m> --adapter-path <a>
```

Khái niệm không có gì mới, vẫn là LoRA Tuần 9 (adapter hạng thấp, base đóng băng), chỉ đổi framework + phần cứng. Data format của `mlx_lm.lora` là JSONL, xem ví dụ trong [`02_mlx_commands.md`](02_mlx_commands.md). "Fuse" = "merge" của Tuần 9: `W' = W + (α/r)BA`.

## 3. Local inference stack: GGUF, Ollama, LM Studio

- **GGUF** = định dạng file model của llama.cpp (nhắc lần 3 trong roadmap vì hay nhầm): một file chứa trọng số đã quantize (Q4_K_M, Q5_K_M, Q8_0…) + metadata + tokenizer. **Không phải thuật toán**: cùng một model có nhiều bản GGUF ở mức bit khác nhau.
- **Ollama**: serve model local qua API; `Modelfile` khai báo GGUF nguồn + template chat + tham số. Đây là backend generate cho RAG Tuần 13.
- **LM Studio**: GUI chạy cả GGUF lẫn MLX, tiện so sánh nhanh hai format trên cùng máy Mac.
- Quy tắc chọn mức quantize (mục nâng cao B4): 8-bit gần như không mất chất lượng, 4-bit là điểm ngọt local; bit càng thấp perplexity càng tăng, nghi ngờ chất lượng thì thử lại ở Q8_0 trước khi đổ lỗi cho model.

## 4. Đo tốc độ Mac vs 3070 Ti: làm cho ra số, đừng cảm nhận

Protocol tối thiểu (điền kết quả vào [`03_hardware_decision.md`](03_hardware_decision.md)):

1. Cùng model, cùng mức quantize (vd. cùng file GGUF Q4_K_M), cùng prompt, cùng `max_tokens`.
2. Chạy ≥3 lần mỗi máy, bỏ lần đầu (warmup/load), lấy trung bình **tokens/giây** (Ollama in sẵn `eval rate`).
3. Ghi kèm: nhiệt/throttling nếu có, RAM/VRAM chiếm dụng, ngày đo.

Kết quả bảng này + trải nghiệm fine-tune là căn cứ viết bảng quyết định Mac vs 3070 Ti vs cloud, không chép ước lượng của người khác.

## 5. Kiểm tra catastrophic forgetting: bắt buộc với model song ngữ

Fine-tune lệch về một thứ tiếng có thể làm suy giảm khả năng thứ tiếng kia. Đừng tranh luận lý thuyết, **đo**:

1. Trước khi fine-tune: chốt bộ 10 prompt cố định (5 tiếng Việt + 5 tiếng Anh, có cả nghiệp vụ lẫn thường thức), sinh và lưu output của base.
2. Sau fine-tune: chạy đúng 10 prompt đó (temperature 0), so từng cặp.
3. Suy giảm rõ ở tiếng Anh → giảm tỷ lệ data một chiều, trộn thêm data tiếng Anh (chiến lược mục 8 của [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md)), train lại.

Bộ 10 prompt này giữ cố định vĩnh viễn, nó là "bài kiểm tra sức khỏe song ngữ" cho mọi model sau này của dự án.

Bài kiểm tra này có chỗ dựa từ paper chứ không phải lo xa: Biderman et al. 2024 (PDF trong repo: [`../docs/papers/2405.09673_lora-learns-less-forgets-less.pdf`](../docs/papers/2405.09673_lora-learns-less-forgets-less.pdf)) đo được full fine-tuning quên kiến thức ngoài domain đích nhiều hơn hẳn LoRA, tức là mức quên **phụ thuộc cách bạn fine-tune**, và chỉ có đo mới biết mình đang ở đâu trên trade-off đó. LoRA của MLX ở mục 2 nằm ở phía "quên ít" của phổ này, nhưng số của máy bạn vẫn phải tự đo.

## 6. Tiếng Việt trong tuần này

- Mục 5 chính là nội dung tiếng Việt trọng tâm của tuần: **giữ được song ngữ sau fine-tune là một deliverable đo được**, không phải cảm nhận.
- Khi viết `Modelfile` cho Ollama: **template chat phải khớp đúng template lúc fine-tune** (bài học Tuần 9 mục 3): sai template, model tiếng Việt trả lời lẫn tiếng Anh hoặc lặp vô hạn là triệu chứng kinh điển. [Suy luận]: dựa trên cơ chế model học phân phối template; gặp triệu chứng thì kiểm template đầu tiên.
- Kiểm tra sanity encoding: prompt có dấu tiếng Việt qua API Ollama phải ra text có dấu chuẩn NFC (Tuần 13 sẽ dùng nghiêm túc, thấy mojibake thì soi encoding client trước khi nghi model).

## 7. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| ml-explore/mlx-lm (MIT, có LORA.md) | https://github.com/ml-explore/mlx-lm | 2 |
| Biderman et al. 2024, LoRA Learns Less and Forgets Less (CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2405.09673, PDF local: [`../docs/papers/`](../docs/papers/README.md) | 5 |

(Ollama, LM Studio, llama.cpp/GGUF: link trong README nguồn học, công cụ cài trên máy, tự xác minh version lúc cài. Các con số tốc độ trong tuần này do BẠN đo, không có số tham khảo nào đáng tin hơn máy của chính bạn.)

## Sau khi đọc xong

1. Cài `mlx-lm` trên Mac, chạy flow 3 lệnh (mục 2) theo [`02_mlx_commands.md`](02_mlx_commands.md).
2. Chốt bộ 10 prompt song ngữ TRƯỚC khi fine-tune (mục 5).
3. Dựng Ollama + LM Studio, đo tốc độ hai máy theo protocol mục 4.
4. Viết [`03_hardware_decision.md`](03_hardware_decision.md) từ số đo thật; làm [`quiz.md`](quiz.md).

## 8. Prefill, decode và KV cache: khung để đo inference đúng cách

Protocol đo tốc độ ở mục 4 cho một con số tokens mỗi giây. Mục này giải thích vì sao một con số là chưa đủ, dựa trên khung hai pha mà mọi engine serving (Ollama, MLX, llama.cpp, vLLM) đều dùng.

**Hai pha.** Xiao và Zhu (*Foundations of LLMs* mục 5.1.2, trang 207) xuất phát từ việc language modeling là quá trình tự hồi quy, sinh từng token điều kiện trên các token trước, và với Transformer điều đó đòi model duy trì một KV cache lưu các biểu diễn quá khứ để token mới attend vào. Nhìn từ góc KV cache, inference tách tự nhiên thành hai pha. **Prefilling** tính KV cache cho toàn bộ chuỗi đầu vào x: model chuẩn bị và lưu cặp key, value cho từng token của prompt; pha này xử lý nhiều token cùng lúc nên giống một forward pass batch. **Decoding** sinh từng token một, mỗi bước chỉ tính cho token mới rồi attend vào cache. Fleuret ghi single-stream inference "is bounded by memory size and speed far more than by computation" (*Little Book* mục 8.2, trang 154); [Suy luận] áp vào hai pha, decode là pha bị bộ nhớ giới hạn vì mỗi token đọc lại toàn bộ trọng số và cache, còn prefill nặng compute hơn vì gom nhiều token vào một lần nhân ma trận. Hệ quả cho việc đo: tốc độ prefill (token prompt mỗi giây) và tốc độ decode (token sinh mỗi giây) là hai số khác bản chất; prompt dài với câu trả lời ngắn và prompt ngắn với câu trả lời dài cho cảm giác nhanh chậm rất khác dù cùng model. Trong `03_hardware_decision.md`, ghi tách hai số này cho mỗi máy.

**KV cache lớn đến đâu và làm sao chặn nó.** Cache tăng tuyến tính theo độ dài chuỗi, và với chuỗi rất dài nó trở thành nút thắt bộ nhớ (mục nâng cao B1 tính công thức theo số layer, số head KV và chiều head). FoLLM mục 2.3.3.1 (trang 72) trình bày cách chặn bằng bộ nhớ Mem kích thước cố định: viết attention tại vị trí i là Att(q_i, Mem) với Mem = (K_{≤i}, V_{≤i}) trong trường hợp thường; nếu định nghĩa Mem có kích thước cố định thì chi phí mỗi bước cũng cố định. Hai cách đơn giản nhất: giữ một cửa sổ n_c cặp key, value gần nhất (local attention, eq. 2.53), hoặc thay lịch sử bằng một cặp vector tóm tắt như trung bình trượt của n_c cặp gần nhất. Sliding window attention ở mục nâng cao A6 là cách thứ nhất. Khi Ollama hay MLX cho phép đặt context length, chính là bạn đang chọn n_c này, và giới hạn 24 GB của Mac quyết định nó.

**Đo cái gì ngoài tốc độ.** FoLLM mục 5.1.4 (trang 221) nhắc rằng đánh giá inference gồm nhiều nhóm metric: độ chính xác (perplexity, F1), độ bền trước input mơ hồ hay lệch phân phối, và tính dùng được (trôi chảy, mạch lạc, đúng trọng tâm) thường cần người chấm. Bộ 10 prompt song ngữ ở mục 5 của tuần là phiên bản nhỏ của nhóm cuối; đừng để một con số tokens mỗi giây thay cho nó.

## Đọc thêm từ kệ sách

> Catalog và điều khoản ở [`../docs/books/README.md`](../docs/books/README.md). Số trang là trang in của bản PDF đã tải ngày 2026-09-04; câu trong ngoặc kép là trích nguyên văn.

- **Prefill và decode.** Xiao và Zhu, *Foundations of LLMs* mục 5.1 Prefilling and Decoding (trang 204) mô tả khung hai pha mà mọi engine serving (Ollama, MLX, vLLM) đều dùng: xử lý prompt một lượt, rồi sinh từng token. Mục 2.3.3.1 Fixed-size KV Cache bàn cách chặn KV cache khỏi phình theo độ dài chuỗi, đúng nút thắt VRAM ở mục nâng cao B1.
