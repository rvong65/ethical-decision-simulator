"""Ethical Decision Simulator — Streamlit navigation entry point."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from src.config import bootstrap_env
from src.ui.theme import apply_theme

_ASSETS = Path(__file__).parent / "docs" / "assets"
_FAVICON = _ASSETS / "favicon.svg"

st.set_page_config(
    page_title="Ethical Decision Simulator",
    page_icon=str(_FAVICON) if _FAVICON.exists() else "⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

bootstrap_env()
apply_theme()

home = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
explore = st.Page("pages/explore.py", title="Explore", icon="🔍")
compare = st.Page("pages/compare.py", title="Compare", icon="📊")

pg = st.navigation([home, explore, compare])
pg.run()
