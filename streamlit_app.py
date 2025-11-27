"""
fullshtack - the whole thing. no mystery meat.

A website builder that actually teaches you what you're building.
"""
import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.state import init_state, get_project, reset_project, get_progress_summary
from utils.content import HERO_TITLE, HERO_SUBTITLE, LANDING_PITCH

# Page config
st.set_page_config(
    page_title="fullshtack",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the vibe
st.markdown("""
<style>
    /* Clean, unpretentious styling */
    .main-title {
        font-size: 4rem;
        font-weight: 300;
        letter-spacing: -0.02em;
        margin-bottom: 0;
        color: #1a1a1a;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        font-weight: 400;
        margin-top: 0.5rem;
        margin-bottom: 2rem;
    }
    .pitch-text {
        font-size: 1.1rem;
        line-height: 1.8;
        max-width: 700px;
    }
    .cta-button {
        font-size: 1.2rem;
        padding: 1rem 2rem;
    }
    .progress-item {
        padding: 0.5rem 0;
        border-bottom: 1px solid #eee;
    }
    .progress-done {
        color: #28a745;
    }
    .progress-pending {
        color: #999;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Make it feel less "app" more "page" */
    .block-container {
        padding-top: 3rem;
        max-width: 1000px;
    }

    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize state
init_state()
project = get_project()
progress = get_progress_summary()


def show_landing_page():
    """The main pitch - what this is and why it's different."""

    # Header
    st.markdown(f'<h1 class="main-title">{HERO_TITLE}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{HERO_SUBTITLE}</p>', unsafe_allow_html=True)

    # The pitch
    st.markdown(LANDING_PITCH)

    st.markdown("---")

    # CTA
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("alright, let's build something", type="primary", use_container_width=True):
            st.session_state.wizard_started = True
            st.rerun()

        st.markdown("")

        if progress["has_name"]:
            st.markdown("---")
            st.markdown("#### or pick up where you left off")
            if st.button(f"continue with: {project.project_name}", use_container_width=True):
                st.switch_page("pages/1_what_are_we_building.py")


def show_progress_sidebar():
    """Show what's been set up in the sidebar."""
    with st.sidebar:
        st.markdown("### your schtack")

        if not progress["has_name"]:
            st.markdown("*nothing yet - let's start*")
            return

        st.markdown(f"**{project.project_name}**")

        if project.project_description:
            st.markdown(f"*{project.project_description[:100]}{'...' if len(project.project_description) > 100 else ''}*")

        st.markdown("---")

        # Progress checklist
        steps = [
            ("project basics", progress["has_name"], "1_what_are_we_building"),
            ("data model (nouns)", progress["has_nouns"], "2_what_are_the_nouns"),
            ("authentication", progress["has_auth"], "3_how_do_people_get_in"),
            ("pages & routing", progress["has_pages"], "4_what_pages_exist"),
            ("styling & vibe", progress["has_style"], "5_pick_a_vibe"),
        ]

        for step_name, is_done, page_name in steps:
            status = "done" if is_done else "..."
            icon = "" if is_done else ""
            if st.button(f"{icon} {step_name}", key=f"nav_{page_name}", use_container_width=True):
                st.switch_page(f"pages/{page_name}.py")

        st.markdown("---")

        # Quick links
        if progress["has_nouns"]:
            if st.button("component library", use_container_width=True):
                st.switch_page("pages/6_component_library.py")

        if progress["is_complete"]:
            if st.button("your schtack (dashboard)", use_container_width=True):
                st.switch_page("pages/7_your_schtack.py")

        st.markdown("---")

        if st.button("start over", type="secondary"):
            reset_project()
            st.rerun()


# Main app logic
if st.session_state.get('wizard_started') or progress["has_name"]:
    show_progress_sidebar()
    if st.session_state.get('wizard_started') and not progress["has_name"]:
        st.switch_page("pages/1_what_are_we_building.py")
    else:
        show_landing_page()
else:
    show_landing_page()
