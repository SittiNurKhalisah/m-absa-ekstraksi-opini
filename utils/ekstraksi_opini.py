import re

# ==========================================================
# 1. PEMECAHAN OPINI BERDASARKAN TANDA BACA
# ==========================================================

PUNCTUATION_SEPARATORS = {
    '.', ',', '!', '?', ';', ':', '...', '!!', '??'
}

def is_separator_token(token):
    return token in PUNCTUATION_SEPARATORS


def pisahkan_opini(teks_pos):
    """
    Input  : string POS tagging
    Output : list of opini, tiap opini berupa list (token, tag)
    """
    teks_pos = str(teks_pos)
    pasangan = re.findall(r'\[\s*(.+?)\/(.+?)\s*\]', teks_pos)

    opini_list, temp = [], []

    for token, tag in pasangan:
        token, tag = token.strip(), tag.strip()

        if is_separator_token(token):
            if temp:
                opini_list.append(temp)
                temp = []
        else:
            temp.append((token, tag))

    if temp:
        opini_list.append(temp)

    return opini_list


# ==========================================================
# 2. RULE POLA SEDERHANA (1–30)
# ==========================================================

PATTERNS_SEDERHANA = {
    1: ['NN', 'JJ'], 2: ['NN', 'VB', 'JJ'], 3: ['NN', 'ADV', 'JJ'],
    4: ['NN', 'PR', 'JJ'], 5: ['NN', 'PR', 'VB'], 6: ['NN', 'DT', 'JJ'],
    7: ['NN', 'NN', 'VB'], 8: ['NN', 'JJ', 'JJ'], 9: ['NN', 'NN', 'JJ'],
    10: ['JJ', 'NN', 'PR'], 11: ['NN', 'NEG', 'JJ'], 12: ['NN', 'ADV', 'VB'],
    13: ['NN', 'JJ', 'ADV'], 14: ['NN', 'VB', 'ADV', 'JJ'],
    15: ['NN', 'NN', 'ADV', 'VB'], 16: ['NN', 'NN', 'ADV', 'JJ'],
    17: ['NN', 'NN', 'PR', 'JJ'], 18: ['NN', 'NN', 'PR', 'VB'],
    19: ['NN', 'DT', 'ADV', 'VB'], 20: ['NN', 'DT', 'ADV', 'JJ'],
    21: ['NN', 'PR', 'ADV', 'JJ'], 22: ['NN', 'NN', 'NNP', 'JJ'],
    23: ['NN', 'PR', 'VB', 'JJ'], 24: ['NN', 'PR', 'JJ', 'JJ'],
    25: ['NN', 'VB', 'PR', 'JJ'], 26: ['DT', 'NN', 'NN', 'ADV', 'VB'],
    27: ['NN', 'DT', 'ADV', 'VB'], 28: ['NN', 'NN', 'PR', 'ADV', 'JJ'],
    29: ['NN', 'NN', 'IN', 'PR', 'ADV', 'JJ'],
    30: ['NN', 'NN', 'IN', 'NN', 'PR', 'JJ']
}

def cek_ada_nn_dan_jj(tags):
    return 'NN' in tags and 'JJ' in tags

def cek_ada_cc(tags):
    return 'CC' in tags

def cek_pola_sederhana(opini_parsed):
    tokens, tags = [list(t) for t in zip(*opini_parsed)]

    if not cek_ada_nn_dan_jj(tags):
        return []

    for rule_num, pattern in PATTERNS_SEDERHANA.items():
        for i in range(len(tags) - len(pattern) + 1):
            if tags[i:i+len(pattern)] == pattern:
                return [" ".join(tokens)]

    return []


# ==========================================================
# 3. RULE KONJUNGSI (31–37)
# ==========================================================

def proses_rule_31(op):
    t, g = zip(*op)
    for i in range(len(g)-2):
        if g[i]=='NN' and g[i+1]=='CC' and g[i+2]=='NN':
            rest = t[i+3:]
            if 'JJ' in g[i+3:] or 'VB' in g[i+3:]:
                return [
                    " ".join([t[i]] + list(rest)),
                    " ".join([t[i+2]] + list(rest))
                ]
    return []

def proses_rule_32(op):
    t, g = zip(*op)
    for i in range(len(g)-2):
        if g[i]=='JJ' and g[i+1]=='CC' and g[i+2]=='JJ':
            subject = t[:i]
            if 'NN' in g[:i]:
                return [
                    " ".join(list(subject)+[t[i]]),
                    " ".join(list(subject)+[t[i+2]])
                ]
    return []

def proses_rule_33(op):
    t, g = zip(*op)
    try:
        nn = g.index('NN')
        jj1 = g.index('JJ', nn+1)
        cc = g.index('CC', jj1+1)
        jj2 = g.index('JJ', cc+1)
        return [
            " ".join(t[:cc]),
            " ".join(t[:jj1+1]+(t[jj2],))
        ]
    except:
        return []

def proses_rule_34(op):
    t, g = zip(*op)
    try:
        nn1 = g.index('NN')
        cc = g.index('CC', nn1+1)
        nn2 = g.index('NN', cc+1)
        jj = g.index('JJ', nn2+1)
        return [
            " ".join(t[cc+1:]),
            " ".join(t[:cc]+(t[jj],))
        ]
    except:
        return []

def proses_rule_35(op):
    t, g = zip(*op)
    try:
        nn1 = g.index('NN')
        cc = g.index('CC', nn1+1)
        nn2 = g.index('NN', cc+1)
        vb = g.index('VB', nn2+1)
        return [
            " ".join(t[cc+1:]),
            " ".join(t[:cc]+(t[vb],))
        ]
    except:
        return []

def proses_rule_36(op):
    t, g = zip(*op)
    for i in range(len(g)-1):
        if g[i]=='NN' and g[i+1]=='NN':
            try:
                jj = g.index('JJ', i+2)
                cc = g.index('CC', jj+1)
                jj2 = g.index('JJ', cc+1)
                return [
                    " ".join(t[:cc]),
                    " ".join(t[i:i+2]+t[cc+1:])
                ]
            except:
                pass
    return []

def proses_rule_37(op):
    t, g = zip(*op)
    for i in range(len(g)-1):
        if g[i]=='NN' and g[i+1]=='JJ':
            try:
                cc = g.index('CC', i+2)
                nn2 = g.index('NN', cc+1)
                jj2 = g.index('JJ', nn2+1)
                return [
                    " ".join(t[:cc]+(t[jj2],)),
                    " ".join(t[cc+1:])
                ]
            except:
                pass
    return []


RULES_CC = [
    proses_rule_31, proses_rule_32, proses_rule_33,
    proses_rule_34, proses_rule_35, proses_rule_36, proses_rule_37
]


# ==========================================================
# 4. FUNGSI UTAMA (DIPANGGIL STREAMLIT)
# ==========================================================

def extract_opinions(pos_tagged_text):
    """
    Input  : string POS tagging
    Output : list string opini hasil ekstraksi
    """
    hasil_akhir = []

    opini_mentah = pisahkan_opini(pos_tagged_text)

    for op in opini_mentah:
        tags = [t[1] for t in op]
        extracted = []

        if cek_ada_cc(tags):
            for rule in RULES_CC:
                extracted = rule(op)
                if extracted:
                    break

        if not extracted:
            extracted = cek_pola_sederhana(op)

        hasil_akhir.extend(extracted)

    return sorted(list(set(hasil_akhir)))
