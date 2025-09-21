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

# Use find para mover de forma confiável os arquivos de imagem
if [ -d "$UNZIPPED_DIR/train" ]; then
    echo "Movendo imagens de treino..."
    # Move imagens de gatos
    find "$UNZIPPED_DIR/train/cats" -name "*.jpg" -exec mv {} "../processed/cats/" \;
    # Move imagens de cachorros
    find "$UNZIPPED_DIR/train/dogs" -name "*.jpg" -exec mv {} "../processed/dogs/" \;

    echo "Movendo imagens de validação..."
    find "$UNZIPPED_DIR/validation/cats" -name "*.jpg" -exec mv {} "../processed/cats/" \;
    find "$UNZIPPED_DIR/validation/dogs" -name "*.jpg" -exec mv {} "../processed/dogs/" \;

    echo "Limpeza..."
    # Remove o diretório descompactado para evitar duplicação
    rm -rf "$UNZIPPED_DIR"
else
    echo "⚠️ Diretório de origem não encontrado: $UNZIPPED_DIR/train"
    echo "Por favor, verifique a estrutura do arquivo ZIP."
    exit 1
fi

echo "✅ Dataset preparado em: $PROCESSED_DIR"
