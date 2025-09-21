# tests/conftest.py
import pytest
from io import BytesIO
from PIL import Image

@pytest.fixture
def dummy_image():
    """
    Retorna uma imagem dummy em memória (vermelha 64x64).
    """
    buf = BytesIO()
    img = Image.new("RGB", (64, 64), color=(255, 0, 0))
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

@pytest.fixture
def dummy_images():
    """
    Retorna uma lista de imagens dummy de diferentes cores e tamanhos.
    """
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    sizes = [(64, 64), (128, 128), (32, 32)]
    images = []

    for color in colors:
        for size in sizes:
            buf = BytesIO()
            img = Image.new("RGB", size, color=color)
            img.save(buf, format="JPEG")
            buf.seek(0)
            images.append(buf)
    return images

@pytest.fixture
def synthetic_dataset(tmp_path):
    """
    Cria um diretório de dataset sintético com várias imagens dummy organizadas em classes.
    """
    classes = ["cat", "dog", "shoe"]
    for cls in classes:
        class_dir = tmp_path / cls
        class_dir.mkdir()
        for i in range(3):  # 3 imagens por classe
            buf = BytesIO()
            img = Image.new("RGB", (64, 64), color=(i*40, i*40, i*40))
            img.save(buf, format="JPEG")
            buf.seek(0)
            file_path = class_dir / f"{cls}.{i+1}.jpg"
            with open(file_path, "wb") as f:
                f.write(buf.read())
    return tmp_path
