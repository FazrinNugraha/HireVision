import streamlit as st

from tabs.predict_salary.constants import (
    PENDIDIKAN_MAP,
    PENGALAMAN_MAP,
    SERTIFIKAT_MAP,
)
from tabs.predict_salary.layout import render_section_header


def render_input_parameter(list_kategori, list_lokasi):
    """Render baris input utama: Judul, Kategori, Lokasi."""
    render_section_header("🎯 Parameter Utama")

    col1, col2, col3 = st.columns(3)

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


def render_input_maf():
    """Render input faktor MAF: Pengalaman, Pendidikan, Sertifikasi."""
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
