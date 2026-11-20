import base64
from pathlib import Path

import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification

check_authentification()
st.title("New audit")

default_id = st.session_state.get("audit_project_id", 1)
id_project = st.number_input("Project ID", min_value=1, step=1, value=int(default_id))
qualitygate_type = st.selectbox("Quality gate", ["eco", "security", "global"])
code_file = st.file_uploader("Code file")
dep_file = st.file_uploader("Dependency file", type=["txt", "json", "xml", "toml"])
signature = "".join(st.text_input("HMAC signature of the two files").split()).strip("\"'")
st.caption("You can compute the signature from the Projects page.")

if st.button("Run audit"):
    if not (signature and code_file and dep_file):
        st.warning("Please provide the signature and both files.")
        st.stop()

    code, dep = code_file.getvalue(), dep_file.getvalue()
    body = {
        "project": {
            "id_project": int(id_project),
            "codefile": {
                "name": Path(code_file.name).stem,
                "content": base64.b64encode(code).decode("ascii"),
                "type_file": Path(code_file.name).suffix.lstrip("."),
            },
            "dependencyfile": {
                "name": Path(dep_file.name).stem,
                "content": base64.b64encode(dep).decode("ascii"),
                "type_file": Path(dep_file.name).suffix.lstrip("."),
            },
        },
        "qualitygate_type": qualitygate_type,
        "hmac_signature": signature,
    }

    with st.spinner("Audit in progress..."):
        res = api_client.post("/audit/", json=body, timeout=120)

    if res["status_code"] == 200:
        st.session_state["last_audit"] = res["data"]
    else:
        st.session_state.pop("last_audit", None)
        detail = res["data"].get("detail") if isinstance(res["data"], dict) else res["data"]
        st.error(f"Audit failed ({res['status_code']}): {detail}")
