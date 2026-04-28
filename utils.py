import streamlit as st
import pandas as pd
import joblib
import google.generativeai as genai
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

def calculate_distance(loc1, loc2):
    """Menghitung jarak lurus (KM) antara dua nama kota menggunakan Haversine Formula"""
    from math import radians, cos, sin, asin, sqrt
    
    # Ambil koordinat
    coord1 = COORDINATES.get(loc1)
    coord2 = COORDINATES.get(loc2)
    
    if not coord1 or not coord2:
        return 0
    
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Haversine formula
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius bumi dalam kilometer
    return round(c * r, 1)

# ==========================================
# 2. MODEL MACHINE LEARNING (CACHED)
# ==========================================

@st.cache_resource
def load_ml_resources():
    """Memuat Model XGBoost dan Kolom Fitur agar tidak reload berulang kali"""
    import xgboost as xgb
    model = joblib.load('models/salary/salary_model_xgboost.pkl')
    kolom_fitur = joblib.load('models/salary/kolom_fitur_model.pkl')
    
    list_lokasi = [
        'Bekasi', 'Bogor', 'Depok', 'Jakarta Barat', 'Jakarta Pusat', 
        'Jakarta Raya (General)', 'Jakarta Selatan', 'Jakarta Timur', 
        'Jakarta Utara', 'Tangerang', 'Tangerang Selatan'
    ]
    
    list_kategori = [
        'Administrative & Customer Service', 'Creative, Design & Media', 
        'Engineering & Manufacturing', 'Finance & Accounting', 
        'HR & General Affairs', 'Healthcare & Medical', 'IT, Tech & Data', 
        'Lainnya / Umum', 'Logistics & Supply Chain', 'Management & Supervisor', 
        'Retail, F&B & Hospitality', 'Sales & Marketing'
    ]
    
    return model, kolom_fitur, list_kategori, list_lokasi

def predict_salary(kategori, lokasi, senioritas, model, kolom_fitur):
    """Menerjemahkan teks jadi array One-Hot lalu memprediksi gaji dengan XGBoost"""
    try:
        import pandas as pd
        input_data = {col: 0 for col in kolom_fitur}
        
        if f'Lokasi_Clean_{lokasi}' in input_data:
            input_data[f'Lokasi_Clean_{lokasi}'] = 1
            
        if f'Kategori_Pekerjaan_{kategori}' in input_data:
            input_data[f'Kategori_Pekerjaan_{kategori}'] = 1
            
        if f'Senioritas_{senioritas}' in input_data:
            input_data[f'Senioritas_{senioritas}'] = 1
            
        df_input = pd.DataFrame([input_data])[kolom_fitur]
        pred_value = model.predict(df_input)[0]
        # XGBoost model trained on natural log of target variable to handle skewness, apply exp() back
        import numpy as np
        return float(np.exp(pred_value))
    except Exception as e:
        st.error(f"Error prediksi ML: {e}")
        return None

@st.cache_resource
def load_housing_resources():
    kos_model = joblib.load('models/kos/kos_price_model.pkl')
    region_enc = joblib.load('models/kos/region_encoder.pkl')
    tipe_kos_enc = joblib.load('models/kos/tipe_kos_encoder.pkl')
    electricity_enc = joblib.load('models/kos/is_electricity_included_encoder.pkl')
    return kos_model, region_enc, tipe_kos_enc, electricity_enc

def predict_kos_price(region):
    kos_model, _, _, _ = load_housing_resources()
    
    # Perbaikan Bug: Encoder dari notebook aslinya melakukan fit pada data yang sudah jadi angka,
    # bukan pada teks kota. Jadi kita bypass encoder yang rusak dan mapping manual ke nilai aslinya.
    kos_region_mapping = {
        'Bekasi': 0,
        'Bogor': 1,
        'Depok': 2,
        'Jakarta Barat': 3,
        'Jakarta Pusat': 4,
        'Jakarta Selatan': 5,
        'Jakarta Timur': 6,
        'Jakarta Utara': 7,
        'Tangerang': 8,
        'Tangerang Selatan': 9,
        'Jakarta Raya (General)': 4  # Mengambil nilai tengah ibukota
    }
    
    region_val = kos_region_mapping.get(region, 4)
    tipe_kos_val = 0      # 0 = Kos Campur
    electricity_val = 1   # 1 = Termasuk Listrik
    
    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            # Fitur: [region, tipe_kos, is_electricity, rating, rating_count, room_area]
            prediction = kos_model.predict([[region_val, tipe_kos_val, electricity_val, 4.5, 10, 12.0]])[0]
        return int(prediction)
    except Exception as e:
        return 1600000

# ==========================================
# 3. KONSULTAN KARIR AI (GEMINI)
# ==========================================

def get_gemini_client():
    """Memanggil konfigurasi Gemini menggunakan token dari secrets.toml"""
    api_key = st.secrets.get("GEMINI_API_KEY")
        
    if not api_key or len(api_key) < 10:
        return None
        
    genai.configure(api_key=api_key)
    return True

def chat_with_career_bot(client, user_message, chat_history, system_prompt_text=None):
    """Membuat interaksi chat dengan persona konsultan + konteks dari prediksi gaji"""

    if system_prompt_text is None:
        system_prompt_text = (
            "Anda adalah asisten konsultan karir profesional dan ramah yang khusus "
            "membantu pencari kerja di wilayah Jabodetabek (Indonesia). Tugas Anda menjawab pertanyaan "
            "seputar negosiasi gaji, tren industri, persiapan wawancara, dan skill set. "
            "Jawab dengan bahasa Indonesia yang santai tapi profesional. "
            "Jawaban harus ringkas, tepat sasaran (maksimal 3 paragraf), dan berikan 1-3 bullet points jika perlu."
        )

    try:
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_prompt_text)
        
        # Mengubah format history agar sesuai dengan struktur Gemini
        gemini_history = []
        for msg in chat_history:
            role = "model" if msg["role"] == "assistant" else "user"
            if msg["role"] == "system":
                continue
            gemini_history.append({"role": role, "parts": [msg["content"]]})
            
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(user_message, stream=True)
        return response
    except Exception as e:
        st.error(f"Error AI: {str(e)}")
        return None
