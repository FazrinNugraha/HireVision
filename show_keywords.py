from utils import load_ml_resources
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("KATA KUNCI PENTING UNTUK PREDIKSI GAJI")
print("="*70)

resources, _, _, _ = load_ml_resources()
model = resources['model']
tfidf_word = resources['tfidf_word']
tfidf_char = resources['tfidf_char']

# Get feature importances
importances = model.feature_importances_
n_word = len(tfidf_word.vocabulary_)
n_char = len(tfidf_char.vocabulary_)

# Get word importances
word_importances = importances[:n_word]

# Get vocabulary (kata → index)
vocab = tfidf_word.vocabulary_

# Buat dictionary: kata → importance
word_imp_dict = {}
for word, idx in vocab.items():
    word_imp_dict[word] = word_importances[idx]

# Sort by importance
sorted_words = sorted(word_imp_dict.items(), key=lambda x: x[1], reverse=True)

print("\n🏆 TOP 50 KATA PALING PENTING (Word-Level TF-IDF):")
print("-" * 70)
print(f"{'Rank':<6} {'Kata':<25} {'Importance':<12} {'Kategori'}")
print("-" * 70)

# Kategorisasi kata
def categorize_word(word):
    # Level/Senioritas
    if word in ['senior', 'junior', 'lead', 'head', 'chief', 'director', 'manager', 'staff', 'associate']:
        return "🎖️  Level"
    # Tech/IT
    elif word in ['data', 'software', 'developer', 'engineer', 'programmer', 'analyst', 'scientist', 'devops', 'backend', 'frontend', 'fullstack', 'web', 'mobile', 'cloud', 'ai', 'ml', 'python', 'java', 'javascript']:
        return "💻 Tech/IT"
    # Business/Management
    elif word in ['business', 'product', 'project', 'operations', 'strategy', 'consultant', 'executive']:
        return "💼 Business"
    # Sales/Marketing
    elif word in ['sales', 'marketing', 'digital', 'account', 'customer', 'service']:
        return "📈 Sales/Marketing"
    # Finance
    elif word in ['finance', 'accounting', 'financial', 'audit', 'tax']:
        return "💰 Finance"
    # HR/Admin
    elif word in ['hr', 'human', 'resources', 'admin', 'administrative', 'recruitment']:
        return "👥 HR/Admin"
    else:
        return "📋 Lainnya"

for rank, (word, imp) in enumerate(sorted_words[:50], 1):
    category = categorize_word(word)
    print(f"{rank:<6} {word:<25} {imp:<12.6f} {category}")

print("\n" + "="*70)
print("🔤 TOP 30 N-GRAM KARAKTER PENTING (Char-Level TF-IDF):")
print("-" * 70)

# Get char importances
char_importances = importances[n_word:n_word+n_char]
char_vocab = tfidf_char.vocabulary_

char_imp_dict = {}
for ngram, idx in char_vocab.items():
    char_imp_dict[ngram] = char_importances[idx]

sorted_chars = sorted(char_imp_dict.items(), key=lambda x: x[1], reverse=True)

print(f"{'Rank':<6} {'N-gram':<15} {'Importance':<12} {'Contoh Kata'}")
print("-" * 70)

# Contoh kata untuk setiap n-gram
ngram_examples = {
    'sen': 'senior, senioritas',
    'ior': 'senior, junior',
    'man': 'manager, management',
    'age': 'manager, management',
    'dat': 'data, database',
    'ata': 'data',
    'dev': 'developer, devops',
    'eng': 'engineer, engineering',
    'mar': 'marketing, market',
    'sal': 'sales, salary',
    'acc': 'account, accounting',
    'fin': 'finance, financial',
    'ana': 'analyst, analytics',
    'pro': 'programmer, product, project',
    'sof': 'software',
    'web': 'web, website',
    'dig': 'digital',
    'bus': 'business',
    'ead': 'head, lead',
    'chi': 'chief',
    'dir': 'director',
    'exe': 'executive',
    'con': 'consultant, controller',
    'sta': 'staff, specialist',
}

for rank, (ngram, imp) in enumerate(sorted_chars[:30], 1):
    example = ngram_examples.get(ngram, '...')
    print(f"{rank:<6} {ngram:<15} {imp:<12.6f} {example}")

print("\n" + "="*70)
print("💡 INSIGHT & TIPS:")
print("="*70)
print("""
1. 🎖️  LEVEL/SENIORITAS sangat penting!
   → Kata: senior, lead, head, chief, director
   → Tip: Sertakan level di judul (misal: "Senior Data Scientist")

2. 💻 TECH KEYWORDS punya bobot tinggi
   → Kata: data, software, engineer, developer, analyst
   → Tip: Gunakan kata teknis yang spesifik

3. 📋 SPESIFIK > UMUM
   → ✅ "Senior Data Scientist" > ❌ "Staff IT"
   → ✅ "Backend Developer" > ❌ "Programmer"

4. 🔤 N-GRAM KARAKTER menangkap pola
   → Model belajar dari potongan kata (sen, ior, man, age)
   → Bahkan typo/variasi ejaan bisa tertangkap

5. 💼 KOMBINASI KATA penting
   → "Data Scientist" > "Scientist" saja
   → "Product Manager" > "Manager" saja
""")

print("="*70)
print("🧪 COBA SENDIRI:")
print("="*70)
print("""
Buka aplikasi Streamlit dan coba judul-judul ini:

HIGH SALARY (Kata kunci kuat):
  • "Senior Data Scientist"
  • "Lead Software Engineer"
  • "Head of Product"
  • "Chief Technology Officer"

MEDIUM SALARY:
  • "Data Analyst"
  • "Software Developer"
  • "Product Manager"
  • "Marketing Manager"

LOW SALARY (Kata kunci lemah):
  • "Staff IT"
  • "Admin"
  • "Junior Programmer"
  • "Intern"
""")
