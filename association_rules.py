import sys
import pandas as pd
import itertools
import time

t = time.time()


def log(x, s=sys.argv[2], c = sys.argv[3]):
    print(x)
    with open('logs/'+ str(t)+'_'+str(s)+'_'+str(c)+'.txt', 'a+') as file:
        file.write(x+'\n')


def compute_confidence(itemsets, min_conf):
    rules = {}
    ct_rules_extracted = 0
    for iset in itemsets.keys():
        if len(iset) >= 2:
            for i in iset:
                lhs = iset.difference([i])
                rhs = iset
                numerator = itemsets[rhs]
                denominator = itemsets[lhs]
                score = float(numerator)/float(denominator)
                if score >= min_conf and (lhs,i) not in rules:
                        rules[(lhs,i)] = score
                        ct_rules_extracted += 1

    return rules, ct_rules_extracted


### Returns large 1-itemsets
def one_itemsets(items, min_sup):
    L_1 = {}
    for item in items:
        if frozenset([item]) not in L_1:
            L_1[frozenset([item])] = 1
        else: L_1[frozenset([item])] += 1

    L_1_copy = L_1.copy()
    num_baskets = float(len(L_1.keys()))
    for item,count in L_1.items():
        if (float(count)/num_baskets < min_sup):
            del L_1_copy[item]

    return L_1_copy


### Find large itemsets
def large_k_itemsets(items, table, min_sup):
    large_itemsets = {}
    L = one_itemsets(items, min_sup) # L_(k-1): set of large itemsets that have k-1 items, L from previous iteration
    large_itemsets.update(L)
    k = 2
    while (L != {}):
        C_k = apriori_gen(list(L.keys()),k) # C_k : set of potentially large itemsets that have k number of items
        for row in table:
            for c in C_k:
                if (c <= set(row)):
                    C_k[c] += 1

        L_k = {}
        for c,count in C_k.items():
            if float(count)/len(table) >= min_sup:
                L_k[c] = count

        k += 1
        large_itemsets.update(L_k)
        L = L_k # L: set of large itemsets that have k number of items that meet min support out of C_k

    return large_itemsets


## takes a set of large k-1 itemsets and returns a superset of all large k-itemsets.
def apriori_gen(prior_itemsets,k):
    #join
    C_k = set()
    for p in prior_itemsets: # L_(k-1)
        new_p = []
        if isinstance(p,tuple):
            for i in p:
                new_p.append(i)
            p = new_p
        else:
            p = list(p)
        for q in prior_itemsets:
            new_q = []
            if isinstance(q,tuple):
                for i in q:
                    new_q.append(i)
                q = new_q
            else:
                q = list(q)
            if p[:-1] == q[:-1] and p[-1] < q[-1]:
                new_itemset = frozenset(set(p).union(set(q))) # a set that belongs in C_k
                if (len(new_itemset) == k):
                    C_k.add(new_itemset)

    #prune
    C_new = C_k.copy() # C_new is a copy of C_k for deletion during iteration.
    for c in C_k:
        subsets = [list(x) for x in itertools.combinations(list(c),k-1)]
        for s in subsets:
            if frozenset(s) not in prior_itemsets:
                C_new.remove(frozenset(c))
                break

    return dict.fromkeys(C_new,0)



### Get input
dataset = sys.argv[1]
min_sup = float(sys.argv[2])
min_conf = float(sys.argv[3])


### read data
data = pd.read_csv(dataset)
table = []
for i in range(data.shape[0]):
    table.append([str(data.values[i,j]) for j in range(data.shape[1])])

### get list of items
items = []
for row in table:
    for item in row:
        if (item != 'nan'):
            items.append(item)

log('############# ITEMS #############')
log('Number of items: '+str(len(items)))
#log(str(items)+ '\n\n')
log('\n############# TABLE #############')
log('Number of rows: '+str(len(table)))
#log(str(table)+ '\n\n')
### find large itemsets

itemsets = large_k_itemsets(items,table,min_sup)
log('\n############# ITEMSETS #############\n')
for i in itemsets:
    log(str(set(i))+': '+ str(itemsets[i]))
log('\nNumber of itemsets: '+str(len(itemsets)))


print('\n############# ASSOCIATION RULES #############\n')
high_conf_rules, ct_rules = compute_confidence(itemsets, min_conf)
for r in high_conf_rules:
    log('Rule: ' +  str(set(r[0])) + '--> (' +  str(r[1]) +  ')\t Score:' +  str(high_conf_rules[r]))
log(str(ct_rules) + ' Rules Extracted. ')
