import nltk

try:
    from nlp_id.postag import PosTag
    NLPID_AVAILABLE = True
except:
    NLPID_AVAILABLE = False

def pos_tagging(text):
    if NLPID_AVAILABLE:
        postagger = PosTag()
        return " ".join([f"[ {t}/{p} ]" for t,p in postagger.get_pos_tag(text)])
    else:
        tokens = nltk.word_tokenize(text)
        return " ".join([f"[ {t}/NN ]" for t in tokens])
