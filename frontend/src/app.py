from pathlib import Path

import streamlit as st

from utils.env_variables import display_values, load_environment_variables
from utils.log_init import initialize_logs

ASSETS = Path(__file__).parent / "assets"

st.set_page_config(
    page_title="CleanOps",
    page_icon=str(ASSETS / "logo_cleanops.png"),
)

st.logo(str(ASSETS / "logo_cleanops.png"), size="large")


if "logs_initialized" not in st.session_state:
    initialize_logs("Streamlit App")
    load_environment_variables()
    display_values(include_prefix="BACKEND")
    st.session_state["logs_initialized"] = True

logged_in = bool(st.session_state.get("access_token"))

home = st.Page("pages/home.py", title="CleanOps", icon="🌿", default=True)
public_key = st.Page("pages/public_key.py", title="Public key", icon="🔑", url_path="public-key")
verify = st.Page(
    "pages/verify_certificate.py", title="Verify a certificate", icon="✅", url_path="verify"
)

if logged_in:
    pages = {
        "": [home],
        "My space": [
            st.Page("pages/projects.py", title="Projects", icon="📁", url_path="projects"),
            st.Page("pages/new_audit.py", title="New audit", icon="🚀", url_path="new-audit"),
            st.Page("pages/audits.py", title="Audits", icon="📋", url_path="audits"),
        ],
        "Public tools": [public_key, verify],
    }
    st.sidebar.caption(f"Logged in as {st.session_state.get('username', '')}")
    if st.sidebar.button("Log out"):
        for key in ("access_token", "id_user", "username", "last_audit", "pending_key"):
            st.session_state.pop(key, None)
        st.rerun()
else:
    pages = [home, public_key, verify]

st.navigation(pages, position="top").run()
