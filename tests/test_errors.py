from __future__ import annotations

from unittest.mock import MagicMock

import httpx
import pytest

from src.llm.errors import RATE_LIMIT_MESSAGE, friendly_api_error, is_rate_limit
from src.llm.provider import GroqProvider, MockProvider, ResilientProvider
from src.models.schemas import LensMode


class TestFriendlyErrors:
    def test_rate_limit_message_has_no_exception_type(self):
        exc = Exception("Error code: 429 - rate limit exceeded")
        msg = friendly_api_error(exc)
        assert "429" not in msg
        assert "Exception" not in msg
        assert "rate limit" in msg.lower() or "rate-limited" in msg.lower()

    def test_is_rate_limit_detects_429_text(self):
        assert is_rate_limit(Exception("HTTP 429 Too Many Requests"))

    def test_resilient_provider_rate_limit_uses_friendly_message(self):
        primary = MagicMock(spec=GroqProvider)
        primary.complete.side_effect = Exception("rate limit exceeded (429)")
        mock = MockProvider()
        resilient = ResilientProvider(primary, mock)

        result = resilient.complete(
            "system",
            "user dilemma",
            model="llama-3.1-8b-instant",
            lens=LensMode.NEUTRAL,
            dilemma_text="A trolley problem",
        )

        assert result
        assert resilient.last_fallback_reason == RATE_LIMIT_MESSAGE
        assert "429" not in (resilient.last_fallback_reason or "")
        assert "Exception" not in (resilient.last_fallback_reason or "")

    def test_timeout_maps_to_friendly_message(self):
        msg = friendly_api_error(httpx.TimeoutException("timed out"))
        assert "timed out" in msg.lower() or "timeout" in msg.lower()
        assert "TimeoutException" not in msg
