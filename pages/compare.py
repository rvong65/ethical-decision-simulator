from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from src.analysis.compare import build_comparison
from src.analysis.consistency import run_consistency_test
from src.analysis.export import export_comparison_json
from src.llm.provider import default_compare_models, list_available_models, provider_ready
from src.llm.runner import run_parallel
from src.models.schemas import LensMode
from src.ui.components import render_api_status_banner, render_metrics, render_verdict_card
from src.ui.crisis import is_crisis_dilemma, render_crisis_disclaimer
from src.ui.glossary import render_compare_metrics_glossary, render_compare_modes_glossary
from src.ui.provider_panel import render_provider_status
from src.ui.sidebar import get_active_scenario, init_session_state, render_dilemma_sidebar
from src.ui.theme import page_header, render_dilemma_panel

init_session_state()

page_header(
    "Compare",
    "Multi-model audit: measure agreement, stress ethical lenses, and test framing consistency.",
)

with st.sidebar:
    dilemma_text = render_dilemma_sidebar()
    st.divider()
    st.markdown("### Settings")
    models = list(list_available_models().keys())
    defaults = [m for m in default_compare_models() if m in models]
    selected_models = st.multiselect(
        "Models",
        models,
        default=defaults,
        max_selections=3,
    )
    framework_stress = st.checkbox("Framework stress test")
    consistency_test = st.checkbox("Consistency test")
    st.divider()
    render_provider_status()

render_compare_modes_glossary()
render_compare_metrics_glossary()

scenario = get_active_scenario()

if dilemma_text:
    if is_crisis_dilemma(dilemma_text):
        st.markdown(render_crisis_disclaimer(), unsafe_allow_html=True)
    render_dilemma_panel(dilemma_text)

can_run = bool(dilemma_text and selected_models and provider_ready())
if consistency_test and not scenario:
    st.caption("Consistency test requires a curated scenario.")
    can_run = False

if st.button("Run comparison", type="primary", disabled=not can_run):
    lenses = [LensMode.NEUTRAL]
    if framework_stress:
        lenses = [
            LensMode.NEUTRAL,
            LensMode.UTILITARIAN,
            LensMode.DEONTOLOGICAL,
            LensMode.CARE,
        ]

    with st.spinner("Running comparisons..."):
        runs = run_parallel(dilemma_text, selected_models, lenses)

    consistency_val = None
    consistency_runs: list = []
    if consistency_test and scenario and scenario.rephrase_variants:
        with st.spinner("Running consistency test..."):
            baseline, variants, consistency_val = run_consistency_test(
                dilemma_text,
                scenario.rephrase_variants[:2],
                selected_models[0],
            )
            consistency_runs = [baseline, *variants]

    comparison = build_comparison(dilemma_text, runs, consistency_val)
    render_api_status_banner(runs + consistency_runs)

    st.markdown("---")
    render_metrics(
        comparison.decision_agreement,
        comparison.framework_agreement,
        comparison.avg_uncertainty_count,
        comparison.consistency_score,
        comparison.decision_agreement_lexical,
    )

    st.markdown('<p class="section-heading">Results</p>', unsafe_allow_html=True)
    neutral_runs = [r for r in runs if r.lens == LensMode.NEUTRAL]
    other_runs = [r for r in runs if r.lens != LensMode.NEUTRAL]

    if neutral_runs:
        cols = st.columns(min(len(neutral_runs), 2))
        for i, result in enumerate(neutral_runs):
            with cols[i % len(cols)]:
                with st.container(border=True):
                    render_verdict_card(result, title=result.model_id)

    if other_runs:
        st.markdown('<p class="section-heading">Framework stress test</p>', unsafe_allow_html=True)
        for result in other_runs:
            with st.expander(f"{result.model_id} — {result.lens.value}"):
                render_verdict_card(result)

    export_data = export_comparison_json(
        comparison,
        scenario_id=scenario.id if scenario else None,
        framework_stress=framework_stress,
        consistency_test=consistency_test,
        consistency_runs=consistency_runs or None,
    )
    st.download_button(
        "Export JSON",
        data=export_data,
        file_name=f"ethical_comparison_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
    )

else:
    if not dilemma_text:
        st.caption("Select or enter a dilemma in the sidebar.")
    elif not selected_models:
        st.caption("Select at least one model in the sidebar.")
