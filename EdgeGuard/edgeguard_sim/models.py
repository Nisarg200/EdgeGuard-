"""Dataclasses used by the EdgeGuard simulation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class DeidentificationResult:
    sanitized_text: str
    replacements: List[str]
    sensitive_hits: int


@dataclass
class ThreatAssessment:
    blocked: bool
    score: float
    reasons: List[str]
    policy_action: str


@dataclass
class RetrievalResult:
    documents: List[dict]
    exposure_prevented: bool
