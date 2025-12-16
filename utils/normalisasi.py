import re

def normalize_text(text, kamus):
    text = str(text).replace('&', ' dan ')
    tokens = re.split(r'(\W+)', text)
    return "".join([kamus.get(t.lower(), t) for t in tokens])
