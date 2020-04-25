import sys
import pandas as pd
import itertools
import time

t = time.time()

def log(x, s=sys.argv[2], c = sys.argv[3]):
    print(x)
    with open('logs/'+ str(t)+'_'+str(s)+'_'+str(c)+'.txt', 'a+') as file:
        file.write(x+'\n')


### Returns large 1-itemsets
def one_itemsets(items, min_sup):
    L_1 = {}
    for item in items:
        L_1[item] = items.count(item)
    for item,count in L_1.items():
        if (count < min_sup):
            del L_1[item]
    return L_1


### Find large itemsets
def large_k_itemsets(items, table, min_sup):
    log("start of large k")
    large_itemsets = {}
    L = one_itemsets(items, min_sup) # L_(k-1): set of large itemsets that have k-1 items, L from previous iteration
    large_itemsets.update(L)
    k = 2
    while (L != {}):
        C_k = apriori_gen(list(L.keys()),k) # C_k : set of potentially large itemsets that have k number of items
        log("C_k is after apriori: "+str(C_k))
        for row in table:
            for c in C_k:
                if (set(c) <= set(row)):
                    C_k[c] += 1
        log("Ck after increment: " + str(C_k))
        L_k = {}
        for c,count in C_k.items():
            if float(count)/len(table) >= min_sup:
                L_k[c] = count
        k += 1
        large_itemsets.update(L_k)
        L = L_k # L: set of large itemsets that have k number of items that meet min support out of C_k
        log("L_k is: "+ str(L_k))

    return large_itemsets


## takes a set of large k-1 itemsets and returns a superset of all large k-itemsets.
def apriori_gen(prior_itemsets,k):
    log("in apriori")
    log("prior itemsets: "+str(prior_itemsets))
    #join
    C_k = set()
    for p in prior_itemsets: # L_(k-1)
        new_p = []
        if isinstance(p,tuple):
            for i in p:
                new_p.append(i)
            p = new_p
        else:
            p = [p]
        for q in prior_itemsets:
            new_q = []
            if isinstance(q,tuple):
                for i in q:
                    new_q.append(i)
                q = new_q
            else:
                q = [q]
            if p[:-1] == q[:-1] and p[-1] != q[-1]:
                new_itemset = tuple(set(p).union(set(q))) # a set that belongs in C_k
                if (len(new_itemset) == k):
                    C_k.add(new_itemset)
    #prune
    log("C_k is: "+ str(C_k))
    C_new = C_k.copy() # C_new is a copy of C_k for deletion during iteration.
    for c in C_k:
        subsets = [list(x) for x in itertools.combinations(list(c),k-1)]
        log("subsets are: "+str(subsets))
        for s in subsets:
            if len(s) == 1:
                s = s[0]
            else:
                s = tuple(s)
            log("subset is: "+str(s))
            if s not in prior_itemsets:
                C_new.remove(c)
                log("s not in prior: "+str(s))
                break

    return dict.fromkeys(C_new,0)



### Get input
dataset = sys.argv[1]
min_sup = float(sys.argv[2])
min_conf = float(sys.argv[3])


### read data
data = pd.read_csv(dataset)
table = data.values

### get list of items
items = []
for row in table:
    for item in row:
        if (item != 'nan'):
            items.append(item)

log('############# ITEMS #############')
log('Number of items: '+str(len(items)))
#log(str(items)+ '\n\n')
log('############# TABLE #############')
log('Number of rows: '+str(len(table)))
#log(str(table)+ '\n\n')
### find large itemsets
itemsets = large_k_itemsets(items,table,min_sup)
log('############# ITEMSETS #############\n')
for i in itemsets:
    log(str(i)+': '+ str(itemsets[i]))
log('\nNumber of itemsets: '+str(len(itemsets)))
