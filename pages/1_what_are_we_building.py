"""
Step 1: What are we building?
The plain-language project description.
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.state import init_state, get_project, update_project, mark_step_complete
from utils.content import STEP_EXPLANATIONS, ERROR_MESSAGES, SUCCESS_MESSAGES

st.set_page_config(
    page_title="what are we building? | fullshtack",
    page_icon="",
    layout="wide"
)

# Initialize
init_state()
project = get_project()
step_content = STEP_EXPLANATIONS["project"]

# Header
st.markdown(f"## {step_content['title']}")
st.markdown(f"*{step_content['subtitle']}*")

# Two column layout - form on left, explanation on right
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown(step_content["explanation"])

    st.markdown("---")

    # Project name
    project_name = st.text_input(
        "what should we call this thing?",
        value=project.project_name,
        placeholder="my awesome project, the thing, literally anything",
        help="working title. you can change it later. probably will."
    )

    # Project description
    project_description = st.text_area(
        "what does it do? (explain it like you're telling a friend)",
        value=project.project_description,
        placeholder="It's a tool that helps people track their... / It's a site where users can browse and... / It connects people who have X with people who need Y...",
        height=150,
        help="don't overthink it. we just need to understand what we're building."
    )

    # Project type
    st.markdown("what kind of thing is this, roughly?")
    project_type = st.radio(
        "project type",
        options=["app", "site", "tool", "marketplace", "dashboard", "other"],
        horizontal=True,
        index=["app", "site", "tool", "marketplace", "dashboard", "other"].index(project.project_type) if project.project_type else 0,
        label_visibility="collapsed",
        help="this helps us suggest sensible defaults later"
    )

    st.markdown("---")

    # Framework choice with plain explanation
    st.markdown("### quick tech decision")
    st.markdown("what should we build this with? (don't stress, they're all good)")

    framework = st.selectbox(
        "framework",
        options=["nextjs", "sveltekit", "astro"],
        index=["nextjs", "sveltekit", "astro"].index(project.framework) if project.framework else 0,
        format_func=lambda x: {
            "nextjs": "Next.js - React-based, most popular, tons of resources",
            "sveltekit": "SvelteKit - simpler syntax, less boilerplate, gaining momentum",
            "astro": "Astro - great for content sites, ships less JavaScript"
        }[x],
        label_visibility="collapsed"
    )

    database = st.selectbox(
        "database",
        options=["supabase", "planetscale", "sqlite"],
        index=["supabase", "planetscale", "sqlite"].index(project.database) if project.database else 0,
        format_func=lambda x: {
            "supabase": "Supabase - Postgres with auth built in, generous free tier",
            "planetscale": "PlanetScale - MySQL, scales well, branching like git",
            "sqlite": "SQLite - simple file-based, good for smaller projects"
        }[x],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Validation and save
    col_back, col_spacer, col_next = st.columns([1, 2, 1])

    with col_back:
        if st.button(" back to start", use_container_width=True):
            st.switch_page("streamlit_app.py")

    with col_next:
        if st.button("next: the nouns ", type="primary", use_container_width=True):
            # Validate
            if not project_name.strip():
                st.error(ERROR_MESSAGES["empty_name"])
            elif not project_description.strip():
                st.error(ERROR_MESSAGES["empty_description"])
            else:
                # Save
                update_project(
                    project_name=project_name.strip(),
                    project_description=project_description.strip(),
                    project_type=project_type,
                    framework=framework,
                    database=database
                )
                mark_step_complete(0)
                st.success(SUCCESS_MESSAGES["project_saved"])
                st.switch_page("pages/2_what_are_the_nouns.py")

with col2:
    st.markdown("### why this matters")
    st.markdown(step_content["why_this_matters"])

    st.markdown("---")

    st.markdown("### the tech translation")
    st.markdown("""
    What we're doing here in nerd speak:

    - **Project name** → your app's identifier
    - **Description** → the README, basically
    - **Type** → informs architecture decisions
    - **Framework** → the thing that structures your code
    - **Database** → where your data lives

    But you don't need to think about it that way.
    We're just figuring out what we're building.
    """)

    if project.project_name:
        st.markdown("---")
        st.markdown("### current setup")
        st.code(f"""
project: {project.project_name}
type: {project.project_type or 'not set'}
stack: {project.framework} + {project.database}
        """, language="yaml")
