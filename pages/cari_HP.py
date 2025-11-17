import streamlit as st

st.title("📱 Masukkan Spesifikasi SmartPhone")

# Input pencarian
search_keyword = st.text_input("Cari berdasarkan nama HP:")

# Filter
st.subheader("🔍 Filter")
col1, col2, col3 = st.columns(3)

with col1:
    min_price = st.number_input("Harga Minimal", min_value=0, value=0)
with col2:
    max_price = st.number_input("Harga Maksimal", min_value=0, value=10000000)
with col3:
    min_ram = st.number_input("RAM minimum (GB)", min_value=0, value=0)

st.write("---")

# Tombol cari
if st.button("Cari"):
    st.info("Fitur pencarian belum terhubung ke backend.")
