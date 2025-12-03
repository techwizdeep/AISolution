from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.openai_client import AzureOpenAIClient
from app.services.search_client import AzureSearchService
from config.settings import get_settings
from models.chat import AnswerResponse, QuestionRequest

settings = get_settings()
app = FastAPI(title="Azure RAG App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

search_service = AzureSearchService(settings)
openai_client = AzureOpenAIClient(settings)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def build_prompt(question: str, documents: list[dict]) -> str:
    context_blocks = [f"Source {i+1}: {doc['content']}" for i, doc in enumerate(documents)]
    context = "\n\n".join(context_blocks) if context_blocks else "No relevant context found."
    system = (
        "You are a helpful assistant that answers questions using the provided context. "
        "If the answer is not in the context, say you don't know."
    )
    return f"{system}\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer succinctly and cite sources."


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask(question: QuestionRequest) -> AnswerResponse:
    documents = search_service.retrieve(question.question)
    prompt = build_prompt(question.question, documents)
    answer = openai_client.generate_answer(prompt)
    if not answer:
        raise HTTPException(status_code=500, detail="No answer generated")
    sources = [doc["source"] for doc in documents if doc.get("source")]
    return AnswerResponse(answer=answer, sources=sources)
