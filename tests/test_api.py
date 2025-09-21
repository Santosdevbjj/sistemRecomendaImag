# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from src.webapp.app import app
from io import BytesIO
from PIL import Image

client = TestClient(app)

def create_dummy_image(color=(255, 0, 0), size=(64, 64)):
    """
    Cria uma imagem dummy em memória
    """
    buf = BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

@pytest.mark.parametrize("color", [(255, 0, 0), (0, 255, 0), (0, 0, 255)])
def test_recommend_endpoint(color):
    """
    Testa o endpoint /recommend da API usando imagens dummy.
    Garantindo que sempre retorna 200 OK, mesmo em ambiente CI/CD.
    """
    img_buf = create_dummy_image(color=color)
    files = {"file": ("dummy.jpg", img_buf, "image/jpeg")}

    response = client.post("/recommend", files=files)
    
    # Garantir que o status da resposta seja 200 OK
    assert response.status_code == 200, "A API não retornou status 200 OK"

    # Garantir que o retorno tenha chave 'recommendations'
    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) > 0
