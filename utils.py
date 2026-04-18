import streamlit as st
import pandas as pd
import joblib
from groq import Groq
import os

# ==========================================
# 1. PETA SPASIAL & KOORDINAT
# ==========================================

# Kamus Latitude dan Longitude Kota Jabodetabek
COORDINATES = {
    'Jakarta Selatan': [-6.2615, 106.8106],
    'Jakarta Barat': [-6.1683, 106.7588],
    'Jakarta Utara': [-6.1384, 106.8643],
    'Jakarta Timur': [-6.2250, 106.9004],
    'Jakarta Pusat': [-6.1805, 106.8284],
    'Jakarta Raya (General)': [-6.2000, 106.8166],
    'Tangerang Selatan': [-6.2886, 106.7179],
    'Tangerang': [-6.1702, 106.6403],
    'Bekasi': [-6.2383, 106.9756],
    'Bogor': [-6.5971, 106.7996],
    'Depok': [-6.4025, 106.7942],
    'Luar Jabodetabek': [-6.2000, 106.8166] # Standar ke Jakarta
}

@st.cache_data
def load_map_data(filepath):
    """Memuat data CSV agregasi dan menyuntikkan koordinat statis"""
    df = pd.read_csv(filepath)
    df['lat'] = df['Lokasi_Clean'].apply(lambda x: COORDINATES.get(x, [-6.2000, 106.8166])[0])
    df['lon'] = df['Lokasi_Clean'].apply(lambda x: COORDINATES.get(x, [-6.2000, 106.8166])[1])
    return df

# ==========================================
# 2. MODEL MACHINE LEARNING (CACHED)
# ==========================================

@st.cache_resource
def load_ml_resources():
    """Memuat Model RF dan Encoder agar tidak reload berulang kali"""
    model = joblib.load('models/salary_model.pkl')
    kategori_enc = joblib.load('models/kategori_encoder.pkl')
    lokasi_enc = joblib.load('models/lokasi_encoder.pkl')
    
    # Ekstrak original string list untuk dropdown UI
    list_kategori = kategori_enc.classes_
    list_lokasi = lokasi_enc.classes_
    
    return model, kategori_enc, lokasi_enc, list_kategori, list_lokasi

def predict_salary(kategori, lokasi, model, kat_enc, lok_enc):
    """Menerjemahkan teks jadi angka lalu memprediksi gaji"""
    try:
        k_encoded = kat_enc.transform([kategori])
        l_encoded = lok_enc.transform([lokasi])
        # Format input X ke mode DataFrame / 2D Array
        pred_value = model.predict([[k_encoded[0], l_encoded[0]]])[0]
        return pred_value
    except Exception as e:
        return None

# ==========================================
# 3. KONSULTAN KARIR AI (GROQ)
# ==========================================

def get_groq_client():
    """Memanggil client Groq menggunakan token dari secrets.toml"""
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key or len(api_key) < 10:
        return None
    return Groq(api_key=api_key)

def chat_with_career_bot(client, user_message, chat_history, system_prompt_text=None):
    """Membuat interaksi chat dengan persona konsultan + konteks dari prediksi gaji"""

    # Gunakan system prompt dari pemanggil (main.py) jika tersedia,
    # fallback ke prompt generik jika tidak ada konteks prediksi
    if system_prompt_text is None:
        system_prompt_text = (
            "Anda adalah asisten konsultan karir profesional dan ramah yang khusus "
            "membantu pencari kerja di wilayah Jabodetabek (Indonesia). Tugas Anda menjawab pertanyaan "
            "seputar negosiasi gaji, tren industri, persiapan wawancara, dan skill set. "
            "Jawab dengan bahasa Indonesia yang santai tapi profesional. "
            "Jawaban harus ringkas, tepat sasaran (maksimal 3 paragraf), dan berikan 1-3 bullet points jika perlu."
        )

    system_prompt = {"role": "system", "content": system_prompt_text}

    # Gabung System, History, dan Pertanyaan baru
    messages = [system_prompt] + chat_history + [{"role": "user", "content": user_message}]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.6,
            max_tokens=1024,
            stream=True
        )
        return response
    except Exception as e:
        st.error(f"Error AI: {str(e)}")
        return None
