"""Unit tests for the behavioural-intelligence engine (pure, no network)."""
from __future__ import annotations

from app import data, engine


def _responses(score_each: int):
    """Build a full set of responses giving every dimension the same score."""
    out = []
    for dim, bank in data.QUESTION_BANK.items():
        for q in bank:
            out.append({"question_id": q["id"], "dimension": dim, "score": score_each, "max": 8})
    return out


def test_score_dimensions_bounds():
    d = engine.score_dimensions(_responses(8))
    assert set(d.keys()) == set(data.PARAM_KEYS)
    assert all(0 <= v <= 10 for v in d.values())


def test_pattern_score_bands():
    low = engine.pattern_score({k: 0 for k in data.PARAM_KEYS})
    high = engine.pattern_score({k: 10 for k in data.PARAM_KEYS})
    assert low["score"] == 300 and low["band"] == "High-friction"
    assert high["score"] == 900 and high["band"] == "Exceptional"


def test_analyze_shape():
    report = engine.analyze(_responses(6))
    assert 300 <= report["pattern_score"] <= 900
    assert len(report["dimensions"]) == 10
    assert len(report["insights"]) == 6           # 4 styles + hidden + blind spot
    assert len(report["domains"]) == 6
    assert len(report["competencies"]) == 8
    assert len(report["recommendations"]) == 6    # 2 weakest dims × 3 items
    assert report["avatar"]["name"].startswith("The ")


def test_insights_are_explainable():
    report = engine.analyze(_responses(5))
    for ins in report["insights"]:
        assert ins["observation"] and ins["why"]
        assert 0.0 <= ins["confidence"] <= 1.0


def test_edge_cases_do_not_crash():
    for s in (0, 1, 5, 8):
        engine.analyze(_responses(s))
