"""
Tab Prediksi Gaji - HireVision
================================
Modul ini bertanggung jawab untuk:
1. Menerima input user (judul, kategori, lokasi, faktor MAF)
2. Menjalankan prediksi gaji via Random Forest
3. Menampilkan hasil estimasi + Salary Battle
4. Menampilkan analisis keterjangkauan hunian & strategi komuter

Struktur fungsi (urut sesuai alur UI):
- _inject_css()                  : CSS khusus tab ini
- _render_header()               : Judul tab
- _render_input_parameter(...)   : Input judul + kategori + lokasi
- _render_input_maf()            : Input pengalaman + pendidikan + sertifikasi
- _run_prediction(...)           : Jalankan model + simpan ke session state
- _render_hasil_card(res)        : Kartu utama estimasi gaji
- _render_rincian_kalkulasi(res) : Expander breakdown multiplier
- _render_salary_battle(res)     : Fitur perbandingan gaji user vs pasar
- _render_cta_ai_consultant()    : Banner ajakan ke AI Consultant
- _render_analisis_hunian(res)   : Biaya kos & rasio gaji
- _render_strategi_komuter(res)  : Opsi kos di wilayah penyangga
- render()                       : Entry point (orkestrasi)
"""

import streamlit as st
import pandas as pd
from utils import (
    load_ml_resources,
    predict_salary,
    predict_kos_price,
    load_map_data,
    calculate_distance,
)

# ══════════════════════════════════════════════════════════════
#  KONSTANTA MAF (Multiplier Adjustment Factor)
# ══════════════════════════════════════════════════════════════
PENGALAMAN_MAP = {
    "🎓 Fresh Graduate (0-1 thn)": {"m_pengalaman": 0.80, "label": "Fresh Grad"},
    "📈 Junior (1-3 thn)": {"m_pengalaman": 0.95, "label": "Junior"},
    "💼 Mid-Level (3-5 thn)": {"m_pengalaman": 1.10, "label": "Mid-Level"},
    "🏆 Senior (5+ thn)": {"m_pengalaman": 1.20, "label": "Senior"},
}

PENDIDIKAN_MAP = {
    "🎓 SMA / SMK": {"m_pendidikan": 0.75, "label": "SMA/SMK"},
    "🏅 Diploma (D3/D4)": {"m_pendidikan": 0.90, "label": "Diploma"},
    "🎓 S1 / Sarjana": {"m_pendidikan": 1.00, "label": "S1/Sarjana"},
    "🎖️ S2 / Magister ke atas": {"m_pendidikan": 1.10, "label": "S2+"},
}

SERTIFIKAT_MAP = {
    "📄 Tanpa Sertifikasi": {"m_sertifikat": 1.00, "label": "None"},
    "🏅 Sertifikat BNSP / Lokal": {"m_sertifikat": 1.03, "label": "Lokal/BNSP"},
    "🎖️ Sertifikat Associate (Intl)": {"m_sertifikat": 1.05, "label": "Associate"},
    "🏆 Sertifikat Expert (Intl)": {"m_sertifikat": 1.10, "label": "Expert"},
}

GENERIC_TITLE_TERMS = {
    "staff",
    "admin",
    "administrasi",
    "administrator",
    "assistant",
    "operator",
    "clerk",
    "crew",
    "helper",
    "support",
    "generalist",
    "general",
}

GENERIC_CATEGORY_KEYWORDS = {
    "Administrative & Customer Service": {"staff", "admin", "administrasi", "assistant"},
    "HR & General Affairs": {"staff", "admin", "assistant", "generalist"},
    "Retail, F&B & Hospitality": {"crew", "staff", "helper"},
    "Logistics & Supply Chain": {"staff", "operator", "helper", "admin"},
}

NON_PRIME_LOCATIONS = {"Bogor", "Depok", "Bekasi", "Tangerang", "Tangerang Selatan"}


# ══════════════════════════════════════════════════════════════
#  CSS & HEADER
# ══════════════════════════════════════════════════════════════
def _inject_css():
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
</style>
""",
        unsafe_allow_html=True,
    )


def _render_header():
    """Render judul utama + deskripsi tab."""
    st.markdown(
        """
<div style="margin-bottom:6px;">
    <h2 style="font-size:1.55rem;font-weight:800;color:#fff;margin:0 0 6px 0;">
        Kalkulator Estimasi Gaji Pasar
    </h2>
    <p style="color:rgba(255,255,255,0.45);font-size:0.9rem;margin:0;">
        Estimasi gaji berbasis AI dengan proyeksi inflasi masa depan, latar belakang pendidikan, dan sertifikasi profesional.
    </p>
</div>
<hr style="border:none;border-top:1px solid rgba(255,255,255,0.07);margin:18px 0 24px 0;">
""",
        unsafe_allow_html=True,
    )


def _section_header(emoji_text: str):
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


def _tokenize_title(judul: str) -> list[str]:
    """Normalisasi judul pekerjaan menjadi token sederhana."""
    cleaned = (
        judul.lower()
        .replace("/", " ")
        .replace("-", " ")
        .replace(",", " ")
        .replace(".", " ")
    )
    return [token for token in cleaned.split() if token]


def _analyze_title_ambiguity(judul: str, kategori: str, lokasi: str) -> dict:
    """Deteksi judul generik agar hasil bisa dibuat lebih konservatif."""
    tokens = _tokenize_title(judul)
    token_count = len(tokens)
    generic_matches = [token for token in tokens if token in GENERIC_TITLE_TERMS]
    category_matches = [
        token
        for token in tokens
        if token in GENERIC_CATEGORY_KEYWORDS.get(kategori, set())
    ]

    is_single_generic = token_count == 1 and len(generic_matches) == 1
    is_short_generic = token_count <= 2 and len(generic_matches) >= 1
    is_ambiguous = is_single_generic or is_short_generic or (
        token_count <= 2 and len(category_matches) >= 1
    )

    title_correction = 1.0
    confidence_label = "Tinggi"

    if is_single_generic:
        title_correction *= 0.84
        confidence_label = "Rendah"
    elif is_short_generic:
        title_correction *= 0.90
        confidence_label = "Sedang"
    elif len(generic_matches) >= 1:
        title_correction *= 0.95
        confidence_label = "Sedang"

    if is_ambiguous and lokasi in NON_PRIME_LOCATIONS:
        title_correction *= 0.97

    if is_ambiguous and kategori == "Administrative & Customer Service":
        title_correction *= 0.97

    notes = []
    if is_single_generic:
        notes.append(
            "Judul pekerjaan sangat umum, sehingga sistem menerapkan koreksi realistis."
        )
    elif is_short_generic:
        notes.append(
            "Judul masih cukup generik, sehingga estimasi dibuat lebih konservatif."
        )

    if is_ambiguous:
        notes.append(
            "Coba judul yang lebih spesifik seperti 'Admin Finance', 'HR Staff', atau 'Customer Service Staff' untuk akurasi yang lebih baik."
        )

    return {
        "is_ambiguous": is_ambiguous,
        "generic_matches": generic_matches,
        "title_correction": round(title_correction, 4),
        "confidence_label": confidence_label,
        "notes": notes,
    }


def _get_profile_adjustment(peng: str, pend: str, sert: str, kategori: str) -> dict:
    """Hitung multiplier personal yang lebih defensif untuk entry-level."""
    m_peng = PENGALAMAN_MAP[peng]["m_pengalaman"]
    m_pend = PENDIDIKAN_MAP[pend]["m_pendidikan"]
    m_sert = SERTIFIKAT_MAP[sert]["m_sertifikat"]

    realism_correction = 1.0
    notes = []

    if "Fresh Graduate" in peng:
        realism_correction *= 0.97
        notes.append("Fresh graduate diberi penyesuaian ekstra agar hasil lebih realistis.")

        if kategori in {
            "Administrative & Customer Service",
            "HR & General Affairs",
            "Retail, F&B & Hospitality",
        }:
            realism_correction *= 0.97
            notes.append(
                "Role entry-level umum di kategori ini dibuat lebih konservatif."
            )

    elif "Junior" in peng and kategori in {
        "Administrative & Customer Service",
        "HR & General Affairs",
    }:
        realism_correction *= 0.98

    total_multiplier = m_peng * m_pend * m_sert * realism_correction
    return {
        "m_pengalaman": m_peng,
        "m_pendidikan": m_pend,
        "m_sertifikat": m_sert,
        "realism_correction": round(realism_correction, 4),
        "total_multiplier": round(total_multiplier, 4),
        "notes": notes,
    }


# ══════════════════════════════════════════════════════════════
#  FORM INPUT
# ══════════════════════════════════════════════════════════════
def _render_input_parameter(list_kategori, list_lokasi):
    """
    Render baris input utama: Judul, Kategori, Lokasi.
    Returns: (pilihan_judul, pilihan_kategori, pilihan_lokasi)
    """
    _section_header("🎯 Parameter Utama")

    col1, col2, col3 = st.columns(3)

    # ── Judul Pekerjaan ──
    with col1:
        st.markdown(
            "<p style='font-size:14px;font-weight:600;margin-bottom:8px;color:rgba(255,255,255,0.9);'>Judul / Posisi Pekerjaan</p>",
            unsafe_allow_html=True,
        )
        pilihan_judul = st.text_input(
            "Judul / Posisi Pekerjaan",
            label_visibility="collapsed",
            placeholder="Contoh: Senior Data Scientist...",
            help="Ketik jabatan pekerjaan yang ingin diprediksi gajinya. Semakin spesifik semakin akurat.",
        )

    # ── Kategori Pekerjaan ──
    with col2:
        st.markdown(
            "<p style='font-size:14px;font-weight:600;margin-bottom:8px;color:rgba(255,255,255,0.9);'>Kategori Pekerjaan</p>",
            unsafe_allow_html=True,
        )

        def _update_kategori(kategori_baru):
            st.session_state.kategori_terpilih = kategori_baru

        if "kategori_terpilih" not in st.session_state:
            st.session_state.kategori_terpilih = list_kategori[6]

        pilihan_kategori = st.session_state.kategori_terpilih

        with st.expander(f"💼 {st.session_state.kategori_terpilih}"):
            st.markdown(
                "<div class='marker-dropdown-list'></div>", unsafe_allow_html=True
            )
            for kat in list_kategori:
                st.button(
                    kat,
                    key=f"btn_kat_{kat}",
                    use_container_width=True,
                    on_click=_update_kategori,
                    args=(kat,),
                )

    # ── Lokasi Penempatan ──
    with col3:
        st.markdown(
            "<p style='font-size:14px;font-weight:600;margin-bottom:8px;color:rgba(255,255,255,0.9);'>Lokasi Penempatan</p>",
            unsafe_allow_html=True,
        )

        def _update_lokasi(lokasi_baru):
            st.session_state.lokasi_terpilih = lokasi_baru

        if "lokasi_terpilih" not in st.session_state:
            st.session_state.lokasi_terpilih = (
                "Jakarta Selatan"
                if "Jakarta Selatan" in list_lokasi
                else list_lokasi[0]
            )

        pilihan_lokasi = st.session_state.lokasi_terpilih

        with st.expander(f"📍 {st.session_state.lokasi_terpilih}"):
            st.markdown(
                "<div class='marker-dropdown-list'></div>", unsafe_allow_html=True
            )
            for loc in list_lokasi:
                st.button(
                    loc,
                    key=f"btn_loc_{loc}",
                    use_container_width=True,
                    on_click=_update_lokasi,
                    args=(loc,),
                )

    return pilihan_judul, pilihan_kategori, pilihan_lokasi


def _render_input_maf():
    """
    Render input faktor MAF: Pengalaman, Pendidikan, Sertifikasi.
    Returns: (pilihan_pengalaman, pilihan_pendidikan, pilihan_sertifikat)
    """
    st.markdown(
        """
<div class="sec-hd">
    <div class="sec-hd-dot"></div>
    <span class="sec-hd-text">⚙️ Penyesuaian Realistis & Proyeksi Karir</span>
    <div class="sec-hd-line"></div>
</div>
<p style="color:rgba(255,255,255,0.45);font-size:0.85rem;line-height:1.6;margin:-8px 0 20px 0;">
    Optimalkan estimasi gaji Anda dengan menyesuaikan faktor kunci keberhasilan karir: Level Pengalaman kerja,
    Sertifikasi Profesional untuk nilai tambah keahlian, dan Pendidikan Terakhir.
</p>
""",
        unsafe_allow_html=True,
    )

    cola, colb, colc = st.columns(3)
    with cola:
        pilihan_pengalaman = st.selectbox(
            "Level Pengalaman", list(PENGALAMAN_MAP.keys()), index=2
        )
    with colb:
        pilihan_pendidikan = st.selectbox(
            "Pendidikan Terakhir", list(PENDIDIKAN_MAP.keys()), index=2
        )
    with colc:
        pilihan_sertifikat = st.selectbox(
            "Sertifikasi Profesional", list(SERTIFIKAT_MAP.keys()), index=0
        )

    return pilihan_pengalaman, pilihan_pendidikan, pilihan_sertifikat


# ══════════════════════════════════════════════════════════════
#  PREDICTION LOGIC
# ══════════════════════════════════════════════════════════════
def _run_prediction(judul, kategori, lokasi, peng, pend, sert, resources):
    """
    Jalankan pipeline ML + apply MAF, simpan hasil ke session_state['last_prediction'].
    """
    if not judul.strip():
        st.warning("⚠️ Mohon isi Judul Pekerjaan terlebih dahulu.")
        return

    with st.spinner("Memproses Random Forest + penyesuaian profil..."):
        hasil_basis = predict_salary(
            judul_pekerjaan=judul.strip(),
            kategori_pekerjaan=kategori,
            lokasi=lokasi,
            resources=resources,
        )

        if hasil_basis is None:
            st.error("Terjadi masalah saat membaca output model ML.")
            return

        title_meta = _analyze_title_ambiguity(judul.strip(), kategori, lokasi)
        profile_meta = _get_profile_adjustment(peng, pend, sert, kategori)

        title_correction = title_meta["title_correction"]
        total_multiplier = profile_meta["total_multiplier"]
        gaji_setelah_koreksi_judul = hasil_basis * title_correction
        gaji_akhir = int(gaji_setelah_koreksi_judul * total_multiplier)

        estimasi_kos = predict_kos_price(lokasi)
        rasio_kos = (estimasi_kos / gaji_akhir) * 100

        st.session_state["last_prediction"] = {
            "judul": judul.strip(),
            "kategori": kategori,
            "lokasi": lokasi,
            "pengalaman": PENGALAMAN_MAP[peng]["label"],
            "pendidikan": PENDIDIKAN_MAP[pend]["label"],
            "sertifikasi": SERTIFIKAT_MAP[sert]["label"],
            "gaji_basis": int(hasil_basis),
            "gaji_setelah_koreksi_judul": int(gaji_setelah_koreksi_judul),
            "gaji_prediksi": gaji_akhir,
            "gaji_min": int(gaji_akhir * 0.90),
            "gaji_max": int(gaji_akhir * 1.10),
            "multiplier": round(total_multiplier, 2),
            "m_pengalaman": profile_meta["m_pengalaman"],
            "m_pendidikan": profile_meta["m_pendidikan"],
            "m_sertifikat": profile_meta["m_sertifikat"],
            "m_koreksi_realistis": profile_meta["realism_correction"],
            "m_koreksi_judul": title_correction,
            "is_ambiguous_title": title_meta["is_ambiguous"],
            "generic_tokens": title_meta["generic_matches"],
            "confidence_label": title_meta["confidence_label"],
            "adjustment_notes": title_meta["notes"] + profile_meta["notes"],
            "estimasi_kos": estimasi_kos,
            "rasio_kos": rasio_kos,
        }

        # Reset chat history saat ada prediksi baru
        if "messages" in st.session_state:
            del st.session_state["messages"]


# ══════════════════════════════════════════════════════════════
#  HASIL: KARTU UTAMA & RINCIAN
# ══════════════════════════════════════════════════════════════
def _get_warna_rasio_kos(rasio):
    """Tentukan skema warna berdasarkan rasio biaya kos vs gaji."""
    if rasio <= 30:
        return {
            "bg": "linear-gradient(135deg, rgba(46,204,113,0.12), rgba(39,174,96,0.06))",
            "border": "rgba(46,204,113,0.32)",
            "title": "rgba(180,255,180,0.7)",
            "val": "#2ecc71",
        }
    if rasio <= 50:
        return {
            "bg": "linear-gradient(135deg, rgba(241,196,15,0.12), rgba(243,156,18,0.06))",
            "border": "rgba(241,196,15,0.32)",
            "title": "rgba(255,230,180,0.7)",
            "val": "#f1c40f",
        }
    return {
        "bg": "linear-gradient(135deg, rgba(231,76,60,0.12), rgba(192,57,43,0.06))",
        "border": "rgba(231,76,60,0.32)",
        "title": "rgba(255,180,180,0.7)",
        "val": "#e74c3c",
    }


def _render_hasil_card(res):
    """Render kartu utama estimasi gaji (dengan MAF)."""
    _section_header("📊 Hasil Estimasi Gaji")
    warna = _get_warna_rasio_kos(res["rasio_kos"])

    st.markdown(
        f"""
<div style="background:{warna['bg']};border:1px solid {warna['border']};border-radius:20px;padding:32px 36px;text-align:center;margin-bottom:16px;">
    <p style="margin:0 0 6px 0;color:{warna['title']};font-size:13px;font-weight:700;letter-spacing:1px;text-transform:uppercase;">✨ Estimasi Gaji Anda</p>
    <h1 style="margin:0 0 8px 0;color:{warna['val']};font-size:2.8rem;font-weight:800;letter-spacing:-1px;">Rp {res['gaji_prediksi']:,}</h1>
</div>""",
        unsafe_allow_html=True,
    )
    st.caption(
        "Catatan: Estimasi ini dihasilkan oleh sistem berbasis Decision Support System (DSS) "
        "yang menggabungkan model prediksi dan penyesuaian realistis. Nilai yang ditampilkan "
        "bersifat estimasi pendukung keputusan, sehingga tidak selalu sama dengan angka final "
        "yang ditawarkan oleh setiap perusahaan."
    )


def _render_rincian_kalkulasi(res):
    """Render expander berisi tabel breakdown multiplier MAF."""
    with st.expander("📋 Lihat Rincian Kalkulasi Multiplier"):
        df = pd.DataFrame(
            {
                "Faktor": [
                    "Jabatan",
                    "Kategori",
                    "Lokasi",
                    "Koreksi Judul Generik",
                    "Level Pengalaman",
                    "Pendidikan Terakhir",
                    "Sertifikasi",
                    "Koreksi Personal",
                    "Total Gabungan",
                    "Gaji Basis ML",
                    "Setelah Koreksi Judul",
                    "Hasil Akhir",
                ],
                "Pilihan": [
                    res["judul"],
                    res["kategori"],
                    res["lokasi"],
                    res.get("confidence_label", "Tinggi"),
                    res["pengalaman"],
                    res["pendidikan"],
                    res["sertifikasi"],
                    "Realism Layer",
                    "—",
                    f"Rp {res['gaji_basis']:,}",
                    f"Rp {res['gaji_setelah_koreksi_judul']:,}",
                    f"Rp {res['gaji_prediksi']:,}",
                ],
                "Multiplier": [
                    "—",
                    "—",
                    "—",
                    f"×{res.get('m_koreksi_judul', 1.0)}",
                    f"×{res['m_pengalaman']}",
                    f"×{res['m_pendidikan']}",
                    f"×{res['m_sertifikat']}",
                    f"×{res.get('m_koreksi_realistis', 1.0)}",
                    f"×{res['multiplier']}",
                    "",
                    "",
                    "",
                ],
            }
        ).set_index("Faktor")
        st.table(df)
        st.caption(
            "_Multiplier pengalaman berdasarkan standar industri. Multiplier pendidikan bersumber dari BPS Sakernas 2023._"
        )
        for note in res.get("adjustment_notes", []):
            st.caption(f"• {note}")


# ══════════════════════════════════════════════════════════════
#  SALARY BATTLE
# ══════════════════════════════════════════════════════════════
def _get_status_battle(persen):
    """Tentukan label + warna + deskripsi status gaji user vs pasar."""
    if persen >= 15:
        return {
            "label": "OVERPAID 🤑",
            "color": "#2ecc71",
            "bg": "rgba(46,204,113,0.08)",
            "border": "rgba(46,204,113,0.25)",
            "desc": f"Gaji Anda <b>{abs(persen):.1f}%</b> di atas rata-rata pasar. Posisi Anda sangat kompetitif!",
            "emoji": "🏆",
        }
    if persen >= 0:
        return {
            "label": "SESUAI PASAR ✅",
            "color": "#5dade2",
            "bg": "rgba(93,173,226,0.08)",
            "border": "rgba(93,173,226,0.25)",
            "desc": f"Gaji Anda <b>{abs(persen):.1f}%</b> di atas rata-rata. Sudah sesuai standar pasar!",
            "emoji": "👍",
        }
    if persen >= -15:
        return {
            "label": "SEDIKIT DI BAWAH ⚠️",
            "color": "#f1c40f",
            "bg": "rgba(241,196,15,0.08)",
            "border": "rgba(241,196,15,0.25)",
            "desc": f"Gaji Anda <b>{abs(persen):.1f}%</b> di bawah rata-rata. Ada ruang untuk negosiasi!",
            "emoji": "📊",
        }
    return {
        "label": "UNDERPAID 😱",
        "color": "#e74c3c",
        "bg": "rgba(231,76,60,0.08)",
        "border": "rgba(231,76,60,0.25)",
        "desc": f"Gaji Anda <b>{abs(persen):.1f}%</b> di bawah rata-rata pasar. Saatnya nego atau cari peluang baru!",
        "emoji": "🚨",
    }


def _render_salary_battle(res):
    """
    Render fitur Salary Battle.
    Input: gaji user dalam juta Rp.
    Output: status, progress bar, mini-cards, deskripsi.
    Returns: bool (True jika user sudah input gaji > 0)
    """
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
<div class="sec-hd">
    <div class="sec-hd-dot"></div>
    <span class="sec-hd-text">⚔️ Salary Battle — Gaji Anda vs Pasar</span>
    <div class="sec-hd-line"></div>
</div>
<p style="color:rgba(255,255,255,0.38);font-size:0.82rem;margin:-8px 0 16px 0;">
    Masukkan gaji Anda saat ini atau target gaji, lalu lihat posisi Anda dibanding rata-rata pasar untuk posisi ini.
</p>
""",
        unsafe_allow_html=True,
    )

    sb_col1, sb_col2 = st.columns([2, 1])
    with sb_col1:
        gaji_juta_input = st.number_input(
            "Masukkan Gaji Anda (dalam Juta Rp)",
            min_value=0.0,
            max_value=100.0,
            step=0.5,
            value=st.session_state.get("salary_battle_input", 0.0),
            format="%.1f",
            placeholder="Contoh: 7.5 berarti Rp 7.500.000",
            help="Masukkan gaji dalam satuan juta. Contoh: 7.5 = Rp 7.500.000",
            key="salary_battle_input",
        )
        gaji_user = int(gaji_juta_input * 1_000_000)
    with sb_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("⚔️ Bandingkan!", type="primary", use_container_width=True)

    if gaji_user <= 0:
        return False

    # ── Kalkulasi perbandingan ──
    gaji_pasar = res["gaji_basis"]  # rata-rata pasar = output mentah model (tanpa MAF)
    selisih = gaji_user - gaji_pasar
    persen = (selisih / gaji_pasar) * 100
    status = _get_status_battle(persen)

    # Progress bar: posisi gaji user relatif terhadap range 50%-150% gaji_pasar
    range_min = gaji_pasar * 0.5
    range_max = gaji_pasar * 1.5
    pct_bar = min(max((gaji_user - range_min) / (range_max - range_min), 0), 1)
    bar_width = int(pct_bar * 100)

    tanda = "+" if selisih >= 0 else "-"
    selisih_display = f"{tanda}Rp {abs(int(selisih)):,}"

    # CSS + HTML (CSS di <style> agar tidak di-sanitize Streamlit)
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
        <div style="font-size:2.2rem;">{status['emoji']}</div>
        <div>
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:1px;">Status Gaji Anda</p>
            <p style="margin:4px 0 0 0;font-size:1.4rem;font-weight:800;color:{status['color']};">{status['label']}</p>
        </div>
        <div style="margin-left:auto;text-align:right;">
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:0.5px;">Selisih vs Pasar</p>
            <p style="margin:4px 0 0 0;font-size:1.3rem;font-weight:700;color:{status['color']};">{selisih_display}</p>
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
        <div style="display:flex;justify-content:space-between;">
            <span style="font-size:11px;color:rgba(255,255,255,0.3);">Batas Bawah</span>
            <span style="font-size:11px;color:rgba(255,255,255,0.45);">📍 Rata-rata pasar: Rp {int(gaji_pasar):,}</span>
            <span style="font-size:11px;color:rgba(255,255,255,0.3);">Batas Atas</span>
        </div>
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:18px;">
        <div class="sb-mini-card">
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.5px;">Gaji Anda</p>
            <p style="margin:4px 0 0 0;font-size:1rem;font-weight:700;color:#fff;">Rp {gaji_user:,}</p>
        </div>
        <div class="sb-mini-card">
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.5px;">Rata-Rata Pasar</p>
            <p style="margin:4px 0 0 0;font-size:1rem;font-weight:700;color:rgba(255,255,255,0.7);">Rp {int(gaji_pasar):,}</p>
        </div>
        <div class="sb-mini-card">
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.5px;">Target Negosiasi</p>
            <p style="margin:4px 0 0 0;font-size:1rem;font-weight:700;color:#5dade2;">Rp {res['gaji_max']:,}</p>
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


def _get_salary_evaluation_status(persen):
    """Tentukan label evaluasi angka gaji terhadap estimasi wajar profil."""
    if persen >= 15:
        return {
            "label": "DI ATAS ESTIMASI WAJAR",
            "color": "#2ecc71",
            "bg": "rgba(46,204,113,0.08)",
            "border": "rgba(46,204,113,0.25)",
            "desc": f"Angka yang Anda masukkan <b>{abs(persen):.1f}%</b> di atas estimasi wajar untuk profil ini. Cocok sebagai target optimistis atau acuan negosiasi tinggi.",
            "emoji": "TARGET",
        }
    if persen >= -10:
        return {
            "label": "MASIH DALAM KISARAN WAJAR",
            "color": "#5dade2",
            "bg": "rgba(93,173,226,0.08)",
            "border": "rgba(93,173,226,0.25)",
            "desc": f"Angka yang Anda masukkan berada di kisaran yang masih wajar, dengan selisih <b>{abs(persen):.1f}%</b> dari estimasi sistem.",
            "emoji": "OK",
        }
    if persen >= -20:
        return {
            "label": "SEDIKIT DI BAWAH ESTIMASI",
            "color": "#f1c40f",
            "bg": "rgba(241,196,15,0.08)",
            "border": "rgba(241,196,15,0.25)",
            "desc": f"Angka yang Anda masukkan <b>{abs(persen):.1f}%</b> di bawah estimasi wajar. Masih mungkin diterima, tetapi ada ruang untuk negosiasi yang lebih baik.",
            "emoji": "INFO",
        }
    return {
        "label": "DI BAWAH ESTIMASI WAJAR",
        "color": "#e74c3c",
        "bg": "rgba(231,76,60,0.08)",
        "border": "rgba(231,76,60,0.25)",
        "desc": f"Angka yang Anda masukkan <b>{abs(persen):.1f}%</b> di bawah estimasi wajar untuk profil ini. Sebaiknya pertimbangkan negosiasi atau evaluasi ulang target atau offer tersebut.",
        "emoji": "ALERT",
    }


def _render_salary_evaluation(res):
    """Render evaluasi angka gaji untuk membantu pengambilan keputusan."""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
<div class="sec-hd">
    <div class="sec-hd-dot"></div>
    <span class="sec-hd-text">Evaluasi Angka Gaji</span>
    <div class="sec-hd-line"></div>
</div>
<p style="color:rgba(255,255,255,0.38);font-size:0.82rem;margin:-8px 0 16px 0;">
    Masukkan gaji saat ini, offer salary, atau target gaji Anda, lalu bandingkan dengan estimasi wajar untuk profil ini.
</p>
""",
        unsafe_allow_html=True,
    )

    sb_col1, sb_col2 = st.columns([2, 1])
    with sb_col1:
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
    with sb_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Evaluasi", type="primary", use_container_width=True)

    if gaji_user <= 0:
        return False

    gaji_pasar = res["gaji_prediksi"]
    selisih = gaji_user - gaji_pasar
    persen = (selisih / gaji_pasar) * 100
    status = _get_salary_evaluation_status(persen)

    range_min = gaji_pasar * 0.5
    range_max = gaji_pasar * 1.5
    pct_bar = min(max((gaji_user - range_min) / (range_max - range_min), 0), 1)
    bar_width = int(pct_bar * 100)

    tanda = "+" if selisih >= 0 else "-"
    selisih_display = f"{tanda}Rp {abs(int(selisih)):,}"

    emoji_map = {"TARGET": "🎯", "OK": "👍", "INFO": "📊", "ALERT": "📉"}
    emoji = emoji_map.get(status["emoji"], "📌")

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
        <div style="font-size:2.2rem;">{emoji}</div>
        <div>
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:1px;">Hasil Evaluasi</p>
            <p style="margin:4px 0 0 0;font-size:1.4rem;font-weight:800;color:{status['color']};">{status['label']}</p>
        </div>
        <div style="margin-left:auto;text-align:right;">
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:0.5px;">Selisih vs Estimasi</p>
            <p style="margin:4px 0 0 0;font-size:1.3rem;font-weight:700;color:{status['color']};">{selisih_display}</p>
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
        <div style="display:flex;justify-content:space-between;">
            <span style="font-size:11px;color:rgba(255,255,255,0.3);">Batas Bawah</span>
            <span style="font-size:11px;color:rgba(255,255,255,0.45);">Estimasi wajar: Rp {int(gaji_pasar):,}</span>
            <span style="font-size:11px;color:rgba(255,255,255,0.3);">Batas Atas</span>
        </div>
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:18px;">
        <div class="sb-mini-card">
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.5px;">Angka Anda</p>
            <p style="margin:4px 0 0 0;font-size:1rem;font-weight:700;color:#fff;">Rp {gaji_user:,}</p>
        </div>
        <div class="sb-mini-card">
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.5px;">Estimasi Wajar</p>
            <p style="margin:4px 0 0 0;font-size:1rem;font-weight:700;color:rgba(255,255,255,0.7);">Rp {int(gaji_pasar):,}</p>
        </div>
        <div class="sb-mini-card">
            <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.5px;">Target Negosiasi</p>
            <p style="margin:4px 0 0 0;font-size:1rem;font-weight:700;color:#5dade2;">Rp {res['gaji_max']:,}</p>
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


def _render_cta_ai_consultant():
    """Render banner ajakan ke tab AI Consultant (dipanggil setelah Salary Battle)."""
    st.markdown(
        """
<div style="background:linear-gradient(135deg,rgba(93,173,226,0.08),rgba(52,152,219,0.04));border:1px solid rgba(93,173,226,0.25);border-radius:14px;padding:18px 22px;margin-top:14px;display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
    <div style="font-size:1.8rem;">🤖</div>
    <div style="flex:1;min-width:200px;">
        <p style="margin:0;font-size:16px;font-weight:900;color:#fff;">Mau konsultasi mengenai karir anda di Jabodetabek?</p>
        <p style="margin:4px 0 0 0;font-size:13px;color:rgba(255,255,255,0.5);">Tanyakan target negosiasi, tips interview, atau strategi karir ke AI Consultant Career Virtual kita</p>
    </div>
    <div style="font-size:14px;font-weight:700;color:#5dade2;white-space:nowrap;">👉 Buka Tab 🤖 AI Consultant</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════
#  ANALISIS HUNIAN & STRATEGI KOMUTER
# ══════════════════════════════════════════════════════════════
def _render_analisis_hunian(res):
    """Render section analisis keterjangkauan hunian + rasio gaji."""
    _section_header("🏠 Analisis Keterjangkauan Hunian")

    st.metric(
        label=f"Estimasi Biaya Kos (Per Bulan) di {res['lokasi']}",
        value=f"Rp {res['estimasi_kos']:,}",
    )

    if res["rasio_kos"] <= 30:
        st.success(
            f"✅ Biaya hunian ideal ({res['rasio_kos']:.1f}% dari gaji). Gaji Anda cukup untuk hidup nyaman di lokasi ini."
        )
    elif res["rasio_kos"] <= 50:
        st.warning(
            f"⚠️ Biaya hunian cukup tinggi ({res['rasio_kos']:.1f}% dari gaji). Pertimbangkan kos dengan fasilitas dasar atau cari teman sekamar."
        )
    else:
        st.error(
            f"🚨 Beban biaya hidup sangat tinggi ({res['rasio_kos']:.1f}% dari gaji)! Sangat disarankan mencari hunian di wilayah penyangga dan menggunakan KRL/TransJakarta."
        )


def _render_strategi_komuter(res):
    """Render opsi komuter ke wilayah penyangga + tabel harga kos semua wilayah."""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
<div class="sec-hd">
    <div class="sec-hd-dot"></div>
    <span class="sec-hd-text">🚆 Strategi Hunian (Opsi Komuter)</span>
    <div class="sec-hd-line"></div>
</div>
<p style="color:rgba(255,255,255,0.38);font-size:0.82rem;margin:-8px 0 14px 0;">
    Tinggal di wilayah penyangga untuk menghemat biaya hidup bulanan sambil tetap bekerja di pusat bisnis.
</p>
""",
        unsafe_allow_html=True,
    )

    # Load data kota + prediksi kos
    df_map = load_map_data("data/data_peta_jabodetabek.csv")
    df_kota = df_map.groupby("Lokasi_Clean")["Jumlah_Lowongan"].sum().reset_index()
    df_kota["Harga_Kos_Estimasi"] = df_kota["Lokasi_Clean"].apply(predict_kos_price)
    df_kota = df_kota.sort_values(by="Jumlah_Lowongan", ascending=False).reset_index(
        drop=True
    )

    lokasi_kerja = res["lokasi"]
    kos_kerja = res["estimasi_kos"]

    alternatif = df_kota[
        df_kota["Harga_Kos_Estimasi"] <= (kos_kerja - 50000)
    ].sort_values(by="Harga_Kos_Estimasi", ascending=True)

    if alternatif.empty:
        st.success(
            f"🌟 **{lokasi_kerja}** sudah merupakan wilayah dengan biaya hunian paling ekonomis! Tidak perlu pindah lokasi kos."
        )
    else:
        st.info(
            f"💡 Anda bisa menghemat uang jika tinggal di kota-kota penyangga berikut dan komuter ke **{lokasi_kerja}**:"
        )
        cols = st.columns(min(3, len(alternatif)))
        for i, (_, row) in enumerate(alternatif.head(3).iterrows()):
            hemat = kos_kerja - row["Harga_Kos_Estimasi"]
            jarak_km = calculate_distance(lokasi_kerja, row["Lokasi_Clean"])
            menit = int((jarak_km / 25) * 60)

            with cols[i]:
                st.markdown(
                    f"""
<div class="komuter-card">
    <div style="font-weight:700;font-size:15px;color:#fff;margin-bottom:10px;">🏠 Kost di {row['Lokasi_Clean']}</div>
    <div style="font-weight:800;font-size:1.2rem;color:#2ecc71;margin-bottom:12px;">Hemat Rp {int(hemat):,}/bln</div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <span style="background:rgba(52,152,219,0.2);border:1px solid rgba(52,152,219,0.4);color:#5dade2;padding:3px 10px;border-radius:6px;font-size:12px;font-weight:600;">📍 ±{jarak_km} KM</span>
        <span style="background:rgba(230,126,34,0.2);border:1px solid rgba(230,126,34,0.4);color:#f0a500;padding:3px 10px;border-radius:6px;font-size:12px;font-weight:600;">⏱️ ~{menit} mnt</span>
    </div>
</div>
""",
                    unsafe_allow_html=True,
                )

    # Tabel full daftar kos
    with st.expander("📋 Lihat Daftar Rata-Rata Harga Kos Seluruh Wilayah"):
        st.markdown(
            "Berikut adalah tabel perbandingan harga kos rata-rata di Jabodetabek berdasarkan prediksi model AI:"
        )
        df_tabel = df_kota[["Lokasi_Clean", "Harga_Kos_Estimasi"]].copy()
        df_tabel = df_tabel.sort_values(by="Harga_Kos_Estimasi", ascending=True)
        df_tabel.columns = ["Wilayah", "Estimasi Harga Sebulan"]
        df_tabel["Estimasi Harga Sebulan"] = df_tabel["Estimasi Harga Sebulan"].apply(
            lambda x: f"Rp {x:,}"
        )
        st.table(df_tabel)
        st.caption(
            "⚠️ **Catatan:** Harga di atas adalah estimasi untuk *Kamar Luas 12m², Termasuk Listrik, dan Rating Tinggi*."
        )


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════
def render():
    """Entry point tab — orkestrasi semua komponen."""
    _inject_css()
    _render_header()

    try:
        resources, _, list_kategori, list_lokasi = load_ml_resources()

        # ── Input form ──
        judul, kategori, lokasi = _render_input_parameter(list_kategori, list_lokasi)
        st.markdown("<br>", unsafe_allow_html=True)
        peng, pend, sert = _render_input_maf()

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Tombol prediksi ──
        if st.button(
            "🔍 Hitung Prediksi Gaji", type="primary", use_container_width=True
        ):
            _run_prediction(judul, kategori, lokasi, peng, pend, sert, resources)

        # ── Tampilkan hasil (jika ada) ──
        if "last_prediction" in st.session_state:
            res = st.session_state["last_prediction"]
            st.markdown("<br>", unsafe_allow_html=True)

            _render_hasil_card(res)
            _render_rincian_kalkulasi(res)

            has_battle_input = _render_salary_evaluation(res)
            if has_battle_input:
                _render_cta_ai_consultant()

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)

            _render_analisis_hunian(res)
            _render_strategi_komuter(res)

    except Exception as e:
        st.error(
            f"Gagal memuat Model: {str(e)}. Pastikan file .pkl lengkap di folder models/salary/"
        )
