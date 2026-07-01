"""Simple keyword retrieval for the first CM-EGQA pilot."""

from __future__ import annotations

from typing import Any


def retrieve_evidence(
    query: str,
    evidence: list[dict[str, Any]],
    *,
    top_k: int = 4,
) -> list[dict[str, Any]]:
    scored: list[tuple[int, dict[str, Any]]] = []
    for item in evidence:
        keywords = item.get("keywords", [])
        text = item.get("text", "")
        score = 0
        for keyword in keywords:
            if keyword and keyword in query:
                score += 3
            if keyword and keyword in text:
                score += 1
        if item.get("title") and any(token in query for token in item["title"].split()):
            score += 1
        scored.append((score, item))

    ranked = sorted(scored, key=lambda pair: pair[0], reverse=True)
    return [item for score, item in ranked[:top_k] if score > 0]
