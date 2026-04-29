import joblib, numpy as np
from scipy.sparse import hstack, csr_matrix
import pandas as pd

model = joblib.load('models/salary/salary_model_lgbm.pkl')
tfidf_word = joblib.load('models/salary/tfidf_word_vectorizer.pkl')
tfidf_char = joblib.load('models/salary/tfidf_char_vectorizer.pkl')
enc = joblib.load('models/salary/target_encoder.pkl')
kolom = joblib.load('models/salary/kolom_fitur_model.pkl')

print('Model type:', type(model).__name__)
print('Encoder keys:', list(enc.keys()))
print('Kolom fitur:', kolom)

judul = 'Senior Data Scientist'
perusahaan = 'PT Gojek Indonesia'
lokasi = 'Jakarta Selatan'
senioritas = 'Senior/Managerial'

X_word = tfidf_word.transform([judul])
X_char = tfidf_char.transform([judul])
target_val = enc['perusahaan_target_dict'].get(perusahaan, enc['global_mean'])
comp_size = np.log1p(enc['company_size_dict'].get(perusahaan, 1))
title_len = len(judul)
title_wc = len(judul.split())
extra = csr_matrix([[title_len, title_wc, comp_size]])
target_sparse = csr_matrix([[target_val]])

df_cat = pd.DataFrame([[0]*len(kolom)], columns=kolom)
lok_col = 'Lokasi_Clean_' + lokasi
sen_col = 'Senioritas_' + senioritas
if lok_col in df_cat.columns: df_cat[lok_col] = 1
if sen_col in df_cat.columns: df_cat[sen_col] = 1
X_cat = csr_matrix(df_cat.values)

X_final = hstack([X_word, X_char, target_sparse, extra, X_cat])
pred = model.predict(X_final)[0]
print('Test OK - Prediksi:', round(np.expm1(pred)))
