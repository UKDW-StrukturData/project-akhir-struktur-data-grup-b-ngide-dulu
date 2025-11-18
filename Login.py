# ...existing code...
import streamlit as st
import time

st.set_page_config(
    page_title="Phone Finder",
    page_icon="📱",
    layout="wide"
)

st.title("📱 Phone Finder")
st.write("Selamat datang di aplikasi pencarian dan rekomendasi smartphone.")
st.write("Silakan pilih menu di sidebar untuk mulai.")

# ...existing code...
# ===== Login menu =====
# Simple credentials (ganti sesuai kebutuhan)
CREDENTIALS = {
    "admin": "password123",
    "user": "userpass"
}

# keep credentials in session so register persists during session
if "CREDENTIALS" not in st.session_state:
    st.session_state.CREDENTIALS = dict(CREDENTIALS)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# initialize UI flags (login/register/forgot behave the same)
if "show_register" not in st.session_state:
    st.session_state.show_register = False
if "show_forgot" not in st.session_state:
    st.session_state.show_forgot = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False

# safe rerun wrapper to avoid AttributeError on some Streamlit versions
def safe_rerun():
    if hasattr(st, "experimental_rerun"):
        try:
            st.experimental_rerun()
            return
        except Exception:
            pass
    # fallback: set query params using new API or toggle session state
    try:
        # replace experimental_set_query_params with st.query_params
        st.query_params = {"_t": str(int(time.time() * 1000))}
    except Exception:
        st.session_state["_rerun_toggle"] = not st.session_state.get("_rerun_toggle", False)

def authenticate(username: str, password: str) -> bool:
    return st.session_state.CREDENTIALS.get(username) == password

if not st.session_state.logged_in:
    # three top-level buttons that open only their form and close the others
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("Login", key="btn_login"):
            st.session_state.show_login = True
            st.session_state.show_register = False
            st.session_state.show_forgot = False
    with col2:
        if st.button("Register", key="btn_register"):
            st.session_state.show_register = True
            st.session_state.show_login = False
            st.session_state.show_forgot = False
    with col3:
        if st.button("Reset Password", key="btn_forgot"):
            st.session_state.show_forgot = True
            st.session_state.show_login = False
            st.session_state.show_register = False

    # LOGIN form (opened when Login button pressed)
    if st.session_state.get("show_login", False):
        st.subheader("Login")
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            submitted = st.form_submit_button("Login")
            if submitted:
                if authenticate(username.strip(), password):
                    st.session_state.logged_in = True
                    st.session_state.username = username.strip()
                    # close all forms on success
                    st.session_state.show_login = False
                    st.session_state.show_register = False
                    st.session_state.show_forgot = False
                    st.success(f"Login berhasil. Halo, {st.session_state.username}!")
                    safe_rerun()
                else:
                    st.error("Username atau password salah.")

    # REGISTER form
    if st.session_state.get("show_register", False):
        st.subheader("Register")
        with st.form("register_form", clear_on_submit=False):
            new_user = st.text_input("Pilih username", key="reg_user")
            new_pass = st.text_input("Pilih password", type="password", key="reg_pass")
            confirm = st.text_input("Konfirmasi password", type="password", key="reg_confirm")
            reg_sub = st.form_submit_button("Daftar")
            if reg_sub:
                uname = new_user.strip()
                if not uname or not new_pass:
                    st.error("Username dan password tidak boleh kosong.")
                elif uname in st.session_state.CREDENTIALS:
                    st.error("Username sudah terdaftar. Silakan pilih username lain.")
                elif new_pass != confirm:
                    st.error("Password dan konfirmasi tidak cocok.")
                else:
                    st.session_state.CREDENTIALS[uname] = new_pass
                    st.success("Registrasi berhasil. Silakan login dengan akun baru.")
                    st.session_state.show_register = False
                    safe_rerun()

    # RESET PASSWORD form
    if st.session_state.get("show_forgot", False):
        st.subheader("Reset Password")
        with st.form("forgot_form", clear_on_submit=False):
            fp_user = st.text_input("Masukkan username", key="fp_user")
            fp_new = st.text_input("Password baru", type="password", key="fp_new")
            fp_confirm = st.text_input("Konfirmasi password baru", type="password", key="fp_confirm")
            fp_sub = st.form_submit_button("Reset")
            if fp_sub:
                uname = fp_user.strip()
                if not uname or not fp_new:
                    st.error("Username dan password tidak boleh kosong.")
                elif uname not in st.session_state.CREDENTIALS:
                    st.error("Username tidak ditemukan.")
                elif fp_new != fp_confirm:
                    st.error("Password dan konfirmasi tidak cocok.")
                else:
                    st.session_state.CREDENTIALS[uname] = fp_new
                    st.success("Password berhasil direset. Silakan login dengan password baru.")
                    st.session_state.show_forgot = False
                    safe_rerun()
else:
    st.sidebar.success(f"Logged in sebagai: {st.session_state.username}")
    st.write(f"Anda sudah login sebagai **{st.session_state.username}**.")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        safe_rerun()
# ...existing code...