import os
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./data/faiss_index")
DOCS_DIR = Path(__file__).parent / "docs"


def load_documents() -> list[Document]:
    docs = []
    for txt_file in sorted(DOCS_DIR.glob("*.txt")):
        content = txt_file.read_text(encoding="utf-8").strip()
        if not content:
            continue
        docs.append(Document(
            page_content=content,
            metadata={"source": txt_file.stem},
        ))
    return docs


def build_index(documents: list[Document]) -> FAISS:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    store = FAISS.from_documents(documents, embeddings)
    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
    store.save_local(FAISS_INDEX_PATH)
    return store


def load_index() -> FAISS:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    if os.path.exists(FAISS_INDEX_PATH):
        return FAISS.load_local(
            FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True
        )
    return build_index(load_documents())


def search(query: str, store: FAISS, top_k: int = 3) -> list[dict]:
    # retorna (Document, distância L2) — score menor = mais relevante
    results = store.similarity_search_with_score(query, k=top_k)
    return [
        {
            "source": doc.metadata.get("source", "unknown"),
            "content": doc.page_content[:300],
            "score": round(float(score), 4),
        }
        for doc, score in results
    ]


if __name__ == "__main__":
    print("Carregando/construindo índice FAISS...")
    store = load_index()
    print("Índice pronto.\n")

    queries = [
        "Como iterar sobre uma lista em Python?",
        "Como funciona programação assíncrona?",
        "Como criar uma classe com herança?",
    ]

    for query in queries:
        print(f"\n{'=' * 60}")
        print(f"Query: {query}")
        print(f"{'=' * 60}")
        for i, result in enumerate(search(query, store), 1):
            print(f"\n[{i}] Fonte: {result['source']}  |  Score L2: {result['score']}")
            print(f"    {result['content']}...")
