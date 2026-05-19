import streamlit as st

from tabs.predict_salary.layout import render_section_gap, render_section_header
from utils import calculate_distance, load_map_data, predict_kos_price


def get_warna_rasio_kos(rasio):
    """Tentukan skema warna berdasarkan rasio biaya kos vs gaji."""
    if rasio <= 30:
        return {
            "bg": "linear-gradient(135deg, rgba(46,204,113,0.12), rgba(39,174,96,0.06))",
            "border": "rgba(46,204,113,0.32)",
            "title": "rgba(180,255,180,0.7)",
            "val": "#2ecc71",
        }
    if rasio <= 50:
        return {
            "bg": "linear-gradient(135deg, rgba(241,196,15,0.12), rgba(243,156,18,0.06))",
            "border": "rgba(241,196,15,0.32)",
            "title": "rgba(255,230,180,0.7)",
            "val": "#f1c40f",
        }
    return {
        "bg": "linear-gradient(135deg, rgba(231,76,60,0.12), rgba(192,57,43,0.06))",
        "border": "rgba(231,76,60,0.32)",
        "title": "rgba(255,180,180,0.7)",
        "val": "#e74c3c",
    }


def render_hasil_card(res):
    """Render kartu utama estimasi gaji."""
    render_section_header("Hasil Estimasi Gaji")
    warna = get_warna_rasio_kos(res["rasio_kos"])

    st.markdown(
        f"""
<style>
.salary-result-card {{
    background:{warna['bg']};
    border:1px solid {warna['border']};
    border-radius:20px;
    padding:32px 36px;
    text-align:center;
    margin-bottom:16px;
    overflow:hidden;
}}
.salary-result-value {{
    margin:0 0 8px 0;
    color:{warna['val']};
    font-size:2.8rem;
    font-weight:800;
    letter-spacing:0;
    line-height:1.12;
    overflow-wrap:anywhere;
}}
@media (max-width: 768px) {{
    .salary-result-card {{
        border-radius:16px;
        padding:24px 18px;
    }}
    .salary-result-value {{
        font-size:2.15rem;
    }}
}}
@media (max-width: 420px) {{
    .salary-result-value {{
        font-size:1.85rem;
    }}
}}
</style>
<div class="salary-result-card">
    <p style="margin:0 0 6px 0;color:{warna['title']};font-size:13px;font-weight:700;letter-spacing:1px;text-transform:uppercase;">Estimasi Gaji Anda</p>
    <h1 class="salary-result-value">Rp {res['gaji_prediksi']:,}</h1>
</div>""",
        unsafe_allow_html=True,
    )
    st.caption(
        "Catatan: Estimasi ini dihasilkan oleh sistem berbasis Decision Support System (DSS) "
        "yang menggabungkan model prediksi dan penyesuaian realistis. Nilai yang ditampilkan "
        "bersifat estimasi pendukung keputusan, sehingga tidak selalu sama dengan angka final "
        "yang ditawarkan oleh setiap perusahaan."
    )


def render_analisis_hunian(res):
    """Render section analisis keterjangkauan hunian + rasio gaji."""
    rasio = res["rasio_kos"]
    sisa_gaji = res["gaji_prediksi"] - res["estimasi_kos"]

    if rasio <= 30:
        status = {
            "label": "IDEAL",
            "color": "#2ecc71",
            "bg": "linear-gradient(160deg, rgba(46,204,113,0.14), rgba(16,24,24,0.18))",
            "border": "rgba(46,204,113,0.30)",
            "desc": f"Biaya hunian ideal ({rasio:.1f}% dari gaji). Gaji Anda cukup untuk hidup nyaman di lokasi ini.",
        }
    elif rasio <= 50:
        status = {
            "label": "PERLU PERTIMBANGAN",
            "color": "#f1c40f",
            "bg": "linear-gradient(160deg, rgba(241,196,15,0.14), rgba(28,20,10,0.18))",
            "border": "rgba(241,196,15,0.30)",
            "desc": f"Biaya hunian cukup tinggi ({rasio:.1f}% dari gaji). Pertimbangkan kos yang lebih efisien atau berbagi tempat tinggal.",
        }
    else:
        status = {
            "label": "BERAT",
            "color": "#e74c3c",
            "bg": "linear-gradient(160deg, rgba(231,76,60,0.14), rgba(30,16,18,0.18))",
            "border": "rgba(231,76,60,0.30)",
            "desc": f"Beban biaya hidup cukup berat ({rasio:.1f}% dari gaji). Sebaiknya pertimbangkan wilayah penyangga atau strategi komuter.",
        }

    st.markdown(
        f"""
<style>
.housing-card {{
    background: {status['bg']};
    border: 1px solid {status['border']};
    box-shadow: 0 14px 30px rgba(0,0,0,0.22);
    border-radius: 18px;
    padding: 20px 22px 18px 22px;
    margin-top: 8px;
    overflow: hidden;
    max-width: 100%;
}}
.housing-title-row {{
    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom:12px;
}}
.housing-title-dot {{
    width:12px;
    height:12px;
    border-radius:999px;
    background: linear-gradient(135deg, #FF416C, #FF4B2B);
    flex-shrink:0;
}}
.housing-title-text {{
    color:#ffffff;
    font-size:1.1rem;
    font-weight:800;
    letter-spacing:-0.3px;
}}
.housing-divider-top {{
    height:1px;
    background:rgba(255,255,255,0.07);
    margin-bottom:18px;
}}
.housing-layout {{
    display: grid;
    grid-template-columns: 1.15fr 0.85fr;
    gap: 22px;
}}
.housing-main {{
    padding: 6px 4px 6px 4px;
}}
.housing-side {{
    padding: 6px 0 6px 22px;
    border-left: 1px solid rgba(255,255,255,0.07);
}}
.housing-chip {{
    display: inline-flex;
    align-items: center;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(0,0,0,0.16);
    border: 1px solid {status['border']};
    color: {status['color']};
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.7px;
}}
.housing-stat {{
    padding: 18px 0;
    border-top: 1px solid rgba(255,255,255,0.06);
}}
.housing-stat:first-child {{
    border-top: none;
    padding-top: 0;
}}
.housing-stat:last-child {{
    padding-bottom: 0;
}}
.housing-bar {{
    height: 8px;
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 8px;
    margin-bottom: 14px;
}}
.housing-bar-fill {{
    width: {min(max(rasio, 0), 100)}%;
    height: 100%;
    background: linear-gradient(90deg, {status['color']}99, {status['color']});
    border-radius: 999px;
}}
.housing-kicker {{
    margin:0 0 8px 0;
    font-size:11px;
    color:rgba(255,255,255,0.42);
    text-transform:uppercase;
    letter-spacing:0.8px;
}}
.housing-big-value {{
    margin:0 0 10px 0;
    color:#ffffff;
    font-size:2.8rem;
    line-height:1;
    font-weight:800;
    letter-spacing:0;
    overflow-wrap:anywhere;
}}
.housing-body-copy {{
    margin:0 0 18px 0;
    font-size:13px;
    color:rgba(255,255,255,0.55);
    line-height:1.65;
}}
.housing-range-row {{
    display:flex;
    justify-content:space-between;
    gap:12px;
    flex-wrap:wrap;
    margin-top:16px;
}}
.housing-range-row span {{
    font-size:12px;
}}
.housing-desc {{
    margin:14px 0 0 0;
    font-size:13px;
    color:rgba(255,255,255,0.60);
    line-height:1.65;
}}
.housing-side-title {{
    margin:0 0 10px 0;
    font-size:11px;
    color:rgba(255,255,255,0.42);
    text-transform:uppercase;
    letter-spacing:0.8px;
}}
.housing-side-divider {{
    height:1px;
    background:rgba(255,255,255,0.07);
    margin-bottom:10px;
}}
.housing-stat-row {{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:16px;
}}
.housing-stat-label {{
    margin:0;
    font-size:11px;
    color:rgba(255,255,255,0.50);
    text-transform:uppercase;
    letter-spacing:0.6px;
}}
.housing-stat-value {{
    margin:0;
    font-size:1.08rem;
    font-weight:800;
    color:#ffffff;
    text-align:right;
    overflow-wrap:anywhere;
}}
@media (max-width: 900px) {{
    .housing-layout {{
        grid-template-columns: 1fr;
    }}
    .housing-side {{
        border-left: none;
        border-top: 1px solid rgba(255,255,255,0.06);
        padding: 18px 4px 4px 4px;
    }}
    .housing-big-value {{
        font-size:2.3rem;
    }}
}}
@media (max-width: 520px) {{
    .housing-card {{
        border-radius:14px;
        padding:16px 14px;
    }}
    .housing-title-text {{
        font-size:1rem;
        line-height:1.35;
    }}
    .housing-big-value {{
        font-size:1.95rem;
        line-height:1.12;
    }}
    .housing-range-row {{
        gap:8px;
    }}
    .housing-stat-row {{
        align-items:flex-start;
    }}
    .housing-stat-value {{
        font-size:0.98rem;
    }}
}}
</style>
<div class="housing-card">
<div class="housing-title-row">
<div class="housing-title-dot"></div>
<div class="housing-title-text">Analisis Keterjangkauan Hunian</div>
</div>
<div class="housing-divider-top"></div>
<div class="housing-layout">
<div class="housing-main">
<p class="housing-kicker">Estimasi Biaya Kos Bulanan</p>
<h2 class="housing-big-value">Rp {res['estimasi_kos']:,}</h2>
<p class="housing-body-copy">Perkiraan biaya hunian di {res['lokasi']}, berdasarkan profil lokasi Anda.</p>
<div class="housing-chip">{status['label']}</div>
<div style="margin-top:18px;">
<div class="housing-range-row">
<span style="color:rgba(255,255,255,0.62);">0% Gaji</span>
<span style="color:{status['color']};font-weight:700;">{rasio:.1f}% Gaji Anda</span>
<span style="color:rgba(255,255,255,0.62);">100% Gaji</span>
</div>
<div class="housing-bar">
<div class="housing-bar-fill"></div>
</div>
</div>
<p class="housing-desc">{status['desc']}</p>
</div>
<div class="housing-side">
<p class="housing-side-title">Detail Keuangan</p>
<div class="housing-side-divider"></div>
<div class="housing-stat">
<div class="housing-stat-row">
<p class="housing-stat-label">Estimasi Gaji</p>
<p class="housing-stat-value">Rp {res['gaji_prediksi']:,}</p>
</div>
</div>
<div class="housing-stat">
<div class="housing-stat-row">
<p class="housing-stat-label">Biaya Kos</p>
<p class="housing-stat-value">Rp {res['estimasi_kos']:,}</p>
</div>
</div>
<div class="housing-stat">
<div class="housing-stat-row">
<p class="housing-stat-label">Sisa Setelah Kos</p>
<p class="housing-stat-value" style="color:{status['color']};">Rp {sisa_gaji:,}</p>
</div>
</div>
</div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_strategi_komuter(res):
    """Render opsi komuter ke wilayah penyangga + tabel harga kos semua wilayah."""
    render_section_gap("md")
    st.markdown(
        """
<div class="sec-hd">
    <div class="sec-hd-dot"></div>
    <span class="sec-hd-text">Pilihan Tempat Tinggal (Opsi Komuter)</span>
    <div class="sec-hd-line"></div>
</div>
<p style="color:rgba(255,255,255,0.38);font-size:0.82rem;margin:-8px 0 14px 0;">
    Tinggal di wilayah kota lain di jabodetabekk untuk menghemat biaya hidup bulanan sambil tetap bekerja di pusat bisnis.
</p>
""",
        unsafe_allow_html=True,
    )

    df_map = load_map_data("data/data_peta_jabodetabek.csv")
    df_kota = df_map.groupby("Lokasi_Clean")["Jumlah_Lowongan"].sum().reset_index()
    df_kota["Harga_Kos_Estimasi"] = df_kota["Lokasi_Clean"].apply(predict_kos_price)
    df_kota = df_kota.sort_values(by="Jumlah_Lowongan", ascending=False).reset_index(
        drop=True
    )

    lokasi_kerja = res["lokasi"]
    kos_kerja = res["estimasi_kos"]

    alternatif = df_kota[
        df_kota["Harga_Kos_Estimasi"] <= (kos_kerja - 50000)
    ].sort_values(by="Harga_Kos_Estimasi", ascending=True)

    if alternatif.empty:
        st.success(
            f"**{lokasi_kerja}** sudah merupakan wilayah dengan biaya hunian paling ekonomis. Anda tidak perlu pindah lokasi kos."
        )
    else:
        st.info(
            f"Anda bisa menghemat uang jika tinggal di kota-kota penyangga berikut dan komuter ke **{lokasi_kerja}**:"
        )
        cols = st.columns(min(3, len(alternatif)))
        for i, (_, row) in enumerate(alternatif.head(3).iterrows()):
            hemat = kos_kerja - row["Harga_Kos_Estimasi"]
            jarak_km = calculate_distance(lokasi_kerja, row["Lokasi_Clean"])
            menit = int((jarak_km / 25) * 60)

            with cols[i]:
                st.markdown(
                    f"""
<div class="komuter-card">
    <div style="font-weight:700;font-size:15px;color:#fff;margin-bottom:10px;">Kost di {row['Lokasi_Clean']}</div>
    <div style="font-weight:800;font-size:1.2rem;color:#2ecc71;margin-bottom:12px;">Hemat Rp {int(hemat):,}/bln</div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <span style="background:rgba(52,152,219,0.2);border:1px solid rgba(52,152,219,0.4);color:#5dade2;padding:3px 10px;border-radius:6px;font-size:12px;font-weight:600;">Jarak +/-{jarak_km} KM</span>
        <span style="background:rgba(230,126,34,0.2);border:1px solid rgba(230,126,34,0.4);color:#f0a500;padding:3px 10px;border-radius:6px;font-size:12px;font-weight:600;">Waktu ~{menit} mnt</span>
    </div>
</div>
""",
                    unsafe_allow_html=True,
                )

    with st.expander("Lihat Daftar Rata-Rata Harga Kos Seluruh Wilayah"):
        st.markdown(
            "Berikut adalah tabel perbandingan harga kos rata-rata di Jabodetabek berdasarkan prediksi model AI:"
        )
        df_tabel = df_kota[["Lokasi_Clean", "Harga_Kos_Estimasi"]].copy()
        df_tabel = df_tabel.sort_values(by="Harga_Kos_Estimasi", ascending=True)
        df_tabel.columns = ["Wilayah", "Estimasi Harga Sebulan"]
        df_tabel["Estimasi Harga Sebulan"] = df_tabel["Estimasi Harga Sebulan"].apply(
            lambda x: f"Rp {x:,}"
        )
        st.table(df_tabel)
        st.caption(
            "**Catatan:** Harga di atas adalah estimasi untuk *kamar luas 12m2, termasuk listrik, dan rating tinggi*."
        )


def render_cta_ai_consultant():
    """Render banner ajakan ke tab AI Consultant."""
    st.markdown(
        """
<div style="background:linear-gradient(135deg,rgba(93,173,226,0.08),rgba(52,152,219,0.04));border:1px solid rgba(93,173,226,0.25);border-radius:14px;padding:18px 22px;margin-top:14px;display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
    <div style="flex:1;min-width:200px;">
        <p style="margin:0;font-size:16px;font-weight:900;color:#fff;">Mau konsultasi mengenai karir anda di Jabodetabek?</p>
        <p style="margin:4px 0 0 0;font-size:13px;color:rgba(255,255,255,0.5);">Tanyakan target negosiasi, tips interview, atau strategi karir ke AI Consultant Career Virtual kita</p>
    </div>
    <div style="font-size:14px;font-weight:700;color:#5dade2;white-space:nowrap;">Buka Tab AI Consultant</div>
</div>
""",
        unsafe_allow_html=True,
    )
