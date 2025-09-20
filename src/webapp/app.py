# src/webapp/app.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post('/upload')
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    # salvar e processar -> extrair embedding -> retornar image_id
    return JSONResponse({'image_id': 'demo_123'})

@app.get('/recommend')
def recommend(image_id: str, k: int = 10):
    # buscar embedding salvo e pesquisar no índice
    return JSONResponse({'results': []})
