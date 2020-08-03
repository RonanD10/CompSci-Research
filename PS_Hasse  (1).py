#!/usr/bin/env python
# coding: utf-8

# In[3]:


def powerset(s):
    PS = []
    x = len(s)
    for i in range(1 << x):
        PS.append([s[j] for j in range(x) if (i & (1 << j))])
    PS = sorted(PS, key=len)
    for i in range(1,len(s)+1):
        PS[i] = i 
    return PS
print(powerset([1,2,3]))


# In[2]:


from graphviz import Graph

def ps_hasse(list, n):
    
    g = Graph('G', filename='Power set.gv', node_attr={'height': '0.5'})
    g.attr(rankdir = 'BT') 
    g.attr(size = '(%d,%d)!' %(6*n, 6*n))
    g.attr(ratio = 'fill')
    
    PS = powerset(list)
    
    # Define EDGES:
    
    # Join zero to atoms
    for i in range(1,n+1):
        g.edge('{}', '%d' %i)
        
    # Join atoms to height 2 elements  
    for atom in PS[1:n+1]:
        for SET in PS[n+1:]: 
            if len(SET) > 2:
                break
            if atom in SET:
                g.edge("%d" %atom, " ".join(map(str,SET)))
             
    # Join remaining elements  
    index = n+2
    for SUB in PS[n+1:]:
        for SET in PS[index:]:
            if len(SET) > len(SUB) + 1:
                break
            if(all(x in SET for x in SUB)):
                 g.edge(" ".join(map(str,SUB)), " ".join(map(str,SET)))
        index += 1
    
    
    return g

# for example
list = [1,2,3]
ps_hasse(list,3)

