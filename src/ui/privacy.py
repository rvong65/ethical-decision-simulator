from __future__ import annotations

PRIVACY_README_ANCHOR = "privacy-data"

PRIVACY_CLOUD_NOTE = (
    "> **Privacy (cloud demo):** Dilemma text you enter is sent to **Groq** for inference when "
    "using the public Streamlit Cloud demo (or any cloud deployment with `LLM_PROVIDER=groq`). "
    "Do not submit classified data, credentials, PII, or sensitive organizational details you "
    "cannot share with Groq. Prefer curated scenarios or synthetic examples for testing. "
    "Session state is not written to a project database; see [Privacy & data](#privacy-data) below."
)

PRIVACY_EXPANDER_BODY = """
**Ethical Decision Simulator** is an **educational auditing tool**, not a certified data-processing platform. Understand where your input goes:

| Data you submit | Where it may be sent | Notes |
|-----------------|----------------------|-------|
| Dilemmas (curated or custom) | **LLM provider** (Groq on cloud demo, or local Ollama) | Cloud: processed per [Groq Terms](https://groq.com/terms/) and their privacy policy |
| Ethical lens & model settings | **Same LLM provider** | Included in the system/user prompts |
| Comparison & consistency runs | **Same LLM provider** | Each selected model receives the dilemma text |
| Session results & sidebar state | **Streamlit session memory** | Cleared when the session ends; **not** written to a project database |
| JSON exports (Compare) | **Your browser only** | User-initiated download after a multi-model comparison |

**Public Streamlit Cloud demo:** Treat it like any shared SaaS UI — **no classified data, credentials, PII, or live production incident details** you cannot share with Groq. Prefer built-in **curated scenarios** or synthetic moral dilemmas for testing.

**Sensitive environments:** Run locally or in Docker with **`LLM_PROVIDER=ollama`** so inference stays on your network (requires a local Ollama instance with `gemma3:4b`).

**Rate limits:** If Groq is rate-limited, the app shows a **simulated response** (clearly labeled) so you can keep exploring. If the service is rate-limited, wait a moment and try again.

**Note:** This app does not intentionally log dilemma text to disk. Streamlit Community Cloud and Groq may retain operational or API logs under their own policies — review their documentation if compliance matters.
"""

PRIVACY_README_SECTION = """
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
"""

PRIVACY_ARCHITECTURE_LINE = (
    "**Privacy:** Dilemma text and ethical-lens prompts are transmitted to configured LLM APIs "
    "(Groq or local Ollama). This app does not persist queries to a project database; "
    "see README [Privacy & data](../README.md#privacy-data)."
)
