"""User-facing glossary copy for ethical lenses, Compare audit modes, and metrics."""

from __future__ import annotations

import streamlit as st

LENS_GLOSSARY = """
An **ethical lens** tells the model *how* to reason — not just *what* to decide. You pick a
perspective; the model must follow it and label which framework it used.

| Lens | What it asks the model to prioritize |
|------|--------------------------------------|
| **Neutral** | Reason naturally. We detect which framework best matches the answer (utilitarian, deontological, care, etc.). |
| **Utilitarian** | Outcomes — maximize overall well-being or minimize total harm, even when rules are bent. |
| **Deontological** | Duties and rights — some actions are wrong regardless of how many lives are saved. |
| **Care ethics** | Relationships and vulnerability — who is most at risk, and what care or responsiveness is owed. |

After each run, compare the **forced lens** you selected with the **detected framework** in the
result. A mismatch is an alignment signal (the model may say one thing but reason like another).
"""

COMPARE_MODES_GLOSSARY = """
**Compare** is built for **multi-model audit**, not single-lens exploration.

| Option | What it does |
|--------|----------------|
| **Framework stress test** | Runs each selected model through **all four lenses** (neutral, utilitarian, deontological, care). Surfaces when models flip decisions or mislabel their framework under pressure. |
| **Consistency test** | Re-runs the **same curated scenario** with slightly different wording (rephrase variants). Measures whether a model changes its moral answer when the framing shifts — a common alignment risk. Requires a **curated scenario** with rephrase variants. |

**Why no single “ethical lens” dropdown here?**  
Explore is for *one model, one lens at a time*. Compare runs **up to three models** side-by-side
under a shared audit design: neutral comparison first, then optional **full lens sweep** via
Framework stress test. A single lens picker would hide cross-model disagreement at neutral
and duplicate what Explore already does well. To force one lens on one model, use **Explore**.
"""

HOW_IT_WORKS_EXTRA = """
**Ethical lenses (Explore)** — Optional perspectives (utilitarian, deontological, care) that
steer how the model reasons. Neutral mode lets the model choose its own style so you can audit
what it naturally does.

**Framework stress (Compare)** — Optional batch run of all lenses per model to stress-test
framework adherence and decision stability.

**Consistency (Compare)** — Optional rephrase variants on curated scenarios to test framing
sensitivity.

**Export JSON (Compare only)** — After a comparison run, download metrics and verdicts for offline audit. Explore shows results in the UI only.
"""

METRICS_GLOSSARY = """
After you run a comparison, the metric cards summarize **neutral-lens runs** across your
selected models (unless noted). They help you spot agreement vs. divergence at a glance.

| Metric | Meaning |
|--------|---------|
| **Decision agreement** | **Primary metric.** Do models make the *same moral choice* even when they word it differently? Uses semantic matching (e.g. “report the user” ≈ “breach confidentiality and notify authorities”). **100%** = all models align on the action; **0%** = no pair agrees. |
| **Decision agreement (lexical)** | Same as above, but counts only **identical wording** after normalization. Often **lower** than semantic agreement — useful to see when models agree in spirit but phrase decisions differently. |
| **Framework agreement** | Do models label their reasoning with the **same primary ethical framework** (utilitarian, deontological, care, etc.)? High agreement means they cite similar ethics; low agreement can mean the same decision came from different moral reasoning. |
| **Avg uncertainties** | Average number of **uncertainty items** each model listed (ambiguities, missing facts, judgment calls). **Higher** values mean models flagged more “we can’t be sure” factors — not inherently good or bad, but signals how hedged the answers are. |
| **Consistency score** | *(Only when Consistency test is enabled.)* Share of **rephrase variants** where the **first selected model** gave the **same decision** as the original wording. **100%** = stable under rephrasing; **0%** = framing flipped the answer. |

**Other labels you may see**

| Label | Meaning |
|-------|---------|
| **Simulated** | Live API was unavailable (rate limit, missing key, etc.) — response is a **labeled mock**, not real model output. |
| **Creative alternatives** | Options the model considered *before* committing to a forced tradeoff — engineering or policy escape hatches. |
| **Confidence** | Model’s self-reported certainty (0–100%). Not calibrated; treat as a hint, not ground truth. |
| **Lens adherence mismatch** | *(Framework stress only.)* The **forced lens** (e.g. deontological) does not match the **framework the model detected** in its answer — an alignment audit signal. |
| **Export JSON** | *(Compare only.)* Downloads the full run (metrics, verdicts, consistency data) for offline audit — same structure as on screen. Explore shows results in the UI only. |
"""

RESULTS_GLOSSARY = """
**Results layout**

- **Top cards** — Side-by-side **neutral-lens** verdicts for each model (decision, reasoning, frameworks).
- **Framework stress test** — Expandable sections per model × lens when that option is checked.
- **Consistency test** — Runs in the background; score appears in the metrics row when enabled.

Metrics compare models on the **same dilemma text** you selected. Custom dilemmas and curated
scenarios both work; consistency requires a **curated scenario** with rephrase variants.
"""


def render_lens_glossary(*, expanded: bool = False) -> None:
    with st.expander("What is an ethical lens?", expanded=expanded):
        st.markdown(LENS_GLOSSARY)


def render_compare_modes_glossary(*, expanded: bool = False) -> None:
    with st.expander("Framework stress & consistency — what do these mean?", expanded=expanded):
        st.markdown(COMPARE_MODES_GLOSSARY)


def render_compare_metrics_glossary(*, expanded: bool = False) -> None:
    with st.expander("Understanding agreement metrics & result labels", expanded=expanded):
        st.markdown(METRICS_GLOSSARY)
        st.markdown(RESULTS_GLOSSARY)
