import os
import pytest
from PIL import Image

@pytest.fixture(scope="session", autouse=True)
def prepare_test_images():
    """
    Cria automaticamente imagens de teste para a API e garante
    que os diretórios existam dentro do container.
    """
    base_dir = "/app/data/processed"
    categories = ["cat", "dog"]

    for cat in categories:
        dir_path = os.path.join(base_dir, cat)
        os.makedirs(dir_path, exist_ok=True)
        img_path = os.path.join(dir_path, f"{cat}.1.jpg")
        # Cria uma imagem RGB simples 64x64
        if not os.path.exists(img_path):
            Image.new("RGB", (64, 64), color=(255, 0, 0) if cat == "cat" else (0, 255, 0)).save(img_path)

    yield
