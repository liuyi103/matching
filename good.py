# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 21:59:24 2015

@author: lyc
"""

from FuncDesigner import *
from openopt import MILP
import networkx as nx
import numpy as np

g=nx.random_graphs.erdos_renyi_graph(n=15,p=0.3)
es=g.edges()
print es
p=0.5
m=len(es)
con=np.zeros((m,m))
for i in range(m):
    for j in range(i+1,m):
        if es[i][0] in es[j] or es[i][1] in es[j]:
            con[i,j]=con[j,i]=1
d=oovar('d',domain=int)
bef,ov=oovars('bef ov',domain=bool)
loss=[p*(1-p)**(i+1)-p*(1-p)**i for i in range(m)]
obj = p*m+sum([ov[i]*loss[i%m] for i in range(m*m)])
 
# Start point - currently matters only size of variables
startPoint = {d:[0]*m,bef:[0]*(m*m) ,ov:[0]*(m*m)} # however, using numpy.arrays is more recommended than Python lists
# Define some constraints
cons = [bef[i*m+i]==0 for i in range(m)]+\
    [bef[i*m+j]+bef[j*m+i]==1 for i in range(m) for j in range(i+1,m) if con[i,j]>0.5]+\
    [bef[i*m+j]==0 for i in range(m) for j in range(i+1,m) if con[i,j]<0.5]+\
    [bef[j*m+i]==0 for i in range(m) for j in range(i+1,m) if con[i,j]<0.5]+\
    [d[i]==sum([bef[j*m+i] for j in range(m) if con[i,j]>0.5]+[0]) for i in range(m)]+\
    [d[i/m]<=i%m+ov[i]*100 for i in range(m*m)]
# Create prob
# old-style:
#p = MILP(obj, startPoint, intVars = [y, z], constraints=cons)
# new (OpenOpt v 0.37+): 
p = MILP(obj, startPoint, constraints=cons)
 
# Solve
r = p.maximize('cplex', iprint=-1) # glpk is name of the solver involved, see OOF doc for more arguments
 
# Decode solution
s = r.xf
print s[bef]