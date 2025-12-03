from openai import AzureOpenAI

from config.settings import Settings


class AzureOpenAIClient:
    def __init__(self, settings: Settings) -> None:
        self.client = AzureOpenAI(
            api_version=settings.azure_openai_api_version,
            api_key=settings.azure_openai_key,
            azure_endpoint=settings.azure_openai_endpoint,
        )
        self.deployment = settings.azure_openai_deployment
        self.temperature = settings.temperature
        self.max_tokens = settings.max_tokens

    def generate_answer(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return completion.choices[0].message.content if completion.choices else ""
