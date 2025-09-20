import torch
from torch.utils.data import DataLoader
from src.data.dataset import default_transform, ImageFolderDataset

@torch.no_grad()
def extract_embeddings(model, folder, batch_size=32, device='cpu'):
    model.eval()
    ds = ImageFolderDataset(folder, transform=default_transform())
    dl = DataLoader(ds, batch_size=batch_size, shuffle=False, num_workers=2)
    embeddings = []
    paths = []
    model.to(device)
    for imgs, ps in dl:
        imgs = imgs.to(device)
        emb = model(imgs)
        embeddings.append(emb.cpu())
        paths.extend(ps)
    import torch
    embeddings = torch.cat(embeddings, dim=0).numpy()
    return embeddings, paths
