"""
Step 2: What are the nouns?
Data modeling without saying "schema".
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.state import init_state, get_project, update_project, mark_step_complete, Noun
from utils.content import STEP_EXPLANATIONS, ERROR_MESSAGES, SUCCESS_MESSAGES

st.set_page_config(
    page_title="what are the nouns? | fullshtack",
    page_icon="",
    layout="wide"
)

# Initialize
init_state()
project = get_project()
step_content = STEP_EXPLANATIONS["nouns"]

# Header
st.markdown(f"## {step_content['title']}")
st.markdown(f"*{step_content['subtitle']}*")

# Initialize session state for nouns editing
if 'editing_nouns' not in st.session_state:
    st.session_state.editing_nouns = list(project.nouns) if project.nouns else []
if 'show_add_noun' not in st.session_state:
    st.session_state.show_add_noun = False

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown(step_content["explanation"])

    st.markdown("---")

    # Common nouns suggestions based on project type
    st.markdown("### common nouns (click to add)")

    common_nouns = {
        "app": ["Users", "Posts", "Comments", "Likes", "Messages", "Notifications"],
        "site": ["Users", "Pages", "Posts", "Categories", "Tags", "Media"],
        "tool": ["Users", "Projects", "Tasks", "Settings", "Logs"],
        "marketplace": ["Users", "Sellers", "Buyers", "Listings", "Orders", "Reviews", "Messages"],
        "dashboard": ["Users", "Reports", "Metrics", "Settings", "Exports"],
        "other": ["Users", "Items", "Categories", "Settings"]
    }

    suggestions = common_nouns.get(project.project_type, common_nouns["other"])
    existing_names = [n.name.lower() for n in st.session_state.editing_nouns]

    cols = st.columns(4)
    for i, suggestion in enumerate(suggestions):
        if suggestion.lower() not in existing_names:
            with cols[i % 4]:
                if st.button(f"+ {suggestion}", key=f"add_{suggestion}"):
                    new_noun = Noun(
                        name=suggestion,
                        description=f"The {suggestion.lower()} in your app",
                        fields=[],
                        relationships=[]
                    )
                    st.session_state.editing_nouns.append(new_noun)
                    st.rerun()

    st.markdown("---")

    # Current nouns
    st.markdown("### your nouns")

    if not st.session_state.editing_nouns:
        st.info("no nouns yet. add some above or create a custom one below.")
    else:
        for i, noun in enumerate(st.session_state.editing_nouns):
            with st.expander(f"**{noun.name}**", expanded=True):
                # Basic info
                new_name = st.text_input(
                    "name",
                    value=noun.name,
                    key=f"noun_name_{i}",
                    label_visibility="collapsed"
                )

                new_desc = st.text_input(
                    "what is this?",
                    value=noun.description,
                    key=f"noun_desc_{i}",
                    placeholder="a brief description of what this thing is"
                )

                # Fields
                st.markdown("**what info do you track about each one?**")
                st.caption("(these become columns in your database)")

                # Common field suggestions
                common_fields = {
                    "users": ["email", "name", "password", "avatar", "created_at"],
                    "posts": ["title", "content", "author", "published_at", "status"],
                    "products": ["name", "description", "price", "image", "stock"],
                    "orders": ["user", "items", "total", "status", "created_at"],
                    "messages": ["from", "to", "content", "read", "sent_at"],
                }

                field_suggestions = common_fields.get(noun.name.lower(), ["name", "description", "created_at"])

                # Show current fields
                if noun.fields:
                    for j, field in enumerate(noun.fields):
                        fcol1, fcol2, fcol3 = st.columns([2, 2, 1])
                        with fcol1:
                            st.text(field.get("name", ""))
                        with fcol2:
                            st.text(field.get("type", "text"))
                        with fcol3:
                            if st.button("x", key=f"remove_field_{i}_{j}"):
                                noun.fields.pop(j)
                                st.rerun()

                # Add field
                fcol1, fcol2, fcol3 = st.columns([2, 2, 1])
                with fcol1:
                    new_field_name = st.text_input(
                        "field name",
                        key=f"new_field_name_{i}",
                        placeholder="field name",
                        label_visibility="collapsed"
                    )
                with fcol2:
                    new_field_type = st.selectbox(
                        "type",
                        options=["text", "number", "email", "password", "date", "boolean", "reference"],
                        key=f"new_field_type_{i}",
                        label_visibility="collapsed"
                    )
                with fcol3:
                    if st.button("add", key=f"add_field_{i}"):
                        if new_field_name:
                            noun.fields.append({"name": new_field_name, "type": new_field_type})
                            st.rerun()

                # Quick add common fields
                st.caption("quick add:")
                qcols = st.columns(len(field_suggestions))
                for k, fs in enumerate(field_suggestions):
                    existing_field_names = [f["name"] for f in noun.fields]
                    if fs not in existing_field_names:
                        with qcols[k]:
                            if st.button(fs, key=f"quick_{i}_{fs}"):
                                field_type = "email" if "email" in fs else "password" if "password" in fs else "date" if "_at" in fs else "text"
                                noun.fields.append({"name": fs, "type": field_type})
                                st.rerun()

                st.markdown("---")

                # Update the noun
                st.session_state.editing_nouns[i].name = new_name
                st.session_state.editing_nouns[i].description = new_desc

                # Remove button
                if st.button(f"remove {noun.name}", key=f"remove_noun_{i}", type="secondary"):
                    st.session_state.editing_nouns.pop(i)
                    st.rerun()

    st.markdown("---")

    # Add custom noun
    st.markdown("### add a custom noun")

    with st.expander("create new noun"):
        custom_name = st.text_input("what's the thing called?", key="custom_noun_name")
        custom_desc = st.text_input("what is it?", key="custom_noun_desc", placeholder="a brief description")

        if st.button("add this noun"):
            if custom_name:
                existing_names = [n.name.lower() for n in st.session_state.editing_nouns]
                if custom_name.lower() in existing_names:
                    st.error(ERROR_MESSAGES["duplicate_noun"])
                else:
                    new_noun = Noun(
                        name=custom_name,
                        description=custom_desc or f"The {custom_name.lower()} in your app",
                        fields=[],
                        relationships=[]
                    )
                    st.session_state.editing_nouns.append(new_noun)
                    st.rerun()

    st.markdown("---")

    # Navigation
    col_back, col_spacer, col_next = st.columns([1, 2, 1])

    with col_back:
        if st.button(" back", use_container_width=True):
            st.switch_page("pages/1_what_are_we_building.py")

    with col_next:
        if st.button("next: authentication ", type="primary", use_container_width=True):
            if not st.session_state.editing_nouns:
                st.error(ERROR_MESSAGES["no_nouns"])
            else:
                update_project(nouns=st.session_state.editing_nouns)
                mark_step_complete(1)
                st.success(SUCCESS_MESSAGES["nouns_saved"])
                st.switch_page("pages/3_how_do_people_get_in.py")

with col2:
    st.markdown("### why this matters")
    st.markdown(step_content["why_this_matters"])

    st.markdown("---")

    st.markdown("### the tech translation")
    st.markdown("""
    What we're doing here in nerd speak:

    - **Nouns** → database tables / models / entities
    - **Fields** → columns in those tables
    - **Types** → data types (string, integer, boolean, etc.)
    - **Relationships** → foreign keys, joins

    The fancy term is "data modeling" or "schema design".

    But really: we're just listing the things and what we know about them.
    """)

    if st.session_state.editing_nouns:
        st.markdown("---")
        st.markdown("### your data model")
        for noun in st.session_state.editing_nouns:
            st.markdown(f"**{noun.name}**")
            if noun.fields:
                for field in noun.fields:
                    st.caption(f"  - {field['name']} ({field['type']})")
            else:
                st.caption("  - (no fields yet)")
