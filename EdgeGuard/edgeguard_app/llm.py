"""OpenAI-compatible LLM client with online and offline fallback modes."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import List


def _is_local_base_url(base_url: str) -> bool:
    return "127.0.0.1" in base_url or "localhost" in base_url


class OfflineGroundedResponder:
    provider = "offline-fallback"
    model = "edgeguard-grounded-simulator"

    def generate(self, query: str, docs: List[dict], role: str) -> dict:
        if not docs:
            text = (
                "No approved local context matched this request strongly enough, so EdgeGuard is returning a "
                "minimal safety-focused answer. Confirm operating conditions locally before taking action."
            )
        else:
            bullets = [f"- {doc['title']}: {doc['content']}" for doc in docs[:2]]
            text = (
                "EdgeGuard grounded response\n\n"
                f"Role: {role}\n"
                "Approved local guidance:\n"
                f"{chr(10).join(bullets)}\n\n"
                f"Recommended answer: Based on the sanitized request '{query}', follow the approved SOP guidance "
                "above, limit actions to locally validated steps, and require human confirmation before any "
                "physical intervention."
            )

        return {
            "text": text,
            "provider": self.provider,
            "model": self.model,
            "fallback_used": True,
            "live_configured": False,
            "error": "",
            "path": "offline",
        }


@dataclass
class EndpointConfig:
    provider: str
    base_url: str
    model: str
    api_key: str
    timeout: float
    source: str
    last_model_lookup_failed: bool = False

    def is_enabled(self) -> bool:
        return bool(self.base_url and (self.api_key or _is_local_base_url(self.base_url)))

    def is_configured(self) -> bool:
        return bool(self.is_enabled() and self.resolve_model())

    def display_model(self) -> str:
        return self.model or "auto-detect"

    def resolve_model(self) -> str:
        if self.model:
            return self.model
        if self.last_model_lookup_failed or not self.base_url:
            return ""
        try:
            with urllib.request.urlopen(f"{self.base_url}/models", timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
            for item in body.get("data", []):
                model = item.get("id", "").strip()
                if model:
                    self.model = model
                    self.last_model_lookup_failed = False
                    return model
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, json.JSONDecodeError, ValueError):
            self.last_model_lookup_failed = True
            return ""
        return ""

    def request_headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers


class OpenAICompatibleLLM:
    def __init__(self) -> None:
        timeout = float(os.getenv("EDGEGUARD_LLM_TIMEOUT", "12"))
        local_timeout = float(os.getenv("ONLINE_FALLBACK_TIMEOUT", "1"))
        self.primary = EndpointConfig(
            provider=os.getenv("OPENAI_PROVIDER", "OpenAI").strip(),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip(),
            api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            timeout=timeout,
            source="primary",
        )
        self.secondary = EndpointConfig(
            provider=os.getenv("ONLINE_FALLBACK_PROVIDER", "Ollama").strip(),
            base_url=os.getenv("ONLINE_FALLBACK_BASE_URL", "http://127.0.0.1:11434/v1").rstrip("/"),
            model=os.getenv("ONLINE_FALLBACK_MODEL", "").strip(),
            api_key=os.getenv("ONLINE_FALLBACK_API_KEY", "").strip(),
            timeout=local_timeout,
            source="online-fallback",
        )
        self.fallback = OfflineGroundedResponder()

    def is_configured(self) -> bool:
        return self.primary.is_enabled() or self.secondary.is_enabled()

    def status(self) -> dict:
        primary_enabled = self.primary.is_enabled()
        secondary_enabled = self.secondary.is_enabled()
        active = self.primary if primary_enabled else self.secondary if secondary_enabled else None
        return {
            "live_llm_configured": primary_enabled or secondary_enabled,
            "primary_configured": primary_enabled,
            "online_fallback_configured": secondary_enabled,
            "provider": active.provider if active else self.primary.provider,
            "model": active.display_model() if active else self.primary.display_model(),
            "primary_provider": self.primary.provider,
            "primary_model": self.primary.display_model(),
            "secondary_provider": self.secondary.provider,
            "secondary_model": self.secondary.display_model(),
        }

    def _build_messages(self, query: str, docs: List[dict], role: str) -> List[dict]:
        context_blocks = []
        for doc in docs[:3]:
            context_blocks.append(f"[{doc['id']}] {doc['title']}\nAccess: {doc['access']}\nContent: {doc['content']}")
        local_context = "\n\n".join(context_blocks) if context_blocks else "No local documents supplied."
        system = (
            "You are EdgeGuard, a secure industrial AI assistant. "
            "Answer only from the approved local context and the sanitized query. "
            "Do not reconstruct redacted identifiers. "
            "If the context is limited, say so explicitly. "
            "Keep the tone professional, operational, and safety-first."
        )
        user = (
            f"Requester role: {role}\n"
            f"Sanitized query: {query}\n\n"
            f"Approved local context:\n{local_context}\n\n"
            "Provide a concise but helpful response with:\n"
            "1. Situation summary\n"
            "2. Recommended action\n"
            "3. Safety note"
        )
        return [{"role": "system", "content": system}, {"role": "user", "content": user}]

    def _try_endpoint(self, endpoint: EndpointConfig, query: str, docs: List[dict], role: str) -> dict:
        model_name = endpoint.resolve_model()
        if not model_name:
            raise ValueError("No model available for endpoint")
        payload = json.dumps(
            {
                "model": model_name,
                "messages": self._build_messages(query, docs, role),
                "temperature": 0.2,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{endpoint.base_url}/chat/completions",
            data=payload,
            headers=endpoint.request_headers(),
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=endpoint.timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
        text = body["choices"][0]["message"]["content"].strip()
        return {
            "text": text,
            "provider": endpoint.provider,
            "model": model_name,
            "fallback_used": endpoint.source != "primary",
            "live_configured": True,
            "error": "",
            "path": endpoint.source,
        }

    def generate(self, query: str, docs: List[dict], role: str) -> dict:
        errors: List[str] = []
        for endpoint in (self.primary, self.secondary):
            if not endpoint.is_enabled():
                continue
            try:
                return self._try_endpoint(endpoint, query, docs, role)
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, json.JSONDecodeError, ValueError) as exc:
                errors.append(f"{endpoint.provider}: {exc.__class__.__name__}")

        offline = self.fallback.generate(query, docs, role)
        if errors:
            offline["live_configured"] = True
            offline["error"] = "All online providers failed. Using offline fallback. Details: " + " | ".join(errors)
            return offline

        offline["error"] = (
            "No live backend configured. Set OPENAI_* for the primary provider or ONLINE_FALLBACK_* "
            "for Mistral/Ollama/Llama online fallback."
        )
        return offline
