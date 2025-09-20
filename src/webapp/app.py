import io
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import torch
from src.models.embedding_model import EmbeddingNet
from src.recommender.index import FaissRecommender
from src.data.dataset import default_transform

app = FastAPI(title='Image Recommendation API')

# NOTE: This demo uses global singletons for simplicity
MODEL = None
RECOMMENDER = None
DEVICE = 'cpu'

@app.on_event('startup')
def startup_event():
    global MODEL, RECOMMENDER
    # carregar modelo (pequeno) e index (se existir)
    MODEL = EmbeddingNet(backbone_name='resnet18', embedding_size=256, pretrained=True)
    MODEL.eval()
    RECOMMENDER = None  # carregue com FaissRecommender.load(path) se disponível

@app.post('/upload')
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()
    try:
        img = Image.open(io.BytesIO(content)).convert('RGB')
    except Exception:
        raise HTTPException(status_code=400, detail='Arquivo não é uma imagem válida')
    transform = default_transform()
    x = transform(img).unsqueeze(0)
    with torch.no_grad():
        emb = MODEL(x)
        emb = emb.cpu().numpy()
    if RECOMMENDER is None:
        return JSONResponse({'embedding': emb.tolist()})
    results = RECOMMENDER.search(emb, k=10)
    return JSONResponse({'results': results})

@app.get('/health')
def health():
    return {'status': 'ok'}
