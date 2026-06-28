from __future__ import annotations

import streamlit as st

from src.scenarios.loader import get_scenario_by_id, scenario_options


def init_session_state() -> None:
    defaults = {
        "dilemma_source": "Curated scenario",
        "selected_scenario_id": None,
        "custom_dilemma": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_dilemma_sidebar() -> str | None:
    st.sidebar.markdown("### Dilemma")
    source = st.sidebar.radio(
        "Source",
        ["Curated scenario", "Custom dilemma"],
        key="dilemma_source",
        label_visibility="collapsed",
    )

    if source == "Curated scenario":
        options = scenario_options()
        titles = list(options.keys())
        if not titles:
            st.sidebar.warning("No scenarios loaded.")
            return None

        default_idx = 0
        if st.session_state.selected_scenario_id:
            for i, title in enumerate(titles):
                if options[title] == st.session_state.selected_scenario_id:
                    default_idx = i
                    break

        chosen_title = st.sidebar.selectbox("Scenario", titles, index=default_idx)
        scenario_id = options[chosen_title]
        st.session_state.selected_scenario_id = scenario_id
        scenario = get_scenario_by_id(scenario_id)
        if scenario:
            return scenario.dilemma_text
        return None

    text = st.sidebar.text_area(
        "Custom dilemma",
        value=st.session_state.custom_dilemma,
        height=140,
        placeholder="Describe the moral dilemma and who is affected…",
        label_visibility="collapsed",
    )
    st.session_state.custom_dilemma = text
    return text.strip() or None


def get_active_scenario():
    if st.session_state.dilemma_source != "Curated scenario":
        return None
    if not st.session_state.selected_scenario_id:
        return None
    return get_scenario_by_id(st.session_state.selected_scenario_id)
