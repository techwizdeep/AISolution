from pydantic import BaseModel, Field, field_validator


class QuestionRequest(BaseModel):
    question: str = Field(..., description="User question for the RAG system")

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Question cannot be empty")
        return cleaned


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)
