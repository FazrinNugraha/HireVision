from utils import load_ml_resources
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("FEATURE IMPORTANCE ASLI MODEL (207 FITUR)")
print("="*70)

resources, _, _, _ = load_ml_resources()
model = resources['model']
tfidf_word = resources['tfidf_word']
tfidf_char = resources['tfidf_char']
ohe_encoder = resources['ohe_encoder']

importances = model.feature_importances_

print(f"\nTotal fitur di model: {len(importances)}")
print("\nBreakdown fitur:")

# 1. TF-IDF Word
n_word = len(tfidf_word.vocabulary_)
print(f"\n1. TF-IDF Word Features: {n_word} fitur")
print(f"   Contoh: 'data', 'scientist', 'senior', 'manager', dll")
print(f"   Top 5 importance:")
word_imp = importances[:n_word]
top_5_word = sorted(enumerate(word_imp), key=lambda x: x[1], reverse=True)[:5]
for idx, imp in top_5_word:
    print(f"      - Fitur #{idx}: {imp:.4f}")

# 2. TF-IDF Char
n_char = len(tfidf_char.vocabulary_)
print(f"\n2. TF-IDF Char Features: {n_char} fitur")
print(f"   Contoh: 'dat', 'ata', 'sci', 'ien', dll (n-gram karakter)")
print(f"   Top 5 importance:")
char_imp = importances[n_word:n_word+n_char]
top_5_char = sorted(enumerate(char_imp), key=lambda x: x[1], reverse=True)[:5]
for idx, imp in top_5_char:
    print(f"      - Fitur #{idx}: {imp:.4f}")

# 3. Target Encoding
n_target = 1
print(f"\n3. Target Encoding: {n_target} fitur")
print(f"   Nilai: 5,000,000 (fixed)")
print(f"   Importance: {importances[n_word+n_char]:.4f}")

# 4. Extra Features
n_extra = 3
print(f"\n4. Extra Features: {n_extra} fitur")
print(f"   - title_len (panjang judul): {importances[n_word+n_char+1]:.4f}")
print(f"   - title_wc (jumlah kata): {importances[n_word+n_char+2]:.4f}")
print(f"   - comp_size (ukuran perusahaan): {importances[n_word+n_char+3]:.4f}")

# 5. OHE Features
ohe_feature_names = ohe_encoder.get_feature_names_out(['Lokasi_Clean', 'Kategori_Pekerjaan', 'Senioritas'])
ohe_feature_names = ohe_feature_names[:-3]  # Drop Senioritas
n_ohe = len(ohe_feature_names)
print(f"\n5. One-Hot Encoding: {n_ohe} fitur")
print(f"   - Lokasi (11 fitur): Bekasi, Bogor, Depok, ...")
print(f"   - Kategori (12 fitur): IT Tech Data, Sales Marketing, ...")

ohe_imp = importances[n_word+n_char+n_target+n_extra:]
print(f"\n   Top 5 OHE importance:")
top_5_ohe = sorted(enumerate(ohe_imp), key=lambda x: x[1], reverse=True)[:5]
for idx, imp in top_5_ohe:
    if idx < len(ohe_feature_names):
        print(f"      - {ohe_feature_names[idx]}: {imp:.4f}")

print("\n" + "="*70)
print(f"TOTAL: {n_word} + {n_char} + {n_target} + {n_extra} + {n_ohe} = {len(importances)} fitur")
print("="*70)
