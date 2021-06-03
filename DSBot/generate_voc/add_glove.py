from gensim.models import Word2Vec
from gensim.scripts import glove2word2vec
import numpy as np
import string
import nltk
import nltk.data
import itertools

nltk.download('wordnet')
sent_loc = nltk.tokenize.PunktSentenceTokenizer()
tokenizer = nltk.tokenize.TreebankWordTokenizer()
stemmer = nltk.stem.WordNetLemmatizer()

#Read glove and write into word2vec vectors
#glove_6b = "glove/glove.6B.300d.txt"
#loading the glove vectors
#glove2word2vec.glove2word2vec(glove_6b,'word2vec_out_300.txt')

#Loading the word2vec vector
with open('word2vec_out_300.txt', "rb") as lines:
     wvec = {line.split()[0].decode('utf-8'):np.array(line.split()[1:],dtype=np.float32) for line in lines}
       # line.split()[0].decode(encoding): np.array(line.split()[1:],
       #                                                  dtype=np.float32)
       #                                                 for line in lines}

#my data vectors
print(len(wvec))

#Read my sentence file
with open('src-train.txt') as f:
    lines = [line.rstrip() for line in f]
texts = [x.lower() for x in lines]
texts = [list(itertools.chain(*[tokenizer.tokenize(sent) for sent in sent_loc.tokenize(text)])) for text in texts]
texts = [" ".join(stemmer.lemmatize(token) for token in tokens) for tokens in texts]

lines = texts #+ text
y = [i.lower().replace('-',' ').translate(str.maketrans('', '', string.punctuation)).split(' ') for i in lines]
text_data2 = y

em_model = Word2Vec(text_data2, size=300, window=30, min_count=2, workers=8, sg = 1)
w2v = {w: vec for w, vec in zip(em_model.wv.index2word, em_model.wv.vectors)}
#print(w2v)
a = list(w2v.keys())
#print(len(a))
#mixing them both
for i in a:
    if i in wvec:
       continue
    else:
        wvec.update({i: w2v[i]})
        print(i)
print(len(wvec))

with open('../wf/glove_new_300.txt', "w") as f:
    for k,v in wvec.items():
        f.write(str(k)+' '+' '.join(map(str, v))+'\n')