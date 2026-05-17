import streamlit as st

from tabs.predict_salary.layout import render_section_gap


def get_salary_zone_status(input_salary: int, res: dict):
    """Tentukan zona negosiasi dari angka gaji yang dimasukkan user."""
    gaji_min = res["gaji_min"]
    gaji_prediksi = res["gaji_prediksi"]
    gaji_max = res["gaji_max"]

    if input_salary < gaji_min:
        return {
            "label": "DI BAWAH KISARAN WAJAR",
            "color": "#e74c3c",
            "bg": "rgba(231,76,60,0.08)",
            "border": "rgba(231,76,60,0.25)",
            "desc": "Angka ini masih berada di bawah kisaran wajar sistem. Sebaiknya pertimbangkan negosiasi agar hasil akhirnya lebih kompetitif.",
            "badge": "LOW",
        }
    if input_salary < gaji_prediksi:
        return {
            "label": "ZONA AMAN",
            "color": "#f1c40f",
            "bg": "rgba(241,196,15,0.08)",
            "border": "rgba(241,196,15,0.25)",
            "desc": "Angka ini masih aman dan realistis, tetapi belum menyentuh titik estimasi terbaik untuk profil Anda.",
            "badge": "SAFE",
        }
    if input_salary <= gaji_max:
        return {
            "label": "ZONA NEGOSIASI IDEAL",
            "color": "#2ecc71",
            "bg": "rgba(46,204,113,0.08)",
            "border": "rgba(46,204,113,0.25)",
            "desc": "Angka ini berada di zona negosiasi yang ideal. Cukup kuat untuk diajukan, namun masih terlihat realistis untuk profil Anda.",
            "badge": "IDEAL",
        }
    return {
        "label": "CUKUP AMBISIUS",
        "color": "#5dade2",
        "bg": "rgba(93,173,226,0.08)",
        "border": "rgba(93,173,226,0.25)",
        "desc": "Angka ini sudah melewati batas atas kisaran wajar. Masih bisa dipakai sebagai target optimistis, tetapi perlu alasan negosiasi yang kuat.",
        "badge": "HIGH",
    }


def render_salary_evaluation(res):
    """Render zona negosiasi gaji untuk membantu pengambilan keputusan."""
    render_section_gap("md")
    st.markdown(
        """
<div class="sec-hd">
    <div class="sec-hd-dot"></div>
    <span class="sec-hd-text">Zona Negosiasi Gaji</span>
    <div class="sec-hd-line"></div>
</div>
<p style="color:rgba(255,255,255,0.38);font-size:0.82rem;margin:-8px 0 16px 0;">
    Masukkan gaji saat ini, offer salary, atau target gaji Anda untuk melihat apakah angka tersebut berada di zona aman, ideal, atau terlalu rendah.
</p>
""",
        unsafe_allow_html=True,
    )

    input_col, button_col = st.columns([2, 1])
    with input_col:
        gaji_juta_input = st.number_input(
            "Masukkan Gaji / Offer / Target (dalam Juta Rp)",
            min_value=0.0,
            max_value=100.0,
            step=0.5,
            value=st.session_state.get("salary_battle_input", 0.0),
            format="%.1f",
            placeholder="Contoh: 7.5 berarti Rp 7.500.000",
            help="Bisa diisi dengan gaji saat ini, offer salary, atau target gaji dalam satuan juta rupiah.",
            key="salary_battle_input",
        )
        gaji_user = int(gaji_juta_input * 1_000_000)
    with button_col:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Evaluasi", type="primary", use_container_width=True)

    if gaji_user <= 0:
        return False

    gaji_min = res["gaji_min"]
    gaji_prediksi = res["gaji_prediksi"]
    gaji_max = res["gaji_max"]
    status = get_salary_zone_status(gaji_user, res)

    range_min = gaji_min * 0.85
    range_max = gaji_max * 1.15
    pct_bar = min(max((gaji_user - range_min) / (range_max - range_min), 0), 1)
    bar_width = int(pct_bar * 100)

    if gaji_user < gaji_min:
        delta_text = f"-Rp {int(gaji_min - gaji_user):,} dari batas bawah"
    elif gaji_user > gaji_max:
        delta_text = f"+Rp {int(gaji_user - gaji_max):,} di atas batas atas"
    else:
        delta_text = "Berada dalam kisaran negosiasi"

    st.markdown(
        f"""
<style>
.sb-card {{
    background: {status['bg']};
    border: 1px solid {status['border']};
    border-radius: 18px;
    padding: 28px;
    margin-top: 8px;
}}
.sb-bar-track {{
    height: 12px;
    background: rgba(255,255,255,0.07);
    border-radius: 6px;
    margin: 6px 0;
    overflow: hidden;
}}
.sb-bar-fill {{
    height: 100%;
    width: {bar_width}%;
    background: linear-gradient(90deg, {status['color']}88, {status['color']});
    border-radius: 6px;
}}
.sb-mini-card {{
    background: rgba(0,0,0,0.2);
    border-radius: 10px;
    padding: 12px 14px;
    flex: 1;
    min-width: 140px;
}}
</style>
<div class="sb-card">
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;flex-wrap:wrap;">
        <div>
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:1px;">Zona Gaji Anda</p>
            <p style="margin:4px 0 0 0;font-size:1.4rem;font-weight:800;color:{status['color']};">{status['label']}</p>
        </div>
        <div style="margin-left:auto;text-align:right;">
            <p style="margin:0 0 4px 0;font-size:11px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:0.5px;">Posisi Angka</p>
            <p style="margin:0;font-size:1.1rem;font-weight:700;color:{status['color']};">{delta_text}</p>
        </div>
    </div>
    <div style="margin-bottom:20px;">
        <div style="display:flex;justify-content:space-between;">
            <span style="font-size:12px;color:rgba(255,255,255,0.4);">Rp {int(range_min):,}</span>
            <span style="font-size:12px;color:rgba(255,255,255,0.4);">Rp {int(range_max):,}</span>
        </div>
        <div class="sb-bar-track">
            <div class="sb-bar-fill"></div>
        </div>
        <div style="display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;">
            <span style="font-size:11px;color:rgba(255,255,255,0.3);">Min Wajar: Rp {int(gaji_min):,}</span>
            <span style="font-size:11px;color:rgba(255,255,255,0.45);">Estimasi: Rp {int(gaji_prediksi):,}</span>
            <span style="font-size:11px;color:rgba(255,255,255,0.3);">Max Nego: Rp {int(gaji_max):,}</span>
        </div>
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:18px;">
        <div class="sb-mini-card">
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.5px;">Angka Anda</p>
            <p style="margin:4px 0 0 0;font-size:1rem;font-weight:700;color:#fff;">Rp {gaji_user:,}</p>
        </div>
        <div class="sb-mini-card">
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.5px;">Estimasi Wajar</p>
            <p style="margin:4px 0 0 0;font-size:1rem;font-weight:700;color:rgba(255,255,255,0.7);">Rp {int(gaji_prediksi):,}</p>
        </div>
        <div class="sb-mini-card">
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.5px;">Target Negosiasi</p>
            <p style="margin:4px 0 0 0;font-size:1rem;font-weight:700;color:#5dade2;">Rp {gaji_max:,}</p>
        </div>
    </div>
    <div style="border-top:1px solid rgba(255,255,255,0.07);padding-top:14px;font-size:13px;color:rgba(255,255,255,0.55);line-height:1.6;">
        {status['desc']}
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    return True
