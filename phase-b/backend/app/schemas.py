"""Pydantic models — request/response validation for the API."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ResponseItem(BaseModel):
    question_id: str
    dimension: str
    score: int = Field(ge=0, le=10)
    max: int = Field(gt=0, le=10)


class AssessmentInput(BaseModel):
    template: str = "default"
    responses: list[ResponseItem]


class Option(BaseModel):
    label: str
    score: int


class Question(BaseModel):
    id: str
    dimension: str
    text: str
    options: list[Option]


class CoachMessage(BaseModel):
    """One turn of a conversation with the AI Coach.

    `report` is the user's generated report (the ONLY context the coach gets).
    """
    message: str
    report: dict
    history: list[dict] = []


class CoachReply(BaseModel):
    reply: str
    source: str  # "llm" or "rule-based-fallback"
