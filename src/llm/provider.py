from __future__ import annotations

import os
from typing import Protocol

import httpx
from groq import Groq

from src.llm.errors import friendly_api_error
from src.llm.mock_provider import build_mock_response
from src.models.schemas import LensMode

GROQ_MODELS = {
    "Llama 3.3 70B (Groq)": "llama-3.3-70b-versatile",
    "GPT-OSS 20B (Groq)": "openai/gpt-oss-20b",
    "Llama 3.1 8B (Groq)": "llama-3.1-8b-instant",
}

GROQ_DEFAULT_COMPARE = [
    "Llama 3.3 70B (Groq)",
    "GPT-OSS 20B (Groq)",
]

OLLAMA_MODEL = "gemma3:4b"

class LLMProvider(Protocol):
    def complete(
        self,
        system: str,
        user: str,
        model: str = "",
        json_mode: bool = True,
        lens: LensMode = LensMode.NEUTRAL,
        dilemma_text: str = "",
    ) -> str: ...


class MockProvider:
    def complete(
        self,
        system: str,
        user: str,
        model: str = "",
        json_mode: bool = True,
        lens: LensMode = LensMode.NEUTRAL,
        dilemma_text: str = "",
    ) -> str:
        return build_mock_response(dilemma_text or user, lens)


class GroqProvider:
    def __init__(self) -> None:
        self._client: Groq | None = None

    def _get_client(self) -> Groq | None:
        if self._client is not None:
            return self._client
        if "GROQ_API_KEY" not in os.environ:
            return None
        self._client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        return self._client

    def is_available(self) -> bool:
        return "GROQ_API_KEY" in os.environ

    def complete(
        self,
        system: str,
        user: str,
        model: str,
        json_mode: bool = True,
        lens: LensMode = LensMode.NEUTRAL,
        dilemma_text: str = "",
    ) -> str:
        client = self._get_client()
        if client is None:
            raise RuntimeError("Groq API key not configured.")

        kwargs: dict = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.3,
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""


class OllamaProvider:
    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url
        self.model = OLLAMA_MODEL

    def is_available(self) -> bool:
        try:
            with httpx.Client(timeout=3.0) as client:
                resp = client.get(f"{self.base_url}/api/tags")
                return resp.status_code == 200
        except httpx.HTTPError:
            return False

    def complete(
        self,
        system: str,
        user: str,
        model: str | None = None,
        json_mode: bool = True,
        lens: LensMode = LensMode.NEUTRAL,
        dilemma_text: str = "",
    ) -> str:
        payload = {
            "model": model or self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "format": "json" if json_mode else None,
            "options": {"temperature": 0.3},
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        with httpx.Client(timeout=120.0) as client:
            resp = client.post(f"{self.base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content", "")


class ResilientProvider:
    """Try live API first; fall back to mock on rate limits or connectivity errors."""

    def __init__(self, primary: GroqProvider | OllamaProvider, mock: MockProvider) -> None:
        self.primary = primary
        self.mock = mock
        self.last_fallback_reason: str | None = None

    def complete(
        self,
        system: str,
        user: str,
        model: str = "",
        json_mode: bool = True,
        lens: LensMode = LensMode.NEUTRAL,
        dilemma_text: str = "",
    ) -> str:
        try:
            self.last_fallback_reason = None
            return self.primary.complete(
                system, user, model=model, json_mode=json_mode,
                lens=lens, dilemma_text=dilemma_text,
            )
        except Exception as exc:
            self.last_fallback_reason = friendly_api_error(exc)
            return self.mock.complete(
                system, user, model=model, json_mode=json_mode,
                lens=lens, dilemma_text=dilemma_text,
            )


def get_provider() -> ResilientProvider | MockProvider:
    provider = os.environ.get("LLM_PROVIDER", "groq").lower()
    mock = MockProvider()
    if provider == "ollama":
        if OllamaProvider().is_available():
            return ResilientProvider(OllamaProvider(), mock)
        return mock
    if GroqProvider().is_available():
        return ResilientProvider(GroqProvider(), mock)
    return mock


def list_available_models() -> dict[str, str]:
    provider = os.environ.get("LLM_PROVIDER", "groq").lower()
    if provider == "ollama":
        return {"Gemma 3 4B (Ollama)": OLLAMA_MODEL}
    return GROQ_MODELS


def get_provider_name() -> str:
    return os.environ.get("LLM_PROVIDER", "groq").lower()


def resolve_model_id(display_name: str) -> str:
    models = list_available_models()
    return models.get(display_name, display_name)


def default_compare_models() -> list[str]:
    available = list_available_models()
    if len(available) == 1:
        return list(available.keys())
    if get_provider_name() == "ollama":
        return list(available.keys())
    return [m for m in GROQ_DEFAULT_COMPARE if m in available]


def provider_ready() -> bool:
    """Always ready — mock fallback covers missing or failing APIs."""
    return True
