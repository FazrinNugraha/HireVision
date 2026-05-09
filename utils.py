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
    """Memuat Model Random Forest dan seluruh encoder pipeline agar tidak reload berulang kali"""
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        model      = joblib.load('models/salary/salary_model_random_forest.pkl')
        tfidf_word = joblib.load('models/salary/tfidf_word_vectorizer.pkl')
        tfidf_char = joblib.load('models/salary/tfidf_char_vectorizer.pkl')
        encoder    = joblib.load('models/salary/target_encoder.pkl')
        ohe_encoder = joblib.load('models/salary/ohe_encoder.pkl')

    list_lokasi = [
        'Bekasi', 'Bogor', 'Depok', 'Jakarta Barat', 'Jakarta Pusat',
        'Jakarta Raya (General)', 'Jakarta Selatan', 'Jakarta Timur',
        'Jakarta Utara', 'Tangerang', 'Tangerang Selatan'
    ]

    # list_kategori tetap ada untuk kompatibilitas tab Spasial
    list_kategori = [
        'Administrative & Customer Service', 'Creative, Design & Media',
        'Engineering & Manufacturing', 'Finance & Accounting',
        'HR & General Affairs', 'Healthcare & Medical', 'IT, Tech & Data',
        'Lainnya / Umum', 'Logistics & Supply Chain', 'Management & Supervisor',
        'Retail, F&B & Hospitality', 'Sales & Marketing'
    ]

    resources = {
        'model': model,
        'tfidf_word': tfidf_word,
        'tfidf_char': tfidf_char,
        'encoder': encoder,
        'ohe_encoder': ohe_encoder,
        'list_lokasi': list_lokasi,
        'list_kategori': list_kategori,
    }
    return resources, ohe_encoder, list_kategori, list_lokasi


def predict_salary(judul_pekerjaan, kategori_pekerjaan, lokasi, resources):
    """Pipeline prediksi gaji: TF-IDF + OHE (Lokasi + Kategori only) + Random Forest"""
    try:
        import numpy as np
        import pandas as pd
        from scipy.sparse import hstack, csr_matrix

        model       = resources['model']
        tfidf_word  = resources['tfidf_word']
        tfidf_char  = resources['tfidf_char']
        ohe_encoder = resources['ohe_encoder']

        # 1. TF-IDF pada judul pekerjaan
        X_word = tfidf_word.transform([judul_pekerjaan])
        X_char = tfidf_char.transform([judul_pekerjaan])

        # 2. Fitur numerik judul (tanpa company size)
        title_len = len(judul_pekerjaan)
        title_wc  = len(judul_pekerjaan.split())
        extra = csr_matrix([[title_len, title_wc, 0]])  # comp_size = 0

        # 3. Target encoding default (tanpa perusahaan)
        target_sparse = csr_matrix([[5000000]])  # Default mean salary

        # 4. One-Hot Encoding - urutan: Lokasi, Kategori, Senioritas
        # Senioritas diisi dengan default untuk kompatibilitas encoder
        df_cat = pd.DataFrame({
            'Lokasi_Clean': [lokasi],
            'Kategori_Pekerjaan': [kategori_pekerjaan],
            'Senioritas': ['Mid-Level/Staff']  # Default value
        })
        X_ohe_full = ohe_encoder.transform(df_cat)
        
        # Drop 3 kolom terakhir (Senioritas) karena model tidak dilatih dengan fitur ini
        # OHE menghasilkan: 11 (Lokasi) + 12 (Kategori) + 3 (Senioritas) = 26
        # Model hanya butuh: 11 (Lokasi) + 12 (Kategori) = 23
        X_ohe = X_ohe_full[:, :-3]  # Ambil semua kecuali 3 kolom terakhir

        # 5. Gabungkan & prediksi
        X_final = hstack([X_word, X_char, target_sparse, extra, X_ohe])
        pred_log = model.predict(X_final)[0]
        return float(np.expm1(pred_log))

    except Exception as e:
        st.error(f"Error prediksi ML: {e}")
        import traceback
        st.error(traceback.format_exc())
        return None

@st.cache_resource
def load_housing_resources():
    """Load pipeline kos yang sudah lengkap"""
    pipeline = joblib.load('models/kos/kos_price_pipeline.pkl')
    return pipeline

def predict_kos_price(region):
    """Prediksi harga kos menggunakan pipeline"""
    pipeline = load_housing_resources()
    
    # Mapping region ke format yang diharapkan model (string, bukan integer)
    kos_region_mapping = {
        'Bekasi': 'Bekasi',
        'Bogor': 'Bogor',
        'Depok': 'Depok',
        'Jakarta Barat': 'Jakarta Barat',
        'Jakarta Pusat': 'Jakarta Pusat',
        'Jakarta Selatan': 'Jakarta Selatan',
        'Jakarta Timur': 'Jakarta Timur',
        'Jakarta Utara': 'Jakarta Utara',
        'Tangerang': 'Tangerang',
        'Tangerang Selatan': 'Tangerang Selatan',
        'Jakarta Raya (General)': 'Jakarta Pusat'  # Default ke Jakarta Pusat
    }
    
    region_val = kos_region_mapping.get(region, 'Jakarta Pusat')
    tipe_kos_val = 'Campur'  # Kos Campur
    electricity_val = 'Ya'   # Termasuk Listrik
    
    try:
        import warnings
        import pandas as pd
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            # Buat DataFrame dengan nama kolom yang sesuai dengan pipeline
            df_kos = pd.DataFrame({
                'region': [region_val],
                'tipe_kos': [tipe_kos_val],
                'is_electricity_included': [electricity_val],
                'rating_clean': [4.5],
                'rating_count_clean': [10],
                'room_area': [12.0]
            })
            prediction = pipeline.predict(df_kos)[0]
        # Kemungkinan model dilatih dengan log-transform, jadi perlu expm1
        import numpy as np
        return int(np.expm1(prediction))
    except Exception as e:
        st.error(f"Error prediksi kos: {e}")
        return 1600000  # Fallback default

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
