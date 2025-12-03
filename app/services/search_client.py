from typing import List

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from config.settings import Settings


class AzureSearchService:
    def __init__(self, settings: Settings) -> None:
        self.client = SearchClient(
            endpoint=settings.azure_search_endpoint,
            index_name=settings.azure_search_index,
            credential=AzureKeyCredential(settings.azure_search_key),
        )
        self.top_k = settings.top_k

    def retrieve(self, query: str) -> List[dict]:
        results = self.client.search(search_text=query, top=self.top_k)
        documents: List[dict] = []
        for item in results:
            content = item.get("content") or item.get("text") or ""
            source = item.get("source") or item.get("metadata_storage_path")
            documents.append({"content": content, "source": source})
        return documents
