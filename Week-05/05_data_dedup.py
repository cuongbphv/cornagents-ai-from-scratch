"""
05_data_dedup.py — SKELETON Tuần 5: data curation & dedup trước khi pretrain.

Mục tiêu: TỰ TAY code pipeline lọc dữ liệu kiểu FineWeb thu nhỏ:
    (a) exact dedup qua hash chuẩn hóa,
    (b) near-dedup bằng MinHash from scratch,
    (c) 2-3 quality filter heuristic,
    (d) in báo cáo giữ/loại theo từng bước.
Triết lý của roadmap: TỰ code trước, nhờ Claude review sau. Đừng copy lời giải.

Ý tưởng các bước lấy từ paper FineWeb (Penedo et al. 2024, arXiv 2406.17557,
CC BY 4.0 — PDF local: ../docs/papers/2406.17557_fineweb-datasets.pdf):
  - §3.4: MinHash trên 5-gram (word-level), 112 hash function chia 14 bucket
    x 8 hash, nhắm các document giống nhau >= 75%.
  - §3.6: 3 filter được chọn sau ablation: tỷ lệ dòng kết thúc bằng dấu câu
    <= 0.12 -> loại; tỷ lệ ký tự nằm trong các dòng lặp >= 0.1 -> loại;
    tỷ lệ dòng ngắn hơn 30 ký tự >= 0.67 -> loại. (Kiểm PDF 2026-08-16.)
Ở đây ta làm bản mini: ít hash hơn, so cặp trực tiếp thay vì bucket LSH.

Chỉ dùng stdlib. Dữ liệu vào là MỘT file text local (mỗi document cách nhau
một dòng trống). Tùy chọn: nếu có mạng + thư viện `datasets`, có thể tải
một mẩu FineWeb-Edu (xem tải_fineweb_edu_sample bên dưới) — KHÔNG bắt buộc.

Chạy:  python 05_data_dedup.py duong_dan_file.txt
       python 05_data_dedup.py --fineweb   (tùy chọn, cần `pip install datasets`)
"""

import hashlib
import random
import sys

# ----------------------------------------------------------------------
# 0) Nạp documents (khung có sẵn — không cần sửa)
# ----------------------------------------------------------------------

def load_docs_from_file(path):
    """Đọc file text; mỗi document cách nhau >= 1 dòng trống."""
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    docs = [d.strip() for d in raw.split("\n\n") if d.strip()]
    return docs


def load_fineweb_edu_sample(n=200):
    """TÙY CHỌN: tải n document đầu của FineWeb-Edu sample-10BT (cần mạng)."""
    try:
        from datasets import load_dataset
        ds = load_dataset(
            "HuggingFaceFW/fineweb-edu", name="sample-10BT",
            split="train", streaming=True,
        )
        return [row["text"] for _, row in zip(range(n), ds)]
    except Exception as e:
        print(f"Không tải được FineWeb-Edu ({type(e).__name__}: {e}).")
        print("Dùng file local thay thế:  python 05_data_dedup.py file.txt")
        sys.exit(1)


# ----------------------------------------------------------------------
# 1) Exact dedup — hash trên văn bản đã chuẩn hóa
# ----------------------------------------------------------------------

def normalize_text(text):
    # TODO 1: chuẩn hóa văn bản trước khi hash, để "cùng nội dung, khác
    #   trình bày" vẫn ra cùng hash. Gợi ý tối thiểu:
    #   - lowercase
    #   - gộp mọi chuỗi whitespace (kể cả xuống dòng) thành 1 dấu cách
    #     (vd. " ".join(text.split()))
    #   Trả về chuỗi đã chuẩn hóa.
    raise NotImplementedError("TODO 1: chuẩn hóa văn bản")


def exact_dedup(docs):
    # TODO 2: exact dedup.
    #   - Với mỗi doc: hashlib.sha256(normalize_text(doc).encode("utf-8")).hexdigest()
    #   - Giữ doc ĐẦU TIÊN của mỗi hash, loại các doc sau có hash trùng
    #     (dùng một set các hash đã thấy).
    #   Trả về list docs đã khử trùng lặp, GIỮ NGUYÊN thứ tự.
    raise NotImplementedError("TODO 2: exact dedup qua hash")


# ----------------------------------------------------------------------
# 2) Near-dedup — MinHash from scratch
# ----------------------------------------------------------------------

MERSENNE_P = (1 << 61) - 1  # số nguyên tố lớn cho (a*x + b) mod p
NUM_HASHES = 64             # FineWeb dùng 112; bản mini dùng 64
SHINGLE_K = 5               # FineWeb dùng 5-gram (word-level), §3.4
NEAR_DUP_THRESHOLD = 0.8    # ngưỡng Jaccard ước lượng để coi là near-dup


def make_hash_params(num_hashes=NUM_HASHES, seed=0):
    """Sinh (a, b) cho num_hashes hàm hash dạng (a*x + b) mod p (có sẵn)."""
    rng = random.Random(seed)
    return [(rng.randrange(1, MERSENNE_P), rng.randrange(0, MERSENNE_P))
            for _ in range(num_hashes)]


def shingles(text, k=SHINGLE_K):
    # TODO 3: shingling k-gram mức TỪ (giống FineWeb §3.4 dùng 5-gram từ).
    #   - words = normalize_text(text).split()
    #   - trả về set các tuple k từ liên tiếp: {tuple(words[i:i+k]) ...}
    #   - nếu văn bản < k từ thì trả về set chứa 1 tuple toàn bộ words
    #     (để doc quá ngắn vẫn có signature).
    raise NotImplementedError("TODO 3: shingling k-gram")


def minhash_signature(text, hash_params):
    # TODO 4: tính MinHash signature.
    #   - Đổi mỗi shingle thành số nguyên x:
    #       int.from_bytes(hashlib.sha256(" ".join(shingle).encode()).digest()[:8], "big")
    #   - Với từng (a, b) trong hash_params: giá trị signature thứ j
    #     = min((a*x + b) % MERSENNE_P trên MỌI shingle x).
    #   Trả về list dài len(hash_params).
    #   Ý nghĩa: P(min-hash trùng nhau giữa 2 tập) = Jaccard của 2 tập đó.
    raise NotImplementedError("TODO 4: MinHash signature qua (a*x+b) mod p")


def estimate_jaccard(sig_a, sig_b):
    # TODO 5: ước lượng Jaccard từ 2 signature cùng độ dài:
    #   = (số vị trí j mà sig_a[j] == sig_b[j]) / len(sig_a)
    raise NotImplementedError("TODO 5: ước lượng Jaccard từ signature")


def near_dedup(docs, threshold=NEAR_DUP_THRESHOLD):
    # TODO 6: near-dedup bằng so cặp signature (O(n^2) — đủ cho sample nhỏ;
    #   FineWeb ở quy mô thật dùng bucket LSH 14x8 thay vì so mọi cặp).
    #   - hash_params = make_hash_params()
    #   - tính signature cho mọi doc
    #   - duyệt docs theo thứ tự; doc i bị LOẠI nếu estimate_jaccard với
    #     một doc ĐÃ GIỮ nào đó >= threshold (giữ bản xuất hiện trước).
    #   Trả về list docs được giữ.
    raise NotImplementedError("TODO 6: near-dedup bằng MinHash")


# ----------------------------------------------------------------------
# 3) Quality filters — heuristic kiểu FineWeb §3.6
# ----------------------------------------------------------------------

def passes_quality(text):
    # TODO 7: trả về True nếu doc vượt CẢ 3 heuristic (ngưỡng lấy từ
    #   FineWeb §3.6 — với sample nhỏ/tiếng khác, cứ chỉnh rồi quan sát):
    #   (a) tỷ lệ dòng kết thúc bằng dấu câu (. ! ? ") > 0.12
    #       (FineWeb loại doc có tỷ lệ <= 0.12)
    #   (b) tỷ lệ dòng ngắn hơn 30 ký tự < 0.67
    #       (FineWeb loại doc có tỷ lệ >= 0.67)
    #   (c) tỷ lệ ký tự nằm trong các DÒNG bị lặp (xuất hiện >= 2 lần
    #       trong doc) < 0.1  (FineWeb loại doc có tỷ lệ >= 0.1)
    #   Gợi ý: lines = [l for l in text.splitlines() if l.strip()];
    #   doc không có dòng nào -> False luôn.
    raise NotImplementedError("TODO 7: 3 quality filter heuristic")


def quality_filter(docs):
    """Áp passes_quality lên từng doc (có sẵn)."""
    return [d for d in docs if passes_quality(d)]


# ----------------------------------------------------------------------
# 4) Pipeline + báo cáo (khung có sẵn)
# ----------------------------------------------------------------------

def report_step(name, before, after):
    removed = before - after
    pct = 100.0 * removed / before if before else 0.0
    print(f"{name:<28} giữ {after:>5} / {before:>5}  (loại {removed}, {pct:.1f}%)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    if sys.argv[1] == "--fineweb":
        docs = load_fineweb_edu_sample()
    else:
        docs = load_docs_from_file(sys.argv[1])
    print(f"Nạp {len(docs)} documents.\n")

    n0 = len(docs)
    docs = exact_dedup(docs)
    report_step("(a) exact dedup", n0, len(docs))

    n1 = len(docs)
    docs = near_dedup(docs)
    report_step("(b) near-dedup MinHash", n1, len(docs))

    n2 = len(docs)
    docs = quality_filter(docs)
    report_step("(c) quality filters", n2, len(docs))

    print(f"\nTổng kết: {len(docs)}/{n0} documents sống sót qua pipeline.")
    print("Bước tiếp: dán code cho Claude review, so với datatrove của HF.")


if __name__ == "__main__":
    main()
