import faiss
from langchain.vectorstores import FAISS

def build_vector_store(chunks, embeddings):
    return FAISS.from_texts(chunks, embeddings)
