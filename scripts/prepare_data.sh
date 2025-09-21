#!/bin/bash
# scripts/prepare_data.sh
# Script para preparar o dataset de imagens para o sistema de recomendação

set -e  # Interrompe o script em caso de erro

# --- Variáveis de Configuração ---
DATA_DIR="data/raw"
PROCESSED_DIR="data/processed"
URL="https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip"
FILENAME="cats_and_dogs_filtered.zip"
UNZIPPED_DIR="cats_and_dogs_filtered"

echo "📂 Criando diretórios..."
mkdir -p "$DATA_DIR"
mkdir -p "$PROCESSED_DIR/cats"
mkdir -p "$PROCESSED_DIR/dogs"

echo "➡️ Navegando para o diretório de dados brutos: $DATA_DIR"
cd "$DATA_DIR"

echo "⬇️ Baixando dataset..."
if [ ! -f "$FILENAME" ]; then
    wget -c "$URL" -O "$FILENAME"
    echo "✔️ Dataset baixado com sucesso."
else
    echo "✔️ Arquivo já baixado: $FILENAME"
fi

echo "📦 Extraindo arquivos..."
unzip -o "$FILENAME" -d .

echo "🧹 Organizando dataset..."

# Verifica se a pasta descompactada existe
if [ -d "$UNZIPPED_DIR/train" ]; then
    echo "Movendo imagens de treino..."
    # Move imagens de gatos para o diretório de gatos processados
    mv "$UNZIPPED_DIR/train/cats"/* "../processed/cats/" || true
    # Move imagens de cachorros para o diretório de cachorros processados
    mv "$UNZIPPED_DIR/train/dogs"/* "../processed/dogs/" || true

    echo "Movendo imagens de validação..."
    mv "$UNZIPPED_DIR/validation/cats"/* "../processed/cats/" || true
    mv "$UNZIPPED_DIR/validation/dogs"/* "../processed/dogs/" || true

    echo "Limpeza..."
    # Remove o diretório descompactado para evitar duplicação
    rm -rf "$UNZIPPED_DIR"
else
    echo "⚠️ Diretório de origem não encontrado: $UNZIPPED_DIR/train"
    echo "Por favor, verifique a estrutura do arquivo ZIP."
    exit 1
fi

echo "✅ Dataset preparado em: $PROCESSED_DIR"
