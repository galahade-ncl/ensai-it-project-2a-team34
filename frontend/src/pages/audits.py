import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification

check_authentification()

id_project = st.session_state.get("selected_project")
if id_project is None:
    st.info("Select a project first.")
    if st.button("Back to the projects"):
        st.switch_page("pages/projects.py")
    st.stop()

st.title(f"Audits of project {id_project}")

res = api_client.get(f"/project/{id_project}/audit")
if res["status_code"] != 200 or not isinstance(res["data"], list):
    st.error(f"Could not load the audits ({res['status_code']}).")
    st.stop()

audits = res["data"]
if not audits:
    st.info("No audit for this project yet.")
    st.stop()

st.dataframe(
    [
        {
            "id": a["id_audit"],
            "date": a["date"],
            "gate": (a.get("quality_gate") or {}).get("status"),
        }
        for a in audits
    ],
    hide_index=True,
)

selected = st.selectbox("Audit", audits, format_func=lambda a: f"Audit {a['id_audit']}")
id_audit = selected["id_audit"]

detail = api_client.get(f"/audit/{id_audit}")
if detail["status_code"] == 200:
    st.json(detail["data"])

cert = api_client.get(f"/audit/{id_audit}/certificate")
if cert["status_code"] == 200:
    st.download_button(
        "Download the certificate (PDF)",
        data=cert["content"],
        file_name=f"certificate_{id_audit}.pdf",
        mime="application/pdf",
    )
elif cert["status_code"] == 404:
    st.info("No certificate for this audit (the quality gate failed).")

sbom = api_client.get(f"/audit/{id_audit}/sbom")
if sbom["status_code"] == 200:
    st.download_button(
        "Download the SBOM (JSON)",
        data=sbom["content"],
        file_name=f"sbom_{id_audit}.json",
        mime="application/json",
    )
