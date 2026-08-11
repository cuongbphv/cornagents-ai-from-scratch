"""
qlora_finetune.py — STARTER Tuần 8 (Unsloth QLoRA, 8GB-friendly).

Khác với Phase 1: ở đây dùng tooling production. Đây là starter để bạn
chạy + tinh chỉnh, KHÔNG phải skeleton TODO. Vẫn nên đọc kỹ từng dòng.

Cài (trên máy có CUDA):
    pip install unsloth
    # xem unsloth.ai/docs cho lệnh khớp CUDA/torch của bạn

CHÚ Ý: file này CẦN GPU + Unsloth, không chạy trong môi trường thường.
Điền phần load dataset (phần TODO) theo dữ liệu của bạn.
"""

MAX_SEQ_LEN = 1024          # 8GB: giữ ≤ 1024
MODEL = "unsloth/Meta-Llama-3.1-8B-bnb-4bit"   # hoặc Qwen2.5-7B-bnb-4bit


def main():
    from unsloth import FastLanguageModel
    from trl import SFTTrainer
    from transformers import TrainingArguments

    # 1) Load model 4-bit
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL,
        max_seq_length=MAX_SEQ_LEN,
        load_in_4bit=True,
    )

    # 2) Gắn LoRA adapter
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        lora_alpha=16,
        lora_dropout=0.0,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        use_gradient_checkpointing="unsloth",
        random_state=42,
    )

    # 3) Dataset — TODO: thay bằng dữ liệu của bạn (gợi ý: Finance Banking Q&A)
    #    Format mỗi mẫu thành 1 chuỗi prompt+response (chat template hoặc Alpaca).
    #    Ví dụ dùng HF datasets:
    #       from datasets import load_dataset
    #       ds = load_dataset("json", data_files="data/train.jsonl")["train"]
    #       def fmt(ex): return {"text": f"### Q:\n{ex['q']}\n\n### A:\n{ex['a']}"}
    #       ds = ds.map(fmt)
    raise NotImplementedError("TODO: load + format dataset của bạn vào biến `ds`")

    # 4) Trainer (8GB: batch 1–2, dùng grad accumulation để tăng effective batch)
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=ds,                 # noqa: F821 (định nghĩa ở bước 3)
        dataset_text_field="text",
        max_seq_length=MAX_SEQ_LEN,
        args=TrainingArguments(
            per_device_train_batch_size=1,
            gradient_accumulation_steps=8,
            warmup_steps=10,
            num_train_epochs=1,
            learning_rate=2e-4,
            fp16=True,
            logging_steps=10,
            optim="adamw_8bit",
            output_dir="outputs",
        ),
    )
    trainer.train()

    # 5) Lưu adapter + export GGUF (chạy Ollama ở Tuần 9)
    model.save_pretrained("lora_adapter")
    # model.save_pretrained_gguf("gguf_model", tokenizer, quantization_method="q4_k_m")
    print("Xong. Adapter ở ./lora_adapter")


if __name__ == "__main__":
    main()
