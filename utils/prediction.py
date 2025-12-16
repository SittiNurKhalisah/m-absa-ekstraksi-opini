def predict_aspect_sentiment(processed_opinions, models):
    hasil = []

    aspek_map = {
        0: 'kpms',
        1: 'fi',
        2: 'wt',
        3: 'bl'
    }

    for op in processed_opinions:
        if not isinstance(op, str) or not op.strip():
            continue

        try:
            # PREDIKSI ASPEK
            X_aspek = models['tfidf_aspek'].transform([op])
            aspek_id = int(models['aspek'].predict(X_aspek).ravel()[0])

            aspek = aspek_map.get(aspek_id)
            if aspek is None:
                continue

            # PREDIKSI SENTIMEN
            sent_tfidf = models[f'tfidf_sentimen_{aspek}']
            X_sent = sent_tfidf.transform([op])
            
            sent_models = models[f'sentimen_{aspek}']
            
            if 'Positif' in sent_models:
                sent_pred = sent_models['Positif'].predict(X_sent)[0]
                sentimen = 'Positif' if sent_pred == 1 else 'Negatif'
            elif 'Negatif' in sent_models:
                sent_pred = sent_models['Negatif'].predict(X_sent)[0]
                sentimen = 'Negatif' if sent_pred == 1 else 'Positif'
            else:
                sentimen = 'Unknown'

            hasil.append({
                'opini': op,
                'aspek': aspek.upper(),
                'sentimen': sentimen
            })
            
        except Exception as e:
            print(f"❌ Error untuk opini '{op}': {e}")
            import traceback
            traceback.print_exc()
            continue

    return hasil