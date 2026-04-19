import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utils import load_map_data

def render():
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
