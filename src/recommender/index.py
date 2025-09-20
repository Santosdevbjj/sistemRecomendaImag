import numpy as np
import faiss
import os

class FaissRecommender:
    def __init__(self, dim, index_path=None):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)  # inner product, assume normalized embeddings
        self.paths = []
        self.index_path = index_path

    def build(self, embeddings, paths):
        # embeddings: numpy array (N, D)
        self.index.add(embeddings.astype('float32'))
        self.paths = list(paths)

    def search(self, query_emb, k=10):
        D, I = self.index.search(query_emb.astype('float32'), k)
        results = []
        for ids, dists in zip(I, D):
            res = []
            for i, dist in zip(ids, dists):
                if i < 0 or i >= len(self.paths):
                    continue
                res.append({'path': self.paths[i], 'score': float(dist)})
            results.append(res)
        return results

    def save(self, dirpath):
        os.makedirs(dirpath, exist_ok=True)
        faiss.write_index(self.index, os.path.join(dirpath, 'index.faiss'))
        # save paths
        import json
        with open(os.path.join(dirpath, 'paths.json'), 'w') as f:
            json.dump(self.paths, f)

    def load(self, dirpath):
        import json
        self.index = faiss.read_index(os.path.join(dirpath, 'index.faiss'))
        with open(os.path.join(dirpath, 'paths.json'), 'r') as f:
            self.paths = json.load(f)
