from utils import load_ml_resources, predict_salary
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("TEST: Pengaruh Kategori yang Salah")
print("="*60)

resources, _, _, _ = load_ml_resources()

judul = "Programmer"
lokasi = "Jakarta Selatan"

# Test 1: Kategori BENAR
kategori_benar = "IT, Tech & Data"
gaji_benar = predict_salary(judul, kategori_benar, lokasi, resources)

# Test 2: Kategori SALAH
kategori_salah = "Sales & Marketing"
gaji_salah = predict_salary(judul, kategori_salah, lokasi, resources)

# Test 3: Kategori lain
kategori_lain = "Finance & Accounting"
gaji_lain = predict_salary(judul, kategori_lain, lokasi, resources)

print(f"\nJudul: '{judul}'")
print(f"Lokasi: {lokasi}\n")

print(f"1. Kategori BENAR (IT, Tech & Data):")
print(f"   Gaji: Rp {gaji_benar:>12,}")

print(f"\n2. Kategori SALAH (Sales & Marketing):")
print(f"   Gaji: Rp {gaji_salah:>12,}")
print(f"   Selisih: Rp {abs(gaji_benar - gaji_salah):>10,} ({abs(gaji_benar - gaji_salah)/gaji_benar*100:.1f}%)")

print(f"\n3. Kategori Lain (Finance & Accounting):")
print(f"   Gaji: Rp {gaji_lain:>12,}")
print(f"   Selisih: Rp {abs(gaji_benar - gaji_lain):>10,} ({abs(gaji_benar - gaji_lain)/gaji_benar*100:.1f}%)")

print("\n" + "="*60)
print("KESIMPULAN:")
print("="*60)
if abs(gaji_benar - gaji_salah) > 100000:
    print("✅ Kategori BERPENGARUH ke prediksi gaji!")
    print(f"   Selisih: ~{abs(gaji_benar - gaji_salah)/gaji_benar*100:.1f}% dari gaji")
else:
    print("⚠️  Kategori pengaruhnya kecil (< Rp 100k)")
