import streamlit as st
from utils import load_ml_resources, predict_salary, predict_kos_price

def render():
    st.header("Kalkulator Estimasi Gaji Pasar")
    st.write("Estimasi gaji berdasarkan **kategori industri, lokasi, pengalaman, tipe kontrak, dan skala perusahaan**.")

    try:
        model, kat_enc, lok_enc, list_kategori, list_lokasi = load_ml_resources()

        # ── Baris 1: Input Model ML (Core Prediction) ──
        st.markdown("#### 🎯 Parameter Utama")
        col1, col2 = st.columns(2)
        with col1:
            pilihan_kategori = st.selectbox("Kategori Industri / Jabatan:", list_kategori)
        with col2:
            pilihan_lokasi = st.selectbox("Kota Penempatan:", list_lokasi)

        st.markdown("---")

        # ── Baris 2: Input Penyesuaian (Post-Processing Multiplier) ──
        st.markdown("#### ⚙️ Faktor Penyesuaian Profil")
        st.caption("Input ini digunakan untuk menyesuaikan estimasi basis model berdasarkan profil spesifik Anda.")

        cola, colb, colc = st.columns(3)

        with cola:
            level_map = {
                "🎓 Fresh Graduate (0–1 thn)": 0.75,
                "📈 Junior (1–3 thn)": 0.90,
                "💼 Mid-Level (3–5 thn)": 1.10,
                "🏆 Senior (5–8 thn)": 1.35,
                "🎖️ Expert / Lead (8+ thn)": 1.70,
            }
            pilihan_level = st.selectbox("Level Pengalaman:", list(level_map.keys()))

        with colb:
            kontrak_map = {
                "📝 Magang / Internship": 0.50,
                "🔄 Freelance / Project": 0.85,
                "📋 Kontrak (1–2 thn)": 0.95,
                "🏢 Permanen / Full-Time": 1.00,
            }
            pilihan_kontrak = st.selectbox("Tipe Kontrak:", list(kontrak_map.keys()))

        with colc:
            skala_map = {
                "🚀 Startup / UMKM": 0.85,
                "🏗️ Perusahaan Menengah": 1.00,
                "🏢 Korporasi Lokal Besar": 1.20,
                "🌐 MNC / Multinasional": 1.40,
            }
            pilihan_skala = st.selectbox("Skala Perusahaan:", list(skala_map.keys()))

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
                    st.success("✅ Analisis Selesai! Pindah ke Tab **🤖 AI Consultant** untuk saran personal.")
                else:
                    st.error("Terjadi masalah saat membaca output model ML.")

        # ── RENDER HASIL (Jika Ada di Session State) ──
        if "last_prediction" in st.session_state:
            res = st.session_state["last_prediction"]
            st.markdown("<br>", unsafe_allow_html=True)

            # ── Output: 3 kolom metrik ──
            r1, r2, r3 = st.columns(3)
            with r1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style='margin:0;color:#bdc3c7;font-size:13px'>🤖 Gaji Basis Model ML</h4>
                    <h2 style='margin:8px 0;color:#95a5a6'>Rp {res['gaji_basis']:,}</h2>
                    <p style='margin:0;font-size:11px;color:#7f8c8d'>Output mentah Random Forest</p>
                </div>""", unsafe_allow_html=True)

            with r2:
                st.markdown(f"""
                <div class="metric-card" style='border:2px solid #2ecc71'>
                    <h4 style='margin:0;color:#bdc3c7;font-size:13px'>✨ Estimasi Gaji Anda</h4>
                    <h2 style='margin:8px 0;color:#2ecc71'>Rp {res['gaji_prediksi']:,}</h2>
                    <p style='margin:0;font-size:11px;color:#bdc3c7'>Setelah penyesuaian profil</p>
                </div>""", unsafe_allow_html=True)

            with r3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style='margin:0;color:#bdc3c7;font-size:13px'>📊 Rentang Negosiasi</h4>
                    <h2 style='margin:8px 0;color:#3498db;font-size:18px'>Rp {res['gaji_min']:,}<br>– Rp {res['gaji_max']:,}</h2>
                    <p style='margin:0;font-size:11px;color:#7f8c8d'>±10% dari estimasi Anda</p>
                </div>""", unsafe_allow_html=True)

            # ── Breakdown multiplier ──
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

            st.markdown("---")
            st.subheader("🏠 Analisis Keterjangkauan Hunian")

            st.metric(label=f"Estimasi Biaya Kos (Per Bulan) di {res['lokasi']}", value=f"Rp {res['estimasi_kos']:,}")

            if res['rasio_kos'] <= 30:
                st.success(f"✅ Biaya hunian ideal ({res['rasio_kos']:.1f}% dari gaji). Gaji Anda cukup untuk hidup nyaman di lokasi ini.")
            elif res['rasio_kos'] > 30 and res['rasio_kos'] <= 50:
                st.warning(f"⚠️ Biaya hunian cukup tinggi ({res['rasio_kos']:.1f}% dari gaji). Pertimbangkan kos dengan fasilitas dasar atau cari teman sekamar.")
            else:
                st.error(f"🚨 Beban biaya hidup sangat tinggi ({res['rasio_kos']:.1f}% dari gaji)! Sangat disarankan mencari hunian di wilayah penyangga dan menggunakan KRL/TransJakarta.")

    except Exception as e:
        st.error(f"Gagal memuat Model: {str(e)}. Pastikan file .pkl lengkap di folder models/")
