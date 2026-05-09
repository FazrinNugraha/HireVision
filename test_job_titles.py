from utils import load_ml_resources, predict_salary
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("🧪 TEST BERBAGAI JUDUL PEKERJAAN")
print("="*70)

resources, _, _, _ = load_ml_resources()

# Setting default
kategori = "IT, Tech & Data"
lokasi = "Jakarta Selatan"

# Daftar judul untuk ditest
test_cases = [
    # HIGH SALARY - Kata kunci kuat
    ("Chief Technology Officer", "💎 HIGH"),
    ("Head of Product", "💎 HIGH"),
    ("Senior Data Scientist", "💎 HIGH"),
    ("Lead Software Engineer", "💎 HIGH"),
    ("Senior Manager Product", "💎 HIGH"),
    
    # MEDIUM-HIGH SALARY
    ("Data Scientist", "💰 MED-HIGH"),
    ("Product Manager", "💰 MED-HIGH"),
    ("Software Engineer", "💰 MED-HIGH"),
    ("Backend Developer", "💰 MED-HIGH"),
    ("Business Analyst", "💰 MED-HIGH"),
    
    # MEDIUM SALARY
    ("Data Analyst", "💵 MEDIUM"),
    ("Software Developer", "💵 MEDIUM"),
    ("Marketing Manager", "💵 MEDIUM"),
    ("Project Manager", "💵 MEDIUM"),
    ("Frontend Developer", "💵 MEDIUM"),
    
    # MEDIUM-LOW SALARY
    ("Junior Data Analyst", "💸 MED-LOW"),
    ("Junior Developer", "💸 MED-LOW"),
    ("Staff IT", "💸 MED-LOW"),
    ("Admin", "💸 MED-LOW"),
    
    # LOW SALARY
    ("Intern", "📉 LOW"),
    ("Magang", "📉 LOW"),
]

print(f"\nKategori: {kategori}")
print(f"Lokasi: {lokasi}\n")
print("-" * 70)
print(f"{'Judul Pekerjaan':<40} {'Prediksi Gaji':<20} {'Level'}")
print("-" * 70)

results = []
for judul, level in test_cases:
    gaji = predict_salary(judul, kategori, lokasi, resources)
    results.append((judul, gaji, level))
    print(f"{judul:<40} Rp {gaji:>12,}   {level}")

# Sort by salary
print("\n" + "="*70)
print("📊 RANKING BERDASARKAN GAJI (TERTINGGI → TERENDAH)")
print("="*70)

sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
for rank, (judul, gaji, level) in enumerate(sorted_results, 1):
    print(f"{rank:>2}. {judul:<40} Rp {gaji:>12,}")

print("\n" + "="*70)
print("🔍 ANALISIS KATA KUNCI:")
print("="*70)

# Analisis kata kunci
keywords_analysis = {
    "LEVEL WORDS": {
        "keywords": ["chief", "head", "senior", "lead", "manager", "junior", "staff", "intern"],
        "impact": "🎖️  SANGAT TINGGI - Menentukan level senioritas"
    },
    "TECH WORDS": {
        "keywords": ["data", "scientist", "engineer", "developer", "software", "backend", "frontend"],
        "impact": "💻 TINGGI - Menentukan spesialisasi teknis"
    },
    "BUSINESS WORDS": {
        "keywords": ["product", "business", "project", "marketing", "analyst"],
        "impact": "💼 SEDANG - Menentukan domain bisnis"
    },
    "GENERIC WORDS": {
        "keywords": ["staff", "admin", "officer", "magang"],
        "impact": "📋 RENDAH - Terlalu umum, gaji lebih rendah"
    }
}

for category, info in keywords_analysis.items():
    print(f"\n{category}:")
    print(f"  Keywords: {', '.join(info['keywords'])}")
    print(f"  Impact: {info['impact']}")

print("\n" + "="*70)
print("💡 TIPS OPTIMASI JUDUL PEKERJAAN:")
print("="*70)
print("""
1. ✅ TAMBAHKAN LEVEL:
   ❌ "Data Scientist" → ✅ "Senior Data Scientist" (+15-30%)
   ❌ "Developer" → ✅ "Lead Developer" (+20-40%)

2. ✅ SPESIFIK > UMUM:
   ❌ "Staff IT" → ✅ "Software Engineer" (+50-100%)
   ❌ "Admin" → ✅ "Business Analyst" (+40-80%)

3. ✅ KOMBINASI KATA KUAT:
   ✅ "Senior Data Scientist" (senior + data + scientist)
   ✅ "Lead Software Engineer" (lead + software + engineer)
   ✅ "Head of Product" (head + product)

4. ❌ HINDARI KATA LEMAH:
   ❌ "Magang", "Intern", "Staff", "Admin"
   → Ganti dengan posisi yang lebih spesifik

5. 🎯 FORMULA GAJI TINGGI:
   [LEVEL] + [SPESIALISASI] + [ROLE]
   Contoh: "Senior" + "Data" + "Scientist"
""")

print("\n" + "="*70)
print("🧪 COBA SENDIRI DI STREAMLIT:")
print("="*70)
print("""
1. Buka aplikasi: streamlit run main.py
2. Masuk ke tab "💰 Prediksi Gaji"
3. Coba judul-judul di atas
4. Bandingkan hasilnya!

Eksperimen:
  • Tambah/hapus kata "Senior"
  • Ganti "Developer" dengan "Engineer"
  • Coba "Manager" vs "Staff"
  • Bandingkan "Data Scientist" vs "Data Analyst"
""")
