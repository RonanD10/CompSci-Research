#!/usr/bin/env python
# coding: utf-8

# In[5]:


def oa_check(NEG, COMP, OPLUS):
    
    n = len(NEG)
    
    # QUICK CHECK: check if NEG is valid
    if n != len(set(NEG)):# Check for duplicates    
        return False
    
    for i in range(n): # Check for 0,...,n-1 in NEG
        if i not in NEG: 
            return False
    
    
    # Commutativity 
    for i in range(n):
        for j in range(n):
            if COMP[i,j] == 1 and COMP[j,i] == 0: 
                return False

    
    # Associativity
    for q in range(n):
        for r in range(n):
            # for a given q and r, check if associativity holds for all p
            for p in range(n):
                if COMP[q,r] == 1 and COMP[p, OPLUS[q,r]] == 1:
                    if COMP[p,q] != 1:
                        return False
                    if COMP[OPLUS[p,q], r] != 1:
                        return False
                    if OPLUS[p, OPLUS[q,r]] != OPLUS[OPLUS[p,q], r]: 
                        return False

    
    # Orthocomplementation
    for p in range(n):
        count = 0
        for q in range(n):
            if COMP[p,q] == 1 and OPLUS[p,q] == n-1:
                count += 1
                if count > 1: # Check uniqueness
                    return False
                if NEG[p] != q:
                    return False
    
    # Consistency
    for p in range(n):
        if COMP[p,p] == 1 and p != 0:
            return False
        
    
    # If all tests are passed, return True. (Otherwise False was returned above.)
    return True   


# In[6]:


# Example 

import numpy as np

NEG = [3,2,1,0]
COMP = np.array([[1,1,1,1], 
                 [1,0,1,0], 
                 [1,1,0,0], 
                 [1,0,0,0]], dtype = int)

OPLUS = np.array([[0, 1, 2, 3], 
                  [1, 0, 3, 0], 
                  [2, 3, 0, 0], 
                  [3, 0, 0, 0]], dtype = int)

oa_check(NEG, COMP, OPLUS)


# In[ ]:




