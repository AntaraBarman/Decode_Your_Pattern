"""Quiz + assessment endpoints."""
from __future__ import annotations

import random

from fastapi import APIRouter

from .. import data, engine
from ..schemas import AssessmentInput

router = APIRouter(tags=["assessments"])


@router.get("/quiz/questions")
def get_questions(per_dimension: int = 3) -> dict:
    """Return a randomised question set (drawn fresh each call, like v1)."""
    questions = []
    for dim, bank in data.QUESTION_BANK.items():
        chosen = random.sample(bank, min(per_dimension, len(bank)))
        for q in chosen:
            questions.append({
                "id": q["id"], "dimension": dim, "text": q["text"],
                "options": [{"label": o["label"], "score": o["score"]} for o in q["options"]],
            })
    random.shuffle(questions)
    return {"count": len(questions), "questions": questions}


@router.post("/assessments")
def create_assessment(payload: AssessmentInput) -> dict:
    """Score the answers and return the full explainable report."""
    responses = [r.model_dump() for r in payload.responses]
    report = engine.analyze(responses)
    return {"template": payload.template, "report": report}
