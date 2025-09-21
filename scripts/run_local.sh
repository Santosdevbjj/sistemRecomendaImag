#!/usr/bin/env bash
#
# scripts/run_local.sh
# Inicia a API FastAPI localmente com Uvicorn para desenvolvimento.
#

# Navega para o diretório raiz do projeto para garantir que o Python
# encontre os módulos do 'src' corretamente.
cd "$(dirname "$0")/.."

# Inicia o servidor Uvicorn
# --host 0.0.0.0: Permite que o servidor seja acessível de fora do localhost.
# --port 8000: Define a porta.
# --reload: Recarrega o servidor automaticamente quando o código muda.
python -m uvicorn src.webapp.app:app --host 0.0.0.0 --port 8000 --reload
