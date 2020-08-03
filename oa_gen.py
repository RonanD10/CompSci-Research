#!/usr/bin/env python
# coding: utf-8

# In[3]:


# CHECK 

import numpy as np

def oa_check2(COMP, OPLUS):
    
    n = len(COMP[0])
    
    # Associativity
    for q in range(n):
        for r in range(n):
            # for a given q and r, check if associativity holds for all p
            for p in range(n):
                if COMP[q,r] == 1 and COMP[p, OPLUS[q,r]] == 1 and OPLUS[p, OPLUS[q,r]] != -1:
                    if COMP[p,q] != 1:
                        return False
                    if COMP[OPLUS[p,q], r] != 1:
                        return False
                    if OPLUS[p, OPLUS[q,r]] != OPLUS[OPLUS[p,q], r]: 
                        return False
        
    # If all tests are passed, return True. (Otherwise False was returned above.)
    return True   


# In[4]:


def ass_checker(COMP, OPLUS, entry, value): # return if entry = (q,r) satisfies associativity or not
    n = len(COMP[0])
    q, r = entry
    OPLUS2 = OPLUS.copy()
    OPLUS2[q,r] = value # input guess...
    OPLUS2[r,q] = value
    
    for p in range(n): # check q,r against all other elements
        if(COMP[q,r] == 1 and OPLUS2[p, OPLUS2[q,r]] != -1 and COMP[p, OPLUS2[q,r]] == 1): # check associativity only for non-slots#...if q+r and p+(q+r) are defined, then check...
            if COMP[p,q] != 1 and OPLUS2[p,q] != -1: #p+q is defined
                return False
            if COMP[OPLUS2[p,q], r] != 1 and OPLUS2[OPLUS2[p,q], r] != -1:#(p+q)+r is defined
                return False
            if OPLUS2[p, OPLUS2[q,r]] != OPLUS2[OPLUS2[p,q], r] and OPLUS2[p, OPLUS2[q,r]] != -1 and OPLUS2[OPLUS2[p,q], r] != -1:#p+(q+r) = (P+q)+r holds.
                return False
    return True # if all tests pass, return true


# In[41]:


def generator(COMP, OPLUS):

    """returns solution OPLUS for given COMP,
    else returns no solution"""
    
    n = len(OPLUS[0])
    if oa_check2(COMP, OPLUS):
        return print('This is a valid example:' '\n\n', neg(n), '\n\n', COMP, '\n\n', OPLUS)
    else: 
        for i in range(n):
            for j in range(n):
                if OPLUS[i,j] == -1 and COMP[i,j] == 1:
                    for k in range(n-1): # for each possible guess:
                        if ass_checker(COMP, OPLUS, [i,j], k): # if the element satisfies associativity...
                            OPLUS[i,j] = k  # add new element to OPLUS 
                            OPLUS[j,i] = k
                            generator(COMP, OPLUS)
                            OPLUS[i,j], OPLUS[j,i] = -1, -1
                    return False


# In[38]:


import numpy as np

def random_comp(n): # returns random COMP matrix
    A = np.zeros((n,n), dtype = int)
    A[0,:] = np.ones(n) # fill first row and column with ones
    A[:,0] = np.ones((1,n))
    for i in range(1,n):
        for j in range(i+1,n):
            if i == j:
                A[i,j] = 0
            elif i + j == n-1:
                A[i,j] = 1
            else:  
                A[i,j] = np.random.randint(2,size = 1)
            A[j,i] = A[i,j]
    return A

def temp_oplus(n): # returns OPLUS template 
    
    oplus = np.zeros((n,n), dtype = int)
    
    for i in range(n):
        for j in range(n):
            if i == 0:
                oplus[i,j] = j
            elif j == 0:
                oplus[i,j] = i
            elif i + j == n-1:
                oplus[i,j] = n-1
            else:
                oplus[i,j] = -1
                
    return oplus

def neg(n):
    x = list(range(0,n))
    x.sort(reverse = True)
    return x


# In[39]:


# Example 

import numpy as np

NEG = [3,2,1,0]
COMP = np.array([[1,1,1,1], 
                 [1,0,1,0], 
                 [1,1,0,0], 
                 [1,0,0,0]], dtype = int)

OPLUS = temp_oplus(4)
generator(COMP, OPLUS)


# In[40]:



COMP = np.array([[1,1,1,1,1,1,1,1],
                [1,0,1,1,0,0,1,0],
                [1,1,0,1,0,1,0,0],
                [1,1,1,0,1,0,0,0],
                [1,0,0,1,0,0,0,0],
                [1,0,1,0,0,0,0,0],
                [1,1,0,0,0,0,0,0],
                [1,0,0,0,0,0,0,0]], dtype = int)


OPLUS = np.array([[0,1,2,3,4,5,6,7],
                [1,-1,-1,-1,-1,-1,7,-1],
                [2,-1,-1,6,-1,7,-1,-1],
                [3,-1,6,-1,7,-1,-1,-1],
                [4,-1,-1,7,-1,7,7,-1],
                [5,-1,7,-1,7,-1,7,-1],
                [6,7,-1,-1,7,7,-1,-1],
                [7,-1,-1,-1,-1,-1,-1,-1]], dtype = int)


generator(COMP, OPLUS)


# In[ ]:




