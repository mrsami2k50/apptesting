"""
Your Schtack - The Dashboard
Everything you've set up, in one place. Ready to generate.
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.state import init_state, get_project, get_progress_summary, export_project_config, reset_project
from utils.content import SUCCESS_MESSAGES

st.set_page_config(
    page_title="your schtack | fullshtack",
    page_icon="",
    layout="wide"
)

# Initialize
init_state()
project = get_project()
progress = get_progress_summary()

# Header
st.markdown(f"## your schtack: {project.project_name or 'unnamed project'}")
st.markdown("*everything you've set up, in one place*")

if progress["is_complete"]:
    st.success(SUCCESS_MESSAGES["all_done"])
else:
    st.warning("your schtack isn't complete yet. finish the setup to generate code.")

st.markdown("---")

# Overview columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### the basics")
    st.markdown(f"**project:** {project.project_name or 'not set'}")
    st.markdown(f"**type:** {project.project_type or 'not set'}")
    st.markdown(f"**framework:** {project.framework}")
    st.markdown(f"**database:** {project.database}")

    if project.project_description:
        st.markdown("---")
        st.markdown("**what it does:**")
        st.markdown(f"*{project.project_description}*")

with col2:
    st.markdown("### your data model")
    if project.nouns:
        for noun in project.nouns:
            with st.expander(f"**{noun.name}**"):
                if noun.description:
                    st.caption(noun.description)
                if noun.fields:
                    for field in noun.fields:
                        st.markdown(f"- `{field['name']}` ({field['type']})")
                else:
                    st.caption("no fields defined")
    else:
        st.caption("no nouns defined yet")

with col3:
    st.markdown("### authentication")
    if project.auth_method:
        st.markdown(f"**method:** {project.auth_method}")
        if project.auth_features:
            st.markdown("**features:**")
            for feature in project.auth_features:
                feature_labels = {
                    "password_reset": "password reset",
                    "remember_me": "remember me",
                    "email_verify": "email verification",
                    "magic_link": "magic link login",
                    "two_factor": "two-factor auth"
                }
                st.markdown(f"- {feature_labels.get(feature, feature)}")
    else:
        st.caption("not configured yet")

st.markdown("---")

# Pages section
st.markdown("### your pages")

if project.pages:
    page_cols = st.columns(min(4, len(project.pages)))
    for i, page in enumerate(project.pages):
        with page_cols[i % 4]:
            auth_icon = "" if page.requires_auth else ""
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                <div style="font-weight: 600;">{auth_icon} {page.name}</div>
                <div style="color: #666; font-size: 0.9rem;"><code>{page.path}</code></div>
                <div style="font-size: 0.8rem; color: #999; margin-top: 0.5rem;">{page.description or 'no description'}</div>
            </div>
            """, unsafe_allow_html=True)
            if page.connected_nouns:
                st.caption(f"uses: {', '.join(page.connected_nouns)}")
else:
    st.caption("no pages defined yet")

st.markdown("---")

# Styling section
st.markdown("### the vibe")

if project.style_vibe:
    vibe_descriptions = {
        "clean": "clean & corporate - professional, lots of white space",
        "friendly": "friendly & rounded - warm, approachable",
        "minimal": "minimal & sharp - stark, modern",
        "brutalist": "brutalist & weird - intentionally raw"
    }

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"**style:** {vibe_descriptions.get(project.style_vibe, project.style_vibe)}")
        st.markdown(f"**primary color:** {project.primary_color}")

    with col2:
        st.markdown(f"""
        <div style="width: 100px; height: 100px; background: {project.primary_color}; border-radius: 8px;"></div>
        """, unsafe_allow_html=True)
else:
    st.caption("no style selected yet")

st.markdown("---")

# Architecture diagram
st.markdown("### how it all connects")
st.markdown("""
Here's the big picture of what you're building:
""")

# Simple text-based architecture diagram
architecture = f"""
```
    User
      |
      v
  [ {project.framework.upper()} Frontend ]
      |
      | (API calls)
      v
  [ {project.database.upper()} ]
      |
      +-- {', '.join([n.name for n in project.nouns]) or 'your data'}
      |
      +-- User accounts {'('+project.auth_method+')' if project.auth_method else ''}

Pages: {' -> '.join([p.path for p in project.pages[:5]]) or '/'}
```
"""
st.markdown(architecture)

st.markdown("---")

# Export section
st.markdown("### export your config")
st.markdown("this is the structured definition of your project. it's what we'd use to generate code.")

config = export_project_config()

with st.expander("view full config (JSON)"):
    st.code(config, language="json")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="download config.json",
        data=config,
        file_name=f"{project.project_name.lower().replace(' ', '-') if project.project_name else 'project'}-config.json",
        mime="application/json"
    )

with col2:
    if st.button("copy to clipboard"):
        st.code(config, language="json")
        st.info("select and copy the config above")

st.markdown("---")

# What's next section
st.markdown("### what's next")

if not progress["is_complete"]:
    st.markdown("**finish your setup:**")

    if not progress["has_name"]:
        if st.button("1. define your project"):
            st.switch_page("pages/1_what_are_we_building.py")
    elif not progress["has_nouns"]:
        if st.button("2. add your data model (nouns)"):
            st.switch_page("pages/2_what_are_the_nouns.py")
    elif not progress["has_auth"]:
        if st.button("3. configure authentication"):
            st.switch_page("pages/3_how_do_people_get_in.py")
    elif not progress["has_pages"]:
        if st.button("4. define your pages"):
            st.switch_page("pages/4_what_pages_exist.py")
    elif not progress["has_style"]:
        if st.button("5. pick your style"):
            st.switch_page("pages/5_pick_a_vibe.py")
else:
    st.markdown("""
    **your schtack is complete.**

    you now have:
    - a clear project definition
    - a data model you understand
    - authentication configured
    - pages mapped out
    - a consistent style

    **what you can do now:**

    1. **export the config** and use it as a reference while building
    2. **browse the component library** to see what pieces you'll need
    3. **start coding** - you know exactly what you're building

    the point was never to generate code for you.
    the point was to make sure you understand what you're building
    before you build it.

    now go build the thing.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("browse components"):
            st.switch_page("pages/6_component_library.py")

    with col2:
        if st.button("edit setup"):
            st.switch_page("pages/1_what_are_we_building.py")

    with col3:
        if st.button("start a new project", type="secondary"):
            reset_project()
            st.rerun()

st.markdown("---")

# Plain language summary
st.markdown("### in plain words")

summary_parts = []

if project.project_name and project.project_description:
    summary_parts.append(f"You're building **{project.project_name}** - {project.project_description}")

if project.nouns:
    noun_names = [n.name.lower() for n in project.nouns]
    if len(noun_names) == 1:
        summary_parts.append(f"It keeps track of **{noun_names[0]}**.")
    else:
        summary_parts.append(f"It keeps track of **{', '.join(noun_names[:-1])}** and **{noun_names[-1]}**.")

if project.auth_method:
    if project.auth_method == "none":
        summary_parts.append("Anyone can use it without logging in.")
    elif project.auth_method == "email":
        summary_parts.append("People log in with their email and password.")
    elif project.auth_method == "google":
        summary_parts.append("People log in with their Google account.")
    elif project.auth_method == "both":
        summary_parts.append("People can log in with email/password or Google.")

if project.pages:
    public_pages = [p for p in project.pages if not p.requires_auth]
    private_pages = [p for p in project.pages if p.requires_auth]

    if public_pages:
        summary_parts.append(f"There are {len(public_pages)} public page(s) anyone can see.")
    if private_pages:
        summary_parts.append(f"There are {len(private_pages)} private page(s) that require login.")

if project.framework and project.database:
    summary_parts.append(f"It's built with **{project.framework}** and uses **{project.database}** for the database.")

if summary_parts:
    st.markdown("\n\n".join(summary_parts))
else:
    st.caption("complete your setup to see the summary")
