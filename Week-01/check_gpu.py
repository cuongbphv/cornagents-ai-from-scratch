"""
check_gpu.py — Kiểm tra PyTorch nhìn thấy GPU (CUDA trên RTX 3070 Ti hoặc MPS trên Mac).
Chạy:  python check_gpu.py
"""

import platform


def main():
    print("=" * 50)
    print(" KIỂM TRA MÔI TRƯỜNG PYTORCH / GPU")
    print("=" * 50)
    print(f"Hệ điều hành : {platform.platform()}")

    try:
        import torch
    except ImportError:
        print("\n[LỖI] Chưa cài PyTorch. Cài bằng:")
        print("  pip install torch    (xem hướng dẫn theo CUDA tại pytorch.org)")
        return

    print(f"PyTorch      : {torch.__version__}")

    # --- CUDA (NVIDIA, ví dụ RTX 3070 Ti) ---
    if torch.cuda.is_available():
        idx = torch.cuda.current_device()
        name = torch.cuda.get_device_name(idx)
        total = torch.cuda.get_device_properties(idx).total_memory / 1024**3
        print("\n[OK] CUDA khả dụng")
        print(f"  GPU         : {name}")
        print(f"  VRAM tổng   : {total:.1f} GB")
        print(f"  CUDA version: {torch.version.cuda}")
        device = "cuda"
    # --- MPS (Apple Silicon Mac) ---
    elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        print("\n[OK] Apple MPS khả dụng (Mac)")
        device = "mps"
    else:
        print("\n[CHÚ Ý] Không thấy GPU — sẽ chạy trên CPU (vẫn ổn cho Tuần 1).")
        device = "cpu"

    # --- Test nhỏ: nhân ma trận trên device ---
    print(f"\nChạy thử phép nhân ma trận trên: {device}")
    x = torch.randn(1000, 1000, device=device)
    y = torch.randn(1000, 1000, device=device)
    z = x @ y
    print(f"  Kết quả shape: {tuple(z.shape)}  | mean={z.mean().item():.4f}")
    print("\n=> Môi trường sẵn sàng cho Tuần 1.")


if __name__ == "__main__":
    main()
