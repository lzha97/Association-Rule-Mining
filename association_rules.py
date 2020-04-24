import sys
import pandas as pd
import itertools


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
    print("start of large k")
    large_itemsets = {}
    L = one_itemsets(items, min_sup)
    k = 2
    while (L != {}):
        C_k = apriori_gen(list(L.keys()),k)
        print("C_k is after apriori: ", C_k)
        for row in table:
            for c in C_k:
                if (set(c) <= set(row)):
                    C_k[c] += 1
        print("Ck after increment: ", C_k)
        L_k = {}
        for c,count in C_k.items():
            if float(count)/len(table) >= min_sup:
                L_k[c] = count
        k += 1
        large_itemsets.update(L_k)
        L = L_k
        print("L_k is: ", L_k)
        #if k == 4:
            #sys.exit()

    return large_itemsets


## takes a set of large k-1 itemsets and returns a superset of all large k-itemsets.
def apriori_gen(prior_itemsets,k):
    print("in apriori")
    print("prior itemsets: ", prior_itemsets)
    #join
    C_k = set()
    for p in prior_itemsets:
        #print("first p is: ", p)
        #print(type(p))
        new_p = []
        if isinstance(p,tuple):
            #print("yes")
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
                new_itemset = tuple(set(p).union(set(q)))
                if (len(new_itemset) == k):
                    C_k.add(new_itemset)
    #prune
    print("C_k is", C_k)
    C_new = C_k.copy()
    for c in C_k:
        #for i in range(1,k):
            #subsets = []
        subsets = [list(x) for x in itertools.combinations(list(c),k-1)]
        #subsets = list(itertools.combinations(list(c),i))
        print("subsets are: ",subsets)
        for s in subsets:
            if len(s) == 1:
                s = s[0]
            else:
                s = tuple(s)
            print("subset is: ", s)
            if s not in prior_itemsets:
                C_new.remove(c)
                print("s not in prior: ", s)
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

print(items)
print(table)
### find large itemsets
itemsets = large_k_itemsets(items,table,min_sup)
print(itemsets)
