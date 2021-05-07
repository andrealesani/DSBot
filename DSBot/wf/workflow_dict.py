wf = {}

#wf['ds']=[]
wf['statistics']=[]
wf['preprocessing']=['normalization', 'missingValFill', 'missingValRemove', 'zeroVarRemove', 'lowVarRemove', 'highVarKeep']
wf['clustering']=['kmeans','dbscan']
wf['classification']=['randomForest','logisticRegression']
wf['featureSelection']=[]
wf['pca']=[]
wf['plot']=['scatterplot', 'boxplot', 'distplot']
wf['range']=[]
wf['performances']=[]
all_nodes = [k for k in wf.keys()]
all_nodes = all_nodes + [v1 for k,v in wf.items() for v1 in v]
print(len(all_nodes))
print(all_nodes)
possible_wf = []
for k in wf.keys():
    possible_wf.append([k])
    for v in wf[k]:
        possible_wf.append([v])

print(possible_wf)