# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from PIL import Image
from src.webapp.app import app

client = TestClient(app)

def create_dummy_image(color=(255, 0, 0), size=(64, 64)):
    """
    Cria uma imagem dummy em memória.
    """
    img = Image.new("RGB", size, color=color)
    buf = BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

@pytest.mark.parametrize("color", [(255, 0, 0), (0, 255, 0), (0, 0, 255)])
def test_recommend_endpoint(color):
    """
    Teste do endpoint /recommend da API usando imagens dummy.
    """
    img_buf = create_dummy_image(color=color)
    files = {"file": ("dummy.jpg", img_buf, "image/jpeg")}

    response = client.post("/recommend", files=files)

    assert response.status_code == 200, "A API não retornou status 200 OK"
    data = response.json()
    assert "recommendations" in data, "O JSON retornado não contém 'recommendations'"
    assert isinstance(data["recommendations"], list), "'recommendations' não é uma lista"
    assert len(data["recommendations"]) > 0, "Nenhuma recomendação foi retornada"

def test_healthcheck():
    """
    Teste do endpoint raiz ou healthcheck para garantir que a API está ativa.
    """
    response = client.get("/")
    assert response.status_code == 200, "Healthcheck falhou"
    assert "message" in response.json(), "Healthcheck não retornou 'message'"
