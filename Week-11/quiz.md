# Tuần 11, Quiz: QLoRA fine-tuning thực tế (Unsloth)

> Tự kiểm tra **trước** khi xem solution. Tổng **16** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

QLoRA = ?

- **A.** LoRA cho mô hình vision
- **B.** Lượng tử hoá cả adapter xuống 4-bit
- **C.** LoRA chạy trên nhiều GPU
- **D.** Quantize base model xuống 4-bit (NF4, đóng băng) + chỉ train adapter LoRA ở bf16

## Câu 2 (Trắc nghiệm)

Muốn biết workload QLoRA vừa VRAM, cần làm gì?

- **A.** Đo peak memory với model, batch, context, dtype, optimizer và runtime đang dùng
- **B.** Chỉ lấy số weights nhân 4 bit
- **C.** Dùng số của một máy khác làm cam kết
- **D.** Chỉ nhìn dung lượng file tải xuống

## Câu 3 (Tự luận)

Liệt kê config QLoRA hợp lý cho GPU 8GB.

## Câu 4 (Trắc nghiệm)

[Nâng cao] NF4 (trong QLoRA) là gì?

- **A.** Kiểu lượng tử hoá 4-bit 'normal float', phân bố các mức tối ưu cho trọng số gần Gaussian
- **B.** Một optimizer
- **C.** Một định dạng file model
- **D.** Một loại attention

## Câu 5 (Trắc nghiệm)

[Nâng cao] GGUF là gì?

- **A.** Một kiểu attention
- **B.** Một ĐỊNH DẠNG FILE của llama.cpp (chứa weight + metadata, các k-quant như Q4_K_M) mà Ollama/LM Studio load
- **C.** Một benchmark
- **D.** Một thuật toán lượng tử hoá mới

## Câu 6 (Tự luận)

Khi nào nên ngừng fine-tune local và chuyển lên cloud (4090/A100)?

## Câu 7 (Trắc nghiệm)

Fleuret giải thích vì sao model có thể chạy suy luận ở 4 đến 6 bit mỗi tham số mà vẫn tốt, trong khi huấn luyện vẫn cần 16 hoặc 32 bit. Lý do là gì?

- **A.** Sai số lượng tử hóa khi suy luận bị bù bởi softmax cuối cùng, còn khi huấn luyện gradient không đi qua softmax
- **B.** Suy luận chỉ dùng trọng số attention còn huấn luyện dùng toàn bộ trọng số, nên nhạy hơn với sai số làm tròn
- **C.** Activation là tổng của nhiều hạng tử nên sai số lượng tử hóa được trung bình hóa, còn huấn luyện cần tích lũy các thay đổi rất nhỏ
- **D.** Suy luận có thể giải lượng tử về FP16 trước mỗi phép nhân ma trận, còn huấn luyện không có thời gian làm việc đó

## Câu 8 (Trắc nghiệm)

Fleuret lấy Q4_1 của llama.cpp làm ví dụ: mỗi khối 32 trọng số được lưu bằng một scale d và một bias m ở FP16 cộng 32 giá trị 4 bit. Kích thước khối trước và sau lượng tử hóa là bao nhiêu?

- **A.** 64 byte xuống 16 byte, vì d và m được gộp chung vào một byte cùng với bit dấu
- **B.** 64 byte xuống 24 byte, gồm 8 byte cho d và m cộng 16 byte cho 32 giá trị 4 bit
- **C.** 64 byte xuống 20 byte, gồm 4 byte cho d và m cộng 16 byte cho 32 giá trị 4 bit
- **D.** 128 byte xuống 20 byte, vì trọng số gốc của các model này được lưu ở FP32

## Câu 9 (Trắc nghiệm)

Fleuret phân biệt Post-Training Quantization và Quantization-Aware Training. Điểm khác cốt lõi của QAT là gì?

- **A.** QAT lượng tử hóa cả tham số lẫn gradient trong lúc huấn luyện để tiết kiệm bộ nhớ tối đa trên GPU nhỏ
- **B.** QAT huấn luyện lại toàn bộ model từ đầu ở 4 bit, không tái sử dụng trọng số pretrained của base model
- **C.** QAT áp dụng lượng tử hóa trong forward pass nhưng giữ tham số và gradient ở độ chính xác cao, backward pass lan truyền như không có lượng tử hóa
- **D.** QAT chỉ lượng tử hóa sau khi huấn luyện xong nhưng dùng dữ liệu hiệu chuẩn để chọn scale cho từng khối

## Câu 10 (Trắc nghiệm)

Bảng 1.1 của The State of Open Source AI tách quyền sử dụng một model thành ba cột riêng. Ba cột đó là gì, và quan sát nào được rút ra?

- **A.** Code, giấy phép và điều khoản dịch vụ; code thường mở còn điều khoản dịch vụ thường cấm dùng thương mại
- **B.** Trọng số, dữ liệu huấn luyện và output sinh ra; trọng số thường không bị giữ kín, còn dữ liệu huấn luyện hiếm khi được công bố
- **C.** Trọng số, checkpoint trung gian và log huấn luyện; chỉ trọng số cuối cùng được công bố rộng rãi
- **D.** Kiến trúc, tokenizer và benchmark; kiến trúc thường mở còn kết quả benchmark nội bộ thường bị giấu

## Câu 11 (Trắc nghiệm)

Theo The State of Open Source AI, từ góc độ pháp lý, giấy phép "open" chia thành ba nhóm nhỏ. Nhóm nào yêu cầu tác phẩm phái sinh phải dùng cùng giấy phép?

- **A.** Copyleft, với ví dụ GPL-3.0 và CC-BY-SA-4.0, ràng buộc cả bản phái sinh
- **B.** Community licence, với ví dụ giấy phép riêng của một số model lớn
- **C.** Permissive, với ví dụ Apache-2.0 và CC-BY-4.0, chỉ cần ghi tên tác giả
- **D.** Public Domain, với ví dụ Unlicence và CC0-1.0, mức tối thiểu theo luật

## Câu 12 (Trắc nghiệm)

FoLLM tóm tắt các kỹ thuật suy luận hiệu quả bằng hai trade-off chính. Quantization và pruning thuộc trade-off nào, và mặt trái mà FoLLM nêu là gì?

- **A.** Trade-off throughput và latency; mặt trái là batch lớn làm tăng thời gian chờ của từng request
- **B.** Trade-off bộ nhớ và tính toán; mặt trái là phải tính lại self-attention cho các token đã qua
- **C.** Trade-off độ dài ngữ cảnh và bộ nhớ; mặt trái là mất thông tin ở các token xa vị trí hiện tại
- **D.** Trade-off tốc độ và độ chính xác; mặt trái là có thể gây suy giảm nhỏ về chất lượng của model

## Câu 13 (Tự luận)

The State of Open Source AI cho rằng một model ML có thể đồng thời chịu nhiều giấy phép thuộc các nhóm khác nhau. Hãy giải thích lập luận này và nêu hệ quả thực tế khi bạn chọn base model và dataset cho QLoRA.

## Câu 14 (Tự luận)

Fleuret nhận xét rằng triển khai LLM cho một người dùng thường là single-stream inference. Vì sao đặc điểm này làm lượng tử hóa vừa giảm bộ nhớ vừa tăng tốc, và điều đó nối với khung prefill/decode của FoLLM thế nào?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

AWQ (arXiv 2306.00978) bảo vệ khoảng 1% trọng số 'salient'. Theo paper, tín hiệu nào cho biết kênh nào là salient, và vì sao họ không dùng mixed precision?

- **A.** Phân phối activation, không phải trọng số; thay vì trộn độ chính xác (khó tối ưu trên phần cứng) họ nhân scale các kênh salient bằng một phép biến đổi tương đương
- **B.** Entropy của token
- **C.** Gradient khi fine-tune
- **D.** Độ lớn của trọng số; mixed precision quá đắt để tính

## Nâng cao 2 (Tự luận)

QLoRA quantize base model xuống 4-bit nhưng vẫn train được. Hãy nêu ba thành phần paper đặt tên và giải thích vì sao adapter không bị quantize.

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
