from __future__ import annotations

from dataclasses import dataclass
from typing import List

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI

from app.config import settings


@dataclass
class RetrievedDocument:
    content: str
    source: str | None = None


class RAGService:
    def __init__(self) -> None:
        self.search_client = SearchClient(
            endpoint=settings.azure_search_endpoint,
            index_name=settings.azure_search_index,
            credential=AzureKeyCredential(settings.azure_search_key),
        )
        self.ai_client = AzureOpenAI(
            api_version="2024-02-01",
            api_key=settings.azure_openai_key,
            azure_endpoint=settings.azure_openai_endpoint,
        )

    def retrieve(self, query: str) -> List[RetrievedDocument]:
        results = self.search_client.search(search_text=query, top=settings.top_k)
        documents: List[RetrievedDocument] = []
        for item in results:
            content = item.get("content") or item.get("text") or ""
            source = item.get("source") or item.get("metadata_storage_path")
            documents.append(RetrievedDocument(content=content, source=source))
        return documents

    def build_prompt(self, question: str, documents: List[RetrievedDocument]) -> str:
        context_blocks = [f"Source {i+1}: {doc.content}" for i, doc in enumerate(documents)]
        context = "\n\n".join(context_blocks)
        system = (
            "You are a helpful assistant that answers questions using the provided context. "
            "If the answer is not in the context, say you don't know."
        )
        return (
            f"{system}\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer succinctly and cite sources."
        )

    def generate_answer(self, question: str) -> dict:
        documents = self.retrieve(question)
        prompt = self.build_prompt(question, documents)
        completion = self.ai_client.chat.completions.create(
            model=settings.azure_openai_deployment,
            messages=[{"role": "user", "content": prompt}],
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        )
        answer = completion.choices[0].message.content if completion.choices else ""
        sources = [doc.source for doc in documents if doc.source]
        return {"answer": answer, "sources": sources}
