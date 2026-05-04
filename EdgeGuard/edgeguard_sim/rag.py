"""Secure RAG retrieval for local contextualization."""

from __future__ import annotations

import re
from typing import List

from .data import KNOWLEDGE_BASE
from .models import RetrievalResult


class SecureRetriever:
    """Retrieves only the minimum local context allowed for a given role."""

    ACCESS_ORDER = {
        "operations": {"operations"},
        "maintenance": {"maintenance", "operations"},
        "security": {"security", "operations"},
    }

    def __init__(self) -> None:
        self.knowledge_base = KNOWLEDGE_BASE

    def retrieve(self, query: str, role: str, top_k: int = 2) -> RetrievalResult:
        allowed_access = self.ACCESS_ORDER.get(role, {role})
        tokens = set(re.findall(r"[a-z]{4,}", query.lower()))
        scored: List[tuple[int, dict]] = []
        exposure_prevented = False

        for doc in self.knowledge_base:
            if doc["access"] == "restricted":
                if any(term in tokens for term in ("secret", "serial", "formula", "password", "supplier", "prompt")):
                    exposure_prevented = True
                continue

            if doc["access"] not in allowed_access:
                continue

            overlap = len(tokens.intersection(set(doc["tags"])))
            if overlap:
                scored.append((overlap, doc))

        scored.sort(key=lambda item: item[0], reverse=True)
        docs = [doc for _, doc in scored[:top_k]]
        return RetrievalResult(documents=docs, exposure_prevented=exposure_prevented)
