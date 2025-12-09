import streamlit as st
import json
import random
import re

# Guard import google generative ai agar app tidak crash jika package/credential bermasalah
try:
    import google.generativeai as genai
    genai.configure(api_key="AIzaSyDmoosYqfR35JM1ZefMphOPHYEveRO44Bo")  # ← ganti API KEY Anda
    model = genai.GenerativeModel("gemini-pro")
except Exception:
    genai = None
    model = None

# Helper fallback untuk mendapatkan gambar HP jika fungsi eksternal tidak tersedia
def get_phone_image(name: str) -> str:
    # Gunakan placeholder sederhana; user bisa ganti dengan URL gambar yang valid atau logika pencarian
    placeholder = "https://via.placeholder.com/300x300.png?text=No+Image"
    return placeholder


def load_phones():
    """Load data HP dari JSON"""
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except:
        return []

# Tambahkan helper untuk konversi aman ke int
def to_int(value):
    """Convert value (possibly string with non-digits) to int safely. Return 0 if not possible."""
    if value is None:
        return 0
    if isinstance(value, (int, float)):
        try:
            return int(value)
        except:
            return 0
    if isinstance(value, str):
        # Hapus semua karakter bukan digit
        digits = re.sub(r'[^0-9\-]', '', value)
        if digits == '' or digits == '-' or digits == '+':
            return 0
        try:
            return int(digits)
        except:
            return 0
    return 0

def get_recommendation_logic(budget, priority, brand_pref, phones):
    """Logika untuk merekomendasikan HP"""
    recommendations = []
    
    for phone in phones:
        score = 0
        match_reasons = []
        
        # Data HP (konversi aman ke int)
        price = to_int(phone.get("harga", 0))
        camera = to_int(phone.get("kamera_utama", 0))
        battery = to_int(phone.get("baterai", 0))
        ram = to_int(phone.get("ram", 0))
        storage = to_int(phone.get("penyimpanan", 0))
        brand = phone.get("brand", "").lower()
        
        # 1. Filter berdasarkan BUDGET
        if budget == "< Rp 2 juta" and price < 2000000:
            score += 4
            match_reasons.append("💰 Sesuai budget hemat")
        elif budget == "Rp 2-4 juta" and 2000000 <= price <= 4000000:
            score += 4
            match_reasons.append("💰 Sesuai budget menengah")
        elif budget == "Rp 4-7 juta" and 4000000 <= price <= 7000000:
            score += 4
            match_reasons.append("💰 Sesuai budget premium")
        elif budget == "> Rp 7 juta" and price > 7000000:
            score += 4
            match_reasons.append("💰 Sesuai budget flagship")
        
        # 2. Filter berdasarkan PRIORITAS
        if priority == "Kamera Terbaik" and camera >= 48:
            score += 3
            match_reasons.append(f"📷 Kamera {camera}MP (unggulan)")
        elif priority == "Baterai Tahan Lama" and battery >= 5000:
            score += 3
            match_reasons.append(f"🔋 Baterai {battery}mAh (tahan lama)")
        elif priority == "Performas Tinggi" and ram >= 8:
            score += 3
            match_reasons.append(f"⚡ RAM {ram}GB (cepat)")
        elif priority == "Harga Terjangkau" and price <= 3000000:
            score += 3
            match_reasons.append("💸 Harga terjangkau")
        
        # 3. Filter berdasarkan BRAND (jika dipilih)
        if brand_pref:
            brand_match = any(pref.lower() in brand for pref in brand_pref)
            if brand_match:
                score += 2
                match_reasons.append("🏷️ Brand pilihan Anda")
        
        # 4. Bonus points untuk spesifikasi tinggi
        if camera >= 64:
            score += 1
        if battery >= 6000:
            score += 1
        if ram >= 12:
            score += 1
        
        if score > 0:
            recommendations.append({
                "phone": phone,
                "score": score,
                "match_reasons": match_reasons[:3]  # Maksimal 3 alasan
            })
    
    # Urutkan berdasarkan score
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return recommendations

def generate_ai_description(phone, use_type):
    prompt = f"""
    Kamu adalah AI ahli rekomendasi smartphone. Buat deskripsi singkat tetapi informatif,
    tidak lebih dari 8-10 baris. Gunakan bahasa manusia yang natural dan persuasif.

    Berikan output dengan format:
    ## Ringkasan AI
    - Kelebihan:
    - Kekurangan:
    - Cocok untuk pengguna tipe:
    - Review singkat:

    DATA HP:
    Nama: {phone.get('nama')}
    Brand: {phone.get('brand')}
    Kamera: {phone.get('kamera_utama')}MP
    RAM: {phone.get('ram')}GB
    Baterai: {phone.get('baterai')}mAh
    Storage: {phone.get('penyimpanan')}GB
    Harga: Rp {phone.get('harga')}
    Kebutuhan penggunaan user: {use_type}
    """

    try:
        if model is None:
            return "Fitur AI tidak tersedia saat ini."
        response = model.generate_content(prompt)
        return response.text
    except:
        return "AI gagal menghasilkan review."


def main():
    st.set_page_config(page_title="Rekomendasi HP", page_icon="🎯")
    
    # CSS untuk styling
    st.markdown("""
    <style>
    .phone-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .match-badge {
        background: #e3f2fd;
        color: #1976d2;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-right: 5px;
        display: inline-block;
        margin-bottom: 5px;
    }
    .price-tag {
        font-size: 1.3em;
        font-weight: bold;
        color: #d32f2f;
    }
    .spec-item {
        margin-right: 15px;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎯 Rekomendasi HP Pintar")
    st.markdown("Isi preferensi Anda, kami akan rekomendasikan HP yang paling cocok!")
    
    # Form input user
    col1, col2 = st.columns(2)
    
    with col1:
        budget = st.selectbox(
            "💰 **Budget Anda**",
            ["< Rp 2 juta", "Rp 2-4 juta", "Rp 4-7 juta", "> Rp 7 juta"],
            help="Pilih range harga yang sesuai"
        )
        
        brand_pref = st.multiselect(
            "🏷️ **Brand Pilihan** (opsional)",
            ["Samsung", "Xiaomi", "OPPO", "vivo", "iPhone", "Realme", "Google", "OnePlus", "Asus"],
            help="Pilih brand favorit Anda"
        )
    
    with col2:
        priority = st.selectbox(
            "🎯 **Prioritas Utama**",
            ["Kamera Terbaik", "Baterai Tahan Lama", "Performas Tinggi", "Harga Terjangkau", "Gaming", "Desain Premium"],
            help="Fitur apa yang paling penting untuk Anda?"
        )
        
        use_type = st.selectbox(
            "📱 **Penggunaan Utama**",
            ["Sehari-hari", "Gaming", "Fotografi", "Bisnis/Kerja", "Media Sosial", "Multimedia"],
            help="Untuk apa HP Anda paling sering digunakan?"
        )
    
    # Tombol untuk mendapatkan rekomendasi
    if st.button("🔍 Cari Rekomendasi", type="primary", use_container_width=True):
        with st.spinner("Mencari HP terbaik untuk Anda..."):
            phones = load_phones()
            
            if not phones:
                st.error("Data HP tidak ditemukan. Pastikan file data.json ada.")
                return
            
            # Dapatkan rekomendasi
            recommendations = get_recommendation_logic(budget, priority, brand_pref, phones)
            
            if recommendations:
                st.success(f"🎉 **{len(recommendations)} HP ditemukan** yang cocok dengan kriteria Anda!")
                st.divider()
                
                # Tampilkan 5 rekomendasi teratas
                for i, rec in enumerate(recommendations[:5], 1):
                    phone = rec["phone"]
                    
                    # Buat card untuk setiap HP
                    with st.container():
                        st.markdown(f'<div class="phone-card">', unsafe_allow_html=True)
                        
                        # Layout: Gambar + Info
                        col_img, col_info = st.columns([1, 2])
                        
                        with col_img:
                            # Tampilkan gambar HP
                            img_url = phone.get("gambar") or get_phone_image(phone.get("nama", ""))
                            st.image(img_url, use_container_width=True)
                        
                        with col_info:
                            # Nama dan brand
                            st.markdown(f"### **{i}. {phone.get('nama', 'Unknown')}**")
                            st.caption(f"**{phone.get('brand', 'Unknown')}**")
                            
                            # Harga
                            harga = phone.get("harga", 0)
                            st.markdown(f'<div class="price-tag">Rp {harga:,}</div>', unsafe_allow_html=True)
                            
                            # Rating kecocokan
                            match_percent = min(rec["score"] * 10, 100)
                            st.progress(match_percent/100, text=f"Kecocokan: {match_percent:.0f}%")
                            
                            # Alasan kecocokan
                            if rec["match_reasons"]:
                                st.write("**Mengapa cocok:**")
                                for reason in rec["match_reasons"]:
                                    st.markdown(f'<span class="match-badge">{reason}</span>', unsafe_allow_html=True)
                            
                            # Spesifikasi utama
                            st.write("**📊 Spesifikasi Utama:**")
                            col_spec1, col_spec2, col_spec3 = st.columns(3)
                            
                            with col_spec1:
                                st.metric("Kamera", f"{phone.get('kamera_utama', 0)}MP")
                            
                            with col_spec2:
                                st.metric("RAM", f"{phone.get('ram', 0)}GB")
                            
                            with col_spec3:
                                st.metric("Baterai", f"{phone.get('baterai', 0)}mAh")
                            
                            # Deskripsi singkat
                            deskripsi = phone.get('deskripsi', '')
                            if not deskripsi:
                                # Generate deskripsi otomatis jika tidak ada
                                deskripsi = f"{phone.get('brand', '')} {phone.get('nama', '')} adalah smartphone dengan {phone.get('ram', 0)}GB RAM, penyimpanan {phone.get('penyimpanan', 0)}GB, dan baterai {phone.get('baterai', 0)}mAh. Cocok untuk {use_type.lower()}."
                            
                            with st.expander("📝 Deskripsi Lengkap"):
                                st.write(deskripsi)
    
                                if st.button(f"💡 Minta Review AI untuk {phone.get('nama')}", key=f"ai_{i}"):
                                    with st.spinner("AI sedang membuat review..."):
                                        ai_review = generate_ai_description(phone, use_type)
                                    st.markdown(ai_review)

                        
                        # Tombol aksi
                        col_btn1, col_btn2, col_btn3 = st.columns(3)
                        with col_btn1:
                            if st.button("📖 Detail", key=f"detail_{i}", use_container_width=True):
                                st.session_state.selected_phone = phone
                                st.rerun()
                        
                        with col_btn2:
                            if st.button("⭐ Simpan", key=f"save_{i}", use_container_width=True):
                                st.success(f"{phone.get('nama')} ditambahkan ke wishlist!")
                        
                        with col_btn3:
                            if st.button("🔄 Bandingkan", key=f"compare_{i}", use_container_width=True):
                                st.info("Fitur perbandingkan akan dibuka di halaman Bandingkan HP")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.divider()
            else:
                st.warning("""
                ⚠️ **Tidak menemukan HP yang cocok.**
                
                Coba:
                1. **Perluas budget** Anda
                2. **Kurangi filter brand**
                3. **Ubah prioritas** utama
                """)
    
    # Sidebar dengan tips
    with st.sidebar:
        st.header("💡 Tips Memilih HP")
        st.info("""
        **Berdasarkan Budget:**
        - < Rp 2 jt: Entry-level, untuk sosial media & chat""")