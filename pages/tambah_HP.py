import streamlit as st

st.title("➕ Tambah Data HP")

with st.form("add_phone_form"):
    name = st.text_input("Nama HP")
    brand = st.text_input("Brand")
    ram = st.number_input("RAM (GB)", min_value=1)
    battery = st.number_input("Baterai (mAh)", min_value=1000)
    price = st.number_input("Harga (Rp)", min_value=0)
    submitted = st.form_submit_button("Tambah HP")

if submitted:
    st.success(f"HP '{name}' berhasil ditambahkan! (sementara belum disimpan)")
