"""
Step 4: What pages exist?
Routing without the routing jargon.
"""
import streamlit as st
import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.state import init_state, get_project, update_project, mark_step_complete, Page
from utils.content import STEP_EXPLANATIONS, ERROR_MESSAGES, SUCCESS_MESSAGES

st.set_page_config(
    page_title="what pages exist? | fullshtack",
    page_icon="",
    layout="wide"
)

# Initialize
init_state()
project = get_project()
step_content = STEP_EXPLANATIONS["pages"]

# Header
st.markdown(f"## {step_content['title']}")
st.markdown(f"*{step_content['subtitle']}*")

# Initialize session state for pages
if 'editing_pages' not in st.session_state:
    st.session_state.editing_pages = list(project.pages) if project.pages else []

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown(step_content["explanation"])

    st.markdown("---")

    # Common page suggestions based on project type and auth
    st.markdown("### common pages (click to add)")

    base_pages = ["Home", "About"]

    auth_pages = []
    if project.auth_method and project.auth_method != "none":
        auth_pages = ["Sign Up", "Log In", "Profile", "Settings"]

    # Pages based on nouns
    noun_pages = []
    for noun in project.nouns:
        noun_pages.append(f"{noun.name} List")
        noun_pages.append(f"{noun.name} Detail")
        if project.auth_method != "none":
            noun_pages.append(f"Create {noun.name}")

    all_suggestions = base_pages + auth_pages + noun_pages
    existing_names = [p.name.lower() for p in st.session_state.editing_pages]

    cols = st.columns(3)
    for i, suggestion in enumerate(all_suggestions[:12]):  # Limit to 12
        if suggestion.lower() not in existing_names:
            with cols[i % 3]:
                if st.button(f"+ {suggestion}", key=f"add_page_{suggestion}"):
                    # Generate path from name
                    path = "/" + re.sub(r'[^a-z0-9]+', '-', suggestion.lower()).strip('-')
                    if path == "/home":
                        path = "/"

                    # Determine if auth required
                    requires_auth = suggestion in ["Profile", "Settings"] or "Create" in suggestion

                    # Connect to nouns
                    connected = []
                    for noun in project.nouns:
                        if noun.name.lower() in suggestion.lower():
                            connected.append(noun.name)

                    new_page = Page(
                        name=suggestion,
                        path=path,
                        description=f"The {suggestion.lower()} page",
                        requires_auth=requires_auth,
                        connected_nouns=connected
                    )
                    st.session_state.editing_pages.append(new_page)
                    st.rerun()

    st.markdown("---")

    # Current pages
    st.markdown("### your pages")

    if not st.session_state.editing_pages:
        st.info("no pages yet. add some above or create a custom one below.")
    else:
        for i, page in enumerate(st.session_state.editing_pages):
            with st.expander(f"**{page.name}** `{page.path}`", expanded=False):
                # Page name
                new_name = st.text_input(
                    "page name",
                    value=page.name,
                    key=f"page_name_{i}"
                )

                # Path
                new_path = st.text_input(
                    "url path",
                    value=page.path,
                    key=f"page_path_{i}",
                    help="like /about or /users/123"
                )

                # Description
                new_desc = st.text_input(
                    "what's on this page?",
                    value=page.description,
                    key=f"page_desc_{i}"
                )

                # Requires auth?
                if project.auth_method != "none":
                    new_requires_auth = st.checkbox(
                        "requires login to see?",
                        value=page.requires_auth,
                        key=f"page_auth_{i}"
                    )
                else:
                    new_requires_auth = False

                # Connected nouns
                if project.nouns:
                    st.markdown("**which nouns show up here?**")
                    new_connected = []
                    noun_cols = st.columns(len(project.nouns))
                    for j, noun in enumerate(project.nouns):
                        with noun_cols[j]:
                            if st.checkbox(
                                noun.name,
                                value=noun.name in page.connected_nouns,
                                key=f"page_noun_{i}_{j}"
                            ):
                                new_connected.append(noun.name)
                else:
                    new_connected = []

                # Update
                st.session_state.editing_pages[i].name = new_name
                st.session_state.editing_pages[i].path = new_path
                st.session_state.editing_pages[i].description = new_desc
                st.session_state.editing_pages[i].requires_auth = new_requires_auth
                st.session_state.editing_pages[i].connected_nouns = new_connected

                st.markdown("---")

                if st.button(f"remove this page", key=f"remove_page_{i}", type="secondary"):
                    st.session_state.editing_pages.pop(i)
                    st.rerun()

    st.markdown("---")

    # Add custom page
    st.markdown("### add a custom page")

    with st.expander("create new page"):
        custom_name = st.text_input("page name", key="custom_page_name")
        custom_path = st.text_input(
            "url path",
            key="custom_page_path",
            placeholder="/something",
            help="lowercase, no spaces, start with /"
        )
        custom_desc = st.text_input("what's on this page?", key="custom_page_desc")

        custom_auth = False
        if project.auth_method != "none":
            custom_auth = st.checkbox("requires login?", key="custom_page_auth")

        custom_nouns = []
        if project.nouns:
            st.markdown("**uses which nouns?**")
            for noun in project.nouns:
                if st.checkbox(noun.name, key=f"custom_noun_{noun.name}"):
                    custom_nouns.append(noun.name)

        if st.button("add this page"):
            if custom_name and custom_path:
                # Validate path
                if not custom_path.startswith("/") or " " in custom_path:
                    st.error(ERROR_MESSAGES["invalid_path"])
                else:
                    new_page = Page(
                        name=custom_name,
                        path=custom_path,
                        description=custom_desc or f"The {custom_name.lower()} page",
                        requires_auth=custom_auth,
                        connected_nouns=custom_nouns
                    )
                    st.session_state.editing_pages.append(new_page)
                    st.rerun()

    st.markdown("---")

    # Navigation
    col_back, col_spacer, col_next = st.columns([1, 2, 1])

    with col_back:
        if st.button(" back", use_container_width=True):
            st.switch_page("pages/3_how_do_people_get_in.py")

    with col_next:
        if st.button("next: styling ", type="primary", use_container_width=True):
            if not st.session_state.editing_pages:
                st.error(ERROR_MESSAGES["no_pages"])
            else:
                update_project(pages=st.session_state.editing_pages)
                mark_step_complete(3)
                st.success(SUCCESS_MESSAGES["pages_saved"])
                st.switch_page("pages/5_pick_a_vibe.py")

with col2:
    st.markdown("### why this matters")
    st.markdown(step_content["why_this_matters"])

    st.markdown("---")

    st.markdown("### the tech translation")
    st.markdown("""
    What we're doing here in nerd speak:

    - **Pages** → routes in your framework
    - **Path** → the URL pattern (`/users`, `/posts/[id]`)
    - **Requires login** → protected routes / auth guards
    - **Connected nouns** → which data this page fetches

    Your framework ({framework}) handles the actual routing.
    We're just mapping out what exists.
    """.format(framework=project.framework))

    if st.session_state.editing_pages:
        st.markdown("---")
        st.markdown("### your sitemap")

        for page in st.session_state.editing_pages:
            auth_badge = " (login)" if page.requires_auth else ""
            nouns_badge = f" [{', '.join(page.connected_nouns)}]" if page.connected_nouns else ""
            st.markdown(f"`{page.path}` - {page.name}{auth_badge}{nouns_badge}")

        # Visual tree
        st.markdown("---")
        st.markdown("### route tree")
        routes = [p.path for p in st.session_state.editing_pages]
        routes.sort()
        for route in routes:
            depth = route.count("/") - 1 if route != "/" else 0
            indent = "  " * depth
            name = route.split("/")[-1] or "home"
            st.code(f"{indent}{name}", language=None)
