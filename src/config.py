from __future__ import annotations

import os

import streamlit as st


def bootstrap_env() -> None:
    """Load secrets into the environment without exposing credential values."""
    if "GROQ_API_KEY" not in os.environ:
        try:
            if "GROQ_API_KEY" in st.secrets:
                os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
        except Exception:
            pass


def groq_configured() -> bool:
    return "GROQ_API_KEY" in os.environ
