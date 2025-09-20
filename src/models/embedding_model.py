import torch.nn as nn
from .backbone import get_backbone

class EmbeddingNet(nn.Module):
    def __init__(self, backbone_name='resnet18', embedding_size=256, pretrained=True):
        super().__init__()
        backbone, dim = get_backbone(backbone_name, pretrained=pretrained)
        self.backbone = backbone
        self.head = nn.Sequential(
            nn.Linear(dim, embedding_size),
            nn.ReLU(),
            nn.BatchNorm1d(embedding_size)
        )

    def forward(self, x):
        feat = self.backbone(x)
        if feat.ndim == 4:
            feat = feat.view(feat.size(0), -1)
        emb = self.head(feat)
        # normalize
        emb = emb / (emb.norm(p=2, dim=1, keepdim=True) + 1e-8)
        return emb
