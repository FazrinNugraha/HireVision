# 📚 Panduan Penggunaan Kamus Kata Kunci

## 📁 File yang Tersedia

1. **`KAMUS_KATA_KUNCI.md`** - Dokumentasi lengkap (Markdown)
2. **`kamus_kata_kunci.json`** - Data terstruktur (JSON)
3. **`show_keywords.py`** - Script untuk melihat kata kunci
4. **`test_job_titles.py`** - Script untuk test judul pekerjaan

---

## 🚀 Cara Menggunakan

### **1. Baca Dokumentasi Lengkap**

```bash
# Buka file Markdown
cat KAMUS_KATA_KUNCI.md

# Atau buka di editor/browser
code KAMUS_KATA_KUNCI.md
```

**Isi:**
- Top 50 kata kunci paling penting
- Kategori kata (Level, Tech, Business, Sales, dll)
- Ranking gaji berdasarkan judul
- Formula optimasi gaji
- Tips & trik

---

### **2. Lihat Kata Kunci dari Model**

```bash
python show_keywords.py
```

**Output:**
- Top 50 kata paling penting (Word-level)
- Top 30 n-gram karakter (Char-level)
- Kategorisasi kata (Level, Tech, Business, dll)
- Insight & tips

---

### **3. Test Berbagai Judul Pekerjaan**

```bash
python test_job_titles.py
```

**Output:**
- Prediksi gaji untuk 21 judul pekerjaan
- Ranking dari tertinggi ke terendah
- Analisis kata kunci
- Tips optimasi

---

### **4. Gunakan Data JSON (Programmatic)**

```python
import json

# Load kamus
with open('kamus_kata_kunci.json', 'r') as f:
    kamus = json.load(f)

# Akses kata kunci level
level_keywords = kamus['keywords']['level_senioritas']['keywords']
for kw in level_keywords:
    print(f"{kw['word']}: {kw['salary_impact']}")

# Akses salary tiers
tier_s = kamus['salary_tiers']['tier_s']
print(f"Tier S Range: {tier_s['range']}")
for job in tier_s['jobs']:
    print(f"  - {job['title']}: Rp {job['salary']:,}")

# Akses formulas
high_salary_formula = kamus['formulas']['high_salary']
print(f"Formula: {high_salary_formula['formula']}")
print(f"Examples: {', '.join(high_salary_formula['examples'])}")
```

---

### **5. Test di Streamlit**

```bash
streamlit run main.py
```

**Langkah:**
1. Buka tab "💰 Prediksi Gaji"
2. Coba judul dari kamus (misal: "Senior Data Scientist")
3. Bandingkan dengan judul lain (misal: "Data Scientist")
4. Lihat perbedaan gajinya!

---

## 🎯 Contoh Penggunaan

### **Contoh 1: Optimasi Judul Pekerjaan**

**Sebelum:**
```
Judul: "Staff IT"
Gaji: Rp 7,302,785
```

**Sesudah (Optimasi):**
```
Judul: "Senior Software Engineer"
Gaji: Rp 7,530,097 (+3.1%)
```

**Kata kunci yang ditambahkan:**
- "Senior" (level)
- "Software" (spesialisasi)
- "Engineer" (role profesional)

---

### **Contoh 2: Boost Gaji dengan "Manager"**

**Sebelum:**
```
Judul: "Product"
Gaji: ~Rp 7,300,000
```

**Sesudah (Tambah "Manager"):**
```
Judul: "Product Manager"
Gaji: Rp 11,566,270 (+58%!) 💎
```

**Magic word:** "Manager" = +50-70% gaji!

---

### **Contoh 3: Kombinasi Kata Kuat**

**Level 1 (Baseline):**
```
Judul: "Data Analyst"
Gaji: Rp 7,275,340
```

**Level 2 (Tambah Spesialisasi):**
```
Judul: "Data Scientist"
Gaji: Rp 7,353,703 (+1.1%)
```

**Level 3 (Tambah Level):**
```
Judul: "Senior Data Scientist"
Gaji: Rp 7,434,792 (+2.2%)
```

**Level 4 (Tambah Manager):**
```
Judul: "Senior Manager Data Science"
Gaji: Rp 11,650,638 (+60%!) 💎💎
```

---

## 📊 Quick Reference

### **Kata Kunci Paling Penting (Top 10)**

| Rank | Kata | Impact | Contoh |
|------|------|--------|--------|
| 1 | manager | +50-70% | Product Manager |
| 2 | mandarin | +40-60% | Mandarin Speaker |
| 3 | chief | +40-60% | Chief Technology Officer |
| 4 | product | +30-40% | Product Manager |
| 5 | project | +20-30% | Project Manager |
| 6 | marketing | +20-30% | Marketing Manager |
| 7 | sales | +10-20% | Sales Manager |
| 8 | senior | +10-20% | Senior Developer |
| 9 | lead | +15-25% | Lead Engineer |
| 10 | engineer | +5-15% | Software Engineer |

---

### **Formula Gaji Tinggi**

```
🏆 TIER S (Rp 11-12 juta):
   [DOMAIN] + MANAGER
   Contoh: Marketing Manager, Product Manager

💰 TIER A (Rp 7.4-7.6 juta):
   [LEVEL] + [TECH] + [ROLE]
   Contoh: Senior Data Scientist, Lead Software Engineer

💵 TIER B (Rp 7.2-7.4 juta):
   [TECH] + [ROLE]
   Contoh: Data Scientist, Software Engineer

💸 TIER C (Rp 7.2-7.3 juta):
   [GENERIC] atau [JUNIOR]
   Contoh: Staff IT, Junior Developer
```

---

### **Urutan Level (Tertinggi → Terendah)**

```
Chief > Head > Senior > Lead > Manager > Supervisor > Staff > Junior > Intern
```

---

### **Urutan Role (Tertinggi → Terendah)**

```
Engineer > Developer > Programmer
Scientist > Analyst > Staff
Manager > Supervisor > Officer > Staff
```

---

## 💡 Tips Cepat

### **✅ DO (Lakukan)**

1. ✅ Tambahkan level: "Senior", "Lead", "Head"
2. ✅ Gunakan "Manager" jika memungkinkan
3. ✅ Spesifik: "Backend Developer" > "Developer"
4. ✅ Kombinasi: "Senior Data Scientist"

### **❌ DON'T (Hindari)**

1. ❌ Kata generic: "Staff", "Admin"
2. ❌ Entry level: "Junior", "Intern", "Magang"
3. ❌ Terlalu umum: "IT", "Programmer"
4. ❌ Tanpa level: "Developer" → "Senior Developer"

---

## 🧪 Eksperimen yang Bisa Dicoba

### **Test 1: Pengaruh "Manager"**
```python
# Coba di Streamlit:
"Product"           # Baseline
"Product Manager"   # +Manager (+58%!)
```

### **Test 2: Pengaruh Level**
```python
"Data Scientist"        # Baseline
"Senior Data Scientist" # +Level (+1.1%)
"Lead Data Scientist"   # +Level (+2%)
```

### **Test 3: Engineer vs Developer**
```python
"Programmer"        # Terendah
"Developer"         # Sedang
"Software Engineer" # Tertinggi (+3%)
```

---

## 📞 Support

Jika ada pertanyaan atau butuh bantuan:

1. Baca `KAMUS_KATA_KUNCI.md` untuk dokumentasi lengkap
2. Jalankan `python show_keywords.py` untuk melihat kata kunci
3. Jalankan `python test_job_titles.py` untuk test prediksi
4. Coba di Streamlit: `streamlit run main.py`

---

## 📝 Changelog

- **2026-05-08**: Initial release
  - Kamus kata kunci lengkap (50 kata)
  - N-gram karakter (30 n-gram)
  - Salary tiers (4 tiers)
  - Formulas & tips
  - JSON data structure

---

**Happy Optimizing! 🚀**
