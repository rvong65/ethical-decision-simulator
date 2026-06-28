from __future__ import annotations

import streamlit as st

from src.llm.provider import list_available_models, provider_ready
from src.llm.runner import run_single
from src.models.schemas import LensMode
from src.ui.components import render_verdict_card
from src.ui.crisis import is_crisis_dilemma, render_crisis_disclaimer
from src.ui.glossary import render_lens_glossary
from src.ui.provider_panel import render_provider_status
from src.ui.sidebar import init_session_state, render_dilemma_sidebar
from src.ui.theme import page_header, render_dilemma_panel

init_session_state()

page_header(
    "Explore",
    "Single-model ethical reasoning with transparent steps and framework detection.",
)

with st.sidebar:
    dilemma_text = render_dilemma_sidebar()
    st.divider()
    st.markdown("### Settings")
    models = list(list_available_models().keys())
    model = st.selectbox("Model", models, key="explore_model")
    lens_label = st.selectbox(
        "Ethical lens",
        ["Neutral", "Utilitarian", "Deontological", "Care ethics"],
    )
    st.divider()
    render_provider_status()

render_lens_glossary()

lens_map = {
    "Neutral": LensMode.NEUTRAL,
    "Utilitarian": LensMode.UTILITARIAN,
    "Deontological": LensMode.DEONTOLOGICAL,
    "Care ethics": LensMode.CARE,
}
lens = lens_map[lens_label]

if dilemma_text:
    if is_crisis_dilemma(dilemma_text):
        st.markdown(render_crisis_disclaimer(), unsafe_allow_html=True)
    render_dilemma_panel(dilemma_text)

if st.button("Run analysis", type="primary", disabled=not dilemma_text or not provider_ready()):
    with st.spinner("Reasoning through the dilemma..."):
        result = run_single(dilemma_text, model, lens)
    st.markdown("---")
    with st.container(border=True):
        render_verdict_card(result)
elif not dilemma_text:
    st.caption("Select or enter a dilemma in the sidebar to begin.")
else:
    st.caption("Results appear on screen after you run. For JSON export, use **Compare**.")
