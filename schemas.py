from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field

class Reflection(BaseModel): # not being used because of gemini limitation
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")


class AnswerQuestion(BaseModel):
    """Answer the question."""

    answer: str = Field(description="~250 word detailed answer to the question.")
    # reflection: Reflection = Field(description="Your reflection on the initial answer.") #gemini cant handle nested pydantic object
    reflection: str = Field(description="Your reflection on the initial answer which should include Critique of what is missing and Critique of what is superfluous")
    search_queries: List[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )

class ReviseAnswer(AnswerQuestion):
    "Revises your original answer to your question. "

    references : List[str] =  Field(description="Citations motivating your updated answer")

