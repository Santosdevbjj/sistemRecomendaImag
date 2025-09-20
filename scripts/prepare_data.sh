#!/bin/bash
# scripts/prepare_data.sh
# Script para preparar o dataset de imagens para o sistema de recomendação

set -e  # interrompe em caso de erro

DATA_DIR="data/raw"
PROCESSED_DIR="data/processed"
URL="https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip"
FILENAME="cats_and_dogs_filtered.zip"

echo "📂 Criando diretórios..."
mkdir -p $DATA_DIR
mkdir -p $PROCESSED_DIR

cd $DATA_DIR

echo "⬇️ Baixando dataset..."
if [ ! -f "$FILENAME" ]; then
    wget -c $URL -O $FILENAME
else
    echo "✔️ Arquivo já baixado: $FILENAME"
fi

echo "📦 Extraindo arquivos..."
unzip -o $FILENAME -d .

echo "🧹 Organizando dataset..."
# Exemplo: mover para estrutura padronizada
if [ -d "cats_and_dogs_filtered/train" ]; then
    mv cats_and_dogs_filtered/train/* ../processed/ 2>/dev/null || true
    mv cats_and_dogs_filtered/validation/* ../processed/ 2>/dev/null || true
fi

echo "✅ Dataset preparado em: $PROCESSED_DIR"
