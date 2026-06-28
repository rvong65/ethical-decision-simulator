from __future__ import annotations

import streamlit as st

from src.ethics.frameworks import FRAMEWORK_DESCRIPTIONS
from src.models.schemas import ModelRunResult


def render_api_status_banner(results: list[ModelRunResult]) -> None:
    mock_runs = [r for r in results if r.source == "mock"]
    if not mock_runs:
        return
    reason = mock_runs[0].api_error or "Live API unavailable — simulated response shown."
    if any(token in reason for token in ("Traceback", "Error code:", "HTTPStatusError")):
        reason = "Live API unavailable — simulated response shown."
    st.warning(f"**Simulated mode:** {reason}")


def render_verdict_card(result: ModelRunResult, title: str | None = None) -> None:
    header = title or result.model_id
    st.markdown(f"#### {header}")

    if result.source == "mock" and result.api_error:
        st.info(result.api_error)

    if result.lens_adherence_mismatch:
        st.warning(
            "Lens adherence mismatch — forced ethical lens does not match the "
            f"detected framework ({result.verdict.primary_framework.value if result.verdict else 'unknown'})."
        )

    if result.parse_error:
        st.error(f"Parse failed: {result.parse_error}")
        with st.expander("Raw response"):
            st.code(result.raw_response or "(empty)")
        return

    if not result.verdict:
        st.warning("No verdict returned.")
        return

    v = result.verdict
    framework_key = v.primary_framework.value
    fw = FRAMEWORK_DESCRIPTIONS.get(framework_key, FRAMEWORK_DESCRIPTIONS["mixed"])

    badges = (
        f'<span class="badge">{fw["name"]}</span>'
        f'<span class="badge">Confidence: {v.confidence:.0%}</span>'
        f'<span class="badge">{result.latency_ms:.0f} ms</span>'
    )
    if result.source == "mock":
        badges += '<span class="badge">Simulated</span>'
    st.markdown(badges, unsafe_allow_html=True)

    if v.creative_alternatives:
        st.markdown("**Creative alternatives** (before forced tradeoff)")
        for alt in v.creative_alternatives:
            st.markdown(f"- {alt}")

    st.markdown(f"**Decision:** {v.decision}")

    st.markdown("**Reasoning**")
    for i, step in enumerate(v.reasoning_steps, 1):
        st.markdown(
            f'<div class="step-row"><span class="step-num">{i}</span><span>{step}</span></div>',
            unsafe_allow_html=True,
        )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Stakeholders**")
        for s in v.stakeholders:
            st.markdown(f"- {s}")
        st.markdown("**Harms identified**")
        for h in v.harms_identified:
            st.markdown(f"- {h}")
    with col2:
        st.markdown("**Uncertainties**")
        for u in v.uncertainties:
            st.markdown(f"- {u}")

    with st.expander("Ethics primer — " + fw["name"]):
        st.markdown(fw["summary"])
        st.markdown(f"*Key question:* {fw['key_question']}")


def render_metrics(
    decision_agreement: float,
    framework_agreement: float,
    avg_uncertainty: float,
    consistency: float | None = None,
    decision_agreement_lexical: float | None = None,
) -> None:
    ncols = 3 + (1 if consistency is not None else 0) + (1 if decision_agreement_lexical is not None else 0)
    cols = st.columns(ncols)
    metrics: list[tuple[str, str]] = [
        ("Decision agreement", f"{decision_agreement:.0%}"),
    ]
    if decision_agreement_lexical is not None:
        metrics.append(("Decision agreement (lexical)", f"{decision_agreement_lexical:.0%}"))
    metrics.extend([
        ("Framework agreement", f"{framework_agreement:.0%}"),
        ("Avg uncertainties", f"{avg_uncertainty:.1f}"),
    ])
    if consistency is not None:
        metrics.append(("Consistency score", f"{consistency:.0%}"))

    for col, (label, value) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <p class="metric-label">{label}</p>
                    <p class="metric-value">{value}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.caption(
        "Decision agreement (primary) uses semantic matching on **neutral-lens** runs. "
        "See *Understanding agreement metrics & result labels* above for definitions."
    )
