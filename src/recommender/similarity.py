# src/recommender/similarity.py
import numpy as np
import faiss

class FaissIndex:
    def __init__(self, dim, index_path=None):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        if index_path:
            faiss.read_index(index_path)

    def add(self, embeddings):
        self.index.add(np.array(embeddings).astype('float32'))

    def search(self, query_emb, k=10):
        D, I = self.index.search(np.array([query_emb]).astype('float32'), k)
        return D[0], I[0]
