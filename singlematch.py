import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
g=nx.random_graphs.binomial_graph(1000, 0.001)
p1=0.2#bad match
p2=0.5#back to market
paces=range(10,1010,10)
ans={i:[]for i in paces}
for k in range(10):
    print k
    for pace in paces:
        pos=pace
        cur=[i for i in g.nodes() if i<pos]
        bad=0
        while True:
            match=nx.maximal_matching(g.subgraph(cur))
            for i in match:
                for j in i:
                    if random.random()>p1:
                        cur.remove(j)
                        continue
                    if random.random()>p2:
                        bad+=1
                        cur.remove(j)
            cur+=range(pos,pos+pace)
            if pos>=1000:
                break
            pos=pos+pace
        bad+=len([i for i in cur if i<1000])
        ans[pace]+=[bad]
plt.plot(paces,[np.mean(ans[i]) for i in paces])
plt.xlabel('pace')
plt.ylabel('bad guys')
plt.show()
