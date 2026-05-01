import streamlit as st
import pandas as pd
from utils import load_ml_resources, predict_salary, predict_kos_price, load_map_data, calculate_distance

def render():
    # ── Custom CSS for Inputs ──
    st.markdown("""
    <style>
    /* Styling for Text Inputs and Selectboxes */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        background-color: rgba(255, 255, 255, 0.02) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Hover state */
    div[data-baseweb="input"]:hover, div[data-baseweb="select"]:hover {
        border-color: rgba(255, 255, 255, 0.25) !important;
        background-color: rgba(255, 255, 255, 0.04) !important;
    }

    /* Focus state */
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {
        border-color: #5dade2 !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        box-shadow: 0 0 12px rgba(93, 173, 226, 0.15) !important;
    }

    /* Style for the expander to match */
    .stExpander {
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.01) !important;
    }
    
    /* Styling khusus untuk tombol di dalam expander bertipe dropdown list */
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
    """, unsafe_allow_html=True)

    # ── Section Header ──
    st.markdown("""
    <div style="margin-bottom:6px;">
        <h2 style="font-size:1.55rem;font-weight:800;color:#fff;margin:0 0 6px 0;">
            Kalkulator Estimasi Gaji Pasar
        </h2>
        <p style="color:rgba(255,255,255,0.45);font-size:0.9rem;margin:0;">
            Estimasi gaji berbasis AI dengan proyeksi inflasi masa depan, latar belakang pendidikan, dan sertifikasi profesional.
        </p>
    </div>
    <hr style="border:none;border-top:1px solid rgba(255,255,255,0.07);margin:18px 0 24px 0;">
    """, unsafe_allow_html=True)

    try:
        resources, kolom_fitur, list_kategori, list_lokasi = load_ml_resources()

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
            pilihan_judul = st.text_input(
                "Judul / Posisi Pekerjaan",
                placeholder="Contoh: Senior Data Scientist, HR Manager, Full Stack Developer...",
                help="Ketik jabatan pekerjaan yang ingin diprediksi gajinya. Semakin spesifik semakin akurat."
            )
            
           
            
            # Callback untuk mempercepat perpindahan lokasi tanpa double-loading
            def update_lokasi(lokasi_baru):
                st.session_state.lokasi_terpilih = lokasi_baru

            # Lokasi Penempatan (Dinamis) - Sesuai mockup posisi yang diinginkan
            if "lokasi_terpilih" not in st.session_state:
                st.session_state.lokasi_terpilih = "Jakarta Selatan" if "Jakarta Selatan" in list_lokasi else list_lokasi[0]
            
            pilihan_lokasi = st.session_state.lokasi_terpilih
            
            with st.expander(f"📍 Lokasi Penempatan: {st.session_state.lokasi_terpilih}"):
                st.markdown("<div class='marker-dropdown-list'></div>", unsafe_allow_html=True)
                for loc in list_lokasi:
                    st.button(
                        loc, 
                        key=f"btn_loc_{loc}", 
                        use_container_width=True,
                        on_click=update_lokasi,
                        args=(loc,)
                    )



        with col2:
            company_size_dict = resources['encoder']['company_size_dict']

            # Fungsi callback untuk list perusahaan
            def update_perusahaan(nama_perusahaan):
                st.session_state.input_perusahaan = nama_perusahaan

            if "input_perusahaan" not in st.session_state:
                st.session_state.input_perusahaan = ""

            pilihan_perusahaan = st.text_input(
                "Nama Perusahaan (Opsional)",
                key="input_perusahaan",
                placeholder="Contoh: PT XL Axiata Tbk, Dexa Group, EUROMEDICA GROUP...",
                help="Ketik nama perusahaan. Jika dikenal model, prediksi lebih akurat. Jika tidak, model pakai rata-rata pasar."
            )

            # # Status pengenalan perusahaan secara real-time
            # if pilihan_perusahaan.strip():
            #     jumlah_data = company_size_dict.get(pilihan_perusahaan.strip(), 0)
            #     if jumlah_data >= 10:
            #         st.caption(f"✅ Dikenal model — **{jumlah_data} data** ditemukan, prediksi sangat akurat.")
            #     elif jumlah_data >= 3:
            #         st.caption(f"⚠️ Dikenal model — **{jumlah_data} data** ditemukan, prediksi cukup akurat.")
            #     elif jumlah_data > 0:
            #         st.caption(f"ℹ️ Data sangat sedikit ({jumlah_data}) — model pakai rata-rata pasar sebagai acuan.")
            #     else:
            #         st.caption("❓ Perusahaan tidak dikenal model — prediksi berdasarkan rata-rata pasar umum.")
            

            # Fitur Expander Contoh Perusahaan
            top_companies = sorted(
                {k: v for k, v in company_size_dict.items() if k not in {"Pengiklan Anonim", "Anonymous", "Confidential"}}.items(),
                key=lambda x: x[1], reverse=True
            )[:30]
            with st.expander("💡 Contoh perusahaan yang dikenal model"):
                st.markdown("<div class='marker-dropdown-list'></div>", unsafe_allow_html=True)
                for nama, count in top_companies:
                    st.button(
                        f"{nama} ({count} data)",
                        key=f"btn_comp_{nama}",
                        use_container_width=True,
                        on_click=update_perusahaan,
                        args=(nama,)
                    )


        st.markdown("<br>", unsafe_allow_html=True)

        # ── INPUT CARD 2: Faktor Penyesuaian Profil ──
        st.markdown("""
        <div class="sec-hd">
            <div class="sec-hd-dot"></div>
            <span class="sec-hd-text">⚙️ Penyesuaian Realistis & Proyeksi Karir</span>
            <div class="sec-hd-line"></div>
        </div>
        <p style="color:rgba(255,255,255,0.45); font-size:0.85rem; line-height:1.6; margin:-8px 0 20px 0;">
            Optimalkan estimasi gaji Anda dengan menyesuaikan faktor kunci keberhasilan karir: Target Tahun Proyeksi untuk inflasi, 
            Sertifikasi Profesional untuk nilai tambah keahlian, Pendidikan Terakhir, Level Pengalaman, dan Tipe Kontrak.
        </p>
        """, unsafe_allow_html=True)

        # Baris Pertama Penyesuaian
        cola, colb, colc = st.columns(3)

        with cola:
            proyeksi_map = {
                "📅 2026 (Tahun Depan)": {"m_proyeksi": 1.17, "label": "2026"},
                "📅 2027 (Jangka Pendek)": {"m_proyeksi": 1.26, "label": "2027"},
                "📅 2028 (Jangka Madya)":  {"m_proyeksi": 1.36, "label": "2028"},
                "📅 2029 (Jangka Panjang)": {"m_proyeksi": 1.47, "label": "2029"},
                "📅 2030 (5 Tahun Depan)":  {"m_proyeksi": 1.59, "label": "2030"},
            }
            pilihan_proyeksi = st.selectbox("Target Tahun Proyeksi", list(proyeksi_map.keys()), index=0)

        with colb:
            pendidikan_map = {
                "🎓 SMA / SMK":         {"m_pendidikan": 0.78, "label": "SMA/SMK"},
                "🏅 Diploma (D3/D4)":  {"m_pendidikan": 0.88, "label": "Diploma"},
                "🎓 S1 / Sarjana":      {"m_pendidikan": 1.00, "label": "S1/Sarjana"},
                "🎖️ S2 / Magister ke atas": {"m_pendidikan": 1.25, "label": "S2+"},
            }
            pilihan_pendidikan = st.selectbox("Pendidikan Terakhir", list(pendidikan_map.keys()), index=2)

        with colc:
            sertifikat_map = {
                "📄 Tanpa Sertifikasi":      {"m_sertifikat": 1.00, "label": "None"},
                "🏅 Sertifikat BNSP / Lokal": {"m_sertifikat": 1.15, "label": "Lokal/BNSP"},
                "🎖️ Sertifikat Associate (Intl)": {"m_sertifikat": 1.30, "label": "Associate"},
                "🏆 Sertifikat Expert (Intl)": {"m_sertifikat": 1.50, "label": "Expert"},
            }
            pilihan_sertifikat = st.selectbox("Sertifikasi Profesional", list(sertifikat_map.keys()), index=0)

        # Baris Kedua Penyesuaian
        st.markdown("<br>", unsafe_allow_html=True)
        col_lvl, col_ktrk = st.columns(2)
        
        with col_lvl:
            level_map = {
                "🌱 Fresh Graduate (0–1 thn)":  {"senioritas": "Junior/Entry",      "m_level": 0.85},
                "📈 Junior – Mid (1–4 thn)":    {"senioritas": "Mid-Level/Staff",   "m_level": 0.95},
                "🏆 Senior (4–8 thn)":           {"senioritas": "Senior/Managerial", "m_level": 1.00},
                "🎖️ Expert / Lead (8+ thn)":    {"senioritas": "Senior/Managerial", "m_level": 1.20},
            }
            pilihan_level = st.selectbox("Level Pengalaman", list(level_map.keys()))
            
        with col_ktrk:
            kontrak_map = {
                "📝 Magang / Internship":  0.50,
                "🔄 Freelance / Project":  0.85,
                "📋 Kontrak (1–2 thn)":    0.95,
                "🏢 Permanen / Full-Time": 1.00,
            }
            pilihan_kontrak = st.selectbox("Tipe Kontrak", list(kontrak_map.keys()), index=3)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔍 Hitung Prediksi Gaji", type="primary", use_container_width=True):
            if not pilihan_judul.strip():
                st.warning("⚠️ Mohon isi Judul Pekerjaan terlebih dahulu.")
            else:
                with st.spinner("Memproses LightGBM + penyesuaian profil..."):
                    level_data     = level_map[pilihan_level]
                    senioritas_val = level_data["senioritas"]
                    
                    hasil_basis = predict_salary(
                        judul_pekerjaan=pilihan_judul.strip(),
                        perusahaan=pilihan_perusahaan.strip() if pilihan_perusahaan.strip() else "__unknown__",
                        lokasi=pilihan_lokasi,  # Menggunakan lokasi dinamis
                        senioritas=senioritas_val,
                        resources=resources
                    )
                    
                    if hasil_basis is not None:
                        m_proyeksi   = proyeksi_map[pilihan_proyeksi]["m_proyeksi"]
                        m_pendidikan = pendidikan_map[pilihan_pendidikan]["m_pendidikan"]
                        m_sertifikat = sertifikat_map[pilihan_sertifikat]["m_sertifikat"]
                        m_level      = level_data["m_level"]
                        m_kontrak    = kontrak_map[pilihan_kontrak]
                        
                        total_multiplier = m_proyeksi * m_pendidikan * m_sertifikat * m_level * m_kontrak
                        gaji_akhir   = int(hasil_basis * total_multiplier)
                        
                        batas_bawah  = int(gaji_akhir * 0.90)
                        batas_atas   = int(gaji_akhir * 1.10)
                        estimasi_kos = predict_kos_price(pilihan_lokasi) # Harga kos mengikuti lokasi dinamis
                        rasio_kos    = (estimasi_kos / gaji_akhir) * 100

                        st.session_state["last_prediction"] = {
                            "judul":          pilihan_judul.strip(),
                            "perusahaan":     pilihan_perusahaan.strip() or "—",
                            "lokasi":         pilihan_lokasi,
                            "tahun_proyeksi": proyeksi_map[pilihan_proyeksi]["label"],
                            "pendidikan":     pendidikan_map[pilihan_pendidikan]["label"],
                            "sertifikasi":    sertifikat_map[pilihan_sertifikat]["label"],
                            "level":          pilihan_level,
                            "kontrak":        pilihan_kontrak,
                            "gaji_basis":     int(hasil_basis),
                            "gaji_prediksi":  gaji_akhir,
                            "gaji_min":       batas_bawah,
                            "gaji_max":       batas_atas,
                            "multiplier":     round(total_multiplier, 2),
                            "m_proyeksi":     m_proyeksi,
                            "m_pendidikan":   m_pendidikan,
                            "m_sertifikat":   m_sertifikat,
                            "m_level":        m_level,
                            "m_kontrak":      m_kontrak,
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
    <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.28);">Output mentah LightGBM</p>
</div>""", unsafe_allow_html=True)

            with r2:
                st.markdown(f"""
<div style="background:{bg_grad};border:1px solid {border_col};border-radius:16px;padding:22px 20px;text-align:center;">
    <p style="margin:0;color:{title_col};font-size:12px;font-weight:600;letter-spacing:0.5px;text-transform:uppercase;">✨ Estimasi Gaji Anda</p>
    <h2 style="margin:12px 0 8px 0;color:{val_col};font-size:1.3rem;font-weight:700;">Rp {res['gaji_prediksi']:,}</h2>
    <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.35);">Setelah penyesuaian 5 faktor</p>
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
| Jabatan | {res['judul']} | — |
| Perusahaan | {res['perusahaan']} | — |
| Lokasi | {res['lokasi']} | — |
| Tahun Proyeksi | {res['tahun_proyeksi']} | `×{res['m_proyeksi']}` |
| Pendidikan Terakhir | {res['pendidikan']} | `×{res['m_pendidikan']}` |
| Sertifikasi | {res['sertifikasi']} | `×{res['m_sertifikat']}` |
| Level Pengalaman | {res['level']} | `×{res['m_level']}` |
| Tipe Kontrak | {res['kontrak']} | `×{res['m_kontrak']}` |
| **Total Gabungan** | — | **`×{res['multiplier']}`** |
| **Gaji Basis ML** | Rp {res['gaji_basis']:,} | |
| **Hasil Akhir** | **Rp {res['gaji_prediksi']:,}** | |
                """)
                st.caption("_Proyeksi tahunan menggunakan asumsi kenaikan upah nominal 8% (BPS). Multiplier pendidikan bersumber dari BPS Sakernas 2023._")

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

            # ── STRATEGI HUNIAN (Opsi Komuter) ──
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="sec-hd">
                <div class="sec-hd-dot"></div>
                <span class="sec-hd-text">🚆 Strategi Hunian (Opsi Komuter)</span>
                <div class="sec-hd-line"></div>
            </div>
            <p style="color:rgba(255,255,255,0.38);font-size:0.82rem;margin:-8px 0 14px 0;">
                Tinggal di wilayah penyangga untuk menghemat biaya hidup bulanan sambil tetap bekerja di pusat bisnis.
            </p>
            """, unsafe_allow_html=True)

            df_map = load_map_data('data/data_peta_jabodetabek.csv')
            raw_kota = df_map.groupby("Lokasi_Clean")["Jumlah_Lowongan"].sum().reset_index()
            raw_kota["Harga_Kos_Estimasi"] = raw_kota["Lokasi_Clean"].apply(predict_kos_price)
            df_kota = raw_kota.sort_values(by="Jumlah_Lowongan", ascending=False).reset_index(drop=True)

            lokasi_kerja = res['lokasi']
            kos_kerja = res['estimasi_kos']

            alternatif = df_kota[df_kota['Harga_Kos_Estimasi'] <= (kos_kerja - 50000)].sort_values(by='Harga_Kos_Estimasi', ascending=True)

            if not alternatif.empty:
                st.info(f"💡 Anda bisa menghemat uang jika tinggal di kota-kota penyangga berikut dan komuter ke **{lokasi_kerja}**:")
                cols = st.columns(min(3, len(alternatif)))
                for i, (idx, row) in enumerate(alternatif.head(3).iterrows()):
                    hemat_rupiah = kos_kerja - row['Harga_Kos_Estimasi']
                    jarak_km = calculate_distance(lokasi_kerja, row['Lokasi_Clean'])
                    menit = int((jarak_km / 25) * 60)

                    with cols[i]:
                        st.markdown(f"""
                        <div class="komuter-card">
                            <div style="font-weight:700;font-size:15px;color:#fff;margin-bottom:10px;">🏠 Kost di {row['Lokasi_Clean']}</div>
                            <div style="font-weight:800;font-size:1.2rem;color:#2ecc71;margin-bottom:12px;">Hemat Rp {int(hemat_rupiah):,}/bln</div>
                            <div style="display:flex;gap:8px;flex-wrap:wrap;">
                                <span style="background:rgba(52,152,219,0.2);border:1px solid rgba(52,152,219,0.4);color:#5dade2;padding:3px 10px;border-radius:6px;font-size:12px;font-weight:600;">📍 ±{jarak_km} KM</span>
                                <span style="background:rgba(230,126,34,0.2);border:1px solid rgba(230,126,34,0.4);color:#f0a500;padding:3px 10px;border-radius:6px;font-size:12px;font-weight:600;">⏱️ ~{menit} mnt</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.success(f"🌟 **{lokasi_kerja}** sudah merupakan wilayah dengan biaya hunian paling ekonomis! Tidak perlu pindah lokasi kos.")

            with st.expander("📋 Lihat Daftar Rata-Rata Harga Kos Seluruh Wilayah"):
                st.markdown("Berikut adalah tabel perbandingan harga kos rata-rata di Jabodetabek berdasarkan prediksi model AI:")
                df_tabel = df_kota[['Lokasi_Clean', 'Harga_Kos_Estimasi']].copy()
                df_tabel = df_tabel.sort_values(by='Harga_Kos_Estimasi', ascending=True)
                df_tabel.columns = ['Wilayah', 'Estimasi Harga Sebulan']
                df_tabel['Estimasi Harga Sebulan'] = df_tabel['Estimasi Harga Sebulan'].apply(lambda x: f"Rp {x:,}")
                st.table(df_tabel)
                st.caption("⚠️ **Catatan:** Harga di atas adalah estimasi untuk *Kamar Luas 12m², Termasuk Listrik, dan Rating Tinggi*.")

    except Exception as e:
        st.error(f"Gagal memuat Model: {str(e)}. Pastikan file .pkl lengkap di folder models/salary/")