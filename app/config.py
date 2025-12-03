import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


auth_required_env_vars = [
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_KEY",
    "AZURE_OPENAI_DEPLOYMENT",
    "AZURE_SEARCH_ENDPOINT",
    "AZURE_SEARCH_KEY",
    "AZURE_SEARCH_INDEX",
]


def _get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@dataclass
class Settings:
    azure_openai_endpoint: str = _get_env("AZURE_OPENAI_ENDPOINT")
    azure_openai_key: str = _get_env("AZURE_OPENAI_KEY")
    azure_openai_deployment: str = _get_env("AZURE_OPENAI_DEPLOYMENT")
    azure_search_endpoint: str = _get_env("AZURE_SEARCH_ENDPOINT")
    azure_search_key: str = _get_env("AZURE_SEARCH_KEY")
    azure_search_index: str = _get_env("AZURE_SEARCH_INDEX")
    top_k: int = int(os.getenv("AZURE_SEARCH_TOP_K", "5"))
    max_tokens: int = int(os.getenv("AZURE_OPENAI_MAX_TOKENS", "400"))
    temperature: float = float(os.getenv("AZURE_OPENAI_TEMPERATURE", "0"))


settings = Settings()
