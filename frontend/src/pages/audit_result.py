import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification

check_authentification()

audit = st.session_state.get("last_audit")
if not audit:
    st.info("No audit to display yet. Run an audit first.")
    st.page_link("pages/new_audit.py", label="New audit", icon="🚀")
    st.stop()


def fmt(value, spec: str) -> str:
    return format(float(value or 0), spec)


id_audit = audit.get("id_audit")
gate = audit.get("quality_gate") or {}
status = gate.get("status")

st.title(f"Audit {id_audit} - project {audit.get('id_project')}")
st.caption(f"Run on {audit.get('date')}")

if status == "Passed":
    st.success("Quality gate passed.")
elif status == "Failed":
    st.error("Quality gate failed: no certificate was issued.")
else:
    st.warning(f"Quality gate status: {status}")

col_complexity, col_energy, col_carbon = st.columns(3)
col_complexity.metric("Complexity", fmt(audit.get("complexity"), ",.0f"))
col_energy.metric("Energy (kWh)", fmt(audit.get("energy_consumption_kwh"), ".3e"))
col_carbon.metric("Carbon (gCO2e)", fmt(audit.get("carbon_emission_gco2e"), ".3e"))

with st.expander("Quality gate details"):
    st.json(gate)

st.subheader("Vulnerabilities")
vulnerabilities = audit.get("vulnerabilities") or []
if vulnerabilities:
    st.caption(f"{len(vulnerabilities)} found")
    st.dataframe(vulnerabilities, hide_index=True)
else:
    st.info("No vulnerability found.")

st.subheader("Licences")
licences = audit.get("licenses")
if isinstance(licences, list) and licences:
    st.dataframe(licences, hide_index=True)
elif isinstance(licences, str) and licences:
    st.write(licences)
else:
    st.info("No licence found.")

st.subheader("Antipatterns")
antipatterns = audit.get("anti_patterns") or []
if antipatterns:
    st.dataframe(antipatterns, hide_index=True)
else:
    st.info("No antipattern found.")

st.subheader("Files")
col_certificate, col_sbom = st.columns(2)

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

if cert and cert.get("signed_data"):
    with st.expander("Signed certificate (content of the QR code)"):
        st.json(cert["signed_data"])
    st.page_link("pages/verify_certificate.py", label="Verify a certificate", icon="✅")
