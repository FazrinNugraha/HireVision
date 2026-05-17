"""
Tab Prediksi Gaji - HireVision
================================
File ini berperan sebagai orkestrator untuk tab Predict Salary.
Setiap feature utama dipisah ke package predict_salary agar maintenance lebih mudah.
"""

import streamlit as st

from tabs.predict_salary.layout import inject_css, render_header, render_section_gap
from tabs.predict_salary.logic import run_prediction
from tabs.predict_salary.sections_input import render_input_maf, render_input_parameter
from tabs.predict_salary.sections_results import (
    render_analisis_hunian,
    render_cta_ai_consultant,
    render_hasil_card,
    render_strategi_komuter,
)
from tabs.predict_salary.sections_salary_zone import render_salary_evaluation
from utils import load_ml_resources


def render():
    """Entry point tab untuk orkestrasi semua komponen."""
    inject_css()
    render_header()

    try:
        resources, _, list_kategori, list_lokasi = load_ml_resources()

        judul, kategori, lokasi = render_input_parameter(list_kategori, list_lokasi)
        st.markdown("<br>", unsafe_allow_html=True)
        peng, pend, sert = render_input_maf()
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Hitung Prediksi Gaji", type="primary", use_container_width=True):
            run_prediction(judul, kategori, lokasi, peng, pend, sert, resources)

        if "last_prediction" in st.session_state:
            res = st.session_state["last_prediction"]
            render_section_gap("md")
            render_hasil_card(res)
            render_section_gap("sm")
            st.markdown("<hr>", unsafe_allow_html=True)

            render_analisis_hunian(res)
            render_strategi_komuter(res)

            has_zone_input = render_salary_evaluation(res)
            if has_zone_input:
                render_cta_ai_consultant()

    except Exception as e:
        st.error(
            f"Gagal memuat Model: {str(e)}. Pastikan file .pkl lengkap di folder models/salary/"
        )
