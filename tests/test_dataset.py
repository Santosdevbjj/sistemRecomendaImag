# tests/test_dataset.py
import os
import pytest

DATA_DIR = "data/processed"

def test_dataset_exists():
    """Verifica se a pasta de dataset existe"""
    assert os.path.exists(DATA_DIR), f"Diretório {DATA_DIR} não encontrado"

def test_dataset_not_empty():
    """Verifica se há pelo menos uma subpasta e arquivos de imagem"""
    classes = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
    assert len(classes) > 0, f"Nenhuma classe encontrada em {DATA_DIR}"
    
    for cls in classes:
        cls_path = os.path.join(DATA_DIR, cls)
        images = [f for f in os.listdir(cls_path) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
        assert len(images) > 0, f"Nenhuma imagem encontrada na classe {cls}"
