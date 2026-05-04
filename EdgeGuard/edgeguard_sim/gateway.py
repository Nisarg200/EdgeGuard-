"""Gateway logic for semantic de-identification and adversarial filtering."""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from .models import DeidentificationResult, ThreatAssessment


class SemanticDeidentifier:
    """Masks sensitive industrial identifiers while preserving request meaning."""

    def __init__(self) -> None:
        self.patterns: List[Tuple[str, str]] = [
            (r"\b[A-Z]{1,4}-\d{2,6}(?:-[A-Z0-9]+)?\b", "asset_id"),
            (r"\bFORM-\d{2,4}-[A-Z0-9]+\b", "formula_ref"),
            (r"\bEMP-\d{3,6}\b", "employee_id"),
            (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "ip_address"),
        ]

    def sanitize(self, text: str) -> DeidentificationResult:
        replacements: List[str] = []
        sanitized = text
        counters: Dict[str, int] = {}

        for pattern, label in self.patterns:
            def repl(match: re.Match[str]) -> str:
                counters[label] = counters.get(label, 0) + 1
                token = f"<{label}_{counters[label]}>"
                replacements.append(f"{match.group(0)} -> {token}")
                return token

            sanitized = re.sub(pattern, repl, sanitized)

        return DeidentificationResult(
            sanitized_text=sanitized,
            replacements=replacements,
            sensitive_hits=len(replacements),
        )


class AdversarialFilter:
    """Scores and blocks natural-language prompt injection and exfiltration attempts."""

    def __init__(self) -> None:
        self.rules = {
            r"\b(ignore|disregard|forget)\b.{0,30}\b(instructions?|rules?|prompts?)\b": ("Prompt override attempt", 0.45),
            r"\bact as\b.{0,20}\b(admin|administrator|root|superuser)\b": ("Privilege escalation request", 0.45),
            r"\b(reveal|show|print|display|expose)\b.{0,40}\b(system|developer|hidden|internal)\b.{0,20}\bprompts?\b": (
                "System-prompt extraction attempt",
                0.60,
            ),
            r"\b(reveal|show|print|expose|dump)\b.{0,40}\b(secret|secrets|credential|credentials|password|token|key)\b": (
                "Secret exfiltration attempt",
                0.55,
            ),
            r"\b(dump|export|list)\b.{0,40}\b(logs?|database|db|records?|confidential|secrets?)\b": (
                "Bulk extraction attempt",
                0.50,
            ),
            r"\b(bypass|override|disable)\b.{0,30}\b(guardrails?|safety|policy|restrictions?)\b": (
                "Policy bypass request",
                0.45,
            ),
            r"\bjailbreak\b|\bdo anything now\b": ("Jailbreak-style prompt detected", 0.45),
        }

    def inspect(self, text: str, prior_threat_level: float = 0.0) -> ThreatAssessment:
        normalized = re.sub(r"[^a-z0-9\s]", " ", text.lower())
        normalized = re.sub(r"\s+", " ", normalized).strip()
        score = min(prior_threat_level, 0.3) * 0.10
        reasons: List[str] = []

        for pattern, (reason, weight) in self.rules.items():
            if re.search(pattern, normalized):
                score += weight
                reasons.append(reason)

        if "confidential" in normalized or "proprietary" in normalized:
            score += 0.20
            reasons.append("Sensitive-data harvesting language")

        reveal_words = {"reveal", "show", "print", "display", "expose", "dump"}
        admin_words = {"admin", "administrator", "root", "superuser"}
        prompt_words = {"prompt", "prompts", "system", "developer", "internal", "hidden"}
        token_set = set(normalized.split())

        if token_set.intersection(reveal_words) and token_set.intersection(prompt_words):
            score += 0.25
            reasons.append("Prompt-disclosure combination detected")

        if token_set.intersection(admin_words) and token_set.intersection(reveal_words):
            score += 0.20
            reasons.append("Admin-plus-extraction combination detected")

        if "system prompt" in normalized or "developer prompt" in normalized:
            score += 0.30
            reasons.append("Direct prompt-targeting language")

        blocked = score >= 0.65
        reasons = list(dict.fromkeys(reasons))
        policy_action = "block_and_escalate" if blocked else "allow_with_monitoring" if score >= 0.30 else "allow"
        return ThreatAssessment(blocked=blocked, score=min(score, 1.0), reasons=reasons, policy_action=policy_action)
