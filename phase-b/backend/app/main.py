"""FastAPI application entry point.

Run locally:   uvicorn app.main:app --reload
Interactive docs:  http://127.0.0.1:8000/docs
"""
from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .routers import assessments, coach

app = FastAPI(
    title="Decode Your Pattern API",
    version=__version__,
    description=(
        "Explainable, rule-based behavioural-intelligence API. "
        "Returns observations for self-reflection — not clinical or scientific assessments."
    ),
)

# CORS — allow the frontend origins (comma-separated env var), default to local dev.
_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assessments.router, prefix="/api/v1")
app.include_router(coach.router, prefix="/api/v1")


@app.get("/", tags=["meta"])
def root() -> dict:
    return {"name": "Decode Your Pattern API", "version": __version__, "docs": "/docs"}


@app.get("/api/v1/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok"}
