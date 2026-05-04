from __future__ import annotations

import time
from typing import Dict, List
import requests

from edgeguard_sim.data import SCENARIOS
from edgeguard_sim.gateway import AdversarialFilter, SemanticDeidentifier
from edgeguard_sim.rag import SecureRetriever


def _threat_status(score: float, blocked: bool) -> str:
    if blocked:
        return "BLOCKED"
    if score >= 0.30:
        return "MONITORED"
    return "SAFE"


class EdgeGuardService:
    def __init__(self) -> None:
        self.deidentifier = SemanticDeidentifier()
        self.filter = AdversarialFilter()
        self.retriever = SecureRetriever()
        self.prior_threat_level = 0.0

    # -------------------------
    # OLLAMA FUNCTION (FIXED)
    # -------------------------
    def call_ollama(self, prompt: str) -> Dict[str, object]:
        print("🚀 USING OLLAMA FUNCTION")

        try:
            response = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=100
            )

            data = response.json()

            return {
                "text": data.get("response", ""),
                "provider": "ollama",
                "model": "llama3",
                "fallback_used": False,
                "live_configured": True,
                "error": "",
                "path": "provider"
            }

        except Exception as e:
            print("❌ OLLAMA ERROR:", e)

            return {
                "text": "Error calling Ollama",
                "provider": "fallback",
                "model": "none",
                "fallback_used": True,
                "live_configured": False,
                "error": str(e),
                "path": "fallback"
            }

    # -------------------------
    # APP STATUS
    # -------------------------
    def app_status(self) -> Dict[str, object]:
        return {
            "primary_configured": True,
            "online_fallback_configured": False,
            "scenario_count": len(SCENARIOS),
            "hint": "Ollama local provider active.",
        }

    # -------------------------
    # SCENARIOS
    # -------------------------
    def scenarios(self) -> List[dict]:
        return [
            {
                "id": item["id"],
                "label": item["label"],
                "role": item["role"],
                "query": item["query"],
                "intent": item["intent"],
            }
            for item in SCENARIOS
        ]

    # -------------------------
    # MAIN PIPELINE
    # -------------------------
    def process(self, query: str, role: str = "operations") -> Dict[str, object]:
        print("🔥 PROCESS STARTED")

        started = time.perf_counter()

        # Step 1: De-identification
        deid = self.deidentifier.sanitize(query)

        # Step 2: Threat filtering
        threat = self.filter.inspect(
            deid.sanitized_text,
            prior_threat_level=self.prior_threat_level
        )

        if threat.blocked:
            retrieval_docs: List[dict] = []

            exposure_prevented = any(
                token in deid.sanitized_text.lower()
                for token in (
                    "secret", "password", "confidential",
                    "formula", "serial", "supplier", "prompt"
                )
            )

            llm_result = {
                "text": "Request blocked by security filter.",
                "provider": "edgeguard-policy-engine",
                "model": "pre-inference-block",
                "fallback_used": False,
                "live_configured": True,
                "error": "",
                "path": "blocked",
            }

        else:
            # Step 3: Retrieval
            retrieval = self.retriever.retrieve(deid.sanitized_text, role)
            retrieval_docs = retrieval.documents
            exposure_prevented = retrieval.exposure_prevented

            # Step 4: CALL OLLAMA (FIXED LINE)
            llm_result = self.call_ollama(deid.sanitized_text)

        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        self.prior_threat_level = threat.score

        timeline = [
            {
                "stage": "Semantic De-identification",
                "status": "completed",
                "detail": f"{len(deid.replacements)} sensitive elements redacted",
            },
            {
                "stage": "Adversarial Input Filtering",
                "status": "blocked" if threat.blocked else "completed",
                "detail": threat.policy_action.replace("_", " "),
            },
            {
                "stage": "Secure Local Retrieval",
                "status": "skipped" if threat.blocked else "completed",
                "detail": (
                    "no retrieval executed"
                    if threat.blocked
                    else f"{len(retrieval_docs)} documents approved"
                ),
            },
            {
                "stage": "LLM Response Synthesis",
                "status": "skipped" if threat.blocked else "completed",
                "detail": (
                    "policy block returned"
                    if threat.blocked
                    else f"{llm_result['provider']} / {llm_result['model']}"
                ),
            },
        ]

        return {
            "original_query": query,
            "role": role,
            "sanitized_query": deid.sanitized_text,
            "metrics": {
                "latency_ms": elapsed_ms,
                "threat_score": round(threat.score, 3),
                "redaction_count": len(deid.replacements),
                "retrieved_documents": len(retrieval_docs),
            },
            "threat": {
                "status": _threat_status(threat.score, threat.blocked),
                "blocked": threat.blocked,
                "reasons": threat.reasons,
                "policy_action": threat.policy_action,
            },
            "redactions": deid.replacements,
            "retrieval": {
                "documents": retrieval_docs,
                "restricted_exposure_prevented": exposure_prevented,
            },
            "llm": llm_result,
            "response": llm_result["text"],
            "timeline": timeline,
        }