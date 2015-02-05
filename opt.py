from FuncDesigner import *
from openopt import MILP
import networkx as nx
import numpy as np
 
# Define some oovars
# old-style:
#x, y, z = oovars('x y z')
# new (OpenOpt v 0.37+): 
g=nx.random_graphs.erdos_renyi_graph(n=8, p=0.4)
edges=[(0,1),(0,3),(1,2),(3,2),(2,5),(3,4),(4,5)]
m,n=len(edges),5
print m
p=0.5
con=[[(edges[i][0] in edges[j] or edges[i][1] in edges[j])for j in range(m)]for i in range(m)]
print con
coe=[p*(1-p)**(m+1)-p*(1-p)**(m) for i in range(m)]
pp,cc = oovars('pp cc',domain=bool)
tp= oovar('tp',domain=int)


# Let's define some linear functions

 
# Define objective; sum(a) and a.sum() are same as well as for numpy arrays
obj = p*m+sum([coe[i%m]*cc[i] for i in range(m*m)])
 
# Start point - currently matters only size of variables
startPoint = {pp:[1]*(m*m), cc:[1]*(m*m), tp:[0]*(m*m)} # however, using numpy.arrays is more recommended than Python lists
 
# Define some constraints
cons = [sum(pp[i*m:(i+1)*m])==1 for i in range(m)]+[sum([pp[i+j*m] for j in range(m)])==1 for i in range(m)]+\
    [tp[i]<=i%m+cc[i]*100 for i in range(m*m)]+[tp[i]==sum([0]+[pp[j*m+k] for j in range(i/m) for k in range(m) if con[i%m][k]]) for i in range(m*m)]
 
# Create prob
# old-style:
#p = MILP(obj, startPoint, intVars = [y, z], constraints=cons)
# new (OpenOpt v 0.37+): 
p = MILP(obj, startPoint, constraints=cons)
 
# Solve
r = p.maximize('cplex', iprint=-1) # glpk is name of the solver involved, see OOF doc for more arguments
 
# Decode solution
s = r.xf
print('Solution: x = %s ' % (str(s[pp])))
print s.obj
res=[0]*m
for i in range(m):
    for j in range(m):
        if s[pp][i*m+j]>0.5:
            res[i]=edges[j]
print res