#!/usr/bin/env python
# coding: utf-8

# In[3]:


from graphviz import Graph

def hg_show(ATOMS, LINES, PLANES):
    
    # ATOMS[i] = [atom name: e.g. 'x_a']
    # LINES[i] triples of three atoms forming an edge
    # PLANES[i] septuples of seven atoms forming a plane
    
    h = Graph('H', filename='Hypergraph.gv', engine='sfdp')
    h.attr('node', shape = 'circle', style = 'filled', height = '0.8', fixedsize = 'true')
    h.attr('edge', shape = 'inv')
    
    n = len(ATOMS)
    
    for i in ATOMS: # Create nodes
        h.node(i, label = i)
    
    # create lines
    
    for i in LINES:
        h.edge(i[0], i[1])
        h.edge(i[2], i[1])

    for i in PLANES: # arrange atoms in plane configuration
        for k in range(1,7):
            h.edge(i[0], i[k]) # join 6 atoms to centre atom
        h.edge(i[1], i[4])
        h.edge(i[1], i[6])
        h.edge(i[2], i[4])
        h.edge(i[2], i[5])
        h.edge(i[3], i[5])
        h.edge(i[3], i[6])
         
        
    return h

ATOMS = ['x_1','x_2','x_3','x_4']
LINES = [['x_1', 'x_2', 'x_3']]
PLANES = []

hg_show(ATOMS, LINES, PLANES)


# In[ ]:




