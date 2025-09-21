# tests/test_similarity.py

import sys
import os
# Adicionando o diretório raiz do projeto ao PATH para que as importações funcionem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pytest
import faiss
from src.models.embedding_model import EmbeddingNet # <-- AQUI ESTÁ A CORREÇÃO

DEVICE = "cpu"
# Use caminhos que existam ou crie-os com fixtures se não existirem
TEST_IMAGES = [
    "data/processed/cat/cat.1.jpg",
    "data/processed/cat/cat.2.jpg",
    "data/processed/dog/dog.1.jpg"
]

@pytest.fixture(scope="module")
def model():
    """Carrega o modelo de embeddings para os testes."""
    m = EmbeddingNet(backbone="resnet50")
    checkpoint_path = "data/models/embedding_model.pth"
    
    if os.path.exists(checkpoint_path):
        import torch
        try:
            m.load_state_dict(torch.load(checkpoint_path, map_location=DEVICE))
        except RuntimeError as e:
            pytest.skip(f"Erro ao carregar o estado do modelo. Verifique o arquivo do checkpoint: {e}")
    m.eval()
    return m

@pytest.fixture(scope="module")
def test_embeddings(model):
    """Gera e retorna os embeddings para as imagens de teste."""
    # Garante que as imagens de teste existem para evitar FileNotFoundError
    for img_path in TEST_IMAGES:
        if not os.path.exists(img_path):
            pytest.skip(f"Imagem de teste não encontrada: {img_path}")
            
    embeddings = [model.get_embedding(img, device=DEVICE) for img in TEST_IMAGES]
    embeddings_np = np.vstack(embeddings)
    return embeddings_np

def test_embeddings_shape(test_embeddings):
    """Verifica se os embeddings têm a dimensão esperada."""
    assert test_embeddings.shape[0] == len(TEST_IMAGES), "Número de embeddings incorreto"
    assert test_embeddings.shape[1] == 2048, "Dimensão do embedding incorreta"

def test_faiss_index_accuracy(test_embeddings):
    """Verifica se o FAISS index retorna a imagem mais próxima corretamente."""
    index = faiss.IndexFlatL2(test_embeddings.shape[1])
    index.add(test_embeddings)

    # A imagem mais próxima de si mesma deve ser ela mesma (distância 0)
    D, I = index.search(test_embeddings[0:1], k=1)
    assert I[0, 0] == 0, "A imagem mais próxima da primeira deve ser ela mesma."

    # Teste para a similaridade. Embeddings da mesma classe devem ser mais próximos
    # que embeddings de classes diferentes.
    # Ex: (cat.1.jpg vs cat.2.jpg) vs (cat.1.jpg vs dog.1.jpg)
    
    # Busca por vizinhos da primeira imagem de gato (índice 0)
    D_cat, I_cat = index.search(test_embeddings[0:1], k=3)
    
    # Encontra os índices das outras imagens de gato e cachorro
    idx_other_cat = np.where(I_cat[0] == 1)[0][0]
    idx_dog = np.where(I_cat[0] == 2)[0][0]
    
    # A distância para a imagem de gato deve ser menor que a do cachorro
    distance_to_other_cat = D_cat[0, idx_other_cat]
    distance_to_dog = D_cat[0, idx_dog]

    # O teste mais importante: a distância entre os gatos deve ser menor
    assert distance_to_other_cat < distance_to_dog, \
           "A distância entre gatos não é menor que a distância para o cachorro, o que é um problema na similaridade."
