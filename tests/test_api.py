# tests/test_api.py
import os
import requests
import pytest

# URL da API (ajuste se mudar porta ou host)
API_URL = "http://localhost:8000/recommend"

# Imagem de teste
TEST_IMAGE = "data/processed/cat/cat.1.jpg"

@pytest.mark.parametrize("image_path", [TEST_IMAGE])
def test_recommend_endpoint(image_path):
    """Teste do endpoint /recommend da API"""
    
    assert os.path.exists(image_path), f"Imagem de teste não encontrada: {image_path}"
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        try:
            response = requests.post(API_URL, files=files)
        except requests.exceptions.ConnectionError:
            pytest.fail("❌ Não foi possível conectar à API. Verifique se o container está rodando.")
    
    assert response.status_code == 200, f"Status code inesperado: {response.status_code}"
    
    data = response.json()
    assert "neighbors" in data, "Resposta não contém chave 'neighbors'"
    assert isinstance(data["neighbors"], list), "'neighbors' deve ser uma lista"
    assert len(data["neighbors"]) > 0, "Lista de vizinhos está vazia"
