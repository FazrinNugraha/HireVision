import streamlit as st

from tabs.predict_salary.constants import (
    GENERIC_CATEGORY_KEYWORDS,
    GENERIC_TITLE_TERMS,
    NON_PRIME_LOCATIONS,
    PENDIDIKAN_MAP,
    PENGALAMAN_MAP,
    SERTIFIKAT_MAP,
)
from utils import predict_kos_price, predict_salary


def tokenize_title(judul: str) -> list[str]:
    """Normalisasi judul pekerjaan menjadi token sederhana."""
    cleaned = (
        judul.lower()
        .replace("/", " ")
        .replace("-", " ")
        .replace(",", " ")
        .replace(".", " ")
    )
    return [token for token in cleaned.split() if token]


def analyze_title_ambiguity(judul: str, kategori: str, lokasi: str) -> dict:
    """Deteksi judul generik agar hasil bisa dibuat lebih konservatif."""
    tokens = tokenize_title(judul)
    token_count = len(tokens)
    generic_matches = [token for token in tokens if token in GENERIC_TITLE_TERMS]
    category_matches = [
        token
        for token in tokens
        if token in GENERIC_CATEGORY_KEYWORDS.get(kategori, set())
    ]

    is_single_generic = token_count == 1 and len(generic_matches) == 1
    is_short_generic = token_count <= 2 and len(generic_matches) >= 1
    is_ambiguous = is_single_generic or is_short_generic or (
        token_count <= 2 and len(category_matches) >= 1
    )

    title_correction = 1.0
    confidence_label = "Tinggi"

    if is_single_generic:
        title_correction *= 0.84
        confidence_label = "Rendah"
    elif is_short_generic:
        title_correction *= 0.90
        confidence_label = "Sedang"
    elif len(generic_matches) >= 1:
        title_correction *= 0.95
        confidence_label = "Sedang"

    if is_ambiguous and lokasi in NON_PRIME_LOCATIONS:
        title_correction *= 0.97

    if is_ambiguous and kategori == "Administrative & Customer Service":
        title_correction *= 0.97

    notes = []
    if is_single_generic:
        notes.append(
            "Judul pekerjaan sangat umum, sehingga sistem menerapkan koreksi realistis."
        )
    elif is_short_generic:
        notes.append(
            "Judul masih cukup generik, sehingga estimasi dibuat lebih konservatif."
        )

    if is_ambiguous:
        notes.append(
            "Coba judul yang lebih spesifik seperti 'Admin Finance', 'HR Staff', atau 'Customer Service Staff' untuk akurasi yang lebih baik."
        )

    return {
        "is_ambiguous": is_ambiguous,
        "generic_matches": generic_matches,
        "title_correction": round(title_correction, 4),
        "confidence_label": confidence_label,
        "notes": notes,
    }


def get_profile_adjustment(peng: str, pend: str, sert: str, kategori: str) -> dict:
    """Hitung multiplier personal yang lebih defensif untuk entry-level."""
    m_peng = PENGALAMAN_MAP[peng]["m_pengalaman"]
    m_pend = PENDIDIKAN_MAP[pend]["m_pendidikan"]
    m_sert = SERTIFIKAT_MAP[sert]["m_sertifikat"]

    realism_correction = 1.0
    notes = []

    if "Fresh Graduate" in peng:
        realism_correction *= 0.97
        notes.append("Fresh graduate diberi penyesuaian ekstra agar hasil lebih realistis.")

        if kategori in {
            "Administrative & Customer Service",
            "HR & General Affairs",
            "Retail, F&B & Hospitality",
        }:
            realism_correction *= 0.97
            notes.append(
                "Role entry-level umum di kategori ini dibuat lebih konservatif."
            )

    elif "Junior" in peng and kategori in {
        "Administrative & Customer Service",
        "HR & General Affairs",
    }:
        realism_correction *= 0.98

    total_multiplier = m_peng * m_pend * m_sert * realism_correction
    return {
        "m_pengalaman": m_peng,
        "m_pendidikan": m_pend,
        "m_sertifikat": m_sert,
        "realism_correction": round(realism_correction, 4),
        "total_multiplier": round(total_multiplier, 4),
        "notes": notes,
    }


def run_prediction(judul, kategori, lokasi, peng, pend, sert, resources):
    """Jalankan pipeline ML + apply MAF, simpan hasil ke session_state."""
    if not judul.strip():
        st.warning("⚠️ Mohon isi Judul Pekerjaan terlebih dahulu.")
        return

    with st.spinner("Memproses Random Forest + penyesuaian profil..."):
        hasil_basis = predict_salary(
            judul_pekerjaan=judul.strip(),
            kategori_pekerjaan=kategori,
            lokasi=lokasi,
            resources=resources,
        )

        if hasil_basis is None:
            st.error("Terjadi masalah saat membaca output model ML.")
            return

        title_meta = analyze_title_ambiguity(judul.strip(), kategori, lokasi)
        profile_meta = get_profile_adjustment(peng, pend, sert, kategori)

        title_correction = title_meta["title_correction"]
        total_multiplier = profile_meta["total_multiplier"]
        gaji_setelah_koreksi_judul = hasil_basis * title_correction
        gaji_akhir = int(gaji_setelah_koreksi_judul * total_multiplier)

        estimasi_kos = predict_kos_price(lokasi)
        rasio_kos = (estimasi_kos / gaji_akhir) * 100

        st.session_state["last_prediction"] = {
            "judul": judul.strip(),
            "kategori": kategori,
            "lokasi": lokasi,
            "pengalaman": PENGALAMAN_MAP[peng]["label"],
            "pendidikan": PENDIDIKAN_MAP[pend]["label"],
            "sertifikasi": SERTIFIKAT_MAP[sert]["label"],
            "gaji_basis": int(hasil_basis),
            "gaji_setelah_koreksi_judul": int(gaji_setelah_koreksi_judul),
            "gaji_prediksi": gaji_akhir,
            "gaji_min": int(gaji_akhir * 0.90),
            "gaji_max": int(gaji_akhir * 1.10),
            "multiplier": round(total_multiplier, 2),
            "m_pengalaman": profile_meta["m_pengalaman"],
            "m_pendidikan": profile_meta["m_pendidikan"],
            "m_sertifikat": profile_meta["m_sertifikat"],
            "m_koreksi_realistis": profile_meta["realism_correction"],
            "m_koreksi_judul": title_correction,
            "is_ambiguous_title": title_meta["is_ambiguous"],
            "generic_tokens": title_meta["generic_matches"],
            "confidence_label": title_meta["confidence_label"],
            "adjustment_notes": title_meta["notes"] + profile_meta["notes"],
            "estimasi_kos": estimasi_kos,
            "rasio_kos": rasio_kos,
        }

        if "messages" in st.session_state:
            del st.session_state["messages"]
