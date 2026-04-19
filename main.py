import streamlit as st

# Mengimpor modul tabs yang sudah kita buat
from tabs import predict_salary, spatial_map, ai_consultant

# Mengatur Konfigurasi Dasar Tampilan Web
st.set_page_config(
    page_title="Jabodetabek Career Navigator",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kustomisasi CSS untuk UI Vibrant
st.markdown("""
<style>
    .big-title {
        font-size: 3rem !important;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: -10px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #7f8c8d;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #2c3e50;
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Judul Header Web
st.markdown('<p class="big-title">Jabodetabek Career Navigator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Empowering Job Seekers with Data-Driven Insights and AI Strategy</p>', unsafe_allow_html=True)

# Menyiapkan 3 Tab Navigasi Utama
tab1, tab2, tab3 = st.tabs(["💰 Predict Salary", "🗺️ Spatial Job Map", "🤖 AI Consultant"])

# -------------------------------------------------------------
# TAB 1: PREDIKSI GAJI (MACHINE LEARNING)
# -------------------------------------------------------------
with tab1:
    predict_salary.render()

# -------------------------------------------------------------
# TAB 2: PETA SPASIAL → VISUALISASI CHART INTERAKTIF
# -------------------------------------------------------------
with tab2:
    spatial_map.render()

# -------------------------------------------------------------
# TAB 3: KONSULTAN KARIR AI (GROQ LLAMA-3)
# -------------------------------------------------------------
with tab3:
    ai_consultant.render()
