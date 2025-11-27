"""
Step 5: Pick a vibe.
Styling without the CSS trauma.
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.state import init_state, get_project, update_project, mark_step_complete
from utils.content import STEP_EXPLANATIONS, SUCCESS_MESSAGES

st.set_page_config(
    page_title="pick a vibe | fullshtack",
    page_icon="",
    layout="wide"
)

# Initialize
init_state()
project = get_project()
step_content = STEP_EXPLANATIONS["styling"]

# Header
st.markdown(f"## {step_content['title']}")
st.markdown(f"*{step_content['subtitle']}*")

# Style definitions with visual examples
VIBES = {
    "clean": {
        "name": "clean & corporate",
        "description": "lots of white space, professional, trustworthy. think: stripe, notion.",
        "colors": {
            "primary": "#0066FF",
            "secondary": "#6B7280",
            "background": "#FFFFFF",
            "surface": "#F9FAFB",
            "text": "#111827",
            "border": "#E5E7EB"
        },
        "border_radius": "8px",
        "font": "Inter, system-ui, sans-serif",
        "shadows": True
    },
    "friendly": {
        "name": "friendly & rounded",
        "description": "softer edges, warmer colors, approachable. think: slack, figma.",
        "colors": {
            "primary": "#7C3AED",
            "secondary": "#EC4899",
            "background": "#FFFBEB",
            "surface": "#FEF3C7",
            "text": "#1F2937",
            "border": "#FCD34D"
        },
        "border_radius": "16px",
        "font": "Nunito, system-ui, sans-serif",
        "shadows": True
    },
    "minimal": {
        "name": "minimal & sharp",
        "description": "less is more, stark contrasts, modern. think: linear, vercel.",
        "colors": {
            "primary": "#000000",
            "secondary": "#666666",
            "background": "#FFFFFF",
            "surface": "#FAFAFA",
            "text": "#000000",
            "border": "#EEEEEE"
        },
        "border_radius": "4px",
        "font": "SF Mono, monospace",
        "shadows": False
    },
    "brutalist": {
        "name": "brutalist & weird",
        "description": "intentionally raw, anti-design. think: are.na, cargo.",
        "colors": {
            "primary": "#FF0000",
            "secondary": "#0000FF",
            "background": "#FFFFFF",
            "surface": "#FFFF00",
            "text": "#000000",
            "border": "#000000"
        },
        "border_radius": "0px",
        "font": "Times New Roman, serif",
        "shadows": False
    }
}

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown(step_content["explanation"])

    st.markdown("---")

    # Vibe selection with live preview
    st.markdown("### pick your vibe")

    current_vibe = project.style_vibe or "clean"

    for vibe_key, vibe_data in VIBES.items():
        is_selected = current_vibe == vibe_key

        # Create a visual card for each vibe
        colors = vibe_data["colors"]
        border = f"3px solid {colors['primary']}" if is_selected else f"1px solid {colors['border']}"

        st.markdown(f"""
        <div style="
            background: {colors['background']};
            border: {border};
            border-radius: {vibe_data['border_radius']};
            padding: 1.5rem;
            margin-bottom: 1rem;
            font-family: {vibe_data['font']};
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="color: {colors['text']}; margin: 0;">{vibe_data['name']}</h4>
                    <p style="color: {colors['secondary']}; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                        {vibe_data['description']}
                    </p>
                </div>
            </div>
            <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
                <button style="
                    background: {colors['primary']};
                    color: white;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: {vibe_data['border_radius']};
                    font-family: {vibe_data['font']};
                    cursor: pointer;
                ">primary button</button>
                <button style="
                    background: {colors['surface']};
                    color: {colors['text']};
                    border: 1px solid {colors['border']};
                    padding: 0.5rem 1rem;
                    border-radius: {vibe_data['border_radius']};
                    font-family: {vibe_data['font']};
                    cursor: pointer;
                ">secondary</button>
            </div>
            <div style="
                margin-top: 1rem;
                padding: 1rem;
                background: {colors['surface']};
                border-radius: {vibe_data['border_radius']};
                border: 1px solid {colors['border']};
            ">
                <p style="color: {colors['text']}; margin: 0; font-size: 0.9rem;">
                    this is what a card would look like. notice the corners, the spacing, the overall feel.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            f"{'selected' if is_selected else 'select'} {vibe_data['name']}",
            key=f"select_{vibe_key}",
            type="primary" if is_selected else "secondary",
            disabled=is_selected
        ):
            current_vibe = vibe_key
            st.rerun()

    st.markdown("---")

    # Color customization
    st.markdown("### customize the primary color")
    st.caption("or just keep the default. it's fine.")

    selected_vibe_data = VIBES[current_vibe]
    default_color = selected_vibe_data["colors"]["primary"]

    primary_color = st.color_picker(
        "primary color",
        value=project.primary_color if project.primary_color != "#0068c9" else default_color,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Navigation
    col_back, col_spacer, col_next = st.columns([1, 2, 1])

    with col_back:
        if st.button(" back", use_container_width=True):
            st.switch_page("pages/4_what_pages_exist.py")

    with col_next:
        if st.button("finish setup ", type="primary", use_container_width=True):
            update_project(
                style_vibe=current_vibe,
                primary_color=primary_color
            )
            mark_step_complete(4)
            st.success(SUCCESS_MESSAGES["all_done"])
            st.balloons()
            st.switch_page("pages/7_your_schtack.py")

with col2:
    st.markdown("### why this matters")
    st.markdown(step_content["why_this_matters"])

    st.markdown("---")

    st.markdown("### the tech translation")
    st.markdown("""
    What we're doing here in nerd speak:

    - **Vibe** → design system / theme
    - **Colors** → design tokens / CSS variables
    - **Border radius** → corner rounding
    - **Font** → typography stack
    - **Shadows** → elevation / depth

    We'll generate CSS variables from this:

    ```css
    :root {
      --color-primary: #...;
      --color-secondary: #...;
      --radius: 8px;
      --font-body: Inter, sans-serif;
    }
    ```

    Then every component uses these variables.
    Change the vibe, everything updates.
    """)

    st.markdown("---")

    st.markdown("### your style config")
    vibe_data = VIBES[current_vibe]
    st.code(f"""
vibe: {current_vibe}
primary: {primary_color}
secondary: {vibe_data['colors']['secondary']}
border-radius: {vibe_data['border_radius']}
font: {vibe_data['font'].split(',')[0]}
shadows: {vibe_data['shadows']}
    """, language="yaml")
