import os
import pytest
from fastapi.testclient import TestClient
from src.webapp.app import app

client = TestClient(app)

# O TEST_IMAGE será definido pelo conftest.py
TEST_IMAGE = "/app/data/processed/cat/cat.1.jpg"

@pytest.mark.parametrize("image_path", [TEST_IMAGE])
def test_recommend_endpoint(image_path):
    """Teste do endpoint /recommend da API"""

    # Verifica se a imagem de teste existe
    assert os.path.exists(image_path), f"Imagem de teste não encontrada: {image_path}"

    # Envia request POST para /recommend
    with open(image_path, "rb") as f:
        response = client.post("/recommend", files={"file": (os.path.basename(image_path), f, "image/jpeg")})

    # Verifica status da resposta
    assert response.status_code == 200
    # Verifica se retorna lista de resultados
    json_data = response.json()
    assert isinstance(json_data, list)
    assert len(json_data) > 0
