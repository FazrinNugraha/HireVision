"""
Tab Spatial Map - HireVision
================================
Modul ini bertanggung jawab untuk:
1. Filter distribusi lowongan per industri/kategori
2. Visualisasi feature importance model Random Forest
3. Scatter plot "sweet spot" (loker vs biaya kos)
4. Chart overlay bar + line (volume loker vs inflasi sewa)
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import streamlit as st

from utils import load_map_data, load_ml_resources, predict_kos_price


BG_COLOR = "#0e1117"
ACCENT_COLOR = "#FF416C"
ACCENT_SECONDARY = "#FF4B2B"
BLUE_COLOR = "#4a90d9"
GRID_COLOR = "#1e1e2e"


def _render_header():
    """Render judul utama + deskripsi tab."""
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


def _section_header(text: str, subtitle: str | None = None):
    """Render section header dengan dot + line + optional subtitle."""
    st.markdown(f"""
<div class="sec-hd">
    <div class="sec-hd-dot"></div>
    <span class="sec-hd-text">{text}</span>
    <div class="sec-hd-line"></div>
</div>
""", unsafe_allow_html=True)
    if subtitle:
        st.markdown(
            f'<p style="color:rgba(255,255,255,0.38);font-size:0.82rem;margin:-8px 0 14px 0;">{subtitle}</p>',
            unsafe_allow_html=True,
        )


def _setup_dark_axes(fig, ax):
    """Styling standar: background gelap, spine transparan, tick putih."""
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.tick_params(colors="white", axis="both")
    ax.spines[:].set_visible(False)


def _load_data_kota(df_map: pd.DataFrame) -> pd.DataFrame:
    """Agregasi total lowongan per kota + prediksi harga kos."""
    df_kota = df_map.groupby("Lokasi_Clean")["Jumlah_Lowongan"].sum().reset_index()
    df_kota["Harga_Kos_Estimasi"] = df_kota["Lokasi_Clean"].apply(predict_kos_price)
    return df_kota.sort_values(by="Jumlah_Lowongan", ascending=False).reset_index(drop=True)


def _render_filter_industri(df_map: pd.DataFrame):
    """Render dropdown filter industri + bar chart distribusi per kota."""
    _section_header("🏭 Filter Distribusi Spesifik per Industri")

    daftar_industri = sorted(df_map["Kategori_Pekerjaan"].unique().tolist())
    filter_industri = st.selectbox("Pilih Kategori Industri Spesifik", daftar_industri)

    df_industri = (
        df_map[df_map["Kategori_Pekerjaan"] == filter_industri]
        .groupby("Lokasi_Clean")["Jumlah_Lowongan"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 4))
    _setup_dark_axes(fig, ax)

    colors = [ACCENT_COLOR if i == 0 else BLUE_COLOR for i in range(len(df_industri))]
    bars = ax.bar(df_industri["Lokasi_Clean"], df_industri["Jumlah_Lowongan"], color=colors, width=0.6)

    for bar, val in zip(bars, df_industri["Jumlah_Lowongan"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{int(val):,}",
            ha="center",
            va="bottom",
            color="white",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_title(f"Loker '{filter_industri}' Terbaik", color="white", fontsize=12)
    ax.set_ylabel("Lowongan Akumulatif", color="white")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    st.pyplot(fig)


def _compute_feature_importance(resources: dict) -> pd.DataFrame:
    """Agregasi feature importance model Random Forest ke 4 grup utama."""
    model = resources["model"]
    tfidf_word = resources["tfidf_word"]
    tfidf_char = resources["tfidf_char"]
    ohe_encoder = resources["ohe_encoder"]

    importances = model.feature_importances_
    n_word = len(tfidf_word.vocabulary_)
    n_char = len(tfidf_char.vocabulary_)
    n_target = 1
    n_extra = 3

    ohe_names = ohe_encoder.get_feature_names_out(["Lokasi_Clean", "Kategori_Pekerjaan", "Senioritas"])
    ohe_names = ohe_names[:-3]

    imp_judul = float(importances[: n_word + n_char].sum())
    imp_target = float(importances[n_word + n_char : n_word + n_char + n_target + n_extra].sum())
    imp_ohe_start = n_word + n_char + n_target + n_extra

    imp_lokasi = sum(
        importances[imp_ohe_start + i]
        for i, col in enumerate(ohe_names)
        if col.startswith("Lokasi_Clean")
    )
    imp_kategori = sum(
        importances[imp_ohe_start + i]
        for i, col in enumerate(ohe_names)
        if col.startswith("Kategori_Pekerjaan")
    )

    total = imp_judul + imp_target + imp_lokasi + imp_kategori
    if total > 0:
        imp_judul /= total
        imp_target /= total
        imp_lokasi /= total
        imp_kategori /= total

    return pd.DataFrame(
        {
            "Fitur": ["Judul Pekerjaan", "Kategori Pekerjaan", "Lokasi", "Target Encoding"],
            "Kepentingan": [imp_judul, imp_kategori, imp_lokasi, imp_target],
        }
    ).sort_values(by="Kepentingan", ascending=True)


def _render_feature_importance():
    """Render section AI Market Logic dengan horizontal bar chart."""
    _section_header(
        "🧠 AI Market Logic: Penentu Gaji Terbesar",
        subtitle="Grafik ini menjelaskan bobot kepentingan fitur yang digunakan model Machine Learning kami dalam menentukan prediksi gaji.",
    )

    try:
        resources, _, _, _ = load_ml_resources()
        df_imp = _compute_feature_importance(resources)

        fig, ax = plt.subplots(figsize=(10, 3))
        _setup_dark_axes(fig, ax)

        bars = ax.barh(df_imp["Fitur"], df_imp["Kepentingan"], color=ACCENT_COLOR, height=0.4)
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.1%}",
                ha="left",
                va="center",
                color="white",
                fontweight="bold",
            )

        ax.set_xlabel("Bobot Pengaruh", color="white")
        ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
        plt.tight_layout()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Gagal memuat visualisasi feature importance: {str(e)}")


def _render_scatter_sweetspot(df_kota: pd.DataFrame):
    """Render scatter plot kuadran loker vs biaya kos."""
    _section_header(
        "🎯 Scatter Plot Kuadran Sweet Spot",
        subtitle="Kanan bawah: loker terbanyak dan kos murah. Kiri atas: loker sedikit dan kos mahal.",
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    _setup_dark_axes(fig, ax)

    median_loker = df_kota["Jumlah_Lowongan"].median()
    median_kos = df_kota["Harga_Kos_Estimasi"].median()

    ax.scatter(
        df_kota["Harga_Kos_Estimasi"],
        df_kota["Jumlah_Lowongan"],
        color=ACCENT_COLOR,
        s=120,
        alpha=0.85,
        edgecolors="white",
        linewidth=1.2,
    )

    for _, row in df_kota.iterrows():
        ax.text(
            row["Harga_Kos_Estimasi"] + 10000,
            row["Jumlah_Lowongan"] + 50,
            row["Lokasi_Clean"],
            color=(1, 1, 1, 0.7),
            fontsize=9,
        )

    ax.axvline(median_kos, color=ACCENT_SECONDARY, linestyle="--", alpha=0.35)
    ax.axhline(median_loker, color=ACCENT_SECONDARY, linestyle="--", alpha=0.35)

    ax.set_xlabel("Rata-Rata Biaya Kos - Prediksi ML (Rp)", color="white")
    ax.set_ylabel("Total Lowongan Aktif", color="white")
    ax.grid(True, color=GRID_COLOR, linestyle="-", alpha=0.5)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"Rp{x/1e6:.1f}JT"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, p: f"{int(y):,}"))
    plt.tight_layout()
    st.pyplot(fig)


def _render_chart_overlay(df_kota: pd.DataFrame):
    """Render dual-axis chart: bar lowongan + line harga kos."""
    _section_header(
        "📈 Chart Overlay: Volume Pekerjaan dan Inflasi Harga Sewa",
        subtitle="Bar = ketersediaan loker. Garis merah = inflasi biaya kos per bulan.",
    )

    fig, ax_bar = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(BG_COLOR)
    ax_bar.set_facecolor(BG_COLOR)

    ax_bar.bar(df_kota["Lokasi_Clean"], df_kota["Jumlah_Lowongan"], color=BLUE_COLOR, width=0.6)
    ax_bar.set_ylabel("Jumlah Lowongan", color=BLUE_COLOR, fontweight="bold")
    ax_bar.tick_params(axis="y", colors=BLUE_COLOR)
    ax_bar.tick_params(axis="x", colors="white", rotation=30)

    ax_line = ax_bar.twinx()
    ax_line.plot(
        df_kota["Lokasi_Clean"],
        df_kota["Harga_Kos_Estimasi"],
        color=ACCENT_COLOR,
        marker="o",
        linewidth=2.5,
        markersize=8,
    )
    ax_line.set_ylabel("Estimasi Biaya Kos (Rp)", color=ACCENT_COLOR, fontweight="bold")
    ax_line.tick_params(axis="y", colors=ACCENT_COLOR)
    ax_line.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"Rp{x/1e6:.1f}JT"))

    ax_bar.spines[:].set_visible(False)
    ax_line.spines[:].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)


def render():
    """Entry point tab untuk orkestrasi semua komponen."""
    _render_header()

    try:
        df_map = load_map_data("data/data_peta_jabodetabek.csv")
        df_kota = _load_data_kota(df_map)

        _render_filter_industri(df_map)
        st.markdown("<br>", unsafe_allow_html=True)

        _render_feature_importance()
        st.markdown("<br>", unsafe_allow_html=True)

        _render_scatter_sweetspot(df_kota)
        st.markdown("<br>", unsafe_allow_html=True)

        _render_chart_overlay(df_kota)

    except Exception as e:
        st.error(f"Gagal memuat data visualisasi: {str(e)}")
