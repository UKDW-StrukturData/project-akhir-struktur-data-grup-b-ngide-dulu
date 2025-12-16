import streamlit as st
import google.generativeai as genai

# ================= CONFIG API =================
try:
    # GANTI: os.environ -> st.secrets
    gemini_key = st.secrets["GEMINI_API_KEY"]
    
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    model = None

# ================= AI CONSULTATION (BEBAS) =================
def ask_ai_consultant(user_query: str) -> str:
    if model is None:
        return "⚠️ AI belum aktif. Periksa API Key."

    prompt = f"""
Kamu adalah konsultan smartphone profesional.

ATURAN:
- Berikan rekomendasi HP secara UMUM
- Boleh menyebut merek dan model apa pun
- Gunakan pengetahuan umum
- JANGAN mengklaim ketersediaan stok toko
- Sarankan user untuk mengecek ketersediaan di database toko

PERTANYAAN USER:
"{user_query}"

FORMAT JAWABAN:
- Bullet points
- Nama HP
- Alasan singkat
- Kelebihan & kekurangan
"""

    try:
        response = model.generate_content(prompt)
        return response.text or "⚠️ AI tidak memberikan jawaban."
    except Exception as e:
        return f"❌ Error AI: {e}"

# ================= MAIN APP =================
def main():
    st.set_page_config(
        page_title="Konsultasi HP AI",
        page_icon="🤖",
        layout="centered"
    )

    st.title("💬 Konsultasi HP AI")
    st.markdown(
        """
Tanya **apa saja soal HP** 🚀  
AI akan memberi **rekomendasi umum**,  
lalu kamu bisa **cek ketersediaannya di fitur Cari HP**.
"""
    )
    st.divider()

    user_prompt = st.text_area(
        "Tulis kebutuhanmu di sini:",
        placeholder="Contoh: HP gaming 5 jutaan, kamera bagus, atau iPhone terbaru",
        height=100
    )

    if st.button("✨ Send", type="primary", use_container_width=True):
        if not user_prompt.strip():
            st.warning("⚠️ Tuliskan pertanyaanmu dulu.")
        else:
            with st.spinner("🤖 AI sedang berpikir..."):
                answer = ask_ai_consultant(user_prompt)

            st.markdown("### 💡 Jawaban AI")
            st.success("Selesai ✨")
            st.markdown(answer)

# ================= RUN =================
if __name__ == "__main__":
    main()
