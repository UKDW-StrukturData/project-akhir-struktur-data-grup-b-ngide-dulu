import streamlit as st
import requests
import pandas as pd
from data import load_local_data

import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import tempfile


# ================= CONFIG =================
st.set_page_config(page_title="Bandingkan HP", page_icon="⚖️", layout="wide")

# ================= PROTEKSI =================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan Login Terlebih Dahulu!")
    st.switch_page("Halaman_Login.py")

# ================= HELPER FUNCTION =================
def extract_number(value):
    try:
        return float(
            str(value)
            .lower()
            .replace("mah", "")
            .replace("gb", "")
            .replace("rp", "")
            .replace(".", "")
            .strip()
        )
    except:
        return 0

def normalize(val, max_val):
    return round(val / max_val, 2) if max_val != 0 else 0

def safe_get(d, key):
    val = d.get(key)
    return val if val else "-"

def format_rupiah(price):
    try:
        price = float(price)
        return "Rp {:,.0f}".format(price * 16500).replace(",", ".")
    except:
        return "-"

# ================= API =================
RAPIDAPI_KEY = "cc1faaabd3mshbea5306ec5b4287p10ec02jsn5b0d08ae2470"
SMARTPHONE_API_URL = "https://smart-phone-api1.p.rapidapi.com/sphone"
SMARTPHONE_API_HOST = "smart-phone-api1.p.rapidapi.com"

@st.cache_data(ttl=3600)
def fetch_all_phones():
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": SMARTPHONE_API_HOST
    }
    try:
        res = requests.get(SMARTPHONE_API_URL, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()
        return data if isinstance(data, list) else []
    except Exception as e:
        st.error(f"Gagal mengambil data API: {e}")
        return []

# ================= UI HEADER =================
st.title("⚖️ Bandingkan Spesifikasi HP")
st.markdown("Pilih dua perangkat untuk melihat perbandingan spesifikasi.")
st.divider()

# ================= LOAD DATA =================
with st.spinner("Mengambil database HP..."):
    phones_api = fetch_all_phones()
    phones_local = load_local_data()
    phones_data = phones_api + phones_local

if not phones_data:
    st.warning("Data HP tidak tersedia.")
    st.stop()

# ================= INPUT =================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📱 Perangkat 1")
    input_a = st.text_input("Nama HP Pertama")

with col2:
    st.subheader("📱 Perangkat 2")
    input_b = st.text_input("Nama HP Kedua")

# ================= SEARCH FUNCTION =================
def find_phone(query):
    q = (query or "").lower().strip()
    exact = None
    partial = []

    for p in phones_data:
        brand = (p.get("brand") or "").lower()
        name = (p.get("name") or "").lower()
        full = f"{brand} {name}"

        if q == name or q == full:
            exact = p
            break
        if q in name or q in brand:
            partial.append(p)

    return exact, partial

# ================= ACTION =================
if st.button("Bandingkan"):
    if not input_a or not input_b:
        st.error("Masukkan kedua nama HP.")
        st.stop()

    a_exact, a_list = find_phone(input_a)
    b_exact, b_list = find_phone(input_b)

    if not a_exact and not a_list:
        st.error("HP pertama tidak ditemukan.")
        st.stop()

    if not b_exact and not b_list:
        st.error("HP kedua tidak ditemukan.")
        st.stop()

    hp_a = a_exact if a_exact else a_list[0]
    hp_b = b_exact if b_exact else b_list[0]

    if hp_a == hp_b:
        st.warning("Pilih dua HP yang berbeda.")
        st.stop()

    # ================= HEADER VS =================
    colA, colVS, colB = st.columns([4,1,4])

    with colA:
        st.markdown(f"<h3 style='text-align:center'>{hp_a['name']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:gray'>{hp_a['brand']}</p>", unsafe_allow_html=True)

    with colVS:
        st.markdown("<h1 style='text-align:center;color:red'>VS</h1>", unsafe_allow_html=True)

    with colB:
        st.markdown(f"<h3 style='text-align:center'>{hp_b['name']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:gray'>{hp_b['brand']}</p>", unsafe_allow_html=True)

    # ================= TABLE =================
    df = pd.DataFrame({
        "Spesifikasi": ["Harga", "OS", "RAM", "Storage", "Kamera", "Baterai", "5G"],
        hp_a["name"]: [
            format_rupiah(hp_a.get("price")),
            safe_get(hp_a, "os"),
            safe_get(hp_a, "ram"),
            safe_get(hp_a, "storage"),
            safe_get(hp_a, "camera"),
            safe_get(hp_a, "battery"),
            "✅" if hp_a.get("support_5g") else "❌"
        ],
        hp_b["name"]: [
            format_rupiah(hp_b.get("price")),
            safe_get(hp_b, "os"),
            safe_get(hp_b, "ram"),
            safe_get(hp_b, "storage"),
            safe_get(hp_b, "camera"),
            safe_get(hp_b, "battery"),
            "✅" if hp_b.get("support_5g") else "❌"
        ]
    })

    st.dataframe(df, use_container_width=True, hide_index=True)


    # ================= VISUALISASI =================
    st.markdown("## 📊 Grafik Perbandingan")

    labels = ["Harga", "Baterai", "Storage"]
    a_vals = [extract_number(hp_a.get(k)) for k in ["price","battery","storage"]]
    b_vals = [extract_number(hp_b.get(k)) for k in ["price","battery","storage"]]

    fig, ax = plt.subplots()
    x = np.arange(len(labels))
    ax.bar(x - 0.2, a_vals, 0.4, label=hp_a["name"])
    ax.bar(x + 0.2, b_vals, 0.4, label=hp_b["name"])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    st.pyplot(fig)
    # ===== SIMPAN GRAFIK UTAMA UNTUK PDF =====
    tmp_chart = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig.savefig(tmp_chart.name, bbox_inches="tight")


    # ================= TAMBAHAN VISUALISASI RAM =================
    st.markdown("### 📊 Perbandingan RAM")

    ram_a = extract_number(hp_a.get("ram"))
    ram_b = extract_number(hp_b.get("ram"))

    fig_ram, ax_ram = plt.subplots()
    ax_ram.bar([hp_a["name"], hp_b["name"]], [ram_a, ram_b])
    ax_ram.set_ylabel("RAM (GB)")
    ax_ram.set_ylim(0, max(ram_a, ram_b) + 2)
    ax_ram.set_title("Perbandingan Kapasitas RAM")

    st.pyplot(fig_ram)
    # ===== SIMPAN GRAFIK RAM UNTUK PDF =====
    tmp_ram = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig_ram.savefig(tmp_ram.name, bbox_inches="tight")
    # ================= EXPORT PDF =================
    st.markdown("## 📄 Download Sebagai PDF")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Perbandingan Spesifikasi HP", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 11)
    pdf.cell(
        0,
        8,
        f"{hp_a['brand']} {hp_a['name']}  VS  {hp_b['brand']} {hp_b['name']}",
        ln=True,
        align="C"
    )
    pdf.ln(10)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(50, 8, "Spesifikasi", 1)
    pdf.cell(65, 8, hp_a["name"], 1)
    pdf.cell(65, 8, hp_b["name"], 1)
    pdf.ln()

    pdf.set_font("Arial", "", 11)
    specs = ["Harga", "OS", "RAM", "Storage", "Kamera", "Baterai", "5G"]
    values_a = [
        format_rupiah(hp_a.get("price")),
        safe_get(hp_a, "os"),
        safe_get(hp_a, "ram"),
        safe_get(hp_a, "storage"),
        safe_get(hp_a, "camera"),
        safe_get(hp_a, "battery"),
        "Ya" if hp_a.get("support_5g") else "Tidak"
    ]
    values_b = [
        format_rupiah(hp_b.get("price")),
        safe_get(hp_b, "os"),
        safe_get(hp_b, "ram"),
        safe_get(hp_b, "storage"),
        safe_get(hp_b, "camera"),
        safe_get(hp_b, "battery"),
        "Ya" if hp_b.get("support_5g") else "Tidak"
    ]

    for i in range(len(specs)):
        pdf.cell(50, 8, specs[i], 1)
        pdf.cell(65, 8, str(values_a[i]), 1)
        pdf.cell(65, 8, str(values_b[i]), 1)
        pdf.ln()
        # ===== TAMBAHKAN GRAFIK KE PDF =====
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Grafik Perbandingan HP", ln=True)

    pdf.image(tmp_chart.name, x=10, w=180)
    pdf.ln(5)
    pdf.image(tmp_ram.name, x=10, w=180)


    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)

        st.download_button(
            label="⬇️ Download ",
            data=open(tmp.name, "rb"),
            file_name="Perbandingan_HP.pdf",
            mime="application/pdf"
        )



# ================= NAVIGATION =================
st.divider()
if st.button("⬅️ Kembali ke Beranda"):
    st.switch_page("pages/01_🏠_Beranda.py")
