import base64
from pathlib import Path

import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification
from utils.signature import generate_signature

check_authentification()
st.title("New audit")

default_id = st.session_state.get("audit_project_id", 1)
id_project = st.number_input("Project ID", min_value=1, step=1, value=int(default_id))
qualitygate_type = st.selectbox("Quality gate", ["eco", "security", "global"])
code_file = st.file_uploader("Code file")
dep_file = st.file_uploader("Dependency file", type=["txt", "json", "xml", "toml"])
key_file = st.file_uploader("Project secret key file (.key)", type=["key", "txt"])
secret_b64 = "".join(st.text_input("Project secret key").split()).strip("\"'")

if st.button("Run audit"):
    if not (secret_b64 and code_file and dep_file):
        st.warning("Please provide the key and both files.")
        st.stop()

    try:
        secret = base64.b64decode(secret_b64, validate=True)
    except ValueError:
        st.error("The secret key is not valid base64.")
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
        "hmac_signature": generate_signature(secret, int(id_project), code, dep),
    }

    with st.spinner("Audit in progress..."):
        res = api_client.post("/audit/", json=body, timeout=120)

    if res["status_code"] == 200:
        st.session_state["last_audit"] = res["data"]
    else:
        st.session_state.pop("last_audit", None)
        st.error(f"Audit failed ({res['status_code']}): {res['data']}")

audit = st.session_state.get("last_audit")
if audit:
    st.success(f"Audit {audit['id_audit']} completed.")
    st.json(audit["quality_gate"])

    certificate = audit.get("certificate")
    if certificate:
        st.download_button(
            "Download the certificate (PDF)",
            data=base64.b64decode(certificate["content"]),
            file_name=f"certificate_{audit['id_audit']}.pdf",
            mime="application/pdf",
        )
        with st.expander("Signed certificate (content of the QR code)"):
            st.json(certificate["signed_data"])
    else:
        st.warning("The quality gate failed: no certificate was issued.")

    sbom = audit.get("sbom")
    if sbom and sbom.get("content"):
        st.download_button(
            "Download the SBOM (JSON)",
            data=base64.b64decode(sbom["content"]),
            file_name=f"sbom_{audit['id_audit']}.json",
            mime="application/json",
        )
