import streamlit as st

from utils.api_client import api_client

PUBLIC_KEY_PATH = "/.well-known/public-key"  # check the exact path in your Swagger

st.title("CleanOps public key")
st.write(
    "Certificates are signed with a private key that never leaves the server."
)

res = api_client.get(PUBLIC_KEY_PATH)
data = res["data"] if isinstance(res["data"], dict) else {}

if res["status_code"] != 200 or "public_key" not in data:
    st.error(f"Could not retrieve the public key ({res['status_code']}).")
    st.stop()

col_kid, col_alg = st.columns(2)
col_kid.metric("Key ID (kid)", data["kid"])
col_alg.metric("Algorithm", data["alg"])

st.code(data["public_key"])
st.download_button(
    "Download the key (PEM)",
    data=data["public_key"],
    file_name=f"cleanops_{data['kid']}.pem",
)
st.caption(
    "The kid written in a certificate must match the one above. Keep this key if you want "
    "to verify certificates yourself, offline."
)
