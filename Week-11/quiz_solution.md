# Tuần 11, Đáp án & Giải thích: QLoRA fine-tuning thực tế (Unsloth)

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

QLoRA = ?

- **A.** LoRA cho mô hình vision
- **B.** Lượng tử hoá cả adapter xuống 4-bit
- **C.** LoRA chạy trên nhiều GPU
- **D.** Quantize base model xuống 4-bit (NF4, đóng băng) + chỉ train adapter LoRA ở bf16 (đáp án đúng)

**Đáp án: D**

**Giải thích:** Quantization giảm phần bộ nhớ base weights; peak VRAM vẫn phụ thuộc toàn cấu hình và workload.

## Câu 2 (Trắc nghiệm)

Muốn biết workload QLoRA vừa VRAM, cần làm gì?

- **A.** Đo peak memory với model, batch, context, dtype, optimizer và runtime đang dùng (đáp án đúng)
- **B.** Chỉ lấy số weights nhân 4 bit
- **C.** Dùng số của một máy khác làm cam kết
- **D.** Chỉ nhìn dung lượng file tải xuống

**Đáp án: A**

**Giải thích:** Theo tài liệu chương trình mục 1.1 và 10.6: đo toàn workload, không suy từ weights riêng.

## Câu 3 (Tự luận)

Liệt kê config QLoRA hợp lý cho GPU 8GB.

**Trả lời mẫu:** load_in_4bit=True; batch_size 1-2; sequence length ≤ 1024; gradient_checkpointing=True; LoRA r=16, lora_alpha=16; target tất cả projection của attention + MLP. Nếu vẫn sát giới hạn: giảm seq len, tăng gradient accumulation, hoặc dùng Colab T4 15GB.

**Giải thích:** Threshold: nếu OOM ở batch 1 hoặc run >24h → chuyển 4090/A100 thuê.

## Câu 4 (Trắc nghiệm)

[Nâng cao] NF4 (trong QLoRA) là gì?

- **A.** Kiểu lượng tử hoá 4-bit 'normal float', phân bố các mức tối ưu cho trọng số gần Gaussian (đáp án đúng)
- **B.** Một optimizer
- **C.** Một định dạng file model
- **D.** Một loại attention

**Đáp án: A**

**Giải thích:** NF4 đặt các mức lượng tử theo phân vị của phân phối chuẩn → ít sai số hơn int4 đều cho trọng số ~Gaussian.

## Câu 5 (Trắc nghiệm)

[Nâng cao] GGUF là gì?

- **A.** Một kiểu attention
- **B.** Một ĐỊNH DẠNG FILE của llama.cpp (chứa weight + metadata, các k-quant như Q4_K_M) mà Ollama/LM Studio load (đáp án đúng)
- **C.** Một benchmark
- **D.** Một thuật toán lượng tử hoá mới

**Đáp án: B**

**Giải thích:** GGUF là định dạng đóng gói, không phải thuật toán; nhầm lẫn này rất phổ biến. Tuần 12 sẽ load GGUF qua Ollama.

## Câu 6 (Tự luận)

Khi nào nên ngừng fine-tune local và chuyển lên cloud (4090/A100)?

**Trả lời mẫu:** Khi một lần fine-tune dự kiến chạy >24h ở local, hoặc khi OOM ngay cả ở batch size 1 (sau khi đã bật 4-bit, gradient checkpointing, giảm seq len). Lúc đó thuê RTX 4090/A100 sẽ rẻ hơn nhiều về thời gian.

**Giải thích:** Đây là 'ngưỡng kích hoạt cloud' của roadmap; verify bằng smoke test ngắn trước khi cam kết run dài.

## Câu 7 (Trắc nghiệm)

Fleuret giải thích vì sao model có thể chạy suy luận ở 4 đến 6 bit mỗi tham số mà vẫn tốt, trong khi huấn luyện vẫn cần 16 hoặc 32 bit. Lý do là gì?

- **A.** Sai số lượng tử hóa khi suy luận bị bù bởi softmax cuối cùng, còn khi huấn luyện gradient không đi qua softmax
- **B.** Suy luận chỉ dùng trọng số attention còn huấn luyện dùng toàn bộ trọng số, nên nhạy hơn với sai số làm tròn
- **C.** Activation là tổng của nhiều hạng tử nên sai số lượng tử hóa được trung bình hóa, còn huấn luyện cần tích lũy các thay đổi rất nhỏ (đáp án đúng)
- **D.** Suy luận có thể giải lượng tử về FP16 trước mỗi phép nhân ma trận, còn huấn luyện không có thời gian làm việc đó

**Đáp án: C**

**Giải thích:** Fleuret: "The precision it provides is necessary for training, to allow gradual changes to accumulate. However, since activations are the sums of many terms, quantization during inference is mitigated by an averaging effect." Điều này càng đúng với kiến trúc lớn; model 6 hay 4 bit "exhibit remarkable performance". Đây cũng là nền của QLoRA: base quantized, adapter không quantized. (Fleuret mục 8.2, tr. 153)

## Câu 8 (Trắc nghiệm)

Fleuret lấy Q4_1 của llama.cpp làm ví dụ: mỗi khối 32 trọng số được lưu bằng một scale d và một bias m ở FP16 cộng 32 giá trị 4 bit. Kích thước khối trước và sau lượng tử hóa là bao nhiêu?

- **A.** 64 byte xuống 16 byte, vì d và m được gộp chung vào một byte cùng với bit dấu
- **B.** 64 byte xuống 24 byte, gồm 8 byte cho d và m cộng 16 byte cho 32 giá trị 4 bit
- **C.** 64 byte xuống 20 byte, gồm 4 byte cho d và m cộng 16 byte cho 32 giá trị 4 bit (đáp án đúng)
- **D.** 128 byte xuống 20 byte, vì trọng số gốc của các model này được lưu ở FP32

**Đáp án: C**

**Giải thích:** Fleuret: "Such a block was encoded originally as 32 values in FP16, hence 64 bytes, while the quantized version needs 4 bytes for d and m and 32 · 4 bits = 16 bytes for the entries, hence a total of 20 bytes." Giá trị giải lượng tử là x̃ = dq + m với q trong {0, ..., 2^4 − 1}. (Fleuret mục 8.2, tr. 154-155)

## Câu 9 (Trắc nghiệm)

Fleuret phân biệt Post-Training Quantization và Quantization-Aware Training. Điểm khác cốt lõi của QAT là gì?

- **A.** QAT lượng tử hóa cả tham số lẫn gradient trong lúc huấn luyện để tiết kiệm bộ nhớ tối đa trên GPU nhỏ
- **B.** QAT huấn luyện lại toàn bộ model từ đầu ở 4 bit, không tái sử dụng trọng số pretrained của base model
- **C.** QAT áp dụng lượng tử hóa trong forward pass nhưng giữ tham số và gradient ở độ chính xác cao, backward pass lan truyền như không có lượng tử hóa (đáp án đúng)
- **D.** QAT chỉ lượng tử hóa sau khi huấn luyện xong nhưng dùng dữ liệu hiệu chuẩn để chọn scale cho từng khối

**Đáp án: C**

**Giải thích:** Fleuret: "An alternative to Post-Training Quantization is Quantization-Aware Training that applies quantization during the forward pass but keeps high-precision encoding of parameters and gradients, and propagates the gradients during the backward pass as if there was no quantization". (Fleuret mục 8.2, tr. 155)

## Câu 10 (Trắc nghiệm)

Bảng 1.1 của The State of Open Source AI tách quyền sử dụng một model thành ba cột riêng. Ba cột đó là gì, và quan sát nào được rút ra?

- **A.** Code, giấy phép và điều khoản dịch vụ; code thường mở còn điều khoản dịch vụ thường cấm dùng thương mại
- **B.** Trọng số, dữ liệu huấn luyện và output sinh ra; trọng số thường không bị giữ kín, còn dữ liệu huấn luyện hiếm khi được công bố (đáp án đúng)
- **C.** Trọng số, checkpoint trung gian và log huấn luyện; chỉ trọng số cuối cùng được công bố rộng rãi
- **D.** Kiến trúc, tokenizer và benchmark; kiến trúc thường mở còn kết quả benchmark nội bộ thường bị giấu

**Đáp án: B**

**Giải thích:** Bảng 1.1 có ba cột Weights, Training Data và Output. Các quan sát của sách: "Pre-trained model weights are typically not closely guarded", "Generated outputs often are usable commercially, but with conditions", "Training data is seldom available". Khi chọn base model để QLoRA, cần kiểm tra riêng từng cột này tại thời điểm dùng. (State of Open Source AI mục 1.1, tr. 9-10)

## Câu 11 (Trắc nghiệm)

Theo The State of Open Source AI, từ góc độ pháp lý, giấy phép "open" chia thành ba nhóm nhỏ. Nhóm nào yêu cầu tác phẩm phái sinh phải dùng cùng giấy phép?

- **A.** Copyleft, với ví dụ GPL-3.0 và CC-BY-SA-4.0, ràng buộc cả bản phái sinh (đáp án đúng)
- **B.** Community licence, với ví dụ giấy phép riêng của một số model lớn
- **C.** Permissive, với ví dụ Apache-2.0 và CC-BY-4.0, chỉ cần ghi tên tác giả
- **D.** Public Domain, với ví dụ Unlicence và CC0-1.0, mức tối thiểu theo luật

**Đáp án: A**

**Giải thích:** Table 1.2: Public Domain (mức tối thiểu theo luật, về kỹ thuật không phải giấy phép), Permissive (ghi tên tác giả gốc), Copyleft với điều kiện "Derivatives use the same licence", ví dụ GPL-3.0 và CC-BY-SA-4.0. Sách cũng lưu ý từ "open" đứng một mình là mơ hồ vì có thể chỉ open licence hoặc open source code. (State of Open Source AI mục 1.3, tr. 10)

## Câu 12 (Trắc nghiệm)

FoLLM tóm tắt các kỹ thuật suy luận hiệu quả bằng hai trade-off chính. Quantization và pruning thuộc trade-off nào, và mặt trái mà FoLLM nêu là gì?

- **A.** Trade-off throughput và latency; mặt trái là batch lớn làm tăng thời gian chờ của từng request
- **B.** Trade-off bộ nhớ và tính toán; mặt trái là phải tính lại self-attention cho các token đã qua
- **C.** Trade-off độ dài ngữ cảnh và bộ nhớ; mặt trái là mất thông tin ở các token xa vị trí hiện tại
- **D.** Trade-off tốc độ và độ chính xác; mặt trái là có thể gây suy giảm nhỏ về chất lượng của model (đáp án đúng)

**Đáp án: D**

**Giải thích:** FoLLM: "One important trade-off is between inference speed and accuracy. For example, techniques like quantization, pruning, and knowledge distillation can significantly reduce computational overhead and latency but may introduce minor degradations in model performance." Trade-off thứ hai là memory-compute, ví dụ KV cache đổi bộ nhớ lấy việc không phải tính lại attention. (FoLLM mục 5.2.4, tr. 233)

## Câu 13 (Tự luận)

The State of Open Source AI cho rằng một model ML có thể đồng thời chịu nhiều giấy phép thuộc các nhóm khác nhau. Hãy giải thích lập luận này và nêu hệ quả thực tế khi bạn chọn base model và dataset cho QLoRA.

**Trả lời mẫu:** Sách lập luận rằng một model được định nghĩa một phần bằng code (kiến trúc, quy trình huấn luyện) và một phần bằng tham số, mà tham số lại được định nghĩa ngầm bởi dữ liệu huấn luyện; do đó trọng số là sản phẩm của cả code lẫn dữ liệu và phải chịu cùng lúc giấy phép cho code và giấy phép cho nội dung, hai loại giấy phép vốn không được thiết kế để dùng chung và có thể không tương thích. Hệ quả là khi chọn base model và dataset, bạn phải kiểm tra riêng giấy phép trọng số, tình trạng dữ liệu huấn luyện và điều khoản với output, và ghi ngày tra cứu vì các điều khoản này thay đổi nhanh. Sách nêu ví dụ Falcon đổi sang Apache-2.0 và LLaMA-2 community licence chỉ vài tuần sau khi có người tuyên bố thời kỳ open AI sắp kết thúc.

**Giải thích:** State of Open Source AI: "A working model is defined partially in code (architecture & training regimen) and partially by its parameters (trained weights, i.e. a list of numbers). The latter is implicitly defined by the training data ... One could therefore argue that models must be simultaneously bound by multiple licences for multiple different domains. Such licences were not designed to work simultaneously, and may not even be compatible." Mục 1.2 nói thêm điều này "may be problematic or even nonsensical". (State of Open Source AI mục 1.1-1.2, tr. 9-10)

## Câu 14 (Tự luận)

Fleuret nhận xét rằng triển khai LLM cho một người dùng thường là single-stream inference. Vì sao đặc điểm này làm lượng tử hóa vừa giảm bộ nhớ vừa tăng tốc, và điều đó nối với khung prefill/decode của FoLLM thế nào?

**Trả lời mẫu:** Theo Fleuret, single-stream inference bị giới hạn bởi dung lượng và tốc độ bộ nhớ nhiều hơn là bởi tính toán, nên khi mỗi tham số chỉ còn 4 đến 6 bit thì lượng dữ liệu phải đọc mỗi bước giảm theo, và tốc độ suy luận tăng đáng kể chứ không chỉ tiết kiệm VRAM. Điều này khớp với FoLLM: giai đoạn decoding sinh từng token và truy cập KV cache liên tục nên là memory-bound, trong khi prefilling xử lý cả prompt song song và là compute-bound. Nối hai nguồn lại thì phần được lợi về tốc độ khi chạy model 4-bit local là giai đoạn decode; đây là suy luận nối hai nguồn, bạn cần tự đo prefill và decode riêng để xác nhận.

**Giải thích:** Fleuret: "deployment of a Large Language Model for individual use requires generally single-stream inference, which is bounded by memory size and speed far more than by computation" và "In addition to reducing the memory footprint, quantization also improves inference speed significantly." FoLLM: "the prefilling process is considered compute-bound" còn decoding "is memory-bound due to its frequent access to the KV cache". (Fleuret mục 8.2, tr. 153; FoLLM mục 5.1.2, tr. 209-210)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

AWQ (arXiv 2306.00978) bảo vệ khoảng 1% trọng số 'salient'. Theo paper, tín hiệu nào cho biết kênh nào là salient, và vì sao họ không dùng mixed precision?

- **A.** Phân phối activation, không phải trọng số; thay vì trộn độ chính xác (khó tối ưu trên phần cứng) họ nhân scale các kênh salient bằng một phép biến đổi tương đương (đáp án đúng)
- **B.** Entropy của token
- **C.** Gradient khi fine-tune
- **D.** Độ lớn của trọng số; mixed precision quá đắt để tính

**Đáp án: A**

**Giải thích:** Abstract AWQ: 'To identify salient weight channels, we should refer to the activation distribution, not weights' và 'To avoid the hardware-inefficient mix-precision quantization, we mathematically derive that scaling up the salient channels can reduce the quantization error'.

## Nâng cao 2 (Tự luận)

QLoRA quantize base model xuống 4-bit nhưng vẫn train được. Hãy nêu ba thành phần paper đặt tên và giải thích vì sao adapter không bị quantize.

**Trả lời mẫu:** Ba thành phần: NF4, kiểu dữ liệu 4-bit 'information theoretically optimal for normally distributed weights'; double quantization, quantize cả các hằng số quantization; paged optimizers để xử lý đỉnh bộ nhớ (arXiv 2305.14314, abstract). Gradient được lan ngược qua base đã đóng băng và quantize vào adapter LoRA; adapter là phần đang học, cần tích lũy thay đổi nhỏ nên giữ ở độ chính xác cao hơn, đúng lý do Fleuret nêu cho training (Little Book mục 8.2).

**Giải thích:** Kết quả paper báo: fine-tune model 65B trên một GPU 48GB mà giữ hiệu năng full 16-bit.
