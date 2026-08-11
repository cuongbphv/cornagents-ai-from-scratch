"""
rag_pipeline.py — STARTER Tuần 10. RAG baseline end-to-end.

Pipeline: load PDF -> chunk -> embed -> Chroma -> retrieve top-k -> generate.
Đây là starter có cấu trúc rõ; điền phần cấu hình + generate theo lựa chọn của bạn.

Cài (trên máy của bạn):
    pip install langchain langchain-community langchain-chroma \
                chromadb sentence-transformers pypdf

Generate: dùng Ollama local (Tuần 9) hoặc Claude API.
"""

from pathlib import Path

DATA_DIR = Path("data")          # đặt PDF Finance Banking vào đây
PERSIST_DIR = "chroma_db"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 4
EMBED_MODEL = "BAAI/bge-small-en-v1.5"   # local, nhẹ


def load_documents(data_dir: Path):
    from langchain_community.document_loaders import PyPDFLoader
    docs = []
    for pdf in sorted(data_dir.glob("*.pdf")):
        docs.extend(PyPDFLoader(str(pdf)).load())
    if not docs:
        raise FileNotFoundError(f"Không thấy PDF trong {data_dir}/ — thêm tài liệu trước.")
    return docs


def chunk(docs):
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_documents(docs)


def build_index(chunks):
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma
    emb = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return Chroma.from_documents(chunks, emb, persist_directory=PERSIST_DIR)


def retrieve(vectorstore, query, k=TOP_K):
    return vectorstore.similarity_search(query, k=k)


def build_prompt(query, contexts):
    ctx = "\n\n---\n\n".join(c.page_content for c in contexts)
    return (
        "Trả lời câu hỏi CHỈ dựa trên ngữ cảnh dưới đây. "
        "Nếu ngữ cảnh không đủ, nói 'Không đủ thông tin'.\n\n"
        f"# Ngữ cảnh:\n{ctx}\n\n# Câu hỏi:\n{query}\n\n# Trả lời:"
    )


def generate(prompt: str) -> str:
    # TODO: chọn 1 cách generate:
    #  (a) Ollama local:
    #       import ollama
    #       return ollama.generate(model="llama3.1", prompt=prompt)["response"]
    #  (b) Claude API:
    #       from anthropic import Anthropic
    #       client = Anthropic()
    #       msg = client.messages.create(model="claude-...", max_tokens=512,
    #               messages=[{"role":"user","content":prompt}])
    #       return msg.content[0].text
    raise NotImplementedError("TODO: chọn backend generate (Ollama hoặc Claude)")


def main():
    docs = load_documents(DATA_DIR)
    chunks = chunk(docs)
    print(f"{len(docs)} trang -> {len(chunks)} chunks")
    vs = build_index(chunks)

    query = "Quy trình phê duyệt trong tài liệu nghiệp vụ này gồm những bước nào?"
    contexts = retrieve(vs, query)
    print(f"Lấy {len(contexts)} đoạn liên quan.")
    answer = generate(build_prompt(query, contexts))
    print("\n=== TRẢ LỜI ===\n", answer)


if __name__ == "__main__":
    main()
