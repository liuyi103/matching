# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 19:32:39 2015

@author: lyc
"""

from FuncDesigner import *
from openopt import MILP
import networkx as nx
import numpy as np

g=nx.random_graphs.erdos_renyi_graph(n=15,p=0.3)
g=nx.random_graphs.gnm_random_graph(20,15)
es=g.edges()
print es
p=0.9
m=len(es)
con=np.zeros((m,m))
corr={}
corr2={}
xtt=0
lyc=0
for i in range(m):
    for j in range(i+1,m):
        if es[i][0] in es[j] or es[i][1] in es[j]:
            con[i,j]=1
            con[j,i]=1
            corr[i,j]=lyc
            corr[j,i]=lyc+1
            lyc+=2
for i in range(m):
    for j in range(int(sum(con[i]))):
        corr2[i,j]=xtt
        xtt+=1
d=oovar('d',domain=int)
bef,ov=oovars('bef ov',domain=bool)
loss=[p*(1-p)**(i+1)-p*(1-p)**i for i in range(m)]
obj = p*m+sum([ov[corr2[i,j]]*loss[j] for i in range(m) for j in range(int(sum(con[i])))])

# Start point - currently matters only size of variables
startPoint = {d:[0]*m,bef:[0]*lyc ,ov:[0]*xtt} # however, using numpy.arrays is more recommended than Python lists
# Define some constraints
cons = [bef[corr[i,j]]+bef[corr[j,i]]==1 for i in range(m) for j in range(i+1,m) if con[i,j]>0.5]+\
    [d[i]==sum([bef[corr[j,i]] for j in range(m) if con[i,j]>0.5]+[0]) for i in range(m)]+\
    [d[i]<=j+ov[corr2[i,j]]*100 for i in range(m) for j in range(int(sum(con[i])))]
# Create prob
# old-style:
#p = MILP(obj, startPoint, intVars = [y, z], constraints=cons)
# new (OpenOpt v 0.37+): 
p = MILP(obj, startPoint, constraints=cons)
 
# Solve
r = p.maximize('cplex') # glpk is name of the solver involved, see OOF doc for more arguments
 
# Decode solution
s = r.xf
tmp=[[i,s[d][i]]for i in range(m)]
order=[i[0] for i in sorted(tmp,key=lambda x:x[1])]
print order,loss
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
print payoff(order)











