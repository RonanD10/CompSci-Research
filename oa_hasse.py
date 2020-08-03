#!/usr/bin/env python
# coding: utf-8

# In[6]:


from graphviz import Graph

def oa_hasse(NEG, COMP, OPLUS):
    
    g = Graph('G', filename = 'Orthoalgebra Hasse Diagram')
    
    g.attr(rankdir = 'BT')
    
    n = len(NEG)

    # Create edges
    for i in range(n):
        for j in range(n):
            if COMP[i,j] == 1:
                # join i with OPLUS[i,j]
                if i != OPLUS[i,j]:
                    g.edge("%d" %i, "%d" % OPLUS[i,j])
                    
    return g


# In[7]:


# example 

import numpy as np

NEG = [3,2,1,0]
COMP = np.array([[1,1,1,1], [1,0,1,0], [1,1,0,0], [1,0,0,0]], dtype = int)
OPLUS = np.array([[0, 1, 2, 3], [1, 0, 3, 0], [2, 3, 0, 0], [3, 0, 0, 0]], dtype = int)

oa_hasse(NEG, COMP, OPLUS)

