# ...existing code...
import streamlit as st

# cek login
if not st.session_state.get("logged_in", False):
    st.warning("Silakan login terlebih dahulu untuk mengakses halaman ini.")
    st.stop()

st.title("🧠 Buat AI")
st.write("Halaman pembuatan AI — fitur belum diimplementasi.")