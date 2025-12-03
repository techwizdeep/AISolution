import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def _get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@dataclass
class Settings:
    azure_openai_endpoint: str
    azure_openai_key: str
    azure_openai_deployment: str
    azure_openai_api_version: str
    azure_search_endpoint: str
    azure_search_key: str
    azure_search_index: str
    top_k: int
    max_tokens: int
    temperature: float


@lru_cache
def get_settings() -> Settings:
    return Settings(
        azure_openai_endpoint=_get_env("AZURE_OPENAI_ENDPOINT"),
        azure_openai_key=_get_env("AZURE_OPENAI_KEY"),
        azure_openai_deployment=_get_env("AZURE_OPENAI_DEPLOYMENT"),
        azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        azure_search_endpoint=_get_env("AZURE_SEARCH_ENDPOINT"),
        azure_search_key=_get_env("AZURE_SEARCH_KEY"),
        azure_search_index=_get_env("AZURE_SEARCH_INDEX"),
        top_k=int(os.getenv("AZURE_SEARCH_TOP_K", "5")),
        max_tokens=int(os.getenv("AZURE_OPENAI_MAX_TOKENS", "400")),
        temperature=float(os.getenv("AZURE_OPENAI_TEMPERATURE", "0")),
    )
