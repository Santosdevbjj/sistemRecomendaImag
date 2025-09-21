import io
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import torch
import os
import logging
from src.models.embedding_model import EmbeddingNet
from src.recommender.index import FaissRecommender
from src.data.dataset import default_transform
import sys

# Configurar logging para depuração
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adiciona o diretório raiz ao caminho do sistema para as importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

app = FastAPI(title='Image Recommendation API')

MODEL = None
RECOMMENDER = None
DEVICE = 'cpu'

MODEL_PATH = 'data/models/embedding_model.pth'
INDEX_PATH = 'data/models/image_faiss_index.bin'

@app.on_event('startup')
async def startup_event():
    global MODEL, RECOMMENDER, DEVICE

    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(f"Using device: {DEVICE}")

    try:
        # Tenta carregar o modelo de embedding
        MODEL = EmbeddingNet(backbone="resnet50", embedding_dim=2048)
        
        # Carrega os pesos se o arquivo existir
        if os.path.exists(MODEL_PATH):
            try:
                model_state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
                MODEL.load_state_dict(model_state_dict)
                logger.info("Embedding model loaded from disk.")
            except Exception as e:
                logger.error(f"Failed to load model state: {e}")
                # Continua mesmo se falhar para que a API esteja de pé
                pass
        else:
            logger.warning("Model file not found. Using an untrained model.")
            
        MODEL.to(DEVICE).eval()
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        MODEL = None
        # Levanta uma exceção para que o uvicorn saiba que a inicialização falhou
        raise RuntimeError(f"Could not load the embedding model: {e}")

    try:
        # Tenta carregar o índice FAISS
        if os.path.exists(INDEX_PATH):
            RECOMMENDER = FaissRecommender.load(INDEX_PATH)
            logger.info("FAISS index loaded from disk.")
        else:
            logger.warning("FAISS index not found. The recommend endpoint will only return the embedding.")
            RECOMMENDER = None
    except Exception as e:
        logger.error(f"Error loading FAISS index: {e}")
        RECOMMENDER = None
        # Levanta uma exceção para que o uvicorn saiba que a inicialização falhou
        raise RuntimeError(f"Could not load the FAISS index: {e}")

@app.post('/recommend')
async def recommend_images(file: UploadFile = File(...)):
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Service unavailable.")
        
    content = await file.read()
    try:
        img = Image.open(io.BytesIO(content)).convert('RGB')
    except Exception as e:
        logger.error(f"Failed to process image: {e}")
        raise HTTPException(status_code=400, detail="Invalid image file.")

    transform = default_transform()
    x = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        emb = MODEL(x)
        
    if RECOMMENDER is None:
        return JSONResponse({'embedding': emb.cpu().numpy().tolist()})

    distances, indices = RECOMMENDER.search(emb.cpu().numpy(), k=10)
    results = [{'distance': dist, 'index': int(idx)} for dist, idx in zip(distances[0], indices[0])]
    return JSONResponse({'recommendations': results})

@app.get('/health')
def health():
    if MODEL is None or RECOMMENDER is None:
        # Se um dos componentes principais não estiver carregado, a saúde está "down"
        status_info = {'status': 'down', 'details': {}}
        if MODEL is None:
            status_info['details']['model'] = 'not loaded'
        if RECOMMENDER is None:
            status_info['details']['recommender'] = 'not loaded'
        return JSONResponse(status_info, status_code=503)

    return {'status': 'ok'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
