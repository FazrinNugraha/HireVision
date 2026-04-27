import streamlit as st
from utils import load_ml_resources, predict_salary, predict_kos_price

def render():
    # ── Section Header ──
    st.markdown("""
    <div style="margin-bottom:6px;">
        <h2 style="font-size:1.55rem;font-weight:800;color:#fff;margin:0 0 6px 0;">
            Kalkulator Estimasi Gaji Pasar
        </h2>
        <p style="color:rgba(255,255,255,0.45);font-size:0.9rem;margin:0;">
            Estimasi gaji berdasarkan kategori industri, lokasi, pengalaman, tipe kontrak, dan skala perusahaan.
        </p>
    </div>
    <hr style="border:none;border-top:1px solid rgba(255,255,255,0.07);margin:18px 0 24px 0;">
    """, unsafe_allow_html=True)

    try:
        model, kat_enc, lok_enc, list_kategori, list_lokasi = load_ml_resources()

        # ── INPUT CARD 1: Parameter Utama ──
        st.markdown("""
        <div class="sec-hd">
            <div class="sec-hd-dot"></div>
            <span class="sec-hd-text">🎯 Parameter Utama</span>
            <div class="sec-hd-line"></div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            pilihan_kategori = st.selectbox("Kategori Industri / Jabatan", list_kategori)
        with col2:
            pilihan_lokasi = st.selectbox("Kota Penempatan", list_lokasi)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── INPUT CARD 2: Faktor Penyesuaian ──
        st.markdown("""
        <div class="sec-hd">
            <div class="sec-hd-dot"></div>
            <span class="sec-hd-text">⚙️ Faktor Penyesuaian Profil</span>
            <div class="sec-hd-line"></div>
        </div>
        <p style="color:rgba(255,255,255,0.38);font-size:0.82rem;margin:-8px 0 14px 0;">
            Input ini digunakan untuk menyesuaikan estimasi basis model berdasarkan profil spesifik Anda.
        </p>
        """, unsafe_allow_html=True)

        cola, colb, colc = st.columns(3)

        with cola:
            level_map = {
                "🎓 Fresh Graduate (0–1 thn)": 0.75,
                "📈 Junior (1–3 thn)": 0.90,
                "💼 Mid-Level (3–5 thn)": 1.10,
                "🏆 Senior (5–8 thn)": 1.35,
                "🎖️ Expert / Lead (8+ thn)": 1.70,
            }
            pilihan_level = st.selectbox("Level Pengalaman", list(level_map.keys()))

        with colb:
            kontrak_map = {
                "📝 Magang / Internship": 0.50,
                "🔄 Freelance / Project": 0.85,
                "📋 Kontrak (1–2 thn)": 0.95,
                "🏢 Permanen / Full-Time": 1.00,
            }
            pilihan_kontrak = st.selectbox("Tipe Kontrak", list(kontrak_map.keys()))

        with colc:
            skala_map = {
                "🚀 Startup / UMKM": 0.85,
                "🏗️ Perusahaan Menengah": 1.00,
                "🏢 Korporasi Lokal Besar": 1.20,
                "🌐 MNC / Multinasional": 1.40,
            }
            pilihan_skala = st.selectbox("Skala Perusahaan", list(skala_map.keys()))

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔍 Hitung Prediksi Gaji", type="primary", use_container_width=True):
            with st.spinner("Memproses algoritma Random Forest + penyesuaian profil..."):
                hasil_basis = predict_salary(pilihan_kategori, pilihan_lokasi, model, kat_enc, lok_enc)
                if hasil_basis is not None:
                    m_level   = level_map[pilihan_level]
                    m_kontrak = kontrak_map[pilihan_kontrak]
                    m_skala   = skala_map[pilihan_skala]
                    total_multiplier = m_level * m_kontrak * m_skala
                    gaji_akhir = int(hasil_basis * total_multiplier)
                    batas_bawah = int(gaji_akhir * 0.90)
                    batas_atas  = int(gaji_akhir * 1.10)
                    estimasi_kos = predict_kos_price(pilihan_lokasi)
                    rasio_kos = (estimasi_kos / gaji_akhir) * 100

                    st.session_state["last_prediction"] = {
                        "kategori":       pilihan_kategori,
                        "lokasi":         pilihan_lokasi,
                        "level":          pilihan_level,
                        "kontrak":        pilihan_kontrak,
                        "skala":          pilihan_skala,
                        "gaji_basis":     int(hasil_basis),
                        "gaji_prediksi":  gaji_akhir,
                        "gaji_min":       batas_bawah,
                        "gaji_max":       batas_atas,
                        "multiplier":     round(total_multiplier, 2),
                        "m_level":        m_level,
                        "m_kontrak":      m_kontrak,
                        "m_skala":        m_skala,
                        "estimasi_kos":   estimasi_kos,
                        "rasio_kos":      rasio_kos
                    }

                    if "messages" in st.session_state:
                        del st.session_state["messages"]

                    st.success("✅ Analisis Selesai! Pindah ke Tab **🤖 AI Consultant** untuk saran personal.")
                else:
                    st.error("Terjadi masalah saat membaca output model ML.")

        # ── HASIL PREDIKSI ──
        if "last_prediction" in st.session_state:
            res = st.session_state["last_prediction"]
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <div class="sec-hd">
                <div class="sec-hd-dot"></div>
                <span class="sec-hd-text">📊 Hasil Estimasi Gaji</span>
                <div class="sec-hd-line"></div>
            </div>
            """, unsafe_allow_html=True)

            if res['rasio_kos'] <= 30:
                bg_grad = "linear-gradient(135deg, rgba(46,204,113,0.12), rgba(39,174,96,0.06))"
                border_col = "rgba(46,204,113,0.32)"
                title_col = "rgba(180,255,180,0.7)"
                val_col = "#2ecc71"
            elif res['rasio_kos'] <= 50:
                bg_grad = "linear-gradient(135deg, rgba(241,196,15,0.12), rgba(243,156,18,0.06))"
                border_col = "rgba(241,196,15,0.32)"
                title_col = "rgba(255,230,180,0.7)"
                val_col = "#f1c40f"
            else:
                bg_grad = "linear-gradient(135deg, rgba(231,76,60,0.12), rgba(192,57,43,0.06))"
                border_col = "rgba(231,76,60,0.32)"
                title_col = "rgba(255,180,180,0.7)"
                val_col = "#e74c3c"

            r1, r2, r3 = st.columns(3)
            with r1:
                st.markdown(f"""
<div class="metric-card">
    <p style="margin:0;color:rgba(255,255,255,0.4);font-size:12px;font-weight:600;letter-spacing:0.5px;text-transform:uppercase;">🤖 Gaji Basis Model ML</p>
    <h2 style="margin:12px 0 8px 0;color:rgba(255,255,255,0.65);font-size:1.3rem;font-weight:700;">Rp {res['gaji_basis']:,}</h2>
    <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.28);">Output mentah Random Forest</p>
</div>""", unsafe_allow_html=True)

            with r2:
                st.markdown(f"""
<div style="background:{bg_grad};border:1px solid {border_col};border-radius:16px;padding:22px 20px;text-align:center;">
    <p style="margin:0;color:{title_col};font-size:12px;font-weight:600;letter-spacing:0.5px;text-transform:uppercase;">✨ Estimasi Gaji Anda</p>
    <h2 style="margin:12px 0 8px 0;color:{val_col};font-size:1.3rem;font-weight:700;">Rp {res['gaji_prediksi']:,}</h2>
    <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.35);">Setelah penyesuaian profil</p>
</div>""", unsafe_allow_html=True)

            with r3:
                st.markdown(f"""
<div class="metric-card">
    <p style="margin:0;color:rgba(255,255,255,0.4);font-size:12px;font-weight:600;letter-spacing:0.5px;text-transform:uppercase;">📈 Batas Maks. Negosiasi</p>
    <h2 style="margin:12px 0 8px 0;color:#5dade2;font-size:1.3rem;font-weight:700;">Rp {res['gaji_max']:,}</h2>
    <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.28);">+10% · naik Rp {res['gaji_max'] - res['gaji_prediksi']:,} dari estimasi</p>
</div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📋 Lihat Rincian Kalkulasi Multiplier"):
                st.markdown(f"""
| Faktor | Pilihan | Multiplier |
|--------|---------|-----------|
| Level Pengalaman | {res['level']} | `×{res['m_level']}` |
| Tipe Kontrak | {res['kontrak']} | `×{res['m_kontrak']}` |
| Skala Perusahaan | {res['skala']} | `×{res['m_skala']}` |
| **Total Gabungan** | — | **`×{res['multiplier']}`** |
| **Gaji Basis ML** | Rp {res['gaji_basis']:,} | |
| **Hasil Akhir** | **Rp {res['gaji_prediksi']:,}** | |
                """)
                st.caption("_Multiplier mengacu pada data rata-rata industri & survei kompensasi Jabodetabek._")

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown("""
            <div class="sec-hd">
                <div class="sec-hd-dot"></div>
                <span class="sec-hd-text">🏠 Analisis Keterjangkauan Hunian</span>
                <div class="sec-hd-line"></div>
            </div>
            """, unsafe_allow_html=True)

            st.metric(label=f"Estimasi Biaya Kos (Per Bulan) di {res['lokasi']}", value=f"Rp {res['estimasi_kos']:,}")

            if res['rasio_kos'] <= 30:
                st.success(f"✅ Biaya hunian ideal ({res['rasio_kos']:.1f}% dari gaji). Gaji Anda cukup untuk hidup nyaman di lokasi ini.")
            elif res['rasio_kos'] <= 50:
                st.warning(f"⚠️ Biaya hunian cukup tinggi ({res['rasio_kos']:.1f}% dari gaji). Pertimbangkan kos dengan fasilitas dasar atau cari teman sekamar.")
            else:
                st.error(f"🚨 Beban biaya hidup sangat tinggi ({res['rasio_kos']:.1f}% dari gaji)! Sangat disarankan mencari hunian di wilayah penyangga dan menggunakan KRL/TransJakarta.")

    except Exception as e:
        st.error(f"Gagal memuat Model: {str(e)}. Pastikan file .pkl lengkap di folder models/salary/")
