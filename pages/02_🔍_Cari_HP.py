import streamlit as st
import requests
import re
import google.generativeai as genai
import os
from data import load_local_data   # ⬅️ tambahkan ini

RAPIDAPI_KEY = "cc1faaabd3mshbea5306ec5b4287p10ec02jsn5b0d08ae2470"
SMARTPHONE_API_URL = "https://smart-phone-api1.p.rapidapi.com/sphone"
SMARTPHONE_API_HOST = "smart-phone-api1.p.rapidapi.com"

# ========== Gemini AI ==========
API_KEY = "AIzaSyCOQjmbLhVsg0Ely7s7KYnuW6wwVhCWWLQ"

genai.configure(api_key=API_KEY)
ai_model = genai.GenerativeModel("gemini-2.5-flash")
# cek login
if not st.session_state.get("logged_in", False):
    st.warning("Silakan login terlebih dahulu untuk mengakses halaman ini.")
    st.stop()

st.title("📱 Cari SmartPhone")

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
        api_data = fetch_sphones()
    except Exception as e:
        st.error(f"Gagal mengambil data API: {e}")
        api_data = []

    # ⬇️ Tambah data dari data.json
    local_data = load_local_data()

    return api_data + local_data   # GABUNGKAN

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

def parse_gb(value):
    if not value:
        return 0
    m = re.search(r'(\d+)', str(value))
    return int(m.group(1)) if m else 0

def matches_keyword(phone, keyword):
    if not keyword:
        return True
    q = keyword.lower()
    return q in (phone.get("brand", "") + phone.get("name", "")).lower()

# ================= AI EXPLAIN =================
@st.cache_data(show_spinner=False)
def ai_explain_results(results):
    if ai_model is None:
        return "⚠️ AI tidak aktif."

    limited = results[:5]  # BATAS MAX 5 HP

    prompt = f"""
Kamu adalah reviewer smartphone berpengalaman.

TUGAS:
- Jelaskan kelebihan dan kekurangan HP berikut
- Fokus ke pemakaian nyata (gaming, panas, kamera, baterai)
- JANGAN menambah HP baru
- JANGAN mengarang spesifikasi

DATA HP:
{limited}

FORMAT:
### Nama HP
- Cocok untuk:
- Kelebihan:
- Kekurangan:
"""

    try:
        res = ai_model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"⚠️ AI gagal menganalisis: {e}"

# ================= SEARCH =================
if st.button("Cari"):
    if not phones:
        st.error("Data HP tidak tersedia.")
        st.stop()

    results = []

    for p in phones:
        try:
            if not matches_keyword(p, search_keyword):
                continue

            price_val = p.get("price") or 0
            if isinstance(price_val, str) and price_val.startswith("Rp"):
                price_idr = int(re.sub(r"[^\d]", "", price_val))
            else:
                price_idr = price_val * 16500

            if price_idr > max_price:
                continue

            ram = parse_gb(p.get("ram"))
            rom = parse_gb(p.get("storage"))

            if ram < min_ram or rom < min_rom:
                continue

            results.append({
                "Brand": p.get("brand"),
                "Name": p.get("name"),
                "Price": f"Rp {price_idr:,.0f}".replace(",", "."),
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

        # ===== AI ANALYSIS =====
        st.markdown("### 🤖 Analisis AI")
        with st.spinner("AI sedang menganalisis hasil pencarian..."):
            ai_text = ai_explain_results(results)

        st.markdown(ai_text)