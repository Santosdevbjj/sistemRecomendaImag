# src/utils/viz.py

import matplotlib.pyplot as plt
from PIL import Image
import os

def show_image(path, title=None):
    """
    Exibe uma imagem.
    
    Args:
        path (str): Caminho da imagem.
        title (str): Título opcional.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Imagem não encontrada: {path}")
    
    img = Image.open(path).convert("RGB")
    plt.imshow(img)
    if title:
        plt.title(title)
    plt.axis("off")
    plt.show()

def show_similar_images(query_path, neighbors_paths, cols=5):
    """
    Exibe a imagem de consulta e suas imagens similares lado a lado.
    
    Args:
        query_path (str): Caminho da imagem de consulta.
        neighbors_paths (list): Lista de caminhos das imagens similares.
        cols (int): Número de colunas na visualização.
    """
    all_paths = [query_path] + neighbors_paths
    rows = (len(all_paths) + cols - 1) // cols
    
    plt.figure(figsize=(4 * cols, 4 * rows))
    
    for i, img_path in enumerate(all_paths):
        if not os.path.exists(img_path):
            continue
        img = Image.open(img_path).convert("RGB")
        plt.subplot(rows, cols, i + 1)
        plt.imshow(img)
        plt.axis("off")
        plt.title("Query" if i == 0 else f"Neighbor {i}")
    
    plt.tight_layout()
    plt.show()
