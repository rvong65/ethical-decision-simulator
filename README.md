<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/assets/logo-light.svg">
    <img alt="Ethical Decision Simulator" src="docs/assets/logo-light.svg" width="400">
  </picture>
</h1>

[![Release](https://img.shields.io/github/v/release/rvong65/ethical-decision-simulator?label=release)](https://github.com/rvong65/ethical-decision-simulator/releases)
[![CI](https://github.com/rvong65/ethical-decision-simulator/actions/workflows/tests.yml/badge.svg)](https://github.com/rvong65/ethical-decision-simulator/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Audit](https://img.shields.io/badge/Audit-Multi--model%20ethics-818CF8?style=flat-square)](docs/architecture.md)
[![Docker](https://img.shields.io/badge/Docker-Groq%20%7C%20Ollama-2496ED?style=flat-square&logo=docker&logoColor=white)](https://github.com/rvong65/ethical-decision-simulator#docker)
[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ethical-decision-simulator.streamlit.app/)

An **ethical decision simulator** for auditing how large language models reason through moral dilemmas — surfacing alignment risks, framework conflicts, and cross-model disagreement with structured, exportable outputs. 

> **Educational tool:** This app audits how LLMs reason through moral dilemmas — it does **not** provide moral guidance, legal advice, therapy, or crisis support. Model outputs may be incorrect; users are responsible for their own decisions.

> **Privacy (cloud demo):** Dilemma text you enter is sent to **Groq** for inference when using the public Streamlit Cloud demo (or any cloud deployment with `LLM_PROVIDER=groq`). Do not submit classified data, credentials, PII, or sensitive organizational details you cannot share with Groq. Prefer curated scenarios or synthetic examples for testing. Session state is not written to a project database; see [Privacy & data](#privacy-data) below.

<details open>
<summary><strong>Table of Contents</strong></summary>

| Section | Description |
|---------|-------------|
| **Get started** | |
| 🚀 [Live Demo](#live-demo) | Try the live ethics audit demo (Cloud or local) |
| ✨ [Features](#features) | Capabilities at a glance |
| ⚡ [Quick Start](#quick-start) | Clone, install, run, test, Docker |
| **Overview** | |
| 🎯 [Problem & Motivation](#problem-motivation) | Why auditable LLM ethics testing matters |
| 🛠️ [Tech Stack](#tech-stack) | Languages, libraries, CI |
| 📊 [Data Sources & Attribution](#data-sources) | Scenarios and model licenses |
| 📌 [Version history](#version-history) | Release highlights |
| **Technical** | |
| 🏗️ [Architecture & Design Choices](#architecture-design-choices) | System design and pipeline |
| ↳ [Full architecture doc](docs/architecture.md) | Detailed system design (Mermaid) |
| ↳ [Development Journey](#development-journey) | Capability pipeline diagram |
| 🛡️ [Safety Considerations](#safety-considerations) | Ethics, guardrails, and data privacy |
| 🔄 [CI/CD](#cicd) | GitHub Actions, Docker, and deployment |
| 📈 [Project Status](#project-status) | v1.0.0 capabilities |
| 📁 [Repository Layout](#repository-layout) | File tree |
| **Legal & contact** | |
| 📄 [License](#license) | MIT License |
| 🤝 [Contact / Next Steps](#contact) | Feedback and V2 roadmap |

</details>

<a id="live-demo"></a>

## 🚀 Live Demo

**[▶ Open the live app on Streamlit Cloud](https://ethical-decision-simulator.streamlit.app/)**

**Before you open the app:**
- **Cold start:** This app runs on Streamlit Community Cloud and may go to sleep after inactivity. If you see **“Zzzz — This app has gone to sleep due to inactivity”**, click **“Yes, get this app back up!”** to wake it — anyone can do this; no special permissions required. Startup may take a minute after you click.
- **Privacy:** The public demo sends dilemma text to **Groq** for inference. Do not enter classified data, credentials, PII, or sensitive details you cannot share with a third-party LLM API. Prefer **curated scenarios** or synthetic dilemmas. Session results stay in browser memory only — not stored in a project database. For local-only inference, run with **`LLM_PROVIDER=ollama`** (see [Quick Start](#quick-start)). Full details: [Privacy & data](#privacy-data).

**Local demo:** `streamlit run app.py` · **Docker:** `docker compose up --build` → http://localhost:8501

### Screenshots

![Explore — single-model ethical reasoning](docs/screenshots/explore.png)

*Explore — structured verdict with creative alternatives, reasoning steps, and ethics primer. LLM-generated narrative text may differ by provider, model, and run.*

![Compare — multi-model audit](docs/screenshots/compare.png)

*Compare — side-by-side model verdicts with semantic agreement metrics and optional JSON export. LLM-generated narrative text may differ by provider, model, and run.*

<a id="features"></a>

## ✨ Features

- **Explore** — single-model walkthrough with creative alternatives, reasoning steps, and ethics primers (on-screen results; no file export)
- **Compare** — multi-model side-by-side audit with semantic agreement metrics
- **Framework stress test** — utilitarian, deontological, and care-ethics lenses
- **Consistency test** — rephrase variants to measure framing sensitivity
- **Export JSON (Compare)** — download full metrics, runs, and consistency data after a multi-model comparison
- **Simulated mode** — automatic fallback when API is unavailable (clearly labeled)

<a id="quick-start"></a>

## ⚡ Quick Start

### Prerequisites

- Python 3.11+ **or** [Docker](https://docs.docker.com/get-docker/)
- [Groq API key](https://console.groq.com/) for live cloud models
- *(Optional)* [Ollama](https://ollama.com/) with `gemma3:4b` for local development

### Local setup

```bash
git clone https://github.com/rvong65/ethical-decision-simulator
cd ethical-decision-simulator
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
# Edit secrets.toml — set GROQ_API_KEY
streamlit run app.py
```

**Local Ollama profile:**

```bash
$env:LLM_PROVIDER = "ollama"
streamlit run app.py
```

### Docker

```bash
docker compose up --build
# Open http://localhost:8501
```

Optional: create a `.env` file with `GROQ_API_KEY=your_key` (never commit). Without a key, the app runs in **Simulated mode**.

### Run tests

```bash
pytest tests/ -v --ignore=tests/test_api_integration.py   # 46 offline (matches CI)
pytest tests/test_api_integration.py -v -m api            # 3 live Groq smoke tests (local / optional)
```

See [docs/architecture.md#deployment-topologies](docs/architecture.md#deployment-topologies) for local, Docker, and Streamlit Cloud details.

<a id="problem-motivation"></a>

## 🎯 Problem & Motivation

AI systems do not share a single moral compass. When values conflict, models may disagree with each other, flip answers under slight rephrasing, or cite one ethical framework while reasoning like another. Teams deploying AI in sensitive domains need **transparent, auditable** ways to probe these behaviors — not a black-box “right answer.”

This project makes that visible: pick a dilemma, run one or more models, and inspect decisions, creative alternatives, reasoning chains, detected frameworks, and agreement metrics. It is an **educational ethics auditing tool**, not moral authority, legal advice, or a substitute for professional judgment.

<a id="tech-stack"></a>

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/groq-API-F55036?style=for-the-badge)
![Ollama](https://img.shields.io/badge/ollama-local-000000?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

| Layer | Technology |
|-------|------------|
| UI | Streamlit (`st.navigation`, wide layout) |
| Cloud LLM | Groq API (Llama 3.3 70B, GPT-OSS 20B, Llama 3.1 8B) |
| Local LLM | Ollama (`gemma3:4b`) — optional dev profile |
| Schemas | Pydantic v2 structured verdicts |
| Analysis | Semantic decision agreement, consistency scoring |
| Tests | pytest — 46 offline + 3 API smoke tests |
| CI / Docker | GitHub Actions + `Dockerfile` / `docker-compose.yml` |

<a id="data-sources"></a>

## 📊 Data Sources & Attribution

Curated dilemmas are original scenario text in [`src/scenarios/library.json`](src/scenarios/library.json), inspired by classic ethics thought experiments and applied AI ethics cases — not copied from proprietary datasets.

| Model | Role | License / acknowledgment |
|-------|------|--------------------------|
| `gemma3:4b` (Ollama) | Local dev LLM | [Gemma Terms of Use](https://ai.google.dev/gemma/terms) |
| `llama-3.1-8b-instant` (Groq) | Cloud LLM — fast baseline | Meta Llama via Groq — [Groq Terms](https://groq.com/terms/) |
| `llama-3.3-70b-versatile` (Groq) | Cloud LLM — nuanced reasoning | Meta Llama via Groq — [Groq Terms](https://groq.com/terms/) |
| `openai/gpt-oss-20b` (Groq) | Cloud LLM — cross-family comparison | OpenAI open-weight via Groq — [Groq Terms](https://groq.com/terms/) |

<a id="version-history"></a>

## 📌 Version history

| Version | Date | Highlights |
|---------|------|------------|
| **[1.0.0](CHANGELOG.md#100---2026-06-28)** | 2026-06-28 | MVP: Explore/Compare, 12 scenarios, CI, Docker, docs |

Full details: **[CHANGELOG.md](CHANGELOG.md)** 

<a id="architecture-design-choices"></a>

## 🏗️ Architecture & Design Choices

Dilemmas flow through scenario loading → crisis check → lens-aware prompts → resilient LLM inference → JSON parse/validate → agreement analysis → Streamlit presentation (Explore for single-model review; Compare for multi-model audit and optional JSON export). Mock fallback and crisis guardrails keep the tool usable and responsible without hiding simulation.

**Full design** — goals, end-to-end diagram, module map, deployment topologies (local / Docker / Streamlit Cloud), and architecture-level safety: **[docs/architecture.md](docs/architecture.md)**

**Key design decisions**

| Decision | Rationale |
|----------|-----------|
| Structured JSON verdicts | Auditable, exportable, comparable across models |
| Semantic decision agreement | Lexical match alone mislabels moral agreement (e.g. same “report” decision, different wording) |
| Forced ethical lenses | Surfaces when models mislabel frameworks (alignment audit signal) |
| Creative alternatives first | Separates engineering escape hatches from forced tradeoff analysis |
| Mock fallback with labels | App stays usable when Groq rate-limits or API key is missing — never silent simulation |
| Crisis disclaimer | Self-harm scenarios show 988 resources; app is not a crisis service |
| Docker + CI | Reproducible local runs and automated quality gates on every push |

<a id="development-journey"></a>

### Development Journey

Capability pipeline (Explore, Compare, metrics, and export). Full design: [docs/architecture.md#development-journey](docs/architecture.md#development-journey).

```mermaid
flowchart LR
    A[Structured prompts<br/>JSON verdicts] --> B[Explore + Compare<br/>12 scenarios]
    B --> C[Framework stress<br/>consistency tests]
    C --> D[Responsible AI<br/>crisis · mock · lens warnings]
    D --> E[Streamlit UI<br/>indigo sidebar theme]
    E --> F[Semantic metrics<br/>structured export]
    F --> G[46 offline tests<br/>3 API smoke tests]
    G --> H[GitHub Actions CI<br/>Docker]
    H --> I[Streamlit Cloud deploy<br/>MVP]
```

<a id="safety-considerations"></a>

## 🛡️ Safety Considerations

| Principle | Implementation |
|-----------|----------------|
| **Educational use only** | Framed as an alignment auditing tool — not moral guidance, legal advice, therapy, or crisis intervention (home footer + README) |
| **Transparency** | Structured JSON verdicts, labeled `live` vs `mock` runs, lens-adherence mismatch warnings |
| **No warranty** | Disclaimers state LLM outputs may be wrong; users are responsible for their own decisions |
| **Crisis safety** | Regex detector + prominent 988 / Crisis Text Line banner for self-harm-related dilemma text |
| **Honest simulation** | Mock fallback on rate limits or API failure — always labeled **Simulated mode**, never silent |
| **Data minimization** | Session-only state; no project database; Compare JSON export is a user-initiated download |
| **Third-party inference** | Groq/Ollama terms apply; dilemma text sent only to configured LLM provider |
| **Privacy awareness** | Cloud-demo privacy notice, in-app **Privacy & data** expander, README data-flow table |

<a id="privacy-data"></a>

### Privacy & data

Ethical Decision Simulator is designed for **educational alignment auditing**, not as a certified data-processing platform. Understand where your input goes:

| Data you submit | Where it may be sent | Notes |
|-----------------|----------------------|-------|
| Dilemmas (curated or custom) | **LLM provider** (Groq on cloud demo, or local Ollama) | Cloud: processed per [Groq Terms](https://groq.com/terms/) and their privacy policy |
| Ethical lens & model settings | **Same LLM provider** | Included in the prompts sent for inference |
| Comparison & consistency runs | **Same LLM provider** | Each selected model receives the dilemma text |
| Session results & sidebar state | **Streamlit session memory** | Cleared when the session ends; **not** written to a project database by this app |
| JSON exports (Compare) | **Your browser only** | User-initiated download after a multi-model comparison |

**Public Streamlit Cloud demo:** Treat it like any shared SaaS chat UI — **no classified data, credentials, PII, or sensitive organizational details** you cannot share with Groq. Prefer built-in **curated scenarios** or synthetic moral dilemmas for testing.

**Sensitive environments:** Run locally or in Docker with **`LLM_PROVIDER=ollama`** so inference stays on your network (requires local Ollama with `gemma3:4b`).

**Note:** This app does not intentionally log dilemma text to disk. Streamlit Community Cloud and Groq may retain operational or API logs under their own policies — review their documentation if compliance matters.

<a id="cicd"></a>

## 🔄 CI/CD

**GitHub Actions** runs on every push and pull request to `main` / `master`:

| Job | Step | Action |
|-----|------|--------|
| **offline-tests** | Trigger | Push or PR to `main` / `master` |
| | Environment | `ubuntu-latest`, Python 3.11 |
| | Install | `pip install -r requirements.txt` |
| | Test | `pytest tests/ --ignore=tests/test_api_integration.py` — **46 offline tests** (parser, scenarios, semantic metrics, crisis guard, mock pipeline, LLM error mapping) |
| **docker-tests** | Build | `docker build -t ethical-decision-simulator:ci .` |
| | Test | Run **46 offline tests** inside the container |
| | Run | `docker compose up` on port **8501** (no API key required — **Simulated mode**) |
| | Health | Streamlit `/_stcore/health` |
| **api-smoke-tests** | Trigger | Push to `main` only (after offline-tests pass) |
| | Test | `pytest tests/test_api_integration.py -m api` — **3 live Groq tests** (skipped if `GROQ_API_KEY` secret unset) |

Workflow file: [`.github/workflows/tests.yml`](.github/workflows/tests.yml)

**Releases:** Version history in [CHANGELOG.md](CHANGELOG.md). GitHub Releases are created manually when tagging (e.g. `v1.0.0`) — release notes may differ from the changelog.

**No API keys required for CI gate** — offline tests and the Docker job use fixtures and mocks only; Docker verifies the image builds, tests pass, and Streamlit responds.

**API smoke tests** require `GROQ_API_KEY` as a GitHub repository secret on `main`. Run them locally anytime with `pytest tests/test_api_integration.py -m api`.

**Streamlit Cloud** deploys independently from the `main` branch when connected to this repository (`app.py` + `requirements.txt` + Streamlit secret `GROQ_API_KEY`).

**Docker locally:**

```bash
docker compose up --build
docker run --rm ethical-decision-simulator:ci pytest tests/ -v --ignore=tests/test_api_integration.py
```

<a id="project-status"></a>

## 📈 Project Status

**Current release:** **v1.0.0** — [Streamlit demo](https://ethical-decision-simulator.streamlit.app/) · [GitHub repo](https://github.com/rvong65/ethical-decision-simulator)

| Capability | Included |
|------------|----------|
| Structured prompts + JSON verdict pipeline | ✅ |
| 12 curated scenarios + custom dilemmas | ✅ |
| Explore (single-model) & Compare (multi-model audit) | ✅ |
| Framework stress + consistency tests | ✅ |
| Semantic agreement metrics + Compare JSON export | ✅ |
| Crisis disclaimer + mock fallback | ✅ |
| 46 offline tests + optional API smoke tests | ✅ |
| GitHub Actions CI + Docker | ✅ |

<a id="repository-layout"></a>

## 📁 Repository Layout

```
├── app.py                          # Streamlit navigation entry
├── Dockerfile                      # Production / CI container image
├── docker-compose.yml              # One-command local run
├── CHANGELOG.md                    # Version-by-version change history
├── pages/
│   ├── home.py                     # Landing + how it works
│   ├── explore.py                  # Single-model ethical reasoning
│   └── compare.py                  # Multi-model audit + export
├── src/
│   ├── config.py                   # Secrets bootstrap (no key values exposed)
│   ├── llm/                        # Groq / Ollama / mock / resilient provider
│   ├── ethics/                     # Framework prompts + parser
│   ├── scenarios/                  # library.json (12 dilemmas)
│   ├── analysis/                   # Agreement, consistency, export, semantic
│   ├── models/                     # Pydantic EthicalVerdict types
│   └── ui/                         # Theme, components, crisis, sidebar, glossary
│       ├── glossary.py             # In-app help: lenses, metrics, Compare modes
├── docs/
│   ├── architecture.md             # Full system design reference
│   ├── screenshots/                # README + GitHub social preview images
│   └── assets/                     # icon, favicon, logo (light/dark)
├── tests/                          # 46 offline + 3 API smoke tests
├── .github/workflows/
│   └── tests.yml                   # CI — offline, Docker, API smoke
├── .streamlit/
│   ├── config.toml                 # Theme (indigo sidebar)
│   └── secrets.toml.example        # GROQ_API_KEY template
├── requirements.txt                # App + Streamlit Cloud runtime deps
├── pytest.ini
└── LICENSE                         # MIT
```

<a id="license"></a>

## 📄 License

**MIT License** — see [LICENSE](LICENSE).

<a id="contact"></a>

## 🤝 Contact / Next Steps

Open to feedback, suggestions, and mission-aligned collaboration on responsible AI tooling.

### V2 roadmap (planned)

| Area | Direction |
|------|-----------|
| **Metrics** | Embedding-based semantic agreement (beyond keyword buckets) |
| **UX** | Dedicated “alternatives-only” workshop mode before forced tradeoff analysis |
| **Content** | Additional scenario packs (healthcare, policy, enterprise AI governance) |
| **Analysis** | Multi-turn debate mode between models on the same dilemma |
| **Data** | Persisted audit sessions (optional user export history) |

