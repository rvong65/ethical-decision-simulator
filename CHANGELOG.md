# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Planned
- Embedding-based semantic agreement (v2)

## [1.0.0] - 2026-06-28

### Added
- **Explore** — single-model ethical reasoning with creative alternatives and ethics primers
- **Compare** — multi-model audit (up to 3 models), framework stress test, consistency test
- 12 curated moral dilemmas in `src/scenarios/library.json` plus custom dilemma input
- Structured JSON verdicts (Pydantic): decision, reasoning steps, frameworks, confidence, creative alternatives
- Semantic decision agreement (primary) and lexical agreement (secondary) metrics
- Lens-adherence mismatch warnings when forced lens ≠ detected framework
- Crisis keyword detector with 988 / Crisis Text Line disclaimer banner
- Resilient provider with labeled mock fallback on rate limit, auth failure, or missing API key
- Groq integration: Llama 3.3 70B, GPT-OSS 20B, Llama 3.1 8B
- Optional Ollama profile (`gemma3:4b`) for local development
- Compare JSON export (`ethical_comparison_*.json`) with full metrics and run metadata
- Custom Streamlit theme — white main content, indigo sidebar
- 46 offline pytest tests + 3 live Groq API smoke tests
- GitHub Actions CI (`.github/workflows/tests.yml`)
- Docker image (`Dockerfile`, `docker-compose.yml`) with CI build and health checks
- Architecture documentation (`docs/architecture.md`)
- Brand assets (`docs/assets/`: icon, favicon, logo light/dark)
- MIT License

[Unreleased]: https://github.com/rvong65/ethical-decision-simulator/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/rvong65/ethical-decision-simulator/releases/tag/v1.0.0
