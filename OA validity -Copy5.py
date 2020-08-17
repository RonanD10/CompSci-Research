#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
print(powerset([1,2,3,4]))


# In[3]:


d1 = {'b' : 0, "b'":1, "c":2, "c'":3, "0":4 ,'1':5, "a":6,"a'":7, "d":8,"d'":9, "e":10,"e'":11}

def f(n):
    return d1.get(n)


# now to manually write OPLUS


OPLUS = np.zeros((12,12), dtype = int)

for i in range(12):
    if i == f('0'):
        OPLUS[i,i] = f('0')
    else:
        OPLUS[i,i] = -1

entries = [[f('1'),f("a'"),-1,f('b'), -1,f("c'"),-1,-1,-1,-1,-1],
          [-1,-1,f("b'"),-1,-1,-1,-1,-1,-1,-1],
          [f('1'),f('c'),-1,f("b'"), -1,-1,-1,-1,-1],
          [f("c'"),-1,-1,-1,-1,-1,-1,-1],
          [f("1"),f("a"),f("a'"), f("d"), f("d'"),f("e"),f("e'")],
          [-1,-1,-1,-1,-1,-1],
          [f("1"),f("e'"),-1,f("d'"),-1],
          [-1,-1,-1,-1],
          [f("1"),f("a'"),-1],
          [-1,-1],
          [f("1")]]

# for k in entries:
#     print(len(k))

for i in range(11):
    OPLUS[i,i+1:] = entries[i]
    OPLUS[i+1:,i] = entries[i]
        
print(OPLUS)
    
# now to check associativity

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

print(ass(OPLUS))


# In[18]:


# Create COMP for a Boolean algebra

def indexer(p, E):
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
    
def comp(p, E):
    """takes in powerset p and returns corresponding COMP matrix
       with E being the bottom and right elements"""
    
    COMP = np.zeros((len(p), len(p)), dtype = int)
    
    # index for p
    index = indexer(p, E)
    print(index)

    # find which elements are compatible
    eins = ones(p,index,0)
    
    # fill in ones in COMP
    for x in eins:
        y = list(x)
        i = y[0]
        j = y[1]
        COMP[i, j] = 1
    
    return COMP
    
p = powerset([1,2,3])
print(comp(p, []))
print(comp(p, [[], [1,2,3], [1], [2,3]]))


# In[17]:


# make OPLUS for Boolean algebras

def join(a,b):
    """returns the least upper bound of a,b"""
    if type(a) == int and type(b) != int:
        return b
    else:
        return a.union(b)

def oplus(p,E):
    """returns OPLUS of the powerset p"""
    n = len(p)
    OPLUS = -1*np.ones((n,n), dtype = int)
    
    # index for enumerating elements of p
    index = indexer(p, E)
    
    # non-trivial entries in OPLUS
    entries = ones(p, index, 1)   
    
    for k in entries:
        i = switcher(index, k[0])
        j = switcher(index, k[1])
        OPLUS[i, j] = switcher(index, join(k[0],k[1]))
    
    return OPLUS
    
# p = powerset([1,2])
# print(oplus(p))


# In[8]:


# Checking method works for LL1


COMP1 = comp(powerset([1,2,3]),[])
OPLUS1 = oplus(powerset([1,2,3]),[])
# print(COMP1, '\n')
# print(OPLUS1)
# print(ass(OPLUS1,8))


L1_range = list(range(8))
L2_range = list(range(4,12))

LL1_comp = np.zeros((12,12), dtype = int) # comp pasting template

L1_comp = comp(powerset([1,2,3]), [[], [1,2,3], [1], [2,3]], ) # top-left comp which has 0,1,a,a' at overlap
print(L1_comp,'\n')
L2_comp = comp(powerset([1,2,3]),[]) # bottom-right comp which is unchanged
print(L2_comp,'\n')

for i in range(8):
    for j in range(8):
        LL1_comp[i,j] = L1_comp[i,j]
        LL1_comp[i+4,j+4] = L2_comp[i,j]
    
print(LL1_comp, '\n')

LL1_oplus = -1*np.ones((12,12), dtype = int)

L1_oplus = oplus(powerset([1,2,3]),[[], [1,2,3], [1], [2,3]])

print(L1_oplus, '\n')

L2_oplus = oplus(powerset([1,2,3]), [] )

print(L2_oplus, '\n')

L2_index = list(zip(L1_range, L2_range))
print(L2_index)

for i in range(8):
    for j in range(8):
        old = L2_oplus[i,j]
        if old != -1:
            L2_oplus[i,j] = switcher(L2_index, old) 
            
for i in range(8):
    for j in range(8):
        LL1_oplus[i,j] = L1_oplus[i,j]
        LL1_oplus[i+4,j+4] = L2_oplus[i,j]
        
print(L2_oplus, '\n')

print(LL1_oplus)

print(ass(LL1_oplus,12))


# In[16]:


# Checking LP1


integers = list(range(16))
P1_range = list(range(4,20))

# oplus template
LP1_oplus = -1*np.ones((20,20), dtype = int)

# top-left oplus
L1_oplus = oplus(powerset([1,2,3]),[[], [1,2,3], [1], [2,3]])

print(L1_oplus, '\n')

# bottom-right oplus
P1_oplus = oplus(powerset([1,2,3,4]), [] )

print(P1_oplus, '\n')

P1_index = list(zip(integers, P1_range))
print(P1_index)

# relabel bottom-right
for i in range(16):
    for j in range(16):
        old = P1_oplus[i,j]
        if old != -1:
            P1_oplus[i,j] = switcher(P1_index, old) 

# populate oplus top-right
for i in range(8):
    for j in range(8):
        LP1_oplus[i,j] = L1_oplus[i,j]

for i in range(16):
    for j in range(16):
        LP1_oplus[i+4,j+4] = P1_oplus[i,j]
        
print(P1_oplus, '\n')

print(LP1_oplus)

print(ass(LP1_oplus,12))


# In[10]:


# Checking PP1


integers = list(range(16))
P2_range = list(range(4,20))

# oplus template
PP1_oplus = -1*np.ones((28,28), dtype = int)

# top-left oplus
P1_oplus = oplus(powerset([1,2,3,4]),[[], [1,2,3,4], [1], [2,3,4]])

print(P1_oplus, '\n')

# bottom-right oplus
P2_oplus = oplus(powerset([1,2,3,4]), [] )

print(P2_oplus, '\n')

P2_index = list(zip(integers, P2_range))
print(P2_index)

# relabel bottom-right
for i in range(16):
    for j in range(16):
        old = P2_oplus[i,j]
        if old != -1:
            P2_oplus[i,j] = switcher(P2_index, old) 

# populate oplus top-right
for i in range(16):
    for j in range(16):
        PP1_oplus[i,j] = P1_oplus[i,j]

for i in range(16):
    for j in range(16):
        PP1_oplus[i+12,j+12] = P2_oplus[i,j]
        
print(P2_oplus, '\n')

print(PP1_oplus)

print(ass(PP1_oplus,12))


# In[13]:


# Checking PP3


integers = list(range(16))
P2_range = list(range(8,24))

# oplus template
PP3_oplus = -1*np.ones((24,24), dtype = int)

# top-left oplus
P1_oplus = oplus(powerset([1,2,3,4]),[[], [1,2,3,4], [1], [2,3,4], [2], [1,3,4], [3], [1,2,4]])

print(P1_oplus, '\n')

# bottom-right oplus
P2_oplus = oplus(powerset([1,2,3,4]), [] )

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


# In[21]:


# What happens if we paste along 0,b,b',1 but b is non-atomic? 

# Checking PL1 case 2


integers = list(range(8))
L1_range = list(range(12,20))

# oplus template
PL1_oplus = -1*np.ones((20,20), dtype = int)

# top-left oplus
P1_oplus = oplus(powerset([1,2,3,4]),[[], [1,2,3,4], [1,3], [2,4]])

print(P1_oplus, '\n')

# bottom-right oplus
L1_oplus = oplus(powerset([1,2,3]), [] )

print(P1_oplus, '\n')

L1_index = list(zip(integers, L1_range))
print(L1_index)

# relabel bottom-right
for i in range(8):
    for j in range(8):
        old = L1_oplus[i,j]
        print(old)
        if old != -1:
            L1_oplus[i,j] = switcher(L1_index, old) 

# populate oplus top-right
for i in range(16):
    for j in range(16):
        PL1_oplus[i,j] = P1_oplus[i,j]

for i in range(8):
    for j in range(8):
        LP1_oplus[i+12,j+12] = P1_oplus[i,j]
        
print(P1_oplus, '\n')

print(LP1_oplus)

print(ass(LP1_oplus,12))


# In[ ]:


# Checking PP1 (non-atom)-(non-atom)


integers = list(range(16))
P2_range = list(range(4,20))

# oplus template
PP1_oplus = -1*np.ones((28,28), dtype = int)

# top-left oplus
P1_oplus = oplus(powerset([1,2,3,4]),[[], [1,2,3,4], [1,2], [3,4]])

print(P1_oplus, '\n')

# bottom-right oplus
P2_oplus = oplus(powerset([1,2,3,4]), [] )

print(P2_oplus, '\n')

P2_index = list(zip(integers, P2_range))
print(P2_index)

# relabel bottom-right
for i in range(16):
    for j in range(16):
        old = P2_oplus[i,j]
        if old != -1:
            P2_oplus[i,j] = switcher(P2_index, old) 

# populate oplus top-right
for i in range(16):
    for j in range(16):
        PP1_oplus[i,j] = P1_oplus[i,j]

for i in range(16):
    for j in range(16):
        PP1_oplus[i+12,j+12] = P2_oplus[i,j]
        
print(P2_oplus, '\n')

print(PP1_oplus)

print(ass(PP1_oplus,12))

