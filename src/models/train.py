# src/models/train.py
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from embedding_model import EmbeddingModel

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DATA_DIR = "data/processed"
MODEL_DIR = "data/models"
BATCH_SIZE = 32
EPOCHS = 5
LR = 1e-4

def train_model():
    print(f"🚀 Treinando modelo no dispositivo: {DEVICE}")

    # Transforms para treino e validação
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    model = EmbeddingModel(backbone="resnet50").to(DEVICE)

    # Cabeça simples de classificação (opcional, para treino supervisionado)
    classifier = nn.Linear(model.embedding_dim, len(dataset.classes)).to(DEVICE)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(list(model.parameters()) + list(classifier.parameters()), lr=LR)

    for epoch in range(EPOCHS):
        running_loss = 0.0
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

            optimizer.zero_grad()
            embeddings = model(inputs)
            outputs = classifier(embeddings)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f"Epoch [{epoch+1}/{EPOCHS}], Loss: {running_loss/len(dataloader):.4f}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(MODEL_DIR, "embedding_model.pth"))
    torch.save(classifier.state_dict(), os.path.join(MODEL_DIR, "classifier.pth"))

    print("✅ Treinamento concluído. Modelos salvos em:", MODEL_DIR)


if __name__ == "__main__":
    train_model()
