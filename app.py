import streamlit as st

st.set_page_config(
    page_title="Phone Finder",
    page_icon="📱",
    layout="wide"
)

st.title("📱 Phone Finder")
st.write("Selamat datang di aplikasi pencarian dan rekomendasi smartphone.")
st.write("Silakan pilih menu di sidebar untuk mulai.")

# Auren
menu = st.sidebar.radio(
    "Menu",
    ["Login", "Register", "Forgot Password", "User Profile"]
)

# Hash table sederhana
user_table = {}

def register_user(username, email, password):
    if username in user_table:
        return False
    user_table[username] = {"email": email, "password": password}
    return True

def authenticate(username, password):
    if username in user_table and user_table[username]["password"] == password:
        return True
    return False

def reset_password(email, new_password):
    for user, data in user_table.items():
        if data["email"] == email:
            data["password"] = new_password
            return True
    return False

def update_profile(username, new_email=None, new_username=None):
    if username not in user_table:
        return False

    if new_username:
        user_table[new_username] = user_table.pop(username)
        username = new_username

    if new_email:
        user_table[username]["email"] = new_email

    return True

if menu == "Login":
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.success("Login berhasil!")
            st.session_state["logged_in"] = username
        else:
            st.error("Username atau password salah!")

if menu == "Register":
    st.subheader("📝 Register Akun Baru")

    username = st.text_input("Buat Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Daftar"):
        if register_user(username, email, password):
            st.success("Registrasi berhasil! Silakan login.")
        else:
            st.error("Username sudah digunakan!")

if menu == "Forgot Password":
    st.subheader("🔄 Reset Password")

    email = st.text_input("Masukkan email untuk reset password")
    new_pass = st.text_input("Password Baru", type="password")

    if st.button("Reset Password"):
        if reset_password(email, new_pass):
            st.success("Password berhasil direset!")
        else:
            st.error("Email tidak ditemukan!")
