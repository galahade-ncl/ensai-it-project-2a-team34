import base64

import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification

check_authentification()

st.title("My projects")

id_user = st.session_state.get("id_user")
if id_user is None:
    st.error("Missing user id: please log in again.")
    st.stop()

# --- One-time display of a secret key ---
pending = st.session_state.get("pending_key")
if pending:
    st.warning(
        f"Secret key of Project : {pending['name']} (id : {pending['id']}). It is shown only once: without it you cannot launch audits on this project."
    )
    st.code(pending["key"])
    if st.button("I saved the key"):
        del st.session_state["pending_key"]
        st.rerun()
    st.stop()

# --- Creation ---
with st.form("new_project", clear_on_submit=True):
    name = st.text_input("New project name")
    if st.form_submit_button("Create the project") and name:
        res = api_client.post("/project/", json={"name_project": name}, sensitive=True)
        data = res["data"] if isinstance(res["data"], dict) else {}
        if res["status_code"] in (200, 201) and "secretHMACkey" in data:
            st.session_state["pending_key"] = {
                "id": data["id_project"],
                "name": data["name_project"],
                "key": data["secretHMACkey"],
            }
            st.rerun()
        else:
            st.error(f"Creation failed ({res['status_code']}).")

# --- List ---
res = api_client.get(f"/user/{id_user}/project")
if res["status_code"] != 200 or not isinstance(res["data"], list):
    st.error(f"Could not load the projects ({res['status_code']}).")
    st.stop()

projects = res["data"]
if not projects:
    st.info("No project yet.")
    st.stop()

st.dataframe(
    [{"id": p["id_project"], "name": p["name_project"]} for p in projects],
    hide_index=True,
)

selected = st.selectbox(
    "Project",
    projects,
    format_func=lambda p: f"{p['id_project']} - {p['name_project']}",
)

with st.expander("Compute an HMAC signature"):
    st.caption(
        "To call the API yourself. The signature is only valid for this project and "
        "these exact two files."
    )
    sig_key = "".join(st.text_input("Secret key of the project", key="sig_key").split()).strip(
        "\"'"
    )
    sig_code = st.file_uploader("Code file", key="sig_code")
    sig_dep = st.file_uploader("Dependency file", key="sig_dep")

    if st.button("Compute the signature"):
        if not (sig_key and sig_code and sig_dep):
            st.warning("Please provide the key and both files.")
        else:
            res = api_client.post(
                "/hmac/signature",
                json={
                    "secret": sig_key,
                    "project_id": selected["id_project"],
                    "code": base64.b64encode(sig_code.getvalue()).decode("ascii"),
                    "dependency": base64.b64encode(sig_dep.getvalue()).decode("ascii"),
                },
                sensitive=True,
            )
            data = res["data"] if isinstance(res["data"], dict) else {}
            if res["status_code"] == 200 and "signature" in data:
                st.code(data["signature"])
                st.caption(f"Received by the server: {data.get('debug')}")
            elif res["status_code"] == 400:
                st.error("The secret key is not valid base64.")
            else:
                st.error(f"Signature failed ({res['status_code']}).")

col_audits, col_audit, col_key, col_delete = st.columns(4)

if col_audits.button("See the audits"):
    st.session_state["selected_project"] = selected["id_project"]
    st.switch_page("pages/audits.py")

if col_audit.button("New audit"):
    st.session_state["audit_project_id"] = selected["id_project"]
    st.switch_page("pages/new_audit.py")

confirm_key = col_key.checkbox("Confirm new key")
if col_key.button("New secret key", disabled=not confirm_key):
    res = api_client.post(f"/project/{selected['id_project']}/secret-key", sensitive=True)
    data = res["data"] if isinstance(res["data"], dict) else {}
    if res["status_code"] == 200 and "secretHMACkey" in data:
        st.session_state["pending_key"] = {
            "id": selected["id_project"],
            "name": selected["name_project"],
            "key": data["secretHMACkey"],
        }
        st.rerun()
    else:
        st.error(f"Key regeneration failed ({res['status_code']}).")

confirm = col_delete.checkbox("Confirm deletion")
if col_delete.button("Delete", disabled=not confirm):
    res = api_client.delete(f"/project/{selected['id_project']}")
    if res["status_code"] in (200, 204):
        st.rerun()
    else:
        st.error(f"Deletion failed ({res['status_code']}).")
