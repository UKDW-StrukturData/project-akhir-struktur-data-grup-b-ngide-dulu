import streamlit as st

# ============= JUDUL ==============
st.set_page_config(page_title="Phone Finder", page_icon="📱", layout="wide")

# ============= SESSION STATE ==============
if "mode" not in st.session_state:
    st.session_state.mode = "login"   # login, register, reset

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# dummy database
if "CREDENTIALS" not in st.session_state:
    st.session_state.CREDENTIALS = {
        "admin": "password123",
        "user": "userpass"
    }


if not st.session_state.logged_in:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

# ============= STYLE CSS - biar mirip sama mockup ==============
st.markdown("""
<style>
.container-box {
    border: 3px solid #000;
    border-radius: 8px;
    padding: 30px 40px;
    width: 90%;
    margin: auto;
    background-color: white;
}

.header-title {
    text-align: center;
    font-size: 65px;
    font-weight: 700;
    margin-bottom: 10px;
}

.left-title {
    font-size: 60px;
    font-weight: 1000;
    color: #;
    margin-top: 50px;
    margin-left: 70px;
}

.input-box > div > input {
    background-color: #e8e6e6 !important;
    border: 2px solid black !important;
    border-radius: 4px !important;
}

.custom-button {
    background-color: #ece9e9;
    border: 2px solid black;
    padding: 8px 30px;
    border-radius: 20px;
    font-weight: 600;
    cursor: pointer;
}
.custom-button:hover {
    background-color: #ddd;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
#                     LOGIN UI STYLING
# ============================================================
def login_ui():
    st.markdown('<div class="header-title">Login Page</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown('<div class="left-title">Hi !<br>Welcome</div>', unsafe_allow_html=True)

    with col2:
        username = st.text_input("Username", key="username_login")
        password = st.text_input("Password", type="password", key="password_login")

        login_clicked = st.button("Login", key="login_btn", use_container_width=True, type="primary")
        st.markdown("<style>button[kind='primary'] { background-color:#ff4b4b !important; }</style>", unsafe_allow_html=True)

        if login_clicked:
            if username in st.session_state.CREDENTIALS and \
               st.session_state.CREDENTIALS[username] == password:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Username atau password salah.")

    
        st.markdown(
    "<p style='font-size:14px; margin-top:10px;'>Don't have an account yet? Register now!</p>",
    unsafe_allow_html=True
)
        if st.button("Register"):
            st.session_state.mode = "register"
            st.rerun()


        st.markdown(
    "<p style='font-size:14px; margin-top:10px;'>Forgot your password? Reset!</p>",
    unsafe_allow_html=True
)
        if st.button("Reset Password"):
            st.session_state.mode = "reset"
            st.rerun()


# ============================================================
#                     REGISTER UI
# ============================================================
def register_ui():
    st.markdown('<div class="header-title">Register</div>', unsafe_allow_html=True)

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    confirm = st.text_input("Password Confirmation", type="password")

    if st.button("Register", key=register_ui, help="", type="primary"):
        st.markdown("<style>button[kind='primary'] { background-color:#ff4b4b !important; }</style>", unsafe_allow_html=True)
        if not new_user or not new_pass:
            st.error("Field tidak boleh kosong.")
        elif new_user in st.session_state.CREDENTIALS:
            st.error("Username sudah terdaftar.")
        elif new_pass != confirm:
            st.error("Konfirmasi password tidak cocok.")
        else:
            st.session_state.CREDENTIALS[new_user] = new_pass
            st.success("Registrasi berhasil! Silakan login.")
            st.session_state.mode = "login"
            st.rerun()

    if st.button("Back to Login"):
        st.session_state.mode = "login"
        st.rerun()


# ============================================================
#                     RESET PASSWORD UI
# ============================================================
def reset_ui():
    st.markdown('<div class="header-title">Reset Password</div>', unsafe_allow_html=True)

    user = st.text_input("Username")
    new_pass = st.text_input("New Password", type="password")
    confirm = st.text_input("Password Confirmation", type="password")

    st.markdown(
        "<p style='color:red; font-weight:600; margin-top:10px;'>"
        "Make sure you really want to reset your password."
        "</p>",
        unsafe_allow_html=True
    )

    if st.button("Reset Password", key="reset_submit", type="primary"):
        st.markdown("<style>button[kind='primary'] { background-color:#ff4b4b !important; }</style>", unsafe_allow_html=True)
        if user not in st.session_state.CREDENTIALS:
            st.error("Username tidak ditemukan.")
        elif new_pass != confirm:
            st.error("Konfirmasi password salah.")
        else:
            st.session_state.CREDENTIALS[user] = new_pass
            st.success("Password berhasil direset!")
            st.session_state.mode = "login"
            st.rerun()

    if st.button("Back to Login"):
        st.session_state.mode = "login"
        st.rerun()


# ============================================================
#                   MAIN PAGE (SETELAH LOGIN)
# ============================================================
def main_app():
    st.title("📱 Phone Finder")
    st.write("Selamat datang di aplikasi setelah login!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.mode = "login"
        st.rerun()

# ============================================================
#                     APP FLOW
# ============================================================
if not st.session_state.logged_in:
    if st.session_state.mode == "login":
        login_ui()
    elif st.session_state.mode == "register":
        register_ui()
    elif st.session_state.mode == "reset":
        reset_ui()
else:
    main_app()


