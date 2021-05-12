import tqdm
from scipy import spatial
import pandas as pd

import string
ALPHA = string.ascii_letters

kmean_emb = None
embs = []
d={}
with open("try_glove_new.txt") as f:
    for line in tqdm.tqdm(f):
        s = line.strip().split()
        word = s[0]
        emb = [float(x) for x in s[1:]]
        if word == "kmeans":
            kmean_emb = emb
            d[word]=emb
            #print(d.keys())
        else:
            embs.append((word, emb))
            if len(emb)==100:
                if (word.startswith(tuple(ALPHA))):
                    d[word]=emb

#sim = [(w,e) for w,e in embs[100:500] if spatial.distance.cosine(kmean_emb, emb) < 0.2]
words = []
sim_low = []
sim = []
#for w,e in tqdm.tqdm(embs):
    #if (w.startswith(tuple(ALPHA))):#('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))):
        # try:
        #     if spatial.distance.cosine(kmean_emb, e) < 0.2:
        #         sim_low.append((w,e))
        #         #print(w)
        #         words.append(w)
        #     if spatial.distance.cosine(kmean_emb, e) < 0.65:
        #         sim.append((w,e))
        #         words.append(w)
        #     if spatial.distance.cosine(kmean_emb, e) < 0.9:
        #         words.append(w)
        # except Exception as ex:
        #
        #     print(type(ex), w,len(kmean_emb), len(e))
#words = list(set(words))
# print('<0.2')
# print(len(sim_low))
# x = [w for w,_ in sim_low]
# print(x)
# print('<0.65')
# print(len(sim))
# print([w for w,_ in sim if w not in x])
#print('words', words)
#d = {k: v for k, v in d.items() if k in words or k=='kmeans'}# and ~k[0].isdigit()}
#print('inters', len(set(d.keys()).intersection(set(words))))
#print('dict', len(d))
embs_df = pd.DataFrame(d).T
embs_df.to_csv('embeddings_df_kmeans.csv')

#print(embs_df.shape)
#print('index', embs_df.index.values)
#print(embs_df.head())