# src/models/embedding_model.py
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

# A classe foi renomeada de 'EmbeddingModel' para 'EmbeddingNet'
class EmbeddingNet(nn.Module):
    def __init__(self, backbone="resnet50", embedding_dim=2048, pretrained=True):
        super(EmbeddingNet, self).__init__()
        if backbone == "resnet50":
            model = models.resnet50(pretrained=pretrained)
            # Remove a última camada de classificação para usar como extrator de features
            layers = list(model.children())[:-1]  
            self.backbone = nn.Sequential(*layers)
            self.embedding_dim = embedding_dim
        else:
            raise ValueError(f"Backbone {backbone} não suportado.")

    def forward(self, x):
        x = self.backbone(x)
        # Transforma o tensor para o formato linear (flatten)
        x = x.view(x.size(0), -1)  
        return x

    def get_embedding(self, image_path, device="cpu"):
        """Extrai embedding de uma imagem única a partir do caminho."""
        # Coloca o modelo em modo de avaliação
        self.eval()  
        preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        # 
        img = Image.open(image_path).convert("RGB")
        img_tensor = preprocess(img).unsqueeze(0).to(device)
        with torch.no_grad():
            embedding = self.forward(img_tensor)
        return embedding.cpu().numpy()
