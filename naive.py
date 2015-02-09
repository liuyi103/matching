# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 20:53:56 2015

@author: lyc
"""
import networkx as nx
import itertools as it
g=nx.random_graphs.erdos_renyi_graph(n=5,p=0.7)
es=g.edges()
print es
p=0.5
m=len(es)
def payoff(a,p=0.8):
    m=len(a)
    ans=0
    for i in range(m):
        tmp=p
        for j in range(i):
            if con[a[i],a[j]]>0.5:
                tmp*=(1-p)
        ans+=tmp
    return ans
ans=0
for i in it.permutations(range(m)):
    tmp=payoff(i)
    if tmp>ans:ans=tmp
print ans