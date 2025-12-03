# Azure RAG App

A minimal Retrieval-Augmented Generation (RAG) web app using Azure OpenAI, Azure AI Search, a FastAPI backend, and a vanilla JavaScript frontend. Designed for local development and deployment to Azure Web App.

## Project layout
```
azure-rag-app/
├─ pyproject.toml
├─ .env                      # local-only secrets (NOT checked in)
├─ config/
│  ├─ __init__.py
│  └─ settings.py            # config handling (env + defaults)
├─ models/
│  ├─ __init__.py
│  └─ chat.py                # Pydantic models for API
├─ app/
│  ├─ __init__.py
│  ├─ app.py                 # FastAPI entrypoint
│  ├─ services/
│  │  ├─ openai_client.py    # Azure OpenAI helper
│  │  └─ search_client.py    # Azure AI Search helper
├─ templates/
│  └─ index.html             # vanilla JS chat UI
└─ static/
   ├─ css/
   │  └─ site.css
   └─ js/
      └─ chat.js
```

## Prerequisites
- Python 3.10+
- Azure OpenAI resource with a deployed chat model
- Azure AI Search service with an index containing `content` (or `text`) and optional `source` fields
- Environment variables configured locally or in Azure Web App:
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_KEY`
  - `AZURE_OPENAI_DEPLOYMENT`
  - `AZURE_SEARCH_ENDPOINT`
  - `AZURE_SEARCH_KEY`
  - `AZURE_SEARCH_INDEX`
  - Optional: `AZURE_OPENAI_API_VERSION`, `AZURE_SEARCH_TOP_K`, `AZURE_OPENAI_MAX_TOKENS`, `AZURE_OPENAI_TEMPERATURE`

## Running locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```
Visit http://localhost:8000 to use the app.

## Deploying to Azure Web App
1. Create an Azure Web App (Python runtime) and set the environment variables above in the App Settings.
2. Use a startup command such as:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.app:app
   ```
3. Deploy the project files (e.g., via ZIP deploy or GitHub Actions). The FastAPI app serves the API, HTML template, and static assets.
