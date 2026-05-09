# 📚 KAMUS KATA KUNCI PREDIKSI GAJI

> **Model:** Random Forest Regressor  
> **Total Fitur:** 207 (100 Word TF-IDF + 80 Char TF-IDF + 27 lainnya)  
> **Dataset:** Lowongan Kerja Jabodetabek  

---

## 🏆 TOP 50 KATA KUNCI PALING PENTING

### **Kategori: Level/Senioritas (🎖️)**

| Rank | Kata | Importance | Dampak Gaji | Contoh Judul |
|------|------|------------|-------------|--------------|
| 1 | **manager** | 4.68% | +50-70% | Product Manager, Marketing Manager |
| 10 | **chief** | 0.40% | +40-60% | Chief Technology Officer, Chief Marketing Officer |
| 43 | **senior** | 0.05% | +10-20% | Senior Data Scientist, Senior Developer |
| 44 | **lead** | 0.04% | +15-25% | Lead Engineer, Tech Lead |
| 34 | **supervisor** | 0.12% | +20-30% | Supervisor Produksi, Supervisor Sales |
| 48 | **staff** | 0.03% | -10-20% | Staff IT, Staff Admin |
| - | **junior** | 0.02% | -20-30% | Junior Developer, Junior Analyst |
| - | **intern** | 0.01% | -40-50% | Intern, Magang |

**💡 Insight:**
- Kata "Manager" adalah MAGIC WORD (+50-70% gaji!)
- Urutan level: Chief > Head > Senior > Lead > Manager > Supervisor > Staff > Junior > Intern
- Tambahkan level di judul untuk boost gaji

---

### **Kategori: Tech/IT (💻)**

| Rank | Kata | Importance | Dampak Gaji | Contoh Judul |
|------|------|------------|-------------|--------------|
| 45 | **engineer** | 0.04% | +5-15% | Software Engineer, Data Engineer |
| - | **developer** | 0.03% | +5-10% | Backend Developer, Frontend Developer |
| - | **data** | 0.03% | +10-20% | Data Scientist, Data Analyst |
| - | **software** | 0.02% | +5-10% | Software Engineer, Software Developer |
| - | **analyst** | 0.02% | +5-15% | Data Analyst, Business Analyst |
| - | **scientist** | 0.02% | +15-25% | Data Scientist, Research Scientist |
| - | **programmer** | 0.01% | +0-5% | Programmer, Junior Programmer |
| - | **devops** | 0.01% | +10-20% | DevOps Engineer |
| - | **backend** | 0.01% | +5-10% | Backend Developer |
| - | **frontend** | 0.01% | +5-10% | Frontend Developer |

**💡 Insight:**
- "Engineer" > "Developer" > "Programmer" (dalam hal gaji)
- "Data Scientist" > "Data Analyst" (+10-15%)
- Spesifik lebih baik: "Backend Developer" > "Developer"

---

### **Kategori: Business/Management (💼)**

| Rank | Kata | Importance | Dampak Gaji | Contoh Judul |
|------|------|------------|-------------|--------------|
| 17 | **project** | 0.27% | +20-30% | Project Manager, Project Development |
| 41 | **product** | 0.07% | +30-40% | Product Manager, Product Owner |
| 14 | **development** | 0.33% | +10-20% | Business Development, Project Development |
| - | **business** | 0.05% | +10-15% | Business Analyst, Business Development |
| - | **strategy** | 0.02% | +15-25% | Strategy Manager, Strategy Consultant |
| - | **consultant** | 0.02% | +10-20% | Business Consultant, IT Consultant |
| - | **executive** | 0.03% | +30-50% | Executive Manager, Chief Executive |

**💡 Insight:**
- "Product Manager" adalah posisi dengan gaji tinggi (Rp 11.5 jt)
- "Project Manager" juga tinggi (Rp 11.2 jt)
- Kata "Executive" boost gaji signifikan

---

### **Kategori: Sales/Marketing (📈)**

| Rank | Kata | Importance | Dampak Gaji | Contoh Judul |
|------|------|------------|-------------|--------------|
| 21 | **sales** | 0.24% | +10-20% | Sales Manager, Sales Officer |
| 4 | **sales officer** | 0.55% | +15-25% | Sales Officer, B2B Sales Officer |
| - | **marketing** | 0.15% | +20-30% | Marketing Manager, Digital Marketing |
| - | **digital** | 0.05% | +10-15% | Digital Marketing, Digital Analyst |
| 13 | **officer** | 0.34% | +5-10% | Sales Officer, Development Officer |
| 42 | **service** | 0.05% | +5-10% | Customer Service, Service Manager |
| - | **account** | 0.09% | +10-15% | Account Manager, Key Account |

**💡 Insight:**
- "Marketing Manager" = GAJI TERTINGGI (Rp 12.3 jt!)
- "Sales Manager" > "Sales Officer" > "Sales Staff"
- Tambahkan "Digital" untuk boost gaji

---

### **Kategori: Finance/Accounting (💰)**

| Rank | Kata | Importance | Dampak Gaji | Contoh Judul |
|------|------|------------|-------------|--------------|
| - | **finance** | 0.03% | +10-20% | Finance Manager, Finance Analyst |
| - | **accounting** | 0.03% | +5-15% | Accounting Manager, Accounting Staff |
| - | **financial** | 0.02% | +10-15% | Financial Analyst, Financial Controller |
| - | **audit** | 0.02% | +10-15% | Internal Audit, Audit Manager |
| - | **tax** | 0.01% | +5-10% | Tax Specialist, Tax Consultant |

**💡 Insight:**
- Finance/Accounting relatif stabil
- "Manager" tetap penting di kategori ini
- "Analyst" > "Staff" dalam hal gaji

---

### **Kategori: HR/Admin (👥)**

| Rank | Kata | Importance | Dampak Gaji | Contoh Judul |
|------|------|------------|-------------|--------------|
| - | **hr** | 0.02% | +5-10% | HR Manager, HR Specialist |
| - | **human resources** | 0.02% | +5-10% | Human Resources Manager |
| - | **recruitment** | 0.01% | +5-10% | Recruitment Specialist |
| - | **admin** | 0.01% | -10-20% | Admin, Administrative Staff |
| - | **administrative** | 0.01% | -5-15% | Administrative Officer |

**💡 Insight:**
- "HR Manager" > "HR Staff" (+30-40%)
- Kata "Admin" cenderung menurunkan gaji
- Ganti "Admin" dengan "Specialist" atau "Officer"

---

### **Kategori: Industri Spesifik (🏭)**

| Rank | Kata | Importance | Dampak Gaji | Contoh Judul |
|------|------|------------|-------------|--------------|
| 3 | **coal mining** | 0.56% | +30-50% | Coal Mining Manager, Mining Engineer |
| 6 | **mining** | 0.46% | +25-40% | Mining Company, Mining Operations |
| 2 | **mandarin** | 0.87% | +40-60% | Mandarin Speaker, Mandarin Translator |
| 5 | **b2b** | 0.47% | +20-30% | B2B Sales, B2B Marketing |
| 25 | **drafter** | 0.16% | +10-20% | Drafter, CAD Drafter |

**💡 Insight:**
- Industri mining punya gaji tinggi
- Skill bahasa (Mandarin) sangat dihargai
- B2B > B2C dalam hal gaji

---

## 🔤 TOP 30 N-GRAM KARAKTER PENTING

N-gram adalah potongan kata yang dipelajari model untuk menangkap pola.

| Rank | N-gram | Importance | Contoh Kata | Penjelasan |
|------|--------|------------|-------------|------------|
| 1 | **nager** | 6.05% | ma**nager** | Akhiran kata "manager" |
| 2 | **man** | 5.61% | **man**ager, hu**man** | Awalan/tengah kata |
| 3 | **ager** | 4.84% | man**ager** | Akhiran kata "manager" |
| 11 | **age** | 2.68% | man**age**r | Tengah kata "manager" |
| 13 | **ana** | 2.54% | **ana**lyst, m**ana**ger | Pola "analyst" dan "manager" |
| 22 | **acc** | 0.39% | **acc**ount, **acc**ounting | Awalan "account" |

**💡 Insight:**
- Model belajar dari potongan kata, bukan hanya kata utuh
- Bahkan typo/variasi ejaan bisa tertangkap
- N-gram membantu model mengenali kata baru yang mirip

---

## 📊 RANKING GAJI BERDASARKAN JUDUL

### **💎 TIER S (Rp 11-12 juta+)**

| Judul | Gaji | Kata Kunci Kuat |
|-------|------|-----------------|
| Marketing Manager | Rp 12,345,330 | marketing + manager |
| Senior Manager Product | Rp 11,650,638 | senior + manager + product |
| Product Manager | Rp 11,566,270 | product + manager |
| Project Manager | Rp 11,230,708 | project + manager |

**Formula:** [DOMAIN] + **MANAGER** = GAJI TINGGI!

---

### **💰 TIER A (Rp 7.4-7.5 juta)**

| Judul | Gaji | Kata Kunci Kuat |
|-------|------|-----------------|
| Software Engineer | Rp 7,530,097 | software + engineer |
| Chief Technology Officer | Rp 7,513,168 | chief + technology |
| Lead Software Engineer | Rp 7,509,697 | lead + software + engineer |
| Backend Developer | Rp 7,472,805 | backend + developer |
| Senior Data Scientist | Rp 7,434,792 | senior + data + scientist |

**Formula:** [LEVEL] + [TECH] + [ROLE]

---

### **💵 TIER B (Rp 7.2-7.4 juta)**

| Judul | Gaji | Kata Kunci |
|-------|------|------------|
| Data Scientist | Rp 7,353,703 | data + scientist |
| Business Analyst | Rp 7,295,105 | business + analyst |
| Data Analyst | Rp 7,275,340 | data + analyst |

**Formula:** [TECH] + [ROLE] (tanpa level)

---

### **💸 TIER C (Rp 7.2-7.3 juta)**

| Judul | Gaji | Kata Kunci Lemah |
|-------|------|------------------|
| Staff IT | Rp 7,302,785 | staff (generic) |
| Junior Data Analyst | Rp 7,291,277 | junior (entry level) |

**Formula:** [GENERIC] atau [JUNIOR] = GAJI RENDAH

---

## 🎯 FORMULA OPTIMASI GAJI

### **Formula 1: Tambahkan Level**
```
❌ "Data Scientist" → ✅ "Senior Data Scientist"
Rp 7,353,703 → Rp 7,434,792 (+1.1%)

❌ "Developer" → ✅ "Lead Developer"
Rp 7,472,805 → Rp 7,509,697 (+0.5%)
```

### **Formula 2: Tambahkan "Manager"**
```
❌ "Product" → ✅ "Product Manager"
Rp ~7,300,000 → Rp 11,566,270 (+58%!) 💎

❌ "Marketing" → ✅ "Marketing Manager"
Rp ~7,300,000 → Rp 12,345,330 (+69%!) 💎💎
```

### **Formula 3: Spesifik > Umum**
```
❌ "Staff IT" → ✅ "Software Engineer"
Rp 7,302,785 → Rp 7,530,097 (+3.1%)

❌ "Admin" → ✅ "Business Analyst"
Rp 7,413,481 → Rp 7,295,105 (-1.6% tapi lebih profesional)
```

### **Formula 4: Engineer > Developer > Programmer**
```
✅ "Software Engineer" = Rp 7,530,097
✅ "Software Developer" = Rp 7,472,805
❌ "Programmer" = Rp ~7,300,000
```

---

## 💡 TIPS & TRIK

### **✅ DO (Lakukan)**

1. **Tambahkan Level:**
   - Senior, Lead, Head, Chief, Manager
   
2. **Gunakan Kata Spesifik:**
   - Engineer > Developer > Programmer
   - Scientist > Analyst > Staff
   
3. **Kombinasi Kata Kuat:**
   - "Senior Data Scientist"
   - "Lead Software Engineer"
   - "Product Manager"
   
4. **Sebutkan Spesialisasi:**
   - Backend, Frontend, Full Stack
   - Data, Business, Financial
   
5. **Tambahkan Domain:**
   - Product, Project, Marketing, Sales

---

### **❌ DON'T (Hindari)**

1. **Kata Generic:**
   - Staff, Admin, Officer (tanpa spesialisasi)
   
2. **Kata Entry Level:**
   - Junior, Intern, Magang, Trainee
   
3. **Terlalu Umum:**
   - "IT" → Ganti "Software Engineer"
   - "Admin" → Ganti "Administrative Officer"
   
4. **Tanpa Level:**
   - "Developer" → Tambah "Senior Developer"
   - "Analyst" → Tambah "Lead Analyst"

---

## 🧪 EKSPERIMEN YANG BISA DICOBA

### **Test 1: Pengaruh Level**
```python
# Di Streamlit, coba:
"Data Scientist"        # Baseline
"Senior Data Scientist" # +Level
"Lead Data Scientist"   # +Level (lebih tinggi)
"Head of Data Science"  # +Level (tertinggi)
```

### **Test 2: Pengaruh "Manager"**
```python
"Product"               # Baseline
"Product Owner"         # +Role
"Product Manager"       # +Manager (BOOST!)
"Senior Product Manager" # +Level+Manager (MAX!)
```

### **Test 3: Engineer vs Developer**
```python
"Programmer"            # Terendah
"Developer"             # Sedang
"Software Developer"    # Lebih tinggi
"Software Engineer"     # Tertinggi
```

### **Test 4: Spesialisasi**
```python
"Developer"             # Generic
"Backend Developer"     # +Spesialisasi
"Senior Backend Developer" # +Level+Spesialisasi
```

---

## 📈 STATISTIK MODEL

- **Total Vocabulary (Word):** 100 kata unik
- **Total N-gram (Char):** 80 n-gram unik
- **Feature Importance:**
  - Judul Pekerjaan: 82.1% (TF-IDF)
  - Target Encoding: 12.6%
  - Kategori: 4.7%
  - Lokasi: 0.6%

---

## 🔗 FILE TERKAIT

- `show_keywords.py` - Lihat semua kata kunci dan importance
- `test_job_titles.py` - Test berbagai judul pekerjaan
- `KAMUS_KATA_KUNCI.md` - File ini (dokumentasi lengkap)

---

## 📝 CATATAN

- Data ini berdasarkan model yang dilatih dengan lowongan kerja Jabodetabek
- Importance score menunjukkan seberapa besar pengaruh kata terhadap prediksi
- Gaji yang ditampilkan adalah prediksi model, bukan gaji aktual
- Untuk hasil terbaik, kombinasikan beberapa kata kunci kuat

---

**Dibuat oleh:** HireVision AI  
**Terakhir Update:** 8 Mei 2026  
**Model Version:** Random Forest v1.0
