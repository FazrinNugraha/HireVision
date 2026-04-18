import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utils import load_map_data, load_ml_resources, predict_salary, get_groq_client, chat_with_career_bot

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
                    # Ambil nilai multiplier
                    m_level   = level_map[pilihan_level]
                    m_kontrak = kontrak_map[pilihan_kontrak]
                    m_skala   = skala_map[pilihan_skala]
                    total_multiplier = m_level * m_kontrak * m_skala

                    # Hitung gaji akhir yang disesuaikan
                    gaji_akhir = int(hasil_basis * total_multiplier)
                    batas_bawah = int(gaji_akhir * 0.90)
                    batas_atas  = int(gaji_akhir * 1.10)

                    # Simpan ke session state untuk Tab AI
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
                    }

                    st.success("✅ Analisis Selesai! Pindah ke Tab **🤖 AI Consultant** untuk saran personal.")
                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── Output: 3 kolom metrik ──
                    r1, r2, r3 = st.columns(3)
                    with r1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4 style='margin:0;color:#bdc3c7;font-size:13px'>🤖 Gaji Basis Model ML</h4>
                            <h2 style='margin:8px 0;color:#95a5a6'>Rp {int(hasil_basis):,}</h2>
                            <p style='margin:0;font-size:11px;color:#7f8c8d'>Output mentah Random Forest</p>
                        </div>""", unsafe_allow_html=True)

                    with r2:
                        st.markdown(f"""
                        <div class="metric-card" style='border:2px solid #2ecc71'>
                            <h4 style='margin:0;color:#bdc3c7;font-size:13px'>✨ Estimasi Gaji Anda</h4>
                            <h2 style='margin:8px 0;color:#2ecc71'>Rp {gaji_akhir:,}</h2>
                            <p style='margin:0;font-size:11px;color:#bdc3c7'>Setelah penyesuaian profil</p>
                        </div>""", unsafe_allow_html=True)

                    with r3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4 style='margin:0;color:#bdc3c7;font-size:13px'>📊 Rentang Negosiasi</h4>
                            <h2 style='margin:8px 0;color:#3498db;font-size:18px'>Rp {batas_bawah:,}<br>– Rp {batas_atas:,}</h2>
                            <p style='margin:0;font-size:11px;color:#7f8c8d'>±10% dari estimasi Anda</p>
                        </div>""", unsafe_allow_html=True)

                    # ── Breakdown multiplier ──
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("📋 Lihat Rincian Kalkulasi Multiplier"):
                        st.markdown(f"""
| Faktor | Pilihan | Multiplier |
|--------|---------|-----------|
| Level Pengalaman | {pilihan_level} | `×{m_level}` |
| Tipe Kontrak | {pilihan_kontrak} | `×{m_kontrak}` |
| Skala Perusahaan | {pilihan_skala} | `×{m_skala}` |
| **Total Gabungan** | — | **`×{round(total_multiplier,2)}`** |
| **Gaji Basis ML** | Rp {int(hasil_basis):,} | |
| **Hasil Akhir** | **Rp {gaji_akhir:,}** | |
                        """)
                        st.caption("_Multiplier mengacu pada data rata-rata industri & survei kompensasi Jabodetabek._")
                else:
                    st.error("Terjadi masalah saat membaca output model ML.")
    except Exception as e:
        st.error(f"Gagal memuat Model: {str(e)}. Pastikan file .pkl lengkap di folder models/")


# -------------------------------------------------------------
# TAB 2: PETA SPASIAL → VISUALISASI CHART INTERAKTIF
# -------------------------------------------------------------
with tab2:
    st.header("📊 Peta Kepadatan Lowongan Jabodetabek")
    st.write("Temukan **kota & industri** mana yang paling banyak menyerap tenaga kerja di Jabodetabek.")

    try:
        df_map = load_map_data('data/data_peta_jabodetabek.csv')

        st.markdown("---")

        # ── CHART 1: Total Lowongan Per Kota (Keseluruhan) ──────────────
        st.subheader("🏙️ Chart 1 — Kota dengan Lowongan Terbanyak")
        st.caption("Dari semua industri, inilah ranking kota di Jabodetabek berdasarkan total ketersediaan loker.")

        df_kota = (
            df_map.groupby("Lokasi_Clean")["Jumlah_Lowongan"]
            .sum()
            .sort_values(ascending=True)
            .reset_index()
        )

        fig1, ax1 = plt.subplots(figsize=(10, 5))
        fig1.patch.set_facecolor("#0e1117")
        ax1.set_facecolor("#0e1117")

        bars = ax1.barh(
            df_kota["Lokasi_Clean"],
            df_kota["Jumlah_Lowongan"],
            color=plt.cm.plasma([i / len(df_kota) for i in range(len(df_kota))]),
            edgecolor="none",
            height=0.6,
        )

        # Label angka di ujung bar
        for bar, val in zip(bars, df_kota["Jumlah_Lowongan"]):
            ax1.text(
                bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                f"{int(val):,}", va="center", ha="left",
                color="white", fontsize=9
            )

        ax1.set_xlabel("Jumlah Lowongan Aktif", color="white")
        ax1.set_ylabel("")
        ax1.tick_params(colors="white")
        ax1.xaxis.label.set_color("white")
        ax1.spines[:].set_visible(False)
        ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        plt.tight_layout()
        st.pyplot(fig1)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── CHART 2: Filter Per Industri vs Kota ──────────────────────
        st.subheader("🏭 Chart 2 — Distribusi Per Industri di Tiap Kota")
        st.caption("Pilih industri yang Anda minati, dan lihat kota mana yang paling relevan.")

        daftar_industri = sorted(df_map["Kategori_Pekerjaan"].unique().tolist())
        filter_industri = st.selectbox("Pilih Kategori Industri:", daftar_industri)

        df_industri = (
            df_map[df_map["Kategori_Pekerjaan"] == filter_industri]
            .groupby("Lokasi_Clean")["Jumlah_Lowongan"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        fig2.patch.set_facecolor("#0e1117")
        ax2.set_facecolor("#0e1117")

        colors2 = ["#FF416C" if i == 0 else "#4a90d9" for i in range(len(df_industri))]
        bars2 = ax2.bar(
            df_industri["Lokasi_Clean"],
            df_industri["Jumlah_Lowongan"],
            color=colors2,
            edgecolor="none",
            width=0.6,
        )

        # Anotasi nilai di atas bar
        for bar2, val in zip(bars2, df_industri["Jumlah_Lowongan"]):
            ax2.text(
                bar2.get_x() + bar2.get_width() / 2, bar2.get_height() + 0.5,
                f"{int(val):,}", ha="center", va="bottom",
                color="white", fontsize=9, fontweight="bold"
            )

        ax2.set_title(f"Distribusi Loker '{filter_industri}' di Tiap Kota", color="white", fontsize=12, fontweight="bold")
        ax2.set_ylabel("Jumlah Lowongan", color="white")
        ax2.set_xlabel("")
        ax2.tick_params(colors="white", axis="both")
        ax2.spines[:].set_visible(False)
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        st.pyplot(fig2)

        # Tabel Ringkas
        with st.expander("📋 Lihat Data Mentah"):
            st.dataframe(
                df_industri.rename(columns={"Lokasi_Clean": "Kota", "Jumlah_Lowongan": "Total Lowongan"})
                .reset_index(drop=True),
                use_container_width=True
            )

    except Exception as e:
        st.error(f"Gagal memuat data visualisasi: {str(e)}")

# -------------------------------------------------------------
# TAB 3: KONSULTAN KARIR AI (GROQ LLAMA-3)
# -------------------------------------------------------------
with tab3:
    st.header("Konsultan Karir Virtual 🤖")
    st.write("Tanyakan masalah wawancara Anda, bedah CV Anda, atau tips nego gaji ke ahlinya!")

    client = get_groq_client()

    if client is None:
        st.warning("⚠️ Anda Belum Memasukkan `GROQ_API_KEY` di `.streamlit/secrets.toml`. Chatbot di-nonaktifkan sementara.")
    else:
        # ── BANNER KONTEKS: Tampilkan jika user sudah melakukan prediksi ──
        prediksi_ctx = st.session_state.get("last_prediction")
        if prediksi_ctx:
            st.info(
                f"📌 **Konteks Aktif dari Prediksi Anda:**  \n"
                f"Kategori: **{prediksi_ctx['kategori']}** | Lokasi: **{prediksi_ctx['lokasi']}**  \n"
                f"Profil: {prediksi_ctx.get('level','–')} | {prediksi_ctx.get('kontrak','–')} | {prediksi_ctx.get('skala','–')}  \n"
                f"Estimasi Gaji: **Rp {prediksi_ctx['gaji_prediksi']:,}** "
                f"(Rentang: Rp {prediksi_ctx['gaji_min']:,} – Rp {prediksi_ctx['gaji_max']:,}) | "
                f"Multiplier: `×{prediksi_ctx.get('multiplier', '–')}`  \n"
                f"_AI sudah mengetahui profil ini. Silakan langsung tanya!_"
            )
        else:
            st.caption("💡 **Tips:** Jalankan Prediksi Gaji di Tab 1 terlebih dahulu agar AI bisa memberi saran yang lebih personal.")

        # ── BUILD SYSTEM PROMPT DINAMIS BERDASARKAN KONTEKS ──
        if prediksi_ctx:
            konteks_str = (
                f"Pengguna baru saja menggunakan fitur prediksi gaji dan mendapatkan hasil berikut: "
                f"Kategori pekerjaan: '{prediksi_ctx['kategori']}', lokasi: '{prediksi_ctx['lokasi']}', "
                f"estimasi gaji pasar: Rp {prediksi_ctx['gaji_prediksi']:,} per bulan "
                f"(rentang negosiasi wajar Rp {prediksi_ctx['gaji_min']:,} hingga Rp {prediksi_ctx['gaji_max']:,}). "
                f"Gunakan informasi ini sebagai konteks utama untuk semua jawaban Anda."
            )
        else:
            konteks_str = "Belum ada data prediksi gaji dari pengguna ini."

        system_prompt_dinamis = (
            "Anda adalah asisten konsultan karir profesional dan ramah yang khusus "
            "membantu pencari kerja di wilayah Jabodetabek (Indonesia). Tugas Anda menjawab pertanyaan "
            "seputar negosiasi gaji, tren industri, persiapan wawancara, dan skill set. "
            "Jawab dengan bahasa Indonesia yang santai tapi profesional. "
            "Jawaban harus ringkas, tepat sasaran (maksimal 3 paragraf), dan berikan 1-3 bullet points jika perlu. "
            f"\n\nKONTEKS PENGGUNA SAAT INI: {konteks_str}"
        )

        # ── INISIALISASI HISTORY CHAT ──
        if "messages" not in st.session_state:
            salam_awal = (
                f"Halo! Saya Konsultan Karir Virtual Anda. "
                + (f"Saya sudah melihat hasil prediksi Anda untuk posisi **{prediksi_ctx['kategori']}** di **{prediksi_ctx['lokasi']}** "
                   f"dengan estimasi gaji **Rp {prediksi_ctx['gaji_prediksi']:,}**. Ada pertanyaan seputar ini atau topik karir lainnya?"
                   if prediksi_ctx else
                   "Ada yang bisa saya bantu terkait karir Anda di Jabodetabek hari ini?")
            )
            st.session_state["messages"] = [{"role": "assistant", "content": salam_awal}]

        # ── TAMPILKAN HISTORY CHAT ──
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        # ── INPUT USER ──
        user_input = st.chat_input("Tanya seputar karir, gaji, skill, atau persiapan interview...")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)

            with st.chat_message("assistant"):
                placeholder_resp = st.empty()
                full_response = ""

                history_murni = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]

                # Kirim system prompt dinamis ke utils
                stream = chat_with_career_bot(client, user_input, history_murni, system_prompt_dinamis)

                if stream:
                    for chunk in stream:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            full_response += delta
                            placeholder_resp.markdown(full_response + "▌")
                    placeholder_resp.markdown(full_response)

            if full_response:
                st.session_state.messages.append({"role": "assistant", "content": full_response})
