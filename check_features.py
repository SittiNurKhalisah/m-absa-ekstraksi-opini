import pickle

# Cek Model Sentimen WT
with open('models/best1_model_sentimen_wt.pkl', 'rb') as f:
    model_wt = pickle.load(f)
    if 'Positif' in model_wt:
        print(f"Model Sentimen WT (Positif) mengharapkan: {model_wt['Positif'].n_features_in_} fitur")
    if 'Negatif' in model_wt:
        print(f"Model Sentimen WT (Negatif) mengharapkan: {model_wt['Negatif'].n_features_in_} fitur")

# Cek Model Sentimen BL
with open('models/best1_model_sentimen_bl.pkl', 'rb') as f:
    model_bl = pickle.load(f)
    if 'Positif' in model_bl:
        print(f"Model Sentimen BL (Positif) mengharapkan: {model_bl['Positif'].n_features_in_} fitur")
    if 'Negatif' in model_bl:
        print(f"Model Sentimen BL (Negatif) mengharapkan: {model_bl['Negatif'].n_features_in_} fitur")