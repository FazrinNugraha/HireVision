import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
from utils import load_map_data, predict_kos_price, calculate_distance

def render():
    st.header("📊 Peta Komparasi Karir & Keterjangkauan Hunian")
    st.write("Eksplorasi **kuadran ketersediaan lowongan vs biaya hidup rata-rata** di wilayah Jabodetabek.")

    try:
        df_map = load_map_data('data/data_peta_jabodetabek.csv')

        # Siapkan data aggregat per kota
        raw_kota = df_map.groupby("Lokasi_Clean")["Jumlah_Lowongan"].sum().reset_index()
        
        # Injeksi prediksi harga Kos per kota (gunakan fitur ML kita)
        raw_kota["Harga_Kos_Estimasi"] = raw_kota["Lokasi_Clean"].apply(predict_kos_price)
        
        # Sort untuk konsistensi line chart (Berdasarkan jumlah lowongan turun)
        df_kota = raw_kota.sort_values(by="Jumlah_Lowongan", ascending=False).reset_index(drop=True)

        st.markdown("---")

        # ── 1. STRATEGI HUNIAN (OPSI KOMUTER) ──────────
        st.subheader("🚆 Strategi Hunian (Opsi Komuter)")
        st.caption("Gunakan strategi komuter: Tetap bekera di pusat bisnis (kantor), namun tinggal di wilayah penyangga untuk memaksimalkan tabungan uang kos.")
        
        # Sinkronisasi Otomatis dari Tab Prediksi Gaji
        daftar_kota = sorted(df_kota['Lokasi_Clean'].tolist())
        pred_lokasi = st.session_state.get("last_prediction", {}).get("lokasi", "")
        default_loc = pred_lokasi if pred_lokasi in daftar_kota else 'Jakarta Selatan'
        idx_default = daftar_kota.index(default_loc) if default_loc in daftar_kota else 0
        
        lokasi_kerja = st.selectbox("Lokasi Kantor Incaran Anda:", daftar_kota, index=idx_default)
        
        # Cari data target (Tempat Kerja)
        data_target = df_kota[df_kota['Lokasi_Clean'] == lokasi_kerja].iloc[0]
        kos_kerja = data_target['Harga_Kos_Estimasi']
        
        # Cari pilihan tempat tinggal: Yang lebih murah minimal Rp 50.000
        alternatif = df_kota[df_kota['Harga_Kos_Estimasi'] <= (kos_kerja - 50000)].sort_values(by='Harga_Kos_Estimasi', ascending=True)
        
        if not alternatif.empty:
            st.info(f"Jika Anda tetap bekerja di **{lokasi_kerja}**, Anda bisa menghemat banyak uang dengan tinggal di kota-kota penyangga berikut:")
            
            # Tampilkan top 3 alternatif
            cols = st.columns(min(3, len(alternatif)))
            for i, (idx, row) in enumerate(alternatif.head(3).iterrows()):
                hemat_rupiah = kos_kerja - row['Harga_Kos_Estimasi']
                jarak_km = calculate_distance(lokasi_kerja, row['Lokasi_Clean'])
                
                # Estimasi waktu (asumsi rata-rata 25km/jam di Jabodetabek sibuk)
                jam = jarak_km / 25
                menit = int(jam * 60)
                
                with cols[i]:
                    st.markdown(f"""
                    <div style="background-color: #1a472a; color: #d4edda; padding: 15px; border-radius: 5px; border: 1px solid #2ecc71; margin-bottom: 20px;">
                        <div style="font-weight: bold; font-size: 16px; margin-bottom: 10px;">🏠 Kost di {row['Lokasi_Clean']}</div>
                        <div style="font-weight: bold; font-size: 18px; margin-bottom: 10px; color: #ffffff;">💰 Hemat: Rp {int(hemat_rupiah):,}/bln</div>
                        <div style="margin-bottom: 8px;">
                            <span style="background-color: #3498db; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 13px;">📍 Jarak: ±{jarak_km} KM</span>
                        </div>
                        <div>
                            <span style="background-color: #e67e22; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 13px;">⏱️ Estimasi: ~{menit} menit</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success(f"🌟 **{lokasi_kerja}** sudah merupakan wilayah dengan biaya hunian paling ekonomis. Tidak perlu melirik opsi komuter dari kota lain!")

        # ── Rincian Harga Seluruh Wilayah (Expander) ──────────
        with st.expander("📋 Lihat Daftar Rata-Rata Harga Kos Seluruh Wilayah"):
            st.markdown("Berikut adalah tabel perbandingan harga kos rata-rata di Jabodetabek berdasarkan prediksi model AI:")
            
            # Buat DataFrame sederhana untuk tabel
            df_tabel = df_kota[['Lokasi_Clean', 'Harga_Kos_Estimasi']].copy()
            df_tabel = df_tabel.sort_values(by='Harga_Kos_Estimasi', ascending=True)
            df_tabel.columns = ['Wilayah', 'Estimasi Harga Sebulan']
            
            # Format ke Rupiah untuk tampilan tabel
            df_tabel['Estimasi Harga Sebulan'] = df_tabel['Estimasi Harga Sebulan'].apply(lambda x: f"Rp {x:,}")
            
            st.table(df_tabel)
            st.caption("⚠️ **Catatan:** Harga di atas adalah estimasi untuk *Kamar Luas 12m², Termasuk Listrik, dan Rating Tinggi*.")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 2. SCATTER PLOT THE SWEET SPOT ──────────
        st.subheader("🎯 Scatter Plot Kuadran 'Sweet Spot'")
        st.caption("Kuadran Kanan Bawah: Loker Terbanyak & Kos Murah (The Sweet Spot). Kuadran Kiri Atas: Loker Sedikit & Kos Mahal.")
        
        fig_scatter, ax_sc = plt.subplots(figsize=(10, 6))
        fig_scatter.patch.set_facecolor("#0e1117")
        ax_sc.set_facecolor("#0e1117")
        
        # Calculate Medians to draw quadrants
        median_loker = df_kota["Jumlah_Lowongan"].median()
        median_kos = df_kota["Harga_Kos_Estimasi"].median()

        ax_sc.scatter(df_kota['Harga_Kos_Estimasi'], df_kota['Jumlah_Lowongan'], color='#00d2ff', s=100, alpha=0.8, edgecolors="white", linewidth=1.5)
        
        # Annotate labels
        for idx, row in df_kota.iterrows():
            ax_sc.text(row['Harga_Kos_Estimasi'] + 10000, row['Jumlah_Lowongan'] + 50, row['Lokasi_Clean'], color='white', fontsize=9)
            
        # Draw Quadrant lines
        ax_sc.axvline(median_kos, color='#ff4b4b', linestyle='--', alpha=0.4)
        ax_sc.axhline(median_loker, color='#ff4b4b', linestyle='--', alpha=0.4)

        ax_sc.set_xlabel("Rata-Rata Biaya Kos - Prediksi ML (Rp)", color="white")
        ax_sc.set_ylabel("Total Lowongan Aktif", color="white")
        
        ax_sc.tick_params(colors="white")
        ax_sc.xaxis.label.set_color("white")
        ax_sc.yaxis.label.set_color("white")
        ax_sc.spines[:].set_visible(False)
        ax_sc.grid(True, color="#333333", linestyle='-', alpha=0.3)
        ax_sc.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"Rp{x/1e6:.1f}JT"))
        ax_sc.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, p: f"{int(y):,}"))
        
        plt.tight_layout()
        st.pyplot(fig_scatter)
        st.markdown("<br>", unsafe_allow_html=True)

        # ── 3. DUAL-AXIS BAR CHART ──────────
        st.subheader("📈 Chart Overlay: Volume Pekerjaan & Inflasi Harga Sewa")
        st.caption("Grafik Bar menunjukkan ketersediaan loker. Garis Orange menunjukkan tajamnya inflasi biaya kos per bulan.")

        fig_dual, ax_bar = plt.subplots(figsize=(10, 5))
        fig_dual.patch.set_facecolor("#0e1117")
        ax_bar.set_facecolor("#0e1117")
        
        # Bar Chart untuk Lowongan
        bars = ax_bar.bar(df_kota["Lokasi_Clean"], df_kota["Jumlah_Lowongan"], color="#4a90d9", width=0.6)
        ax_bar.set_ylabel("Jumlah Lowongan", color="#4a90d9", fontweight='bold')
        ax_bar.tick_params(axis='y', colors="#4a90d9")
        ax_bar.tick_params(axis='x', colors="white", rotation=30)
        
        # Line Chart untuk Harga Kos (Secondary Axis)
        ax_line = ax_bar.twinx()
        line = ax_line.plot(df_kota["Lokasi_Clean"], df_kota["Harga_Kos_Estimasi"], color="#f39c12", marker='o', linewidth=2.5, markersize=8)
        ax_line.set_ylabel("Estimasi Biaya Kos (Rp)", color="#f39c12", fontweight='bold')
        ax_line.tick_params(axis='y', colors="#f39c12")
        ax_line.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"Rp{x/1e6:.1f}JT"))
        
        # Styling
        ax_bar.spines[:].set_visible(False)
        ax_line.spines[:].set_visible(False)
        ax_bar.spines['left'].set_visible(True)
        ax_bar.spines['left'].set_color('#333')
        plt.tight_layout()
        st.pyplot(fig_dual)
        
        st.markdown("<br><hr>", unsafe_allow_html=True)

        # ── 4. FILTER INDUSTRI (KONTEN ASLI) ──────────
        st.subheader("🏭 Filter Distribusi Spesifik per Industri")
        daftar_industri = sorted(df_map["Kategori_Pekerjaan"].unique().tolist())
        filter_industri = st.selectbox("Pilih Kategori Industri Spesifik:", daftar_industri)

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

        colors2 = ["#FF416C" if i == 0 else "#2ecc71" for i in range(len(df_industri))]
        bars2 = ax2.bar(df_industri["Lokasi_Clean"], df_industri["Jumlah_Lowongan"], color=colors2, width=0.6)

        for bar2, val in zip(bars2, df_industri["Jumlah_Lowongan"]):
            ax2.text(bar2.get_x() + bar2.get_width() / 2, bar2.get_height() + 0.5, f"{int(val):,}", ha="center", va="bottom", color="white", fontsize=9, fontweight="bold")

        ax2.set_title(f"Loker '{filter_industri}' Terbaik", color="white", fontsize=12)
        ax2.set_ylabel("Lowongan Akumulatif", color="white")
        ax2.tick_params(colors="white", axis="both")
        ax2.spines[:].set_visible(False)
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        st.pyplot(fig2)

    except Exception as e:
        st.error(f"Gagal memuat data visualisasi: {str(e)}")
