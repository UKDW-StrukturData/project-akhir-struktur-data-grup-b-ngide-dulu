import streamlit as st
import json
import os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ========================================
# Cek login
# ========================================
if not st.session_state.get("logged_in", False):
    st.warning("Silakan login terlebih dahulu untuk akses halaman ini.")
    st.stop()

st.title("➕ Tambah Data HP")

# ========================================
# Form tambah data
# ========================================
with st.form("add_phone_form"):
    name = st.text_input("Nama HP")
    brand = st.text_input("Brand")

    os_system = st.selectbox("Sistem Operasi", ["Android", "iOS"])

    ram = st.number_input("RAM (GB)", min_value=1)
    storage = st.number_input("Penyimpanan (GB)", min_value=8)
    camera_main = st.number_input("Kamera Utama (MP)", min_value=1)
    battery = st.number_input("Baterai (mAh)", min_value=1000)
    support_5g = st.selectbox("Support 5G", ["Ya", "Tidak"])
    price_text = st.text_input("Harga (Rp)", placeholder="Contoh: 3.500.000")

# convert ke angka
    price = int(price_text.replace(".", "").replace(",", "")) if price_text else 0


    submitted = st.form_submit_button("Tambah HP")

# ========================================
# Proses simpan
# ========================================
if submitted:
    new_phone = {
        "name": name,
        "brand": brand,
        "os": os_system,
        "ram": f"{ram}GB",
        "storage": f"{storage}GB",
        "camera": f"{camera_main}MP",
        "battery": f"{battery}mAh",
        "price": price,
        "support_5g": support_5g
    }

    # load → append → save
    data = load_data()
    data.append(new_phone)
    save_data(data)

    st.success(f"HP '{name}' berhasil ditambahkan!")
