## Criando um Sistema de Recomendação por Imagens Digitais.

![bairesDev](https://github.com/user-attachments/assets/38e4f46b-98ba-48fc-86e6-793560fdf4cf)


**Bootcamp BairesDev - Machine Learning Training.**


---



# 📸 Sistem de Recomendação de Imagens 

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![CI](https://github.com/Santosdevbjj/sistemRecomendaImag/actions/workflows/ci.yml/badge.svg)](https://github.com/Santosdevbjj/sistemRecomendaImag/actions)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()

Sistema de recomendação de imagens baseado em **aprendizado de máquina** e **embeddings visuais**.  
O projeto permite treinar modelos de similaridade, extrair embeddings de imagens, e realizar buscas eficientes entre imagens (e.g., encontrar imagens de gatos semelhantes a outras imagens de gatos).

---

## 🚀 Tecnologias Utilizadas

- **Python 3.9+**
- **Docker** & **Docker Compose**
- **Jupyter Notebook** (para experimentos e prototipação)
- **PyTorch / TensorFlow** (dependendo do `requirements.txt`)
- **FastAPI** (API para servir as recomendações)
- **Shell Scripts** para automação
- **GitHub Actions** (CI/CD automatizado)

---

## 💻 Requisitos

### Hardware
- CPU Quad-Core  
- 8 GB RAM (mínimo)  
- GPU NVIDIA (opcional, recomendado para treinamento mais rápido)  
- 5 GB de espaço livre em disco  

### Software
- [Python 3.9+](https://www.python.org/downloads/)  
- [Docker](https://www.docker.com/) (opcional, mas recomendado)  
- [pip](https://pip.pypa.io/en/stable/)  

---

## 📂 Estrutura do Projeto

```bash
sistemRecomendaImag/
│── .gitignore                # Arquivos e pastas ignorados pelo Git
│── requirements.txt          # Dependências do projeto
│── Dockerfile                # Definição da imagem Docker
│── docker-compose.yml        # Orquestração de containers
│
├── .github/
│   └── workflows/ci.yml      # Pipeline de integração contínua (CI)
│
├── data/
│   ├── models/               # Modelos treinados
│   └── processed/
│       ├── cats/             # Dataset processado - gatos
│       └── dogs/             # Dataset processado - cachorros
│
├── src/
│   ├── data/dataset.py       # Classe de gerenciamento de datasets
│   ├── features/extractor.py # Extração de features/embeddings
│   ├── models/
│   │   ├── backbone.py       # Modelo base
│   │   ├── embedding_model.py# Modelo de embeddings
│   │   └── train.py          # Script de treinamento
│   ├── recommender/
│   │   ├── similarity.py     # Cálculo de similaridade
│   │   └── index.py          # Indexação para busca eficiente
│   ├── utils/
│   │   ├── io.py             # Funções utilitárias de entrada/saída
│   │   └── viz.py            # Visualização de imagens/resultados
│   └── webapp/app.py         # API Web (FastAPI)
│
├── notebooks/
│   ├── 01-data-exploration.ipynb   # Exploração dos dados
│   ├── 01_train_and_test.ipynb     # Treinamento e teste
│   ├── 01_train_and_similarity.ipynb # Similaridade entre embeddings
│   ├── 02-train-embeddings.ipynb   # Treinamento de embeddings
│   ├── 02_api_inference.ipynb      # Inferência via API
│   └── 03-search-and-eval.ipynb    # Busca e avaliação
│
├── scripts/
│   ├── prepare_data.sh        # Script de preparação de dados
│   └── run_local.sh           # Script de execução local
│
└── tests/
    ├── test_dataset.py        # Testes de datasets
    ├── test_similarity.py     # Testes de similaridade
    └── test_api.py            # Testes da API
```


---



⚙️ **Como Executar o Projeto**

🔹 1. Clonar o repositório

git clone https://github.com/Santosdevbjj/sistemRecomendaImag.git
cd sistemRecomendaImag

🔹 2. Criar ambiente virtual e instalar dependências

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt

🔹 3. Executar localmente

bash scripts/run_local.sh

🔹 4. Rodar com Docker

docker-compose up --build

A aplicação estará disponível em:
👉 http://localhost:8000

🔹 5. Testar a API

pytest tests/


---

🧪 **Exemplos de Uso**

Treinar modelo:

python src/models/train.py --epochs 10 --batch-size 32

Extrair embeddings de imagens:

python src/features/extractor.py --input data/processed/cats/ --output data/models/cat_embeddings.pkl

Rodar API para recomendações:

uvicorn src.webapp.app:app --reload



---

📖 **Notebooks Disponíveis**

01-data-exploration.ipynb → análise inicial do dataset

01_train_and_test.ipynb → treino + avaliação

02-train-embeddings.ipynb → embeddings customizados

03-search-and-eval.ipynb → busca baseada em similaridade

02_api_inference.ipynb → testes diretos da API



---

📌 **Contribuição**

1. Faça um fork do projeto


2. Crie uma branch para sua feature: git checkout -b minha-feature


3. Commit suas alterações: git commit -m 'Minha nova feature'


4. Faça push para a branch: git push origin minha-feature


5. Abra um Pull Request 🚀




---

📜 **Licença**

Este projeto está sob a licença MIT.
Sinta-se livre para usar, modificar e distribuir.


---


**Contato:**

[![Portfólio Sérgio Santos](https://img.shields.io/badge/Portfólio-Sérgio_Santos-111827?style=for-the-badge&logo=githubpages&logoColor=00eaff)](https://santosdevbjj.github.io/portfolio/)
[![LinkedIn Sérgio Santos](https://img.shields.io/badge/LinkedIn-Sérgio_Santos-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/santossergioluiz) 

---






