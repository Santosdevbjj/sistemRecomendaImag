# Imagem base otimizada com Python 3.10
FROM python:3.10-slim

# Evita criação de arquivos pyc e garante logs imediatos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema necessárias para OpenCV, FAISS, Torch etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    unzip \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos primeiro (para aproveitar cache do Docker)
COPY requirements.txt .

# Instala dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para dentro do container
COPY . .

# Expõe a porta da API
EXPOSE 8000

# Comando padrão: inicia a API FastAPI com Uvicorn
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
