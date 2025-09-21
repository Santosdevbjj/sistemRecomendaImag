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

# Configurar logging para depuração
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title='Image Recommendation API')

# Singletons globais para o modelo e o recomendador
MODEL = None
RECOMMENDER = None
DEVICE = 'cpu'

# Caminhos dos arquivos do modelo e do índice
MODEL_PATH = 'data/models/embedding_model.pth'
INDEX_PATH = 'data/models/image_faiss_index.bin'

@app.on_event('startup')
async def startup_event():
    """Carrega o modelo e o índice FAISS ao iniciar a aplicação."""
    global MODEL, RECOMMENDER, DEVICE
    
    # Define o dispositivo de execução (GPU ou CPU)
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(f"Usando dispositivo: {DEVICE}")

    # Carrega o modelo de embedding
    try:
        # A sua classe EmbeddingNet deve aceitar os parâmetros aqui
        MODEL = EmbeddingNet(backbone="resnet50", embedding_dim=2048)
        
        # Carrega os pesos do modelo se o arquivo existir
        if os.path.exists(MODEL_PATH):
            model_state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
            MODEL.load_state_dict(model_state_dict)
            logger.info(f"Modelo de embedding carregado de: {MODEL_PATH}")
        else:
            logger.warning("Arquivo do modelo não encontrado. Usando modelo não treinado.")
        
        MODEL.to(DEVICE).eval()
    except Exception as e:
        logger.error(f"Erro ao carregar o modelo: {e}")
        MODEL = None
        raise RuntimeError("Não foi possível carregar o modelo de embedding.")

    # Carrega o índice FAISS
    if os.path.exists(INDEX_PATH):
        try:
            RECOMMENDER = FaissRecommender.load(INDEX_PATH)
            logger.info(f"Índice FAISS carregado de: {INDEX_PATH}")
        except Exception as e:
            logger.error(f"Erro ao carregar o índice FAISS: {e}")
            RECOMMENDER = None
            raise RuntimeError("Não foi possível carregar o índice de recomendação.")
    else:
        logger.warning("Índice FAISS não encontrado. As recomendações não serão ativas.")
        RECOMMENDER = None

@app.post('/recommend') # <-- Rota ajustada para coincidir com o teste
async def recommend_images(file: UploadFile = File(...)):
    """Recebe uma imagem, extrai o embedding e retorna recomendações."""
    if MODEL is None:
        raise HTTPException(status_code=503, detail="O modelo de embedding não foi carregado.")

    content = await file.read()
    try:
        img = Image.open(io.BytesIO(content)).convert('RGB')
    except Exception as e:
        logger.error(f"Erro ao processar imagem: {e}")
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem válida.")

    # Transformação e extração do embedding
    transform = default_transform()
    x = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        emb = MODEL(x)
        
    # Se o recomendador FAISS não foi carregado, retorna apenas o embedding
    if RECOMMENDER is None:
        return JSONResponse({'embedding': emb.cpu().numpy().tolist()})

    # Busca por recomendações
    distances, indices = RECOMMENDER.search(emb.cpu().numpy(), k=10)
    
    # Formata os resultados e retorna
    results = [{'distance': dist, 'index': idx} for dist, idx in zip(distances[0], indices[0])]
    return JSONResponse({'recommendations': results})

@app.get('/health')
def health():
    """Endpoint de saúde para verificar se a API está ativa."""
    if MODEL is None:
        return JSONResponse({'status': 'down', 'reason': 'model not loaded'}, status_code=503)
    return {'status': 'ok'}

# Executa a aplicação diretamente se o script for chamado
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
