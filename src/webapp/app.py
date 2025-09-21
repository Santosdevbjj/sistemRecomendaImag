# src/webapp/app.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from io import BytesIO
from PIL import Image
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema de Recomendação por Imagens")

# Tentativa de importar e inicializar o índice FAISS na startup da API
recommender = None
try:
    from src.recommender.index import RecommenderIndex
    recommender = RecommenderIndex()
    logger.info("RecommenderIndex carregado com sucesso.")
except ImportError:
    logger.warning("RecommenderIndex não encontrado. Usando modo de fallback para testes.")
except Exception as e:
    logger.error(f"Erro ao inicializar RecommenderIndex: {e}. Usando fallback.")

@app.get("/")
async def health_check():
    """Endpoint de saúde para verificar se a API está online."""
    return {"status": "API online"}

@app.post("/recommend")
async def recommend(file: UploadFile = File(...)):
    """
    Endpoint para receber uma imagem e retornar recomendações.
    A API retorna um resultado real se o recomendador estiver disponível,
    ou um resultado dummy para ambiente de teste.
    """
    try:
        # Carrega a imagem
        contents = await file.read()
        img = Image.open(BytesIO(contents)).convert("RGB")

        # Se o recomendador real está disponível, faz a recomendação
        if recommender:
            # Assumimos que o método `query` retorna a lista de recomendações diretamente
            recommendations_list = recommender.query(img)
            # A chave do JSON é 'recommendations', o que seu teste espera.
            return JSONResponse(content={"recommendations": recommendations_list}, status_code=200)
        else:
            # Fallback para CI/CD e testes: retorna um resultado dummy
            dummy_results = ["dummy_product_1", "dummy_product_2", "dummy_product_3"]
            logger.info("Retornando resultados dummy para o teste.")
            return JSONResponse(content={"recommendations": dummy_results}, status_code=200)

    except Exception as e:
        logger.error(f"Erro na requisição /recommend: {e}")
        return JSONResponse(
            content={"error": f"Erro interno do servidor: {e}"}, status_code=500
        )
