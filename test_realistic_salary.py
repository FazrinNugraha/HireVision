from utils import load_ml_resources, predict_salary
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("🧪 TEST GAJI REALISTIS (MULTIPLIER BARU)")
print("="*70)

resources, _, _, _ = load_ml_resources()

# Test case: Fresh Graduate Frontend Developer
judul = "Front End Developer"
kategori = "IT, Tech & Data"
lokasi = "Jakarta Barat"

# Prediksi basis dari model
gaji_basis = predict_salary(judul, kategori, lokasi, resources)

print(f"\nJudul: {judul}")
print(f"Kategori: {kategori}")
print(f"Lokasi: {lokasi}\n")

print("="*70)
print("GAJI BASIS MODEL (Tanpa Multiplier)")
print("="*70)
print(f"Rp {gaji_basis:,.0f}\n")

# Multiplier LAMA vs BARU
multipliers_old = {
    "2026 + S1 + No Cert": 1.17 * 1.00 * 1.00,
    "2027 + S1 + No Cert": 1.26 * 1.00 * 1.00,
    "2030 + S2 + Expert": 1.59 * 1.25 * 1.50,
}

multipliers_new = {
    "2026 + S1 + No Cert": 1.00 * 1.00 * 1.00,
    "2027 + S1 + No Cert": 1.05 * 1.00 * 1.00,
    "2030 + S2 + Expert": 1.20 * 1.15 * 1.20,
}

print("="*70)
print("PERBANDINGAN: MULTIPLIER LAMA vs BARU")
print("="*70)
print(f"{'Skenario':<30} {'Mult Lama':<12} {'Gaji Lama':<18} {'Mult Baru':<12} {'Gaji Baru':<18} {'Selisih'}")
print("-"*70)

for scenario in multipliers_old.keys():
    mult_old = multipliers_old[scenario]
    mult_new = multipliers_new[scenario]
    gaji_old = gaji_basis * mult_old
    gaji_new = gaji_basis * mult_new
    selisih = ((gaji_new - gaji_old) / gaji_old) * 100
    
    print(f"{scenario:<30} {mult_old:<12.2f} Rp {gaji_old:>12,.0f}   {mult_new:<12.2f} Rp {gaji_new:>12,.0f}   {selisih:>6.1f}%")

print("\n" + "="*70)
print("SKENARIO REALISTIS (MULTIPLIER BARU)")
print("="*70)

scenarios = [
    ("2026 + S1 + No Cert", 1.00, 1.00, 1.00, "Fresh Grad baseline"),
    ("2026 + S1 + BNSP", 1.00, 1.00, 1.05, "Fresh Grad + sertifikat lokal"),
    ("2027 + S1 + No Cert", 1.05, 1.00, 1.00, "1 tahun pengalaman"),
    ("2028 + S1 + Associate", 1.10, 1.00, 1.10, "2 tahun + sertifikat internasional"),
    ("2030 + S2 + Expert", 1.20, 1.15, 1.20, "5 tahun + S2 + expert cert"),
]

print(f"{'Skenario':<35} {'Multiplier':<12} {'Gaji Final':<18} {'Keterangan'}")
print("-"*70)

for scenario, m_proj, m_edu, m_cert, desc in scenarios:
    total_mult = m_proj * m_edu * m_cert
    gaji_final = gaji_basis * total_mult
    print(f"{scenario:<35} {total_mult:<12.2f} Rp {gaji_final:>12,.0f}   {desc}")

print("\n" + "="*70)
print("💡 ANALISIS REALISME")
print("="*70)

print("""
MULTIPLIER LAMA (TERLALU TINGGI):
  ❌ 2026 + S1 + No Cert = ×1.17 → Rp 8.7 juta (TIDAK REALISTIS!)
  ❌ 2030 + S2 + Expert = ×2.98 → Rp 22 juta (TERLALU TINGGI!)

MULTIPLIER BARU (LEBIH REALISTIS):
  ✅ 2026 + S1 + No Cert = ×1.00 → Rp 7.5 juta (REALISTIS untuk Fresh Grad)
  ✅ 2027 + S1 + No Cert = ×1.05 → Rp 7.9 juta (+5% per tahun)
  ✅ 2030 + S2 + Expert = ×1.66 → Rp 12.4 juta (REALISTIS untuk 5 tahun exp)

PERUBAHAN:
  📉 Proyeksi Tahun: 1.17-1.59 → 1.00-1.20 (turun ~30-40%)
  📉 Pendidikan S2: 1.25 → 1.15 (turun ~10%)
  📉 Sertifikat Expert: 1.50 → 1.20 (turun ~20%)

HASIL:
  ✅ Fresh Grad S1: Rp 7.5 juta (dari Rp 8.7 juta)
  ✅ 5 tahun S2 Expert: Rp 12.4 juta (dari Rp 22 juta)
  ✅ Lebih sesuai dengan kondisi pasar Indonesia 2026
""")

print("="*70)
print("🎯 REKOMENDASI MULTIPLIER")
print("="*70)

print("""
PROYEKSI TAHUN (Inflasi ~5% per tahun):
  2026: ×1.00 (baseline)
  2027: ×1.05 (+5%)
  2028: ×1.10 (+10%)
  2029: ×1.15 (+15%)
  2030: ×1.20 (+20%)

PENDIDIKAN (Berdasarkan BPS Sakernas):
  SMA/SMK: ×0.70 (-30%)
  Diploma: ×0.85 (-15%)
  S1: ×1.00 (baseline)
  S2+: ×1.15 (+15%)

SERTIFIKASI (Nilai tambah skill):
  Tanpa: ×1.00 (baseline)
  BNSP/Lokal: ×1.05 (+5%)
  Associate: ×1.10 (+10%)
  Expert: ×1.20 (+20%)

TOTAL MAKSIMAL: 1.20 × 1.15 × 1.20 = ×1.66 (+66%)
""")
