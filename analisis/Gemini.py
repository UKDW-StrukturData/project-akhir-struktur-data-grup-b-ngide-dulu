import google.generativeai as genai

# ============= KONFIGURASI API KEY =============
# Masukkan API key Gemini Kamu
genai.configure(api_key="AIzaSyAZeuZNS7prKK-Zf0tuOZdUmzscdPmqZ9M")

# ============= FUNGSI ANALISIS =============
def analyze_phones(hp_a, hp_b):
    """
    Fungsi ini menerima 2 dictionary HP
    dan mengembalikan teks analisis dari Gemini.
    """

    prompt = f"""
    Kamu adalah analis smartphone profesional.

    Berikut dua HP yang dibandingkan:

    [HP 1]
    Nama: {hp_a.get('name')}
    Brand: {hp_a.get('brand')}
    Spesifikasi: {hp_a}

    [HP 2]
    Nama: {hp_b.get('name')}
    Brand: {hp_b.get('brand')}
    Spesifikasi: {hp_b}

    Buat analisis dengan poin berikut:
    1. Perbandingan kekuatan & kelemahan.
    2. Masalah / kerusakan umum yang sering dialami kedua HP.
    3. Daya tahan fisik, baterai, suhu, dan umur pakai.
    4. Penilaian value for money berdasarkan spesifikasi.
    5. Cocok untuk user seperti apa (gaming / mahasiswa / kamera / casual).
    6. Kesimpulan: HP mana yang lebih direkomendasikan dan alasannya.

    Tulis ringkas, jelas, dan mudah dipahami.
    """

    model = genai.GenerativeModel("gemini-2.0-flash")

    # Panggil AI
    response = model.generate_content(prompt)

    return response.text
