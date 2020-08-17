#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np

def powerset(s):
    PS = []
    x = len(s)
    for i in range(1 << x):
        PS.append([s[j] for j in range(x) if (i & (1 << j))])
    PS = sorted(PS, key=len)
    for i in range(1,len(s)+1):
        PS[i] = i 
        
    for i in range(1,x+1):
        PS[i] = [i]
    return PS


def ass(OPLUS,n):
    for q in range(n):
        for r in range(n):
            # for a given q and r, check if associativity holds for all p
            for p in range(n):
                if OPLUS[q,r] != -1 and OPLUS[p, OPLUS[q,r]] != -1:
                    if OPLUS[p,q] == -1:
                        print(4)
                        return False
                    if OPLUS[OPLUS[p,q], r] == -1:
                        print(5)
                        return False
                    if OPLUS[p, OPLUS[q,r]] != OPLUS[OPLUS[p,q], r]: 
                        print(6)
                        return False
    else:
        return True


# In[2]:


def switcher(L, x):
    """switches x to its enumeration in L"""
    for i in L:
        if i[0] == x:
            return i[1]
        else:
            continue

def ones(p, index, c_or_o):
        """returns COMP for powerset p"""
        ones = []
       
        
        #deal with zero
        if c_or_o == 0:
            ones.append((switcher(index, set()), switcher(index, set())))
        else:
            ones.append((set(), set()))
            
        for i in p[1:]:
            if c_or_o == 0:
                a = switcher(index, set(i))
                b = switcher(index, set())
                ones.append((a,b))
                ones.append((b,a))
            else:
                ones.append((set(),set(i)))
                ones.append((set(i),set()))
            

        #deal with rest
        k = 0
        for i in p[1:]:
            k += 1
            for j in p[k:]:
                if set(i).intersection(set(j)) == set(): # disjoint elements are compatible
                    if c_or_o == 0:
                        a = switcher(index, set(i))
                        b = switcher(index, set(j))
                        ones.append((a,b))
                        ones.append((b,a))
                    else:
                        ones.append((set(i), set(j)))
                        ones.append((set(j), set(i)))
                else:
                    continue
                    
        return ones           
    


# In[3]:


# make OPLUS for Boolean algebras

def join(a,b):
    """returns the least upper bound of a,b"""
    if type(a) == int and type(b) != int:
        return b
    else:
        return a.union(b)

    

def indexer_BR(p, E):
    """orders and enumerates powerset p 
       with elements E going to the start 
       of the index"""
    
    N = len(p)
    # order p
    p_order = []
    for e in E:
        p_order.append(set(e))
    for i in range(N//2):
        if not p[i] in E and not p[N-i-1] in E:
            p_order.append(set(p[i]))
            
            p_order.append(set(p[N-i-1]))
        else:
            continue

    # enumerate p
    labels = list(zip(p_order, list(range(len(p)))))
    
    return labels




def oplus_BR(p,E):
    """returns OPLUS of the powerset p"""
    n = len(p)
    OPLUS = -1*np.ones((n,n), dtype = int)
    
    # index for enumerating elements of p
    index = indexer_BR(p, E)
    
    # non-trivial entries in OPLUS
    entries = ones(p, index, 1)   
    
    for k in entries:
        i = switcher(index, k[0])
        j = switcher(index, k[1])
        OPLUS[i, j] = switcher(index, join(k[0],k[1]))

    
    return OPLUS


def indexer_TL(p, E):
    """orders and enumerates powerset p 
       with elements E going to the end 
       of the index"""
    N = len(p)
    # order p
    p_order = []
    for i in range(N//2):
        if not p[i] in E:
            p_order.append(set(p[i]))
            p_order.append(set(p[N-i-1]))
        else:
            continue
    for e in E:
        p_order.append(set(e)) # move e to the end of p_order 
    
    # enumerate p
    labels = list(zip(p_order, list(range(len(p)))))
    
    return labels

def oplus_TL(p,E):
    """returns OPLUS of the powerset p"""
    n = len(p)
    OPLUS = -1*np.ones((n,n), dtype = int)
    
    # index for enumerating elements of p
    index = indexer_TL(p, E)
    
    # non-trivial entries in OPLUS
    entries = ones(p, index, 1)   
    
    for k in entries:
        i = switcher(index, k[0])
        j = switcher(index, k[1])
        OPLUS[i, j] = switcher(index, join(k[0],k[1]))
    
    return OPLUS


# In[4]:


# X = oplus_BR(powerset([1,2,3,4]), [])
# print(X, '\n')
Y = oplus_tl(powerset([1,2,3,4]), [])
print(Y)


# In[18]:


# Checking PP1 (non-atom)-(non-atom)


integers = list(range(16))
P2_range = list(range(12,28))

# oplus template
PP1_oplus = -1*np.ones((28,28), dtype = int)

# top-left oplus
P1_oplus = oplus_TL(powerset([1,2,3,4]),[[], [1,2,3,4], [1,2], [3,4]])

# bottom-right oplus
P2_oplus = oplus_BR(powerset([1,2,3,4]),[[], [1,2,3,4], [1,2], [3,4]])


P2_index = list(zip(integers, P2_range))
print(P2_index)

# relabel bottom-right
for i in range(16):
    for j in range(16):
        old = P2_oplus[i,j]
        if old != -1:
            P2_oplus[i,j] = switcher(P2_index, old) 

print(P1_oplus, '\n')

print(P2_oplus, '\n')

# populate oplus top-left
for i in range(16):
    for j in range(16):
        PP1_oplus[i,j] = P1_oplus[i,j]

# populate oplus bottom-right
for i in range(16):
    for j in range(16):
        PP1_oplus[i+12,j+12] = P2_oplus[i,j]

print(PP1_oplus)
print(ass(PP1_oplus,12))


# In[ ]:


# Checking PP1 (non-atom)-(non-atom)


integers = list(range(16))
P2_range = list(range(12,28))

# oplus template
PP1_oplus = -1*np.ones((28,28), dtype = int)

# top-left oplus
P1_oplus = oplus_TL(powerset([1,2,3,4]),[[], [1,2,3,4], [1,2], [3,4]])

# bottom-right oplus
P2_oplus = oplus_BR(powerset([1,2,3,4]),[[], [1,2,3,4], [1,2], [3,4]])


P2_index = list(zip(integers, P2_range))
print(P2_index)

# relabel bottom-right
for i in range(16):
    for j in range(16):
        old = P2_oplus[i,j]
        if old != -1:
            P2_oplus[i,j] = switcher(P2_index, old) 

print(P1_oplus, '\n')

print(P2_oplus, '\n')

# populate oplus top-left
for i in range(16):
    for j in range(16):
        PP1_oplus[i,j] = P1_oplus[i,j]

# populate oplus bottom-right
for i in range(16):
    for j in range(16):
        PP1_oplus[i+12,j+12] = P2_oplus[i,j]

print(PP1_oplus)
print(ass(PP1_oplus,12))


# In[ ]:


# Checking PP3 atom-not-atom


integers = list(range(16))
P2_range = list(range(8,24))

# oplus template
PP3_oplus = -1*np.ones((24,24), dtype = int)

# top-left oplus
P1_oplus = oplus_TL(powerset([1,2,3,4]),[[], [1,2,3,4], [1], [2,3,4], [2], [1,3,4], [1,2], [3,4]])

print(P1_oplus, '\n')

# bottom-right oplus
P2_oplus = oplus_BR(powerset([1,2,3,4]),[[], [1,2,3,4], [1], [2,3,4], [2], [1,3,4], [1,2], [3,4]] )

P2_index = list(zip(integers, P2_range))
print(P2_index)

# relabel bottom-right
for i in range(16):
    for j in range(16):
        old = P2_oplus[i,j]
        if old != -1:
            P2_oplus[i,j] = switcher(P2_index, old) 

# populate oplus top-left
for i in range(16):
    for j in range(16):
        PP3_oplus[i,j] = P1_oplus[i,j]

# populate oplus bottom-right
for i in range(16):
    for j in range(16):
        PP3_oplus[i+8,j+8] = P2_oplus[i,j]
        
print(P2_oplus, '\n')

print(PP3_oplus)

print(ass(PP3_oplus,12))


# In[ ]:


# Checking PP3 not-not-atom


integers = list(range(16))
P2_range = list(range(8,24))

# oplus template
PP3_oplus = -1*np.ones((24,24), dtype = int)

# top-left oplus
P1_oplus = oplus_TL(powerset([1,2,3,4]),[[], [1,2,3,4], [1], [2,3,4], [1,2], [3,4], [1,3], [2,4]])

print(P1_oplus, '\n')

# bottom-right oplus
P2_oplus = oplus_BR(powerset([1,2,3,4]),[[], [1,2,3,4], [1], [2,3,4], [1,2], [3,4], [1,3], [2,4]])

P2_index = list(zip(integers, P2_range))
print(P2_index)

# relabel bottom-right
for i in range(16):
    for j in range(16):
        old = P2_oplus[i,j]
        if old != -1:
            P2_oplus[i,j] = switcher(P2_index, old) 

# populate oplus top-left
for i in range(16):
    for j in range(16):
        PP3_oplus[i,j] = P1_oplus[i,j]

# populate oplus bottom-right
for i in range(16):
    for j in range(16):
        PP3_oplus[i+8,j+8] = P2_oplus[i,j]
        
print(P2_oplus, '\n')

print(PP3_oplus)

print(ass(PP3_oplus,12))


# In[8]:


# Checking PP3 not-not-not


integers = list(range(16))
P2_range = list(range(8,24))

# oplus template
PP3_oplus = -1*np.ones((24,24), dtype = int)

# top-left oplus
P1_oplus = oplus_TL(powerset([1,2,3,4]),[[], [1,2,3,4], [1,2], [3,4], [1,3], [2,4], [1,4], [2,3]])

print(P1_oplus, '\n')

# bottom-right oplus
P2_oplus = oplus_BR(powerset([1,2,3,4]),[[], [1,2,3,4], [1,2], [3,4], [1,3], [2,4], [1,4], [2,3]])

P2_index = list(zip(integers, P2_range))
print(P2_index)

# relabel bottom-right
for i in range(16):
    for j in range(16):
        old = P2_oplus[i,j]
        if old != -1:
            P2_oplus[i,j] = switcher(P2_index, old) 

# populate oplus top-left
for i in range(16):
    for j in range(16):
        PP3_oplus[i,j] = P1_oplus[i,j]

# populate oplus bottom-right
for i in range(16):
    for j in range(16):
        PP3_oplus[i+8,j+8] = P2_oplus[i,j]
        
print(P2_oplus, '\n')

print(PP3_oplus)

print(ass(PP3_oplus,12))


# In[7]:


# Checking PP3 not-not-not


integers = list(range(16))

# atom
oplus1 = oplus_TL(powerset([1,2,3,4]),[[],[1,2,3,4],[1,2], [3,4], [1,3],[2,4]])


# not
oplus2 = oplus_TL(powerset([1,2,3,4]),[[1],[2,3,4]])


# # relabel oplus
# for i in range(16):
#     for j in range(16):
#         old = P2_oplus[i,j]
#         if old != -1:
#             P2_oplus[i,j] = switcher(P2_index, old) 
        
print(oplus1, '\n')
print(oplus2)


# In[14]:


# checking PP5 a3,b2 (two lines of plane)


# Checking PP3 not-not-not


integers = list(range(16))
P2_range = list(range(4,20))

# oplus template
PP5_oplus = -1*np.ones((20,20), dtype = int)

# top-left oplus
P1_oplus = oplus_TL(powerset([1,2,3,4]),[[], [1,2,3,4], [1],[2,3,4],[2], [1,3,4], [2,3],[1,4], [1,2], [3,4], [1,3],[2,4]])

print(P1_oplus, '\n')

# bottom-right oplus
P2_oplus = oplus_BR(powerset([1,2,3,4]),[[], [1,2,3,4], [1],[2,3,4],[2], [1,3,4], [2,3], [1,4], [1,2], [3,4], [1,3],[2,4]])

P2_index = list(zip(integers, P2_range))
print(P2_index)

# relabel bottom-right
for i in range(16):
    for j in range(16):
        old = P2_oplus[i,j]
        if old != -1:
            P2_oplus[i,j] = switcher(P2_index, old) 

# populate oplus top-left
for i in range(16):
    for j in range(16):
        PP3_oplus[i,j] = P1_oplus[i,j]

# populate oplus bottom-right
for i in range(16):
    for j in range(16):
        PP3_oplus[i+4,j+4] = P2_oplus[i,j]
        
print(P2_oplus, '\n')

print(PP3_oplus)

print(ass(PP3_oplus,20))


# In[17]:


# checking PP6 a4,b2 (two lines of plane)


# Checking PP3 not-not-not


integers = list(range(16))
P2_range = list(range(2,18))

# oplus template
PP5_oplus = -1*np.ones((18,18), dtype = int)

# top-left oplus
P1_oplus = oplus_TL(powerset([1,2,3,4]),[[], [1,2,3,4], [1],[2,3,4],[2], [1,3,4], [3],[1,2,4], [4],[1,2,3], [1,2], [3,4], [1,3],[2,4]])

print(P1_oplus, '\n')

# bottom-right oplus
P2_oplus = oplus_BR(powerset([1,2,3,4]),[[], [1,2,3,4], [1],[2,3,4],[2], [1,3,4], [3],[1,2,4],[4],[1,2,3], [1,2], [3,4], [1,3],[2,4]])

P2_index = list(zip(integers, P2_range))
print(P2_index)

# relabel bottom-right
for i in range(16):
    for j in range(16):
        old = P2_oplus[i,j]
        if old != -1:
            P2_oplus[i,j] = switcher(P2_index, old) 

# populate oplus top-left
for i in range(16):
    for j in range(16):
        PP3_oplus[i,j] = P1_oplus[i,j]

# populate oplus bottom-right
for i in range(16):
    for j in range(16):
        PP3_oplus[i+2,j+2] = P2_oplus[i,j]
        
print(P2_oplus, '\n')

print(PP3_oplus)

print(ass(PP3_oplus,18))


# In[ ]:




