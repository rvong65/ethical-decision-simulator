"""Map LLM/API exceptions to user-facing messages (no stack traces or raw HTTP bodies)."""

from __future__ import annotations

import httpx

try:
    from groq import APIStatusError, RateLimitError
except ImportError:
    APIStatusError = Exception  # type: ignore[misc, assignment]
    RateLimitError = Exception  # type: ignore[misc, assignment]

RATE_LIMIT_MESSAGE = (
    "Groq rate limit reached. Showing a simulated response so you can keep exploring. "
    "If the service is rate-limited, wait a moment and try again."
)
API_UNAVAILABLE_MESSAGE = (
    "Live API unavailable. Showing a simulated response — results are illustrative only."
)
NOT_CONFIGURED_MESSAGE = (
    "Live API not configured. Showing a simulated response — add GROQ_API_KEY for real models."
)
TIMEOUT_MESSAGE = (
    "The model request timed out. Showing a simulated response — try again in a moment."
)
AUTH_MESSAGE = (
    "Could not authenticate with the API. Showing a simulated response — check your API key."
)


def is_rate_limit(exc: Exception) -> bool:
    if isinstance(exc, RateLimitError):
        return True
    if isinstance(exc, APIStatusError) and getattr(exc, "status_code", None) == 429:
        return True
    text = str(exc).lower()
    return "rate limit" in text or "429" in text


def is_api_unavailable(exc: Exception) -> bool:
    if isinstance(exc, (httpx.HTTPError, ConnectionError, TimeoutError)):
        return True
    if isinstance(exc, APIStatusError):
        code = getattr(exc, "status_code", None)
        return code in (500, 502, 503, 504)
    if isinstance(exc, RuntimeError) and "not configured" in str(exc).lower():
        return True
    return False


def is_auth_error(exc: Exception) -> bool:
    if isinstance(exc, APIStatusError) and getattr(exc, "status_code", None) in (401, 403):
        return True
    text = str(exc).lower()
    return "unauthorized" in text or "invalid api key" in text or "authentication" in text


def friendly_api_error(exc: Exception) -> str:
    if is_rate_limit(exc):
        return RATE_LIMIT_MESSAGE
    if isinstance(exc, (TimeoutError, httpx.TimeoutException)):
        return TIMEOUT_MESSAGE
    if is_auth_error(exc):
        return AUTH_MESSAGE
    if isinstance(exc, RuntimeError) and "not configured" in str(exc).lower():
        return NOT_CONFIGURED_MESSAGE
    if is_api_unavailable(exc):
        return API_UNAVAILABLE_MESSAGE
    return API_UNAVAILABLE_MESSAGE
