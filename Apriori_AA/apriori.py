def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def aprioriGenC1(dataSet):
    '''
    create item sets including only one element
    '''
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            # non duplicate items in C1
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    # C1 will be the keys of a dict, so it must be immutable
    return map(frozenset, C1)

def scanD(dataSet, Ck, minSupport):
    '''
    Ck --> Lk
    :param dataSet: List[List]
    :param Ck: frozenset
    :param minSupport: float
    :return:List, Dict
    '''
    dataSet = map(set, dataSet)
    ssCnt = {}
    # count occurrence number of every candidate item
    for transaction in dataSet:
        for can in Ck:
            # candidate item is in current transaction
            if can.issubset(transaction):
                if can not in ssCnt:
                    # key 'can' does not yet exist
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    totalTrans = float(len(dataSet))
    # meet the minimum requirements
    Lk = []
    supportData = {}
    for key in ssCnt:
        # calculate all 'support'
        support = ssCnt[key]/totalTrans
        if support >= minSupport:
            Lk.append(key)
        supportData[key] = support
    return Lk, supportData

def aprioriGen(Lk):
    '''
    Lk --> C(k+1)
    :param Lk: frequent itemsets (List)
    :return: candidate sets - each contains k+1 elements (List[List])
    '''
    Lk = map(set, Lk)
    Ck1 = []
    k = len(Lk[0])
    for i in range(len(Lk)):
        Lk_1 = list(Lk[i])[:k-1]
        Lk_1.sort()
        for j in range(i+1, len(Lk)):
            # union two sets
            if k < 2:
                Ck1.append(Lk[i] | Lk[j])
            ##########!!!!!!!!!!
            else:
                Lk_2 = list(Lk[j])[:k-1]
                Lk_2.sort()
                if Lk_1 == Lk_2:
                    Ck1.append(Lk[i] | Lk[j])
    return map(frozenset, Ck1)

def apriori(dataSet, minSupport = 0.5):
    '''
    :param dataSet:List[List[int]]
    :param minSupport:float
    :return: L:List[List[frequent item sets]]; supportData:Dict{L:Support}
    '''
    # initialize C1
    C1 = aprioriGenC1(dataSet)
    # C1 --> L1
    L1, supportData = scanD(dataSet, C1, minSupport)
    L = [L1]
    while len(L[-1]) > 0:
        # Lk(i.e. L[-1]) --> Ck1
        Ck1 = aprioriGen(L[-1])
        # Ck1 --> Lk1
        Lk1, supportCurr = scanD(dataSet, Ck1, minSupport)
        L.append(Lk1)
        supportData.update(supportCurr)
    return L, supportData

def calcConf(freqSet, conSeq, supportData, rl, minConf=0.7):
    prunedConseq = []
    for conseq in conSeq:
        # antecedent = frequentSet - consequent
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        if conf >= minConf:
            #print(freqSet-conseq, '-->', conseq, ' ', conf)
            rl.append((freqSet-conseq, conseq, conf))
            prunedConseq.append(conseq)
    return prunedConseq

def rulesFromConseq(freqSet, conSeq, supportData, rl, minConf=0.7):
    k = len(conSeq[0])
    if len(freqSet) > k+1:
        # candidate sets can be generated further
        prunedConseq = aprioriGen(conSeq)
        prunedConseq = calcConf(freqSet, prunedConseq, supportData, rl, minConf)
        if len(prunedConseq) > 1:
            # can be merged further
            rulesFromConseq(freqSet, prunedConseq, supportData, rl, minConf)

def geneRules(L, supportData, minConf=0.7):
    ruleList = []
    # frequent item sets containing more than 1 elem
    # one elem can not form a 'rule'
    for i in range(1, len(L)):
        # for every frequent item set
        for freqSet in L[i]:
            # every item in conSeq1 has only one elem
            conSeq1 = [frozenset([item]) for item in freqSet]
            if i > 1:
                # frequent item set containing more than 2 elems
                rulesFromConseq(freqSet, conSeq1, supportData, ruleList, minConf)
            else:
                # frequent item set containing 2 elems
                calcConf(freqSet, conSeq1, supportData, ruleList, minConf)
    return ruleList


dataSet = loadDataSet()

# Apriori --> frequent item sets(min Support)
L, supportData = apriori(dataSet)
print(L, supportData)

# frequent item sets --> association rules(min Confidence)
rules = geneRules(L, supportData, minConf=0.5)
print(rules)









