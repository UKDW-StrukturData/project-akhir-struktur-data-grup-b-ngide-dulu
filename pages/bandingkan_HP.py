import streamlit as st
import requests
import pandas as pd

# ============= CONFIG ==============
st.set_page_config(page_title="Bandingkan HP", page_icon="⚖️", layout="wide")

# ============= PROTEKSI HALAMAN ==============
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan Login Terlebih Dahulu!")
    st.switch_page("Halaman_Login.py")

# ============= API SETUP ==============
# Gunakan API Key Anda
RAPIDAPI_KEY = "cc1faaabd3mshbea5306ec5b4287p10ec02jsn5b0d08ae2470"
SMARTPHONE_API_URL = "https://smart-phone-api1.p.rapidapi.com/sphone"
SMARTPHONE_API_HOST = "smart-phone-api1.p.rapidapi.com"

# ============= FUNGSI DATA ==============
@st.cache_data(ttl=3600) # Cache selama 1 jam agar hemat kuota API
def fetch_all_phones():
    """Mengambil daftar semua HP dari API"""
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": SMARTPHONE_API_HOST
    }
    try:
        response = requests.get(SMARTPHONE_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Validasi format data (pastikan list)
        if isinstance(data, list):
            return data
        else:
            return []
    except Exception as e:
        st.error(f"Gagal mengambil data dari server: {e}")
        return []

# ============= UI HEADER ==============
st.title("⚖️ Bandingkan Spesifikasi HP")
st.markdown("Pilih dua perangkat di bawah ini untuk melihat perbandingan spesifikasi secara detail.")
st.markdown("---")

# ============= LOGIC UTAMA ==============
# 1. Ambil Data
with st.spinner("Mengambil database HP terbaru..."):
    phones_data = fetch_all_phones()

if not phones_data:
    st.warning("Data HP tidak ditemukan atau API bermasalah.")
    st.stop()

# 2. Siapkan List Nama untuk Dropdown
# Format: "Samsung - Galaxy S24 Ultra"
phone_options = [f"{p.get('brand', 'Unknown')} - {p.get('name', 'Unknown')}" for p in phones_data]
# Mapping balik dari Nama string ke Object Data asli untuk kemudahan akses
phone_map = {f"{p.get('brand', 'Unknown')} - {p.get('name', 'Unknown')}": p for p in phones_data}

# 3. Input User (Side-by-Side)
col_input1, col_input2 = st.columns(2)

with col_input1:
    with st.container(border=True):
        st.subheader("📱 Perangkat 1")
        selected_name_a = st.selectbox(
            "Pilih HP Pertama", 
            options=phone_options, 
            index=None, 
            placeholder="Cari merk atau tipe..."
        )

with col_input2:
    with st.container(border=True):
        st.subheader("📱 Perangkat 2")
        selected_name_b = st.selectbox(
            "Pilih HP Kedua", 
            options=phone_options, 
            index=None, 
            placeholder="Cari merk atau tipe..."
        )

# ============= TAMPILAN PERBANDINGAN ==============
if selected_name_a and selected_name_b:
    # Ambil data objek asli berdasarkan nama yang dipilih
    hp_a = phone_map[selected_name_a]
    hp_b = phone_map[selected_name_b]

    st.divider()

    # --- Tampilan Judul VS ---
    col_header1, col_vs, col_header2 = st.columns([4, 1, 4])
    with col_header1:
        st.markdown(f"<h3 style='text-align: center;'>{hp_a.get('name')}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: gray;'>{hp_a.get('brand')}</p>", unsafe_allow_html=True)
    with col_vs:
        st.markdown("<h1 style='text-align: center; color: red;'>VS</h1>", unsafe_allow_html=True)
    with col_header2:
        st.markdown(f"<h3 style='text-align: center;'>{hp_b.get('name')}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: gray;'>{hp_b.get('brand')}</p>", unsafe_allow_html=True)

    # --- Tabel Perbandingan (Dataframe) ---
    st.write("") # Spacer

    # Normalisasi data agar tidak ada yang None/Null saat masuk tabel
    def safe_get(d, key):
        val = d.get(key)
        return val if val else "-"

    comparison_data = {
        "Spesifikasi": [
            "Harga (Perkiraan)", "Sistem Operasi", "RAM", "Penyimpanan", 
            "Kamera Utama", "Kamera Depan", "Baterai", 
            "Layar", "Support 5G", "Rilis"
        ],
        f"{hp_a.get('name')}": [
            safe_get(hp_a, 'price'),
            safe_get(hp_a, 'os'),
            safe_get(hp_a, 'ram'),
            safe_get(hp_a, 'storage'),
            safe_get(hp_a, 'camera'), # API ini mungkin menggabung kamera dalam satu string
            safe_get(hp_a, 'front_camera'), # Sesuaikan jika key berbeda
            safe_get(hp_a, 'battery'),
            safe_get(hp_a, 'display'), # Sesuaikan jika key berbeda
            "✅ Ya" if safe_get(hp_a, 'support_5g') else "❌ Tidak",
            safe_get(hp_a, 'release_date')
        ],
        f"{hp_b.get('name')}": [
            safe_get(hp_b, 'price'),
            safe_get(hp_b, 'os'),
            safe_get(hp_b, 'ram'),
            safe_get(hp_b, 'storage'),
            safe_get(hp_b, 'camera'),
            safe_get(hp_b, 'front_camera'),
            safe_get(hp_b, 'battery'),
            safe_get(hp_b, 'display'),
            "✅ Ya" if safe_get(hp_b, 'support_5g') else "❌ Tidak",
            safe_get(hp_b, 'release_date')
        ]
    }

    df = pd.DataFrame(comparison_data)
    
    # Menampilkan Tabel dengan lebar penuh
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Spesifikasi": st.column_config.TextColumn("Kategori", width="medium"),
            f"{hp_a.get('name')}": st.column_config.TextColumn(f"{hp_a.get('name')}", width="large"),
            f"{hp_b.get('name')}": st.column_config.TextColumn(f"{hp_b.get('name')}", width="large"),
        }
    )

    # --- Tampilan JSON Mentah (Opsional, untuk debug detail) ---
    with st.expander("Lihat Data Mentah (JSON)"):
        c1, c2 = st.columns(2)
        c1.json(hp_a)
        c2.json(hp_b)

else:
    st.info("👆 Silakan pilih dua HP di atas untuk mulai membandingkan.")

# ============= TOMBOL KEMBALI ==============
st.markdown("---")
if st.button("⬅️ Kembali ke Dashboard"):
    st.switch_page("pages/Halaman_Utama.py")