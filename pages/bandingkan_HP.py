# ...existing code...
import streamlit as st
import requests

RAPIDAPI_KEY = "cc1faaabd3mshbea5306ec5b4287p10ec02jsn5b0d08ae2470"

# cek login
if not st.session_state.get("logged_in", False):
    st.warning("Silakan login terlebih dahulu untuk mengakses halaman ini.")
    st.stop()

st.title("⚖️ Bandingkan Dua HP (menggunakan API)")

# tambahkan fungsi untuk memanggil endpoint smart-phone-api1
SMARTPHONE_API_URL = "https://smart-phone-api1.p.rapidapi.com/sphone"
SMARTPHONE_API_HOST = "smart-phone-api1.p.rapidapi.com"

def fetch_sphones(debug: bool = False) -> dict:
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": SMARTPHONE_API_HOST
    }
    if debug:
        st.write("Request URL:", SMARTPHONE_API_URL)
        st.write("Headers:", {"x-rapidapi-host": SMARTPHONE_API_HOST, "x-rapidapi-key": "****(hidden)"})
    resp = requests.get(SMARTPHONE_API_URL, headers=headers, timeout=15)
    if resp.status_code != 200:
        raise requests.HTTPError(f"{resp.status_code} - {resp.text}")
    return resp.json()
# ...existing code...

# tambahkan: ambil daftar HP sekali dan gunakan input teks untuk pencarian
@st.cache_data(ttl=600)
def get_phone_list():
    try:
        return fetch_sphones()
    except Exception as e:
        st.error(f"Gagal mengambil daftar phone: {e}")
        return []

phones = get_phone_list()
if not phones:
    st.warning("Tidak ada data HP tersedia untuk dibandingkan.")
    st.stop()

# helper untuk mencari phone berdasarkan input user (case-insensitive, partial)
def find_phone(query: str, phones: list):
    q = (query or "").strip().lower()
    if not q:
        return None, []
    exact = None
    partial_matches = []
    for p in phones:
        brand = (p.get("brand") or "").strip()
        name = (p.get("name") or "").strip()
        combos = [
            f"{brand} - {name}".lower(),
            f"{brand} {name}".lower(),
            name.lower()
        ]
        if q in combos[0] or q == combos[1] or q == combos[2]:
            exact = p
            break
        if q in combos[0] or q in combos[1] or q in combos[2] or q in brand.lower():
            partial_matches.append(p)
    return exact, partial_matches

st.write("Ketik nama HP persis atau sebagian nama (contoh: 'Xiaomi 14 Pro' atau hanya 'Xiaomi').")
col1, col2 = st.columns(2)
with col1:
    input_a = st.text_input("Masukkan nama HP A", placeholder="contoh: Xiaomi 14 Pro", key="input_a")
with col2:
    input_b = st.text_input("Masukkan nama HP B", placeholder="contoh: iPhone 15 Pro Max", key="input_b")

if st.button("Bandingkan"):
    a_exact, a_matches = find_phone(input_a, phones)
    b_exact, b_matches = find_phone(input_b, phones)

    if not input_a or not input_b:
        st.error("Masukkan nama untuk kedua HP.")
        st.stop()

    if a_exact is None and not a_matches:
        st.error(f"HP A tidak ditemukan: '{input_a}'. Coba kata kunci lain.")
        st.stop()
    if b_exact is None and not b_matches:
        st.error(f"HP B tidak ditemukan: '{input_b}'. Coba kata kunci lain.")
        st.stop()

    if a_exact is None and len(a_matches) > 1:
        st.warning("Terdapat beberapa hasil untuk HP A. Contoh hasil:")
        st.write([f"{p.get('brand')} - {p.get('name')}" for p in a_matches[:5]])
        st.stop()
    if b_exact is None and len(b_matches) > 1:
        st.warning("Terdapat beberapa hasil untuk HP B. Contoh hasil:")
        st.write([f"{p.get('brand')} - {p.get('name')}" for p in b_matches[:5]])
        st.stop()

    phone_a = a_exact if a_exact is not None else (a_matches[0] if a_matches else None)
    phone_b = b_exact if b_exact is not None else (b_matches[0] if b_matches else None)

    if phone_a is None or phone_b is None:
        st.error("Gagal menentukan HP untuk dibandingkan.")
        st.stop()

    if phone_a == phone_b:
        st.info("Pilih dua HP berbeda untuk membandingkan.")
        st.stop()

    # tampilkan hasil
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("HP A")
        st.write(f"{phone_a.get('brand')} - {phone_a.get('name')}")
        st.json(phone_a)
    with c2:
        st.subheader("HP B")
        st.write(f"{phone_b.get('brand')} - {phone_b.get('name')}")
        st.json(phone_b)


    keys = ["price", "os", "ram", "storage", "camera", "battery", "support_5g", "brand", "name"]
    rows = []
    for k in keys:
        rows.append({"spec": k, "HP A": phone_a.get(k, "-"), "HP B": phone_b.get(k, "-")})
    st.subheader("Perbandingan ringkas")
    st.table(rows)
# ...existing code...