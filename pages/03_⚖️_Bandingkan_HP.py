import streamlit as st
import requests
import pandas as pd
from analisis.Gemini import analyze_phones
from data import load_local_data


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
    phones_api = fetch_all_phones()
    phones_local = load_local_data()
    phones_data = phones_api + phones_local

if not phones_data:
    st.warning("Data HP tidak ditemukan atau API bermasalah.")
    st.stop()

# 2. Siapkan List Nama untuk Dropdown
# Format: "Samsung - Galaxy S24 Ultra"
phone_options = [f"{p.get('brand', 'Unknown')} - {p.get('name', 'Unknown')}" for p in phones_data]
# Mapping balik dari Nama string ke Object Data asli untuk kemudahan akses
phone_map = {f"{p.get('brand', 'Unknown')} - {p.get('name', 'Unknown')}": p for p in phones_data}

# 3. Input User (Side-by-Side)
# ...existing code...
# 3. Input User (Side-by-Side) -- GANTI DROPDOWN DENGAN INPUT TEKS
col_input1, col_input2 = st.columns(2)

with col_input1:
    st.subheader("📱 Perangkat 1")
    input_name_a = st.text_input("Masukkan nama HP Pertama", placeholder="contoh: Xiaomi 14 Pro")

with col_input2:
    st.subheader("📱 Perangkat 2")
    input_name_b = st.text_input("Masukkan nama HP Kedua", placeholder="contoh: iPhone 15 Pro Max")

# helper: cari phone berdasarkan query (exact atau partial)
def find_phone(query: str):
    q = (query or "").strip().lower()
    if not q:
        return None, []
    exact = None
    partial = []
    for p in phones_data:
        brand = (p.get("brand") or "").strip().lower()
        name = (p.get("name") or "").strip().lower()
        combined1 = f"{brand} {name}"
        combined2 = f"{brand} - {name}"
        if q == name or q == combined1 or q == combined2:
            exact = p
            break
        if q in name or q in brand or q in combined1:
            partial.append(p)
    return exact, partial

# tombol bandingkan
if st.button("Bandingkan"):
    if not input_name_a or not input_name_b:
        st.error("Masukkan nama kedua HP untuk dibandingkan.")
        st.stop()

    a_exact, a_matches = find_phone(input_name_a)
    b_exact, b_matches = find_phone(input_name_b)

    if a_exact is None and not a_matches:
        st.error(f"HP Pertama tidak ditemukan: '{input_name_a}'")
        st.stop()
    if b_exact is None and not b_matches:
        st.error(f"HP Kedua tidak ditemukan: '{input_name_b}'")
        st.stop()

    if a_exact is None and len(a_matches) > 1:
        st.warning("Terdapat beberapa hasil untuk HP Pertama. Contoh hasil:")
        st.write([f"{p['brand']} - {p['name']}" for p in a_matches[:5]])
        st.stop()
    if b_exact is None and len(b_matches) > 1:
        st.warning("Terdapat beberapa hasil untuk HP Kedua. Contoh hasil:")
        st.write([f"{p['brand']} - {p['name']}" for p in b_matches[:5]])
        st.stop()

    hp_a = a_exact if a_exact is not None else a_matches[0]
    hp_b = b_exact if b_exact is not None else b_matches[0]

    # Simpan ke session_state agar tidak hilang ketika halaman reload
    st.session_state.hp_a = hp_a
    st.session_state.hp_b = hp_b
    st.session_state.compared = True


    if hp_a == hp_b:
        st.info("Pilih dua HP berbeda untuk membandingkan.")
        st.stop()

    # tampilkan hasil (menggunakan kode tampilan yang sudah ada)
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

    # Normalisasi data agar tidak ada yang None/Null saat masuk tabel
    def safe_get(d, key):
        val = d.get(key)
        return val if val else "-"
    
    def format_rupiah(price):
        try:
            price = float(price)
            # asumsi API ngasih USD → convert ke IDR
            return "Rp {:,.0f}".format(price * 16500).replace(",", ".")
        except:
            return "-"


    comparison_data = {
        "Spesifikasi": [
            "Harga (Perkiraan)", "Sistem Operasi", "RAM", "Penyimpanan", 
            "Kamera Utama", "Baterai", 
            "Support 5G"
        ],
        f"{hp_a.get('name')}": [
            format_rupiah(safe_get(hp_a, 'price')),
            safe_get(hp_a, 'os'),
            safe_get(hp_a, 'ram'),
            safe_get(hp_a, 'storage'),
            safe_get(hp_a, 'camera'),
            safe_get(hp_a, 'battery'),
            "✅ Ya" if hp_a.get('support_5g') else "❌ Tidak"
        ],
        f"{hp_b.get('name')}": [
            format_rupiah(safe_get(hp_b, 'price')),
            safe_get(hp_b, 'os'),
            safe_get(hp_b, 'ram'),
            safe_get(hp_b, 'storage'),
            safe_get(hp_b, 'camera'),
            safe_get(hp_b, 'battery'),
            "✅ Ya" if hp_b.get('support_5g') else "❌ Tidak"
        ]
    }

    df = pd.DataFrame(comparison_data)
    
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

    # ============= TOMBOL ANALISIS CERDAS =============
 
 
    # ============= TOMBOL ANALISIS CERDAS =============
    # ============= TOMBOL ANALISIS CERDAS (SELALU ADA SETELAH PERBANDINGAN) =============
    if st.session_state.get("compared", False):

        st.markdown("---")
        st.subheader("🔍 Analisis Tambahan")

        if st.button("Jalankan Analisis Cerdas 🧠"):
            with st.spinner("AI sedang menganalisis kedua HP..."):
                hasil = analyze_phones(
                    st.session_state.hp_a,
                    st.session_state.hp_b
                )

            st.subheader("📊 Hasil Analisis Cerdas")
            st.write(hasil)



    # with st.expander("Lihat Data Mentah (JSON)"):
    #     c1, c2 = st.columns(2)
    #     c1.json(hp_a)
    #     c2.json(hp_b)

else:
    st.info("👆 Silakan masukkan dua nama HP di atas lalu klik 'Bandingkan'.")


# ============= TOMBOL KEMBALI ==============
st.markdown("---")
if st.button("⬅️ Kembali ke Dashboard"):
    st.switch_page("pages/Halaman_Utama.py")