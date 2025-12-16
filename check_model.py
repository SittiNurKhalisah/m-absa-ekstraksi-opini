import pickle

# Periksa salah satu file sentimen
with open('models/best1_model_sentimen_kpms.pkl', 'rb') as f:
    data = pickle.load(f)
    
print("Type:", type(data))
print("Content:", data)

if isinstance(data, dict):
    print("Keys:", data.keys())