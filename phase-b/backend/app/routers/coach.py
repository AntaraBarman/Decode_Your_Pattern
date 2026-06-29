"""AI Coach — answers using ONLY the user's report as context.

- If an LLM key is configured (env `LLM_API_KEY`), it calls a free-tier,
  OpenAI-compatible provider (e.g. Groq) and returns a real AI reply.
- If no key is set, it falls back to a safe rule-based reply, so the endpoint
  always works with zero setup.

The coach is system-prompted to encourage reflection and to refuse therapy,
diagnosis, or professional (medical/legal/financial) advice.
"""
from __future__ import annotations

import os

import httpx
from fastapi import APIRouter

from ..schemas import CoachMessage, CoachReply

router = APIRouter(tags=["coach"])

SYSTEM_PROMPT = (
    "You are a warm, concise reflection coach inside the app 'Decode Your Pattern'. "
    "You may use ONLY the user's report (provided as JSON) as context about them. "
    "Encourage self-reflection, suggest small habits and learning strategies, and ask "
    "one gentle question back. Frame everything as tendencies and observations, never "
    "facts or diagnoses. You must NOT provide therapy, medical, legal, or financial "
    "advice; if asked, kindly defer to a qualified professional. Keep replies under 150 words."
)


def _fallback(msg: CoachMessage) -> str:
    r = msg.report or {}
    strength = r.get("top_strength", "your strengths")
    focus = r.get("growth_focus", "your growth area")
    return (
        f"Thanks for sharing that. Based on your report, your steadiest strength looks like "
        f"**{strength}**, while **{focus}** is the area with the most room. A small step this "
        f"week: pick one situation linked to {focus.lower()} and try a single different move, "
        f"then notice what changed.\n\nWhat feels like the very next small action you could take? "
        f"\n\n_(I'm a reflection tool, not a substitute for professional advice.)_"
    )


@router.post("/coach/message", response_model=CoachReply)
async def coach_message(msg: CoachMessage) -> CoachReply:
    api_key = os.getenv("LLM_API_KEY", "").strip()
    if not api_key:
        return CoachReply(reply=_fallback(msg), source="rule-based-fallback")

    base_url = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
    model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"User report JSON:\n{msg.report}"},
        *msg.history,
        {"role": "user", "content": msg.message},
    ]
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{base_url}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": messages, "temperature": 0.7, "max_tokens": 280},
            )
            resp.raise_for_status()
            reply = resp.json()["choices"][0]["message"]["content"].strip()
            return CoachReply(reply=reply, source="llm")
    except Exception:
        # Never break the UX — degrade gracefully to the rule-based reply.
        return CoachReply(reply=_fallback(msg), source="rule-based-fallback")
