# src/utils/io.py

import os
from PIL import Image
import numpy as np

def load_image(path, resize=None):
    """
    Carrega uma imagem do disco e retorna como numpy array.
    
    Args:
        path (str): Caminho para a imagem.
        resize (tuple): Tamanho (width, height) para redimensionar a imagem.

    Returns:
        np.ndarray: Imagem como array.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Imagem não encontrada: {path}")
    
    img = Image.open(path).convert("RGB")
    if resize:
        img = img.resize(resize)
    return np.array(img)

def list_images(folder, exts=(".jpg", ".png", ".jpeg")):
    """
    Lista todos os arquivos de imagem em uma pasta e suas subpastas.
    
    Args:
        folder (str): Diretório base.
        exts (tuple): Extensões de arquivos válidas.

    Returns:
        list: Lista de paths das imagens.
    """
    images = []
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(exts):
                images.append(os.path.join(root, f))
    return images

def save_numpy_array(array, path):
    """
    Salva um numpy array no disco.
    
    Args:
        array (np.ndarray): Array a ser salvo.
        path (str): Caminho do arquivo de saída.
    """
    np.save(path, array)

def load_numpy_array(path):
    """
    Carrega um numpy array do disco.
    
    Args:
        path (str): Caminho do arquivo.
    
    Returns:
        np.ndarray: Array carregado.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    return np.load(path)
