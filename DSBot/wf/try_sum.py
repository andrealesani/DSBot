import tqdm
import sklearn.metrics
from scipy import spatial


kmean_emb = None
embs = []
with open("try_glove_new.txt") as f:
    for line in tqdm.tqdm(f):
        s = line.strip().split()
        word = s[0]
        emb = [float(x) for x in s[1:]]
        if word == "kmeans":
            kmean_emb = emb
        else:
            embs.append((word, emb))

#sim = [(w,e) for w,e in embs[100:500] if spatial.distance.cosine(kmean_emb, emb) < 0.2]

sim_low = []
sim = []
for w,e in tqdm.tqdm(embs):
    try:
        if spatial.distance.cosine(kmean_emb, e) < 0.2:
            sim_low.append((w,e))
        if spatial.distance.cosine(kmean_emb, e) < 0.65:
            sim.append((w,e))
    except Exception as ex:
        print(type(ex), w,len(kmean_emb), len(e))

print('<0.2')
print(len(sim_low))
x = [w for w,_ in sim_low]
print(x)
print('<0.65')
print(len(sim))
print([w for w,_ in sim if w not in x])
