from __future__ import annotations

from pathlib import Path

import streamlit as st

_ASSETS_DIR = Path(__file__).resolve().parents[2] / "docs" / "assets"

MODERN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    padding-top: 5.5rem !important;
    padding-bottom: 3rem;
    max-width: 1080px;
}

header[data-testid="stHeader"] {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(8px);
    border-bottom: none;
    box-shadow: none;
}

.page-hero {
    margin: 0 0 1.75rem 0;
    padding: 1.75rem 2rem;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
}

.hero-brand {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
}

.hero-icon {
    flex-shrink: 0;
    border-radius: 12px;
}

.hero-icon svg {
    width: 52px;
    height: 52px;
    display: block;
}

.hero-brand .hero-title {
    margin: 0;
    font-size: 2.35rem;
    letter-spacing: -0.035em;
}

.hero-title {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #0F172A;
    margin: 0 0 0.5rem 0;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 1rem;
    color: #64748B;
    line-height: 1.65;
    margin: 0;
    max-width: 720px;
}

.card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    border-color: #C7D2FE;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.1);
}

.card h3 {
    margin: 0 0 0.5rem 0;
    color: #0F172A;
    font-size: 1.15rem;
}

.card p {
    color: #64748B;
    margin: 0;
    line-height: 1.6;
    font-size: 0.95rem;
}

.card-accent {
    border-left: 4px solid #4F46E5;
}

.card-nav-header {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 0.35rem;
}

.card-nav-header h3 {
    margin: 0;
    font-size: 1.25rem;
}

.card-emoji {
    font-size: 1.85rem;
    line-height: 1;
    flex-shrink: 0;
}

.card-nav-explore {
    border-left-color: #6366F1;
}

.card-nav-compare {
    border-left-color: #8B5CF6;
}

.dilemma-panel {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin: 1rem 0 1.5rem 0;
    color: #334155;
    line-height: 1.7;
    font-size: 0.98rem;
}

.dilemma-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #94A3B8;
    margin-bottom: 0.5rem;
}

.badge {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    background: #EEF2FF;
    color: #4338CA;
    margin: 0 0.35rem 0.35rem 0;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.25rem 1rem;
    text-align: center;
}

.metric-label {
    font-size: 0.72rem;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
    margin: 0 0 0.35rem 0;
}

.metric-value {
    font-size: 1.65rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0;
}

.step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.5rem;
    height: 1.5rem;
    border-radius: 50%;
    background: #EEF2FF;
    color: #4F46E5;
    font-size: 0.72rem;
    font-weight: 700;
    margin-right: 0.5rem;
    flex-shrink: 0;
}

.step-row {
    display: flex;
    align-items: flex-start;
    margin-bottom: 0.65rem;
    color: #334155;
    line-height: 1.55;
}

.disclaimer {
    font-size: 0.85rem;
    color: #94A3B8;
    border-top: 1px solid #E2E8F0;
    padding-top: 1.25rem;
    margin-top: 2rem;
    line-height: 1.6;
}

.section-heading {
    font-size: 1.1rem;
    font-weight: 600;
    color: #0F172A;
    margin: 1.5rem 0 1rem 0;
}

/* Full-height indigo sidebar — gradient on outer shell only; inner blocks stay transparent */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E1B4B 0%, #312E81 50%, #3730A3 100%) !important;
    border-right: none;
}

section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"],
div[data-testid="stSidebar"] {
    background: transparent !important;
    background-color: transparent !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarNav"],
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul {
    background: transparent !important;
}

div[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] .stMarkdown h3,
div[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] label,
div[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] .stCaption,
div[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] p,
div[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] span {
    color: #E0E7FF !important;
}

div[data-testid="stSidebar"] .stRadio label,
div[data-testid="stSidebar"] .stSelectbox label,
div[data-testid="stSidebar"] .stMultiSelect label,
div[data-testid="stSidebar"] .stCheckbox label,
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stCheckbox label {
    color: #C7D2FE !important;
}

div[data-testid="stSidebar"] hr,
section[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.18) !important;
}

div[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    color: #C7D2FE !important;
}

[data-testid="stSidebarNav"] ul li:not(:last-child) {
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    padding-bottom: 0.4rem;
    margin-bottom: 0.4rem !important;
}

[data-testid="stSidebarNav"] ul li a {
    border-radius: 8px;
    padding: 0.55rem 0.75rem !important;
    font-weight: 500;
    color: #E0E7FF !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(255, 255, 255, 0.15) !important;
    color: #FFFFFF !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%);
    border: none;
    border-radius: 10px;
    font-weight: 600;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%);
}

.sidebar-status-badge {
    display: inline-block;
    padding: 0.4rem 0.85rem;
    border-radius: 10px;
    font-size: 0.78rem;
    font-weight: 600;
    border: 1px solid rgba(226, 232, 240, 0.7);
    background: rgba(255, 255, 255, 0.08);
    color: #F1F5F9;
    letter-spacing: 0.01em;
}

/* Sidebar checkboxes — solid white box on indigo (theme.sidebar + CSS) */
section[data-testid="stSidebar"] [data-testid="stCheckbox"] label[data-baseweb="checkbox"] > div:first-child,
section[data-testid="stSidebar"] [data-testid="stCheckbox"] [role="checkbox"],
section[data-testid="stSidebar"] .stCheckbox [data-baseweb="checkbox"] > div:first-child {
    border: 2px solid #FFFFFF !important;
    border-color: #FFFFFF !important;
    background-color: #FFFFFF !important;
    box-shadow: none !important;
    outline: none !important;
    min-width: 1.125rem !important;
    min-height: 1.125rem !important;
}

section[data-testid="stSidebar"] [data-testid="stCheckbox"] [data-baseweb="checkbox"][aria-checked="true"] > div:first-child,
section[data-testid="stSidebar"] [data-testid="stCheckbox"] [role="checkbox"][aria-checked="true"] {
    background-color: #4F46E5 !important;
    border-color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-testid="stCheckbox"] [data-baseweb="checkbox"][aria-checked="true"] svg,
section[data-testid="stSidebar"] [data-testid="stCheckbox"] [data-baseweb="checkbox"][aria-checked="true"] path {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}

/* Sidebar radios — light border when unchecked */
section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child,
section[data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="false"] > div:first-child {
    border: 2px solid #FFFFFF !important;
    background-color: rgba(255, 255, 255, 0.18) !important;
}

section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"][aria-checked="true"] > div:first-child,
section[data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"] > div:first-child {
    background-color: rgba(255, 255, 255, 0.18) !important;
    border-color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"] > div:first-child > div {
    background-color: #4F46E5 !important;
}
</style>
"""


def apply_theme() -> None:
    st.markdown(MODERN_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str, *, show_icon: bool = False) -> None:
    icon_path = _ASSETS_DIR / "icon.svg"
    icon_html = ""
    if show_icon and icon_path.exists():
        icon_svg = icon_path.read_text(encoding="utf-8")
        icon_html = f'<div class="hero-icon">{icon_svg}</div>'

    title_block = (
        f'<div class="hero-brand">{icon_html}<p class="hero-title">{title}</p></div>'
        if icon_html
        else f'<p class="hero-title">{title}</p>'
    )

    st.markdown(
        f"""
        <div class="page-hero">
            {title_block}
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dilemma_panel(text: str) -> None:
    st.markdown(
        f"""
        <div class="dilemma-panel">
            <div class="dilemma-label">Dilemma</div>
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )
