import torch.nn as nn
import torchvision.models as models

def get_backbone(name='resnet18', pretrained=True, use_cuda=False):
    """Retorna backbone (sem a última camada FC) e a dimensão do embedding."""
    name = name.lower()
    if name == 'resnet18':
        m = models.resnet18(pretrained=pretrained)
        dim = m.fc.in_features
        # remove head
        m.fc = nn.Identity()
    elif name == 'mobilenet_v2':
        m = models.mobilenet_v2(pretrained=pretrained)
        dim = m.classifier[1].in_features
        m.classifier = nn.Identity()
    else:
        raise ValueError('backbone não suportado')
    return m, dim
