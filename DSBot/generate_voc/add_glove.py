from gensim.models import Word2Vec
from gensim.scripts import glove2word2vec
import numpy as np
import string
import nltk
import nltk.data
import itertools
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Lasso, LassoCV
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import os


nltk.download('wordnet')
sent_loc = nltk.tokenize.PunktSentenceTokenizer()
tokenizer = nltk.tokenize.TreebankWordTokenizer()
stemmer = nltk.stem.WordNetLemmatizer()


'''
import wikipedia
import re
import string
import re
from scipy import sparse as sp_sparse

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Specify the title of the Wikipedia page
wiki = wikipedia.page('k-means clustering')
# Extract the plain text content of the page
text = wiki.content
# Clean text
text = re.sub('\[\d+\]', '', text)
text = re.sub(r'==.*?==+', '', text)
text = text.replace('\n', '')
text = text.replace('\t', '')
text = text.replace('                        ','')
text = text.replace('        ','')
text = text.replace('   ','')
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))
print(STOPWORDS)

def text_prepare(text):
    """
        text: a string

        return: modified initial string
    """
    text = text.lower()
    text = re.sub(REPLACE_BY_SPACE_RE, " ", text)
    #text = re.sub(BAD_SYMBOLS_RE, "", text)
    text = " ".join([word for word in text.split() if not word in STOPWORDS])
    return text
text=text_prepare(text)
print(text)

text = text.split('.')
text = [re.sub(BAD_SYMBOLS_RE, "", t) for t in text]
text = [t.lower().translate(str.maketrans('', '', string.punctuation)).strip() for t in text if t.lower().translate(str.maketrans('', '', string.punctuation)).strip()!='']
'''

#glove_6b = "glove/glove.6B.100d.txt"

#loading the glove vectors
#glove2word2vec.glove2word2vec(glove_6b,'word2vec_out.txt')
with open('word2vec_out.txt', "rb") as lines:
     wvec = {line.split()[0].decode('utf-8'):np.array(line.split()[1:],dtype=np.float32) for line in lines}
       # line.split()[0].decode(encoding): np.array(line.split()[1:],
       #                                                  dtype=np.float32)
       #                                                 for line in lines}

#my data vectors
print(len(wvec))
with open('src-train.txt') as f:
    lines = [line.rstrip() for line in f]
texts = [x.lower() for x in lines]
texts = [list(itertools.chain(*[tokenizer.tokenize(sent) for sent in sent_loc.tokenize(text)])) for text in texts]
texts = [" ".join(stemmer.lemmatize(token) for token in tokens) for tokens in texts]

lines = texts #+ text
y = [i.lower().replace('-',' ').translate(str.maketrans('', '', string.punctuation)).split(' ') for i in lines]
text_data2 = y
#for sent in text_data2:
    #print(sent)
em_model = Word2Vec(text_data2, size=100, window=10, min_count=2, workers=4)
w2v = {w: vec for w, vec in zip(em_model.wv.index2word, em_model.wv.vectors)}
#print(w2v)
a = list(w2v.keys())
#print(len(a))
#mixing them both
for i in a:
    if i in wvec:
       continue
    else:
       wvec.update({ i  : w2v[i]})
print(len(wvec))

with open('../wf/try_glove_new.txt', "w") as f:
    for k,v in wvec.items():
        f.write(str(k)+' '+' '.join(map(str, v))+'\n')