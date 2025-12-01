import streamlit as st


# ============= LOGIKA PERSISTENSI (AUTO-LOGIN SAAT REFRESH) ==============
# 1. Cek apakah ada username tersimpan di URL (Query Params)
# Ini menjaga agar saat di-refresh (F5), user tidak langsung ter-logout
if "user" in st.query_params:
    st.session_state.logged_in = True
    st.session_state.username = st.query_params["user"]

# 2. PROTEKSI: Jika tetap tidak ada login, baru tendang ke halaman utama
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    # Clear dulu session state yang penting
    for key in ["logged_in", "username", "mode"]:
        if key in st.session_state:
            del st.session_state[key]
    st.switch_page("Halaman_Login.py")

# 3. SET URL: Jika berhasil masuk, pastikan URL mencatat username
if st.session_state.logged_in:
    # Simpan username ke URL agar tahan refresh
    st.query_params["user"] = st.session_state.get("username", "User")

# ============= SIDEBAR ==============
with st.sidebar:
    st.write(f"Logged in as: **{st.session_state.get('username', 'User')}**")
    
    if st.button("Logout", type="primary"):
        # Hapus sesi
        st.session_state.logged_in = False
        st.session_state.mode = "login"
        # PENTING: Hapus data di URL saat logout
        st.query_params.clear() 
        st.rerun() 

# ============= KONTEN DASHBOARD (Main App) ==============
st.title("📱 Phone Finder Dashboard")
st.write(f"Selamat datang kembali, **{st.session_state.get('username', 'User')}**!")
st.markdown("---")

# --- MENU NAVIGATION CARDS ---
st.subheader("Menu Utama")

col1, col2, col3 = st.columns(3)

# CARD 1: PENCARIAN HP
with col1:
    with st.container(border=True):
        st.markdown('<div class="card-box">', unsafe_allow_html=True)

        st.markdown("### 🔍 Pencarian HP")
        st.write("Temukan daftar smartphone berdasarkan merk, harga, RAM, ROM, dan spesifikasi lainnya secara cepat.")

        if st.button("Buka Pencarian", key="btn_search", use_container_width=True):
            st.toast("Mengalihkan ke halaman Pencarian...", icon="🔍")
            st.switch_page("pages/02_🔍_Cari_HP.py")
        st.markdown('</div>', unsafe_allow_html=True)


# CARD 2: BANDINGKAN HP
with col2:
    with st.container(border=True):
        st.markdown('<div class="card-box">', unsafe_allow_html=True)

        st.markdown("### ⚖️ Bandingkan HP")
        st.write("Komparasi spesifikasi, harga, dan fitur antara dua atau lebih perangkat smartphone.")

        if st.button("Mulai Bandingkan", key="btn_compare", use_container_width=True):
            st.toast("Mengalihkan ke halaman Perbandingan...", icon="⚖️")
            st.switch_page("pages/03_⚖️_Bandingkan_HP.py")

        st.markdown('</div>', unsafe_allow_html=True)

            

# CARD 3: TAMBAHKAN HP FAVORIT ANDA
with col3:
    with st.container(border=True):
        st.markdown('<div class="card-box">', unsafe_allow_html=True)

        st.markdown("### ⭐ Tambahkan HP")
        st.write("Masukkan data HP favorit Anda ke database untuk digunakan pada pencarian & perbandingan.")

        if st.button("Tambah HP", key="btn_add_hp", use_container_width=True):
            st.toast("Mengalihkan ke halaman Tambah HP...", icon="⭐")
            st.switch_page("pages/04_➕_Tambah_HP.py")

        st.markdown('</div>', unsafe_allow_html=True)

