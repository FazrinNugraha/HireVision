import streamlit as st


def inject_css():
    """Inject CSS khusus untuk styling input & expander di tab ini."""
    st.markdown(
        """
<style>
div[data-baseweb="input"], div[data-baseweb="select"] {
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    background-color: rgba(255, 255, 255, 0.02) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
div[data-baseweb="input"]:hover, div[data-baseweb="select"]:hover {
    border-color: rgba(255, 255, 255, 0.25) !important;
    background-color: rgba(255, 255, 255, 0.04) !important;
}
div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {
    border-color: #5dade2 !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
    box-shadow: 0 0 12px rgba(93, 173, 226, 0.15) !important;
}
.stExpander {
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 12px !important;
    background: rgba(255, 255, 255, 0.01) !important;
}
div[data-testid="stExpander"]:has(.marker-dropdown-list) div[data-testid="stExpanderDetails"] {
    max-height: 180px;
    overflow-y: auto;
    padding-top: 0 !important;
}
div[data-testid="stExpander"]:has(.marker-dropdown-list) div[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}
div[data-testid="stExpander"]:has(.marker-dropdown-list) button[kind="secondary"] {
    background-color: transparent !important;
    border: none !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 0 !important;
    justify-content: flex-start !important;
    padding: 6px 4px !important;
    width: 100% !important;
    box-shadow: none !important;
    min-height: 0 !important;
    height: auto !important;
}
div[data-testid="stExpander"]:has(.marker-dropdown-list) button[kind="secondary"]:hover {
    background-color: rgba(255, 255, 255, 0.03) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
}
div[data-testid="stExpander"]:has(.marker-dropdown-list) button[kind="secondary"] div[data-testid="stMarkdownContainer"] {
    width: 100% !important;
}
div[data-testid="stExpander"]:has(.marker-dropdown-list) button[kind="secondary"] p {
    color: rgba(255, 255, 255, 0.9) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    text-align: left !important;
    margin: 0 !important;
    width: 100% !important;
}
div[data-testid="stExpander"]:has(.marker-dropdown-list) button[kind="secondary"]:hover p {
    color: #5dade2 !important;
}
@media (max-width: 768px) {
    div[data-baseweb="input"], div[data-baseweb="select"] {
        border-radius: 9px !important;
    }
    div[data-testid="stExpander"]:has(.marker-dropdown-list) div[data-testid="stExpanderDetails"] {
        max-height: 220px;
    }
    div[data-testid="stExpander"]:has(.marker-dropdown-list) button[kind="secondary"] {
        padding: 9px 4px !important;
    }
    div[data-testid="stExpander"]:has(.marker-dropdown-list) button[kind="secondary"] p {
        font-size: 12.5px !important;
        line-height: 1.35 !important;
    }
}
</style>
""",
        unsafe_allow_html=True,
    )


def render_header():
    """Render judul utama + deskripsi tab."""
    st.markdown(
        """
<div style="margin-bottom:6px;">
    <h2 style="font-size:1.55rem;font-weight:800;color:#fff;margin:0 0 6px 0;">
        Market Salary Estimator
    </h2>
    <p style="color:rgba(255,255,255,0.45);font-size:0.9rem;margin:0;">
        Dapatkan proyeksi gaji yang lebih terukur dari model prediksi yang optimal dengan individual adjusment factor yang membaca pengaruh pengalaman, pendidikan, dan sertifikasi profesional.
    </p>
</div>
<hr style="border:none;border-top:1px solid rgba(255,255,255,0.07);margin:18px 0 24px 0;">
""",
        unsafe_allow_html=True,
    )


def render_section_header(emoji_text: str):
    """Helper untuk render section header dengan dot + line decoratif."""
    st.markdown(
        f"""
<div class="sec-hd">
    <div class="sec-hd-dot"></div>
    <span class="sec-hd-text">{emoji_text}</span>
    <div class="sec-hd-line"></div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_section_gap(size="md"):
    """Helper untuk memberi jarak vertikal yang konsisten antar fitur."""
    gap_map = {
        "sm": "12px",
        "md": "20px",
        "lg": "30px",
    }
    height = gap_map.get(size, gap_map["md"])
    st.markdown(
        f"<div style='height:{height};'></div>",
        unsafe_allow_html=True,
    )
