import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

stemmer = StemmerFactory().create_stemmer()

stop_words = set(stopwords.words('indonesian'))
negasi = {'tidak','bukan','jangan','belum','tanpa'}
stop_words = stop_words - negasi

def preprocess_text(text_list):
    hasil = []
    for text in text_list:
        text = re.sub('[^a-zA-Z]', ' ', text.lower())
        tokens = word_tokenize(text)
        tokens = [stemmer.stem(t) for t in tokens if t not in stop_words]
        hasil.append(" ".join(tokens))
    return hasil
