import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
from utils import load_map_data, predict_kos_price, calculate_distance

def render():
    st.markdown("""
    <div style="margin-bottom:6px;">
        <h2 style="font-size:1.55rem;font-weight:800;color:#fff;margin:0 0 6px 0;">
            Peta Komparasi Karir &amp; Keterjangkauan Hunian
        </h2>
        <p style="color:rgba(255,255,255,0.45);font-size:0.9rem;margin:0;">
            Eksplorasi kuadran ketersediaan lowongan vs biaya hidup rata-rata di wilayah Jabodetabek.
        </p>
    </div>
    <hr style="border:none;border-top:1px solid rgba(255,255,255,0.07);margin:18px 0 24px 0;">
    """, unsafe_allow_html=True)

    try:
        df_map = load_map_data('data/data_peta_jabodetabek.csv')

        raw_kota = df_map.groupby("Lokasi_Clean")["Jumlah_Lowongan"].sum().reset_index()
        raw_kota["Harga_Kos_Estimasi"] = raw_kota["Lokasi_Clean"].apply(predict_kos_price)
        df_kota = raw_kota.sort_values(by="Jumlah_Lowongan", ascending=False).reset_index(drop=True)

        # ── 1. STRATEGI HUNIAN (Tetap Nomor Satu) ──
        st.markdown("""
        <div class="sec-hd">
            <div class="sec-hd-dot"></div>
            <span class="sec-hd-text">🚆 Strategi Hunian (Opsi Komuter)</span>
            <div class="sec-hd-line"></div>
        </div>
        <p style="color:rgba(255,255,255,0.38);font-size:0.82rem;margin:-8px 0 14px 0;">
            Tetap bekerja di pusat bisnis, tinggal di wilayah penyangga untuk memaksimalkan tabungan.
        </p>
        """, unsafe_allow_html=True)

        daftar_kota = sorted(df_kota['Lokasi_Clean'].tolist())
        pred_lokasi = st.session_state.get("last_prediction", {}).get("lokasi", "")
        default_loc = pred_lokasi if pred_lokasi in daftar_kota else 'Jakarta Selatan'
        idx_default = daftar_kota.index(default_loc) if default_loc in daftar_kota else 0

        lokasi_kerja = st.selectbox("Lokasi Kantor Incaran Anda", daftar_kota, index=idx_default)

        data_target = df_kota[df_kota['Lokasi_Clean'] == lokasi_kerja].iloc[0]
        kos_kerja = data_target['Harga_Kos_Estimasi']

        alternatif = df_kota[df_kota['Harga_Kos_Estimasi'] <= (kos_kerja - 50000)].sort_values(by='Harga_Kos_Estimasi', ascending=True)

        if not alternatif.empty:
            st.info(f"Jika Anda tetap bekerja di **{lokasi_kerja}**, Anda bisa menghemat banyak uang dengan tinggal di kota-kota penyangga berikut:")
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
            st.success(f"🌟 **{lokasi_kerja}** sudah merupakan wilayah dengan biaya hunian paling ekonomis!")

        with st.expander("📋 Lihat Daftar Rata-Rata Harga Kos Seluruh Wilayah"):
            st.markdown("Berikut adalah tabel perbandingan harga kos rata-rata di Jabodetabek berdasarkan prediksi model AI:")
            df_tabel = df_kota[['Lokasi_Clean', 'Harga_Kos_Estimasi']].copy()
            df_tabel = df_tabel.sort_values(by='Harga_Kos_Estimasi', ascending=True)
            df_tabel.columns = ['Wilayah', 'Estimasi Harga Sebulan']
            df_tabel['Estimasi Harga Sebulan'] = df_tabel['Estimasi Harga Sebulan'].apply(lambda x: f"Rp {x:,}")
            st.table(df_tabel)
            st.caption("⚠️ **Catatan:** Harga di atas adalah estimasi untuk *Kamar Luas 12m², Termasuk Listrik, dan Rating Tinggi*.")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 2. FILTER INDUSTRI ──
        st.markdown("""
        <div class="sec-hd">
            <div class="sec-hd-dot"></div>
            <span class="sec-hd-text">🏭 Filter Distribusi Spesifik per Industri</span>
            <div class="sec-hd-line"></div>
        </div>
        """, unsafe_allow_html=True)

        daftar_industri = sorted(df_map["Kategori_Pekerjaan"].unique().tolist())
        filter_industri = st.selectbox("Pilih Kategori Industri Spesifik", daftar_industri)

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
        bars2 = ax2.bar(df_industri["Lokasi_Clean"], df_industri["Jumlah_Lowongan"], color=colors2, width=0.6)

        for bar2, val in zip(bars2, df_industri["Jumlah_Lowongan"]):
            ax2.text(bar2.get_x() + bar2.get_width() / 2, bar2.get_height() + 0.5,
                     f"{int(val):,}", ha="center", va="bottom", color="white", fontsize=9, fontweight="bold")

        ax2.set_title(f"Loker '{filter_industri}' Terbaik", color="white", fontsize=12)
        ax2.set_ylabel("Lowongan Akumulatif", color="white")
        ax2.tick_params(colors="white", axis="both")
        ax2.spines[:].set_visible(False)
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        st.pyplot(fig2)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 3. SCATTER PLOT ──
        st.markdown("""
        <div class="sec-hd">
            <div class="sec-hd-dot"></div>
            <span class="sec-hd-text">🎯 Scatter Plot Kuadran 'Sweet Spot'</span>
            <div class="sec-hd-line"></div>
        </div>
        <p style="color:rgba(255,255,255,0.38);font-size:0.82rem;margin:-8px 0 14px 0;">
            Kanan Bawah: Loker Terbanyak &amp; Kos Murah (The Sweet Spot). Kiri Atas: Loker Sedikit &amp; Kos Mahal.
        </p>
        """, unsafe_allow_html=True)

        fig_scatter, ax_sc = plt.subplots(figsize=(10, 6))
        fig_scatter.patch.set_facecolor("#0e1117")
        ax_sc.set_facecolor("#0e1117")

        median_loker = df_kota["Jumlah_Lowongan"].median()
        median_kos = df_kota["Harga_Kos_Estimasi"].median()

        ax_sc.scatter(df_kota['Harga_Kos_Estimasi'], df_kota['Jumlah_Lowongan'],
                      color='#FF416C', s=120, alpha=0.85, edgecolors="white", linewidth=1.2)

        for idx, row in df_kota.iterrows():
            ax_sc.text(row['Harga_Kos_Estimasi'] + 10000, row['Jumlah_Lowongan'] + 50,
                       row['Lokasi_Clean'], color=(1, 1, 1, 0.7), fontsize=9)

        ax_sc.axvline(median_kos, color='#FF4B2B', linestyle='--', alpha=0.35)
        ax_sc.axhline(median_loker, color='#FF4B2B', linestyle='--', alpha=0.35)
        ax_sc.set_xlabel("Rata-Rata Biaya Kos - Prediksi ML (Rp)", color="white")
        ax_sc.set_ylabel("Total Lowongan Aktif", color="white")
        ax_sc.tick_params(colors="white")
        ax_sc.spines[:].set_visible(False)
        ax_sc.grid(True, color="#1e1e2e", linestyle='-', alpha=0.5)
        ax_sc.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"Rp{x/1e6:.1f}JT"))
        ax_sc.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, p: f"{int(y):,}"))
        plt.tight_layout()
        st.pyplot(fig_scatter)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 4. CHART OVERLAY (Terakhir) ──
        st.markdown("""
        <div class="sec-hd">
            <div class="sec-hd-dot"></div>
            <span class="sec-hd-text">📈 Chart Overlay: Volume Pekerjaan &amp; Inflasi Harga Sewa</span>
            <div class="sec-hd-line"></div>
        </div>
        <p style="color:rgba(255,255,255,0.38);font-size:0.82rem;margin:-8px 0 14px 0;">
            Bar = ketersediaan loker. Garis oranye = inflasi biaya kos per bulan.
        </p>
        """, unsafe_allow_html=True)

        fig_dual, ax_bar = plt.subplots(figsize=(10, 5))
        fig_dual.patch.set_facecolor("#0e1117")
        ax_bar.set_facecolor("#0e1117")

        ax_bar.bar(df_kota["Lokasi_Clean"], df_kota["Jumlah_Lowongan"], color="#4a90d9", width=0.6)
        ax_bar.set_ylabel("Jumlah Lowongan", color="#4a90d9", fontweight='bold')
        ax_bar.tick_params(axis='y', colors="#4a90d9")
        ax_bar.tick_params(axis='x', colors="white", rotation=30)

        ax_line = ax_bar.twinx()
        ax_line.plot(df_kota["Lokasi_Clean"], df_kota["Harga_Kos_Estimasi"],
                     color="#FF416C", marker='o', linewidth=2.5, markersize=8)
        ax_line.set_ylabel("Estimasi Biaya Kos (Rp)", color="#FF416C", fontweight='bold')
        ax_line.tick_params(axis='y', colors="#FF416C")
        ax_line.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"Rp{x/1e6:.1f}JT"))

        ax_bar.spines[:].set_visible(False)
        ax_line.spines[:].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig_dual)

    except Exception as e:
        st.error(f"Gagal memuat data visualisasi: {str(e)}")
