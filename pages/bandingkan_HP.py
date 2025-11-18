# ...existing code...
import streamlit as st

# cek login
if not st.session_state.get("logged_in", False):
    st.warning("Silakan login terlebih dahulu untuk mengakses halaman ini.")
    st.stop()

st.title("⚖️ Bandingkan Dua HP")

st.write("Pilih dua smartphone yang ingin kamu bandingkan.")

# Dropdown untuk pilih HP (sementara data dummy)
hp_list = ["Pilih HP", "Samsung A14", "Redmi Note 12", "Realme C53", "Infinix Hot 30"]

col1, col2 = st.columns(2)

with col1:
    hp1 = st.selectbox("Pilih HP pertama:", hp_list)

with col2:
    hp2 = st.selectbox("Pilih HP kedua:", hp_list)

st.write("---")

# Tombol bandingkan
if st.button("Bandingkan"):
    if hp1 == "Pilih HP" or hp2 == "Pilih HP":
        st.warning("Pilih dua HP yang valid terlebih dahulu.")
    elif hp1 == hp2:
        st.error("Kamu harus memilih dua HP yang berbeda.")
    else:
        st.success(f"Membandingkan **{hp1}** dan **{hp2}** ...")
        st.info("Fitur ini belum terhubung ke backend. Hasil perbandingan akan muncul di sini.")