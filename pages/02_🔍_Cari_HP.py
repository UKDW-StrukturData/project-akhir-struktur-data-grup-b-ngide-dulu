# ...existing code...
import streamlit as st
import requests
import re

RAPIDAPI_KEY = "cc1faaabd3mshbea5306ec5b4287p10ec02jsn5b0d08ae2470"
SMARTPHONE_API_URL = "https://smart-phone-api1.p.rapidapi.com/sphone"
SMARTPHONE_API_HOST = "smart-phone-api1.p.rapidapi.com"

# cek login
if not st.session_state.get("logged_in", False):
    st.warning("Silakan login terlebih dahulu untuk mengakses halaman ini.")
    st.stop()

st.title("📱 Masukkan Spesifikasi SmartPhone")

def fetch_sphones():
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": SMARTPHONE_API_HOST
    }
    resp = requests.get(SMARTPHONE_API_URL, headers=headers, timeout=15)
    if resp.status_code != 200:
        raise requests.HTTPError(f"{resp.status_code} - {resp.text}")
    return resp.json()

@st.cache_data(ttl=600)
def get_phone_list():
    try:
        return fetch_sphones()
    except Exception as e:
        st.error(f"Gagal mengambil daftar phone: {e}")
        return []

phones = get_phone_list()

# Input pencarian
search_keyword = st.text_input("Cari berdasarkan nama HP:")

# Filter
st.subheader("🔍 Filter")
col1, col2, col3 = st.columns(3)

with col1:
    max_price = st.number_input("Harga Maksimal", min_value=0, value=10000000)
with col2:
    min_ram = st.number_input("RAM minimum (GB)", min_value=0, value=0)
with col3:
    min_rom = st.number_input("ROM minimum (GB)", min_value=0, value=0)

st.write("---")

def parse_gb(value: str) -> int:
    if not value:
        return 0
    # ambil angka pertama (mis. "12GB", "256GB")
    m = re.search(r'(\d+)', str(value))
    return int(m.group(1)) if m else 0

def matches_keyword(phone: dict, keyword: str) -> bool:
    if not keyword:
        return True
    q = keyword.strip().lower()
    brand = (phone.get("brand") or "").lower()
    name = (phone.get("name") or "").lower()
    return q in brand or q in name or q in f"{brand} {name}"

# Tombol cari
if st.button("Cari"):
    if not phones:
        st.error("Data HP tidak tersedia.")
        st.stop()

    results = []
    for p in phones:
        try:
            if not matches_keyword(p, search_keyword):
                continue
            price_usd = p.get("price") or 0
            price_idr = price_usd * 16500  # Konversi ke IDR
            ram = parse_gb(p.get("ram"))
            rom = parse_gb(p.get("storage"))
            if price_idr> max_price:
                continue
            if ram < min_ram:
                continue
            if rom < min_rom:
                continue
            results.append({
                "Brand": p.get("brand"),
                "Name": p.get("name"),
                "Price": f"Rp {price_idr:,.0f}".replace(",","."),
                "RAM": p.get("ram"),
                "ROM": p.get("storage"),
                "Camera": p.get("camera"),
                "Battery": p.get("battery"),
                "5G": p.get("support_5g")
            })
        except Exception:
            continue

    if not results:
        st.info("Tidak ada HP yang memenuhi kriteria pencarian.")
    else:
        st.success(f"Ditemukan {len(results)} hasil.")
        st.table(results)
# ...existing code...