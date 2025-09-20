# Usa uma imagem base Python otimizada
FROM python:3.10-slim

# Define variáveis de ambiente para melhor desempenho e logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema necessárias para FAISS e outras bibliotecas
# O Faiss requer BLAS e LAPACK. Usaremos o OpenBLAS para otimização de CPU.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    build-essential \
    cmake \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libopenblas-dev \
    liblapack-dev && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de requisitos para aproveitar o cache de camadas do Docker
COPY requirements.txt .

# Instala as dependências do Python
# A flag --no-cache-dir é uma boa prática
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da sua aplicação
COPY . .

# Expõe a porta que a API usará
EXPOSE 8000

# Comando para iniciar a API com Uvicorn
# Verifique se o caminho "src.main:app" é o correto para a sua aplicação.
# Se seu arquivo principal for 'src/main.py', este é o caminho certo.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

