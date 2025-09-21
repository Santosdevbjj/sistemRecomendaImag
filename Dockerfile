# Usa uma imagem base Python
FROM python:3.10

# Define variáveis de ambiente para melhor desempenho e logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    build-essential \
    cmake \
    libgl1 \
    libopenblas-dev \
    liblapack-dev && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala as dependências do Python.
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Adiciona permissões de execução para os scripts.
RUN chmod +x ./scripts/run_tests.sh
RUN chmod +x ./scripts/prepare_data.sh

# Expõe a porta que a API usará
EXPOSE 8000

# Comando para iniciar a API com Uvicorn
CMD ["uvicorn", "src.webapp.app:app", "--host", "0.0.0.0", "--port", "8000"]
