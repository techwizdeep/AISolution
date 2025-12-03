# Azure RAG App

A minimal Retrieval-Augmented Generation (RAG) web app using Azure OpenAI, Azure AI Search, FastAPI backend, and a lightweight vanilla JavaScript frontend. Suitable for deployment to Azure Web App.

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
  - Optional: `AZURE_SEARCH_TOP_K`, `AZURE_OPENAI_MAX_TOKENS`, `AZURE_OPENAI_TEMPERATURE`

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
2. Enable the startup command, for example:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.app:app
   ```
3. Deploy the project files (e.g., via ZIP deploy or GitHub Actions). The FastAPI app will serve both the API and static frontend from the `public/` directory.
