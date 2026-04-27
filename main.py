import streamlit as st
from tabs import predict_salary, spatial_map, ai_consultant

st.set_page_config(
    page_title="HireMap — Jabodetabek Career Navigator",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════
#  MASTER CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* BACKGROUND */
.stApp { background: linear-gradient(160deg, #08080f 0%, #0f0a1a 60%, #080810 100%); }

/* HIDE DEFAULT CHROME */
#MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { visibility: hidden; height: 0; }
footer { visibility: hidden; }

/* CONTENT WIDTH */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1120px !important;
}

/* ── HERO ── */
.hero-container {
    padding: 10px 0 30px 0;
    margin-bottom: 24px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.hero-badge {
    display: inline-block;
    color: #FF416C;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
}
.hero-title {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin: 0 0 12px 0 !important;
    letter-spacing: -1.5px !important;
    line-height: 1 !important;
}
.hero-subtitle {
    font-size: 1.1rem !important;
    color: rgba(255,255,255,0.55) !important;
    margin: 0 0 28px 0 !important;
    line-height: 1.6 !important;
    max-width: 700px;
}
.hero-stats { 
    display: flex; 
    gap: 40px; 
    flex-wrap: wrap; 
}
.hero-stat-num {
    font-size: 1.3rem;
    font-weight: 700;
    color: #FF416C;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 3px;
}
.hero-stat-label {
    font-size: 14px;
    color: rgba(255,255,255,0.7);
    font-weight: 500;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 14px !important;
    padding: 5px !important; gap: 4px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    margin-bottom: 8px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 500 !important; font-size: 14px !important;
    color: rgba(255,255,255,0.4) !important;
    background: transparent !important; border: none !important;
    transition: all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: rgba(255,255,255,0.75) !important;
    background: rgba(255,255,255,0.05) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF416C, #FF4B2B) !important;
    color: white !important; font-weight: 600 !important;
    box-shadow: 0 4px 18px rgba(255,65,108,0.4) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── SECTION HEADER ── */
.sec-hd {
    display: flex; align-items: center; gap: 10px; margin-bottom: 16px;
}
.sec-hd-dot {
    width: 8px; height: 8px;
    background: linear-gradient(135deg, #FF416C, #FF4B2B);
    border-radius: 50%; flex-shrink: 0;
}
.sec-hd-text { font-size: 1rem; font-weight: 600; color: rgba(255,255,255,0.85); margin: 0; }
.sec-hd-line { flex: 1; height: 1px; background: rgba(255,255,255,0.07); }

/* ── METRIC CARDS ── */
.metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px; padding: 22px 20px;
    color: white; text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    border-color: rgba(255,255,255,0.15);
}
.metric-card-highlight {
    background: linear-gradient(135deg, rgba(255,65,108,0.12), rgba(255,75,43,0.06));
    border: 1px solid rgba(255,65,108,0.32);
    border-radius: 16px; padding: 22px 20px;
    color: white; text-align: center;
}

/* ── KOMUTER CARDS ── */
.komuter-card {
    background: linear-gradient(135deg, rgba(46,204,113,0.07), rgba(39,174,96,0.03));
    border: 1px solid rgba(46,204,113,0.22);
    border-radius: 14px; padding: 20px 18px;
    margin-bottom: 12px;
}

/* ── INPUTS ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}

/* ── BUTTON ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #FF416C, #FF4B2B) !important;
    border: none !important; border-radius: 12px !important;
    font-weight: 600 !important; font-size: 15px !important;
    padding: 14px 0 !important;
    box-shadow: 0 4px 20px rgba(255,65,108,0.3) !important;
    transition: all 0.25s ease !important; letter-spacing: 0.3px !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 8px 30px rgba(255,65,108,0.5) !important;
    transform: translateY(-2px) !important;
}

/* ── HR ── */
hr { border: none !important; border-top: 1px solid rgba(255,255,255,0.07) !important; margin: 24px 0 !important; }

/* ── ALERTS ── */
[data-testid="stAlert"] { border-radius: 12px !important; }

/* ── EXPANDER ── */
details summary { border-radius: 10px !important; font-weight: 500 !important; }

/* ── CHAT ── */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important; margin-bottom: 8px !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,65,108,0.35); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,65,108,0.55); }

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
    .hero-title { font-size: 2.2rem !important; }
    .hero-subtitle { font-size: 1rem !important; }
    .hero-stats { gap: 20px; }
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    .metric-card, .metric-card-highlight { padding: 18px 14px; }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  HERO SECTION
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">Jabodetabek Career Intelligence</div>
    <p class="hero-title">HireVision</p>
    <p class="hero-subtitle">
        Temukan estimasi gaji pasar yang akurat, eksplorasi peluang kerja di 13 wilayah Jabodetabek,
        dan dapatkan strategi karir personal dari AI — semua dalam satu platform berbasis data nyata.
    </p>
    <div class="hero-stats">
        <div>
            <div class="hero-stat-num">01</div>
            <div class="hero-stat-label">Prediksi Gaji & Biaya Hidup</div>
        </div>
        <div>
            <div class="hero-stat-num">02</div>
            <div class="hero-stat-label">Peta Lowongan Jabodetabek</div>
        </div>
        <div>
            <div class="hero-stat-num">03</div>
            <div class="hero-stat-label">Konsultan Karir Berbasis AI</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  NAVIGASI TABS
# ══════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["💰  Predict Salary", "🗺️  Spatial Job Map", "🤖  AI Consultant"])

with tab1:
    predict_salary.render()

with tab2:
    spatial_map.render()

with tab3:
    ai_consultant.render()
