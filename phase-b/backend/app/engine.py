"""Behavioral Intelligence Engine — explainable, rule-based, pure functions.

This is the Python port of the engine that powers the live v1 app. It is
deliberately free of side effects (no I/O, no globals mutated) so it is easy
to test and could later be swapped for an ML/LLM implementation behind the
same `analyze()` interface.

Every observation is framed as a *tendency* and ships with a `why` and a
`confidence` value — see docs/EXPLAINABILITY.md.
"""
from __future__ import annotations

from statistics import pstdev

from . import data

DimScores = dict[str, int]


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #
def score_dimensions(responses: list[dict]) -> DimScores:
    """Aggregate raw responses into a 0–10 score per dimension."""
    raw: dict[str, int] = {k: 0 for k in data.PARAM_KEYS}
    mx: dict[str, int] = {k: 0 for k in data.PARAM_KEYS}
    for r in responses:
        dim = r["dimension"]
        if dim not in raw:
            continue
        raw[dim] += int(r["score"])
        mx[dim] += int(r["max"])
    return {k: round((raw[k] / mx[k]) * 10) if mx[k] else 0 for k in data.PARAM_KEYS}


SCORE_BANDS = [
    (800, "Exceptional", "#22c55e"),
    (740, "Strong", "#84cc16"),
    (670, "Solid", "#eab308"),
    (580, "Developing", "#f59e0b"),
    (300, "High-friction", "#ef4444"),
]


def pattern_score(dim_scores: DimScores) -> dict:
    """Map the 10 dimensions to a single 300–900 'Pattern Score' with a band."""
    overall = min(100, sum(dim_scores.values()))  # each dim 0–10 → 0–100
    raw = 300 + (overall / 100) * 600
    score = round(raw / 5) * 5
    band = next((b for b in SCORE_BANDS if score >= b[0]), SCORE_BANDS[-1])
    return {"score": score, "band": band[1], "color": band[2],
            "percentile": max(1, min(99, round(overall * 0.95)))}


def _confidence(responses: list[dict], dim: str) -> float:
    """A simple internal-consistency confidence for one dimension (0–1).

    High agreement among a dimension's answers → higher confidence. This is a
    measure of *consistency*, not of correctness.
    """
    vals = [r["score"] / r["max"] for r in responses if r["dimension"] == dim and r["max"]]
    if len(vals) < 2:
        return 0.6
    return round(max(0.4, 1 - pstdev(vals)), 2)


# --------------------------------------------------------------------------- #
# Insights (each is an explainable observation)
# --------------------------------------------------------------------------- #
def build_insights(d: DimScores, responses: list[dict]) -> list[dict]:
    label = lambda k: data.PARAMS[k]["label"].lower()
    ordered = sorted(d.items(), key=lambda kv: kv[1], reverse=True)
    top, low = ordered[0], ordered[-1]
    ins: list[dict] = []

    def add(itype, title, obs, why, dim):
        ins.append({"type": itype, "title": title, "observation": obs,
                    "why": why, "confidence": _confidence(responses, dim)})

    # decision-making
    if d["selftrust"] >= 7 and d["clarity"] >= 7:
        dm = "You tend to decide on your own read and rarely relitigate it — fast, just sanity-check the big calls."
    elif d["selftrust"] <= 4:
        dm = "You tend to gather outside input before committing — safe, but it can outsource calls you could make alone."
    elif d["action"] <= 4:
        dm = "You tend to weigh options thoroughly; the risk is the window closing while you weigh."
    else:
        dm = "You tend to blend gut and input, adjusting as you go."
    add("decision", "Decision-making style", dm,
        "Drawn mainly from your self-trust and clarity responses.", "selftrust")

    # communication
    if d["boundaries"] >= 7 and d["selftrust"] >= 7:
        cm = "You tend to say what you mean and protect your limits — clear, occasionally blunt."
    elif d["boundaries"] <= 4:
        cm = "You tend to read the room and keep the peace — sometimes at the cost of saying what you need."
    else:
        cm = "You tend to adapt your tone to the situation rather than defaulting to one mode."
    add("communication", "Communication style", cm,
        "Based on your boundaries and awareness responses.", "boundaries")

    # stress
    if d["resilience"] >= 7:
        sr = "Pressure rarely knocks you far off line, and you recover quickly."
    elif d["resilience"] <= 4 and d["patience"] <= 4:
        sr = "Stress tends to land hard at first and can spill into the next day before you reset."
    else:
        sr = "Stress affects you, but you generally find your footing within a day or two."
    add("stress", "Stress response", sr,
        "Based on your resilience and patience responses.", "resilience")

    # learning
    if d["growth"] >= 7 and d["awareness"] >= 7:
        ls = "You tend to pull lessons from setbacks — yours and others' — and update fast."
    elif d["growth"] <= 4:
        ls = "Lessons tend to land through direct experience rather than observation — effective but expensive."
    else:
        ls = "You build understanding gradually and apply it once it feels solid."
    add("learning", "Learning style", ls,
        "Based on your growth and awareness responses.", "growth")

    # hidden potential
    cand = next((kv for kv in ordered[2:] if kv[1] >= 5), ordered[2])
    add("hidden_potential", "Hidden potential",
        f"Your {label(cand[0])} ({cand[1]*10}/100) is quietly solid but not yet a headline strength — leaning into it could make it a signature.",
        "It scores above the middle of your profile without being your top trait.", cand[0])

    # blind spot
    add("blind_spot", "Likely blind spot",
        f"{data.PARAMS[low[0]]['label']} ({low[1]*10}/100). {data.IMPROVEMENT_PHRASES[low[0]]} Because it scores low, you may not notice it operating.",
        f"It is your lowest-scoring dimension, driven by your {label(low[0])} responses.", low[0])

    return ins


# --------------------------------------------------------------------------- #
# Other report sections
# --------------------------------------------------------------------------- #
def build_avatar(d: DimScores) -> dict:
    best, best_score = None, -1.0
    for a in data.AVATARS.values():
        s = sum(d[x] for x in a["dims"]) / len(a["dims"])
        if s > best_score:
            best, best_score = a, s
    return {"name": best["name"], "emoji": best["emoji"]}


def build_dna(d: DimScores) -> dict:
    code = " · ".join(f"{data.PARAMS[k]['label'][:2].upper()}{d[k]}" for k in data.PARAM_KEYS)
    bars = [{"label": data.PARAMS[k]["label"], "score": d[k], "color": data.PARAMS[k]["color"]}
            for k in data.PARAM_KEYS]
    return {"code": code, "bars": bars}


def _pct(d: DimScores, dims: list[str]) -> int:
    return round(sum(d[k] for k in dims) / len(dims) * 10)


def build_domains(d: DimScores) -> list[dict]:
    return [{"name": dom["name"], "pct": _pct(d, dom["dims"])} for dom in data.DOMAINS]


def build_competencies(d: DimScores) -> list[dict]:
    return [{"name": c["name"], "pct": _pct(d, c["dims"])} for c in data.COMPETENCIES]


def build_recommendations(d: DimScores) -> list[dict]:
    weakest = [k for k, _ in sorted(d.items(), key=lambda kv: kv[1])[:2]]
    out: list[dict] = []
    for k in weakest:
        rec = data.RECOMMENDATIONS[k]
        dim = data.PARAMS[k]["label"]
        out.append({"category": "Book", "title": rec["book"][0],
                    "why": f"For your {dim.lower()} — {rec['book'][1]}."})
        out.append({"category": "Podcast", "title": rec["podcast"][0],
                    "why": f"For your {dim.lower()} — {rec['podcast'][1]}."})
        out.append({"category": "Habit", "title": rec["habit"],
                    "why": f"A small daily move for your {dim.lower()}."})
    return out


# --------------------------------------------------------------------------- #
# Public interface
# --------------------------------------------------------------------------- #
def analyze(responses: list[dict]) -> dict:
    """The single entry point. v1: rule-based. v2 could blend in ML here."""
    d = score_dimensions(responses)
    ps = pattern_score(d)
    ordered = sorted(d.items(), key=lambda kv: kv[1], reverse=True)
    return {
        "pattern_score": ps["score"],
        "band": ps["band"],
        "band_color": ps["color"],
        "percentile": ps["percentile"],
        "dimensions": d,
        "avatar": build_avatar(d),
        "dna": build_dna(d),
        "top_strength": data.PARAMS[ordered[0][0]]["label"],
        "growth_focus": data.PARAMS[ordered[-1][0]]["label"],
        "insights": build_insights(d, responses),
        "domains": build_domains(d),
        "competencies": build_competencies(d),
        "recommendations": build_recommendations(d),
        "disclaimer": ("These are observations derived from your responses, offered for "
                       "self-reflection. This is not a clinical or scientific assessment."),
    }
