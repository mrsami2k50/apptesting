"""
Step 3: How do people get in?
Authentication without the jargon.
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.state import init_state, get_project, update_project, mark_step_complete
from utils.content import STEP_EXPLANATIONS, SUCCESS_MESSAGES

st.set_page_config(
    page_title="how do people get in? | fullshtack",
    page_icon="",
    layout="wide"
)

# Initialize
init_state()
project = get_project()
step_content = STEP_EXPLANATIONS["auth"]

# Header
st.markdown(f"## {step_content['title']}")
st.markdown(f"*{step_content['subtitle']}*")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown(step_content["explanation"])

    st.markdown("---")

    # Auth method selection
    st.markdown("### pick your login method")

    auth_options = {
        "email": {
            "label": "email & password",
            "description": "classic. they sign up with email, pick a password, log in with those.",
            "icon": ""
        },
        "google": {
            "label": "google / social login",
            "description": "one click with their Google account. less friction, but you're dependent on Google.",
            "icon": ""
        },
        "both": {
            "label": "both options",
            "description": "let them choose. more work to set up, but maximum flexibility.",
            "icon": ""
        },
        "none": {
            "label": "no login needed",
            "description": "public tool, no user accounts. everyone sees the same thing.",
            "icon": ""
        }
    }

    # Current selection
    current_auth = project.auth_method or "email"

    for method, info in auth_options.items():
        is_selected = current_auth == method
        container = st.container()
        with container:
            col_radio, col_text = st.columns([1, 10])
            with col_radio:
                if st.checkbox(
                    info["label"],
                    value=is_selected,
                    key=f"auth_{method}",
                    label_visibility="collapsed"
                ):
                    current_auth = method
            with col_text:
                st.markdown(f"**{info['icon']} {info['label']}**")
                st.caption(info["description"])

    st.markdown("---")

    # Additional features (only if auth is needed)
    if current_auth != "none":
        st.markdown("### extra login features")
        st.caption("check what you want. we'll set it up.")

        features = {
            "password_reset": "forgot password / reset by email",
            "remember_me": "stay logged in (remember me checkbox)",
            "email_verify": "verify email before account works",
            "magic_link": "passwordless login via email link",
            "two_factor": "two-factor authentication (SMS or app)"
        }

        selected_features = project.auth_features or []

        for feature_key, feature_label in features.items():
            is_checked = feature_key in selected_features
            if st.checkbox(feature_label, value=is_checked, key=f"feature_{feature_key}"):
                if feature_key not in selected_features:
                    selected_features.append(feature_key)
            else:
                if feature_key in selected_features:
                    selected_features.remove(feature_key)

        st.markdown("---")

        # Visual representation of what this means
        st.markdown("### what this looks like in practice")

        preview_col1, preview_col2 = st.columns(2)

        with preview_col1:
            st.markdown("**sign up page will have:**")
            if current_auth in ["email", "both"]:
                st.markdown("- email field")
                st.markdown("- password field")
                st.markdown("- confirm password field")
            if current_auth in ["google", "both"]:
                st.markdown("- 'continue with Google' button")
            if "email_verify" in selected_features:
                st.markdown("- sends verification email after signup")

        with preview_col2:
            st.markdown("**login page will have:**")
            if current_auth in ["email", "both"]:
                st.markdown("- email field")
                st.markdown("- password field")
            if current_auth in ["google", "both"]:
                st.markdown("- 'continue with Google' button")
            if "remember_me" in selected_features:
                st.markdown("- 'remember me' checkbox")
            if "password_reset" in selected_features:
                st.markdown("- 'forgot password?' link")
            if "magic_link" in selected_features:
                st.markdown("- 'email me a login link' option")

    else:
        selected_features = []
        st.info("no login means everyone can access everything. make sure that's what you want.")

    st.markdown("---")

    # Navigation
    col_back, col_spacer, col_next = st.columns([1, 2, 1])

    with col_back:
        if st.button(" back", use_container_width=True):
            st.switch_page("pages/2_what_are_the_nouns.py")

    with col_next:
        if st.button("next: pages ", type="primary", use_container_width=True):
            update_project(
                auth_method=current_auth,
                auth_features=selected_features
            )
            mark_step_complete(2)
            st.success(SUCCESS_MESSAGES["auth_saved"])
            st.switch_page("pages/4_what_pages_exist.py")

with col2:
    st.markdown("### why this matters")
    st.markdown(step_content["why_this_matters"])

    st.markdown("---")

    st.markdown("### the tech translation")
    st.markdown("""
    What we're doing here in nerd speak:

    - **Authentication** → proving who someone is
    - **Email/password** → credential-based auth
    - **Google login** → OAuth 2.0 flow
    - **Remember me** → persistent session/token
    - **Password reset** → token-based password recovery
    - **Email verify** → email confirmation flow
    - **Magic link** → passwordless auth via email
    - **2FA** → multi-factor authentication

    Your database setup (**{database}**) handles most of this for you.
    We're just deciding what options to turn on.
    """.format(database=project.database))

    st.markdown("---")

    st.markdown("### security note")
    st.markdown("""
    We're not rolling our own auth. That's how security holes happen.

    Your stack ({database}) has battle-tested auth built in.
    We're using that. You just pick the features.

    - Passwords get hashed (unreadable even to us)
    - Sessions are secure
    - Tokens expire properly
    - All the boring-but-critical stuff is handled
    """.format(database=project.database))

    if current_auth != "none":
        st.markdown("---")
        st.markdown("### your auth setup")
        st.code(f"""
method: {current_auth}
features:
{chr(10).join(f'  - {f}' for f in selected_features) if selected_features else '  (none selected)'}
        """, language="yaml")
