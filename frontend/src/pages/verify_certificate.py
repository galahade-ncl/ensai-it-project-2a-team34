import json

import streamlit as st

from utils.api_client import api_client

st.title("Verify a certificate")
st.caption("Paste the signed certificate (JSON contained in the QR code of the PDF).")

raw = st.text_area("Signed certificate", height=220)

if st.button("Verify") and raw.strip():
    try:
        certificate = json.loads(raw)
    except json.JSONDecodeError:
        st.error("This is not valid JSON.")
        st.stop()

    res = api_client.post("/certificate/verify", json=certificate)
    if res["status_code"] != 200:
        st.error(f"Verification failed ({res['status_code']}): {res['data']}")
        st.stop()

    result = res["data"]
    if result["valid"]:
        payload = result["payload"]
        st.success("Authentic certificate issued by this application.")
        st.write(
            "Compare these values with the text printed on the PDF: only this "
            "information is signed."
        )
        st.json(payload)
    else:
        st.error(result.get("reason") or "Invalid certificate.")
