"""
Project state management for fullshtack.
Keeps track of everything the user has set up, in plain terms.
"""
import streamlit as st
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json


@dataclass
class Noun:
    """A thing you're keeping track of in your app."""
    name: str
    description: str
    fields: List[Dict[str, str]] = field(default_factory=list)
    relationships: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class Page:
    """A page in your app."""
    name: str
    path: str
    description: str
    requires_auth: bool = False
    connected_nouns: List[str] = field(default_factory=list)


@dataclass
class ProjectState:
    """The whole picture of what you're building."""
    # Step 1: What are we building?
    project_name: str = ""
    project_description: str = ""
    project_type: str = ""  # 'app', 'site', 'tool', etc.

    # Step 2: What are the nouns?
    nouns: List[Noun] = field(default_factory=list)

    # Step 3: How do people get in?
    auth_method: str = ""  # 'email', 'google', 'both', 'none'
    auth_features: List[str] = field(default_factory=list)  # 'password_reset', 'remember_me', etc.

    # Step 4: What pages exist?
    pages: List[Page] = field(default_factory=list)

    # Step 5: Pick a vibe
    style_vibe: str = ""  # 'clean', 'friendly', 'brutalist', 'minimal'
    primary_color: str = "#0068c9"

    # Stack choices
    framework: str = "nextjs"  # 'nextjs', 'sveltekit', 'astro'
    database: str = "supabase"  # 'supabase', 'planetscale', 'sqlite'

    # Progress tracking
    current_step: int = 0
    completed_steps: List[int] = field(default_factory=list)


def init_state():
    """Set up the project state if it doesn't exist."""
    if 'project' not in st.session_state:
        st.session_state.project = ProjectState()
    if 'wizard_started' not in st.session_state:
        st.session_state.wizard_started = False
    return st.session_state.project


def get_project() -> ProjectState:
    """Get the current project state."""
    return init_state()


def update_project(**kwargs):
    """Update the project with new values."""
    project = get_project()
    for key, value in kwargs.items():
        if hasattr(project, key):
            setattr(project, key, value)


def mark_step_complete(step: int):
    """Mark a wizard step as done."""
    project = get_project()
    if step not in project.completed_steps:
        project.completed_steps.append(step)
    project.current_step = step + 1


def reset_project():
    """Start over from scratch."""
    st.session_state.project = ProjectState()
    st.session_state.wizard_started = False


def get_progress_summary() -> Dict:
    """Get a plain-language summary of what's been set up."""
    project = get_project()

    summary = {
        "has_name": bool(project.project_name),
        "has_nouns": len(project.nouns) > 0,
        "has_auth": bool(project.auth_method),
        "has_pages": len(project.pages) > 0,
        "has_style": bool(project.style_vibe),
        "is_complete": len(project.completed_steps) >= 5
    }

    return summary


def export_project_config() -> str:
    """Export the project setup as a config that could generate code."""
    project = get_project()

    config = {
        "project": {
            "name": project.project_name,
            "description": project.project_description,
            "type": project.project_type
        },
        "stack": {
            "framework": project.framework,
            "database": project.database
        },
        "data_model": {
            "entities": [
                {
                    "name": noun.name,
                    "description": noun.description,
                    "fields": noun.fields,
                    "relationships": noun.relationships
                }
                for noun in project.nouns
            ]
        },
        "auth": {
            "method": project.auth_method,
            "features": project.auth_features
        },
        "pages": [
            {
                "name": page.name,
                "path": page.path,
                "description": page.description,
                "requires_auth": page.requires_auth,
                "uses_data": page.connected_nouns
            }
            for page in project.pages
        ],
        "styling": {
            "vibe": project.style_vibe,
            "primary_color": project.primary_color
        }
    }

    return json.dumps(config, indent=2)
