import pandas as pd
import pickle
import os

def load_models(model_path="models/"):
    models = {}

    # MODEL KLASIFIKASI ASPEK
    with open(os.path.join(model_path, 'best1_model_rf_aspek.pkl'), 'rb') as f:
        models['aspek'] = pickle.load(f)

    # TF-IDF ASPEK
    with open(os.path.join(model_path, 'tfidf1_vectorizer_final.pkl'), 'rb') as f:
        models['tfidf_aspek'] = pickle.load(f)

    # MODEL SENTIMEN + TF-IDF SENTIMEN
    aspek_list = ['kpms', 'fi', 'wt', 'bl']
    for aspek in aspek_list:
        with open(os.path.join(model_path, f'best1_model_sentimen_{aspek}.pkl'), 'rb') as f:
            models[f'sentimen_{aspek}'] = pickle.load(f)
        
        with open(os.path.join(model_path, f'tfidf_vectorizer_{aspek}.pkl'), 'rb') as f:
            models[f'tfidf_sentimen_{aspek}'] = pickle.load(f)

    return models


def load_dictionary(kamus_path="data/colloquial-indonesian-lexicon1.csv"):
    df = pd.read_csv(kamus_path, encoding='latin-1')
    return dict(zip(
        df['slang'].str.lower().str.strip(),
        df['formal'].str.lower().str.strip()
    ))