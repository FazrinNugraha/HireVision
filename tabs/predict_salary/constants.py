PENGALAMAN_MAP = {
    "🎓 Fresh Graduate (0-1 thn)": {"m_pengalaman": 0.80, "label": "Fresh Grad"},
    "📈 Junior (1-3 thn)": {"m_pengalaman": 0.95, "label": "Junior"},
    "💼 Mid-Level (3-5 thn)": {"m_pengalaman": 1.10, "label": "Mid-Level"},
    "🏆 Senior (5+ thn)": {"m_pengalaman": 1.20, "label": "Senior"},
}

PENDIDIKAN_MAP = {
    "🎓 SMA / SMK": {"m_pendidikan": 0.75, "label": "SMA/SMK"},
    "🏅 Diploma (D3/D4)": {"m_pendidikan": 0.90, "label": "Diploma"},
    "🎓 S1 / Sarjana": {"m_pendidikan": 1.00, "label": "S1/Sarjana"},
    "🎖️ S2 / Magister ke atas": {"m_pendidikan": 1.10, "label": "S2+"},
}

SERTIFIKAT_MAP = {
    "📄 Tanpa Sertifikasi": {"m_sertifikat": 1.00, "label": "None"},
    "🏅 Sertifikat BNSP / Lokal": {"m_sertifikat": 1.03, "label": "Lokal/BNSP"},
    "🎖️ Sertifikat Associate (Intl)": {"m_sertifikat": 1.05, "label": "Associate"},
    "🏆 Sertifikat Expert (Intl)": {"m_sertifikat": 1.10, "label": "Expert"},
}

GENERIC_TITLE_TERMS = {
    "staff",
    "admin",
    "administrasi",
    "administrator",
    "assistant",
    "operator",
    "clerk",
    "crew",
    "helper",
    "support",
    "generalist",
    "general",
}

GENERIC_CATEGORY_KEYWORDS = {
    "Administrative & Customer Service": {"staff", "admin", "administrasi", "assistant"},
    "HR & General Affairs": {"staff", "admin", "assistant", "generalist"},
    "Retail, F&B & Hospitality": {"crew", "staff", "helper"},
    "Logistics & Supply Chain": {"staff", "operator", "helper", "admin"},
}

NON_PRIME_LOCATIONS = {"Bogor", "Depok", "Bekasi", "Tangerang", "Tangerang Selatan"}
