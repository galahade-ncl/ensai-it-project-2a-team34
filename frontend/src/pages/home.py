import streamlit as st

from utils.api_client import api_client

if st.session_state.pop("just_logged_in", False):
    st.switch_page("pages/projects.py")

from pathlib import Path

ASSETS = Path(__file__).parent.parent / "assets"

col_logo, col_title = st.columns([1, 8], vertical_alignment="center")
col_logo.image(str(ASSETS / "logo_cleanops.png"), width=64)
col_title.markdown("# CleanOps")
st.markdown("#### Test your projects to ensure they meet safety and energy efficiency standards.")

if st.session_state.get("access_token"):
    st.markdown(f"Welcome back, **{st.session_state.get('username', '')}**.")
    col_a, col_b, _ = st.columns([1, 1, 3])
    col_a.page_link("pages/projects.py", label="My projects", icon="📁")
    col_b.page_link("pages/new_audit.py", label="New audit", icon="🚀")
else:
    _, center, _ = st.columns([1, 2, 1])
    with center:
        tab_login, tab_signup = st.tabs(["Log in", "Sign up"])

        with tab_login:
            with st.form("login"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Log in", use_container_width=True)

            if submitted:
                res = api_client.post(
                    "/login/", json={"username": username, "password": password}, sensitive=True
                )
                data = res["data"] if isinstance(res["data"], dict) else {}
                if res["status_code"] == 200 and data.get("access_token") and "id_user" in data:
                    st.session_state["access_token"] = data["access_token"]
                    st.session_state["id_user"] = data["id_user"]
                    st.session_state["username"] = username
                    st.session_state["just_logged_in"] = True
                    st.rerun()  # rebuilds the menu with the private pages
                elif res["status_code"] == 200:
                    st.error(f"Unexpected login response, fields received: {list(data)}")
                else:
                    st.error("Login failed: check your username and password.")

        with tab_signup:
            with st.form("signup"):
                new_username = st.text_input("Username", key="su_username")
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password", key="su_password")
                created = st.form_submit_button("Create the account", use_container_width=True)

            if created:
                res = api_client.post(
                    "/user/",
                    json={"username": new_username, "email": new_email, "password": new_password},
                    sensitive=True,
                )
                if res["status_code"] in (200, 201):
                    st.success("Account created, you can now log in.")
                else:
                    st.error(f"Account creation failed ({res['status_code']}).")
                # Add the detail of the HTTPException

st.divider()

st.markdown("#### The evaluation process your files go through :")
col1, col2, col3 = st.columns(3)
with col1.container(border=True):
    st.markdown("##### 🛡️ Security tests")
    st.write("Known vulnerabilities in your project.")
with col2.container(border=True):
    st.markdown("##### ⚡ Energy tests")
    st.write("Estimated consumption and carbon footprint.")
with col3.container(border=True):
    st.markdown("##### 📄 Generate Files")
    st.write("Generate an SBOM and a certificate if passed.")
