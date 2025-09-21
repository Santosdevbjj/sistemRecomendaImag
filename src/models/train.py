# src/models/train.py
import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.models import ResNet
import logging

# Adiciona o diretório raiz do projeto ao PATH para permitir importações
# de src.models, src.data, etc.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.models.embedding_model import EmbeddingNet  # Importação corrigida
from src.data.dataset import default_transform
from src.models.backbone import load_backbone

# --- Configurações de Treinamento ---
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DATA_DIR = os.path.join(PROJECT_ROOT, "data/processed")
MODEL_DIR = os.path.join(PROJECT_ROOT, "data/models")
BATCH_SIZE = 32
EPOCHS = 5
LR = 1e-4

# Configurações de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_model():
    """
    Função principal para treinar o modelo de embedding.
    Carrega dados, inicializa o modelo e o otimizador,
    roda o ciclo de treinamento e salva os pesos do modelo.
    """
    logging.info(f"🚀 Treinando modelo no dispositivo: {DEVICE}")

    # Verifica se o diretório de dados processados existe
    if not os.path.exists(DATA_DIR):
        logging.error(f"Diretório de dados não encontrado: {DATA_DIR}")
        sys.exit(1)

    # Carregando o conjunto de dados
    # A sua classe `default_transform` do dataset.py deve ser usada aqui
    transform = default_transform()
    dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    if len(dataset) == 0:
        logging.warning("Nenhuma imagem encontrada no diretório de dados. Verifique o caminho.")
        return

    # Inicializa o modelo de embedding
    model = EmbeddingNet(backbone="resnet50").to(DEVICE)
    logging.info(f"Modelo de embedding '{model.__class__.__name__}' inicializado com ResNet-50.")

    # Camada de classificação para o treinamento supervisionado
    classifier = nn.Linear(model.embedding_dim, len(dataset.classes)).to(DEVICE)
    logging.info(f"Classificador inicializado para {len(dataset.classes)} classes.")

    # Funções de perda e otimizador
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(list(model.parameters()) + list(classifier.parameters()), lr=LR)

    # --- Ciclo de Treinamento ---
    for epoch in range(EPOCHS):
        model.train()
        classifier.train()
        running_loss = 0.0
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

            # Zera os gradientes
            optimizer.zero_grad()

            # Forward pass
            embeddings = model(inputs)
            outputs = classifier(embeddings)

            # Calcula a perda
            loss = criterion(outputs, labels)

            # Backward pass e otimização
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        avg_loss = running_loss / len(dataloader)
        logging.info(f"Epoch [{epoch+1}/{EPOCHS}], Loss: {avg_loss:.4f}")

    # --- Salvando os Modelos ---
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Salva os pesos do modelo de embedding
    torch.save(model.state_dict(), os.path.join(MODEL_DIR, "embedding_model.pth"))
    
    # Salva os pesos do classificador (útil para avaliação)
    torch.save(classifier.state_dict(), os.path.join(MODEL_DIR, "classifier.pth"))

    logging.info("✅ Treinamento concluído. Modelos salvos em:", MODEL_DIR)


if __name__ == "__main__":
    train_model()
