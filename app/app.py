from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.services.rag import RAGService

app = FastAPI(title="Azure RAG App")
rag_service = RAGService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask")
def ask(question: QuestionRequest) -> dict:
    if not question.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    return rag_service.generate_answer(question.question)


app.mount("/", StaticFiles(directory="public", html=True), name="static")
