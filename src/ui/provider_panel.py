from __future__ import annotations

import streamlit as st

from src.config import groq_configured


def render_provider_status() -> None:
    if groq_configured():
        label = "Groq connected"
    else:
        label = "Simulated mode"
    st.sidebar.markdown(
        f'<span class="sidebar-status-badge">{label}</span>',
        unsafe_allow_html=True,
    )
    if not groq_configured():
        st.sidebar.caption("Add GROQ_API_KEY for live models.")
