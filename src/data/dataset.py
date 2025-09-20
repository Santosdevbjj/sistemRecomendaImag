import os
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset

class ImageFolderDataset(Dataset):
    """Dataset simples que busca imagens em uma pasta e aplica transforms."""
    def __init__(self, root_dir, transform=None, extensions={'.jpg', '.jpeg', '.png'}):
        self.root_dir = root_dir
        self.transform = transform
        self.samples = []
        for root, _, files in os.walk(root_dir):
            for f in files:
                if os.path.splitext(f)[1].lower() in extensions:
                    self.samples.append(os.path.join(root, f))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path = self.samples[idx]
        img = Image.open(path).convert('RGB')
        if self.transform:
            img = self.transform(img)
        return img, path

# helper default transform
def default_transform(image_size=224):
    return transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
