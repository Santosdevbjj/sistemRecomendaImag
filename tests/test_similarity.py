# tests/test_similarity.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pytest
import faiss
from src.models.embedding_model import EmbeddingModel

DEVICE = "cpu"
TEST_IMAGES = [
    "data/processed/cat/cat.1.jpg",
    "data/processed/cat/cat.2.jpg",
    "data/processed/dog/dog.1.jpg"
]

@pytest.fixture
def model():
    """Carrega o modelo de embeddings"""
    m = EmbeddingModel(backbone="resnet50")
    checkpoint_path = "data/models/embedding_model.pth"
    if os.path.exists(checkpoint_path):
        import torch
        m.load_state_dict(torch.load(checkpoint_path, map_location=DEVICE))
    m.eval()
    return m

def test_embeddings_shape(model):
    """Verifica se os embeddings têm a dimensão esperada"""
    emb = model.get_embedding(TEST_IMAGES[0], device=DEVICE)
    assert len(emb.shape) == 2, "Embedding deve ser 2D (1, dim)"
    assert emb.shape[1] > 0, "Dimensão do embedding deve ser > 0"

def test_faiss_index(model):
    """Verifica se o FAISS index funciona corretamente"""
    embeddings = [model.get_embedding(img, device=DEVICE) for img in TEST_IMAGES]
    embeddings_np = np.vstack(embeddings)
    
    index = faiss.IndexFlatL2(embeddings_np.shape[1])
    index.add(embeddings_np)
    
    D, I = index.search(embeddings_np[0:1], k=2)
    
    assert I.shape == (1, 2), "Formato do resultado FAISS incorreto"
    assert D.shape == (1, 2), "Formato das distâncias FAISS incorreto"
    assert I[0, 0] == 0, "A imagem mais próxima deve ser ela mesma"
