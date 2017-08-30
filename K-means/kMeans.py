from numpy import *

def loadDataSet(filename):
    dataMat = []
    fr = open(filename)
    for line in fr.readlines():
        currLine = line.strip().split('\t')
        floatLine = map(float, currLine)
        dataMat.append(floatLine)
    return dataMat

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))

def randCent(dataMat, k):
    col = shape(dataMat)[1]
    centroids = mat(zeros((k, col)))
    for dim in range(col):
        minDim = min(dataMat[:, dim])
        rangeDim = float(max(dataMat[:, dim]) - minDim)
        centroids[:, dim] = minDim + rangeDim *random.rand(k, 1)
    return centroids

def kMeans(dataMat, k, distMeans=distEclud, createCent=randCent):
    row = shape(dataMat)[0]
    clusterAssment = mat(zeros((row, 2)))
    centroids = createCent(dataMat, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(row):
            minDist = inf; minIndex = -1
            for j in range(k):
                distIJ = distMeans(centroids[j, :], dataMat[i, :])
                if distIJ < minDist:
                    minDist = distIJ; minIndex = j
            if clusterAssment[i, 0] != minIndex: clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist**2
        print centroids
        # recalculate new centroids
        for cent in range(k):
            # tuple_of_arrays=nonzero(a):
            #  Parameters: a: array_like
            #  Returns: tuple_of_arrays: tuple (indices of elements that are non-zero)
            # mat.A --> array
            ptsInClust = dataMat[nonzero(clusterAssment[:, 0].A == cent)[0]]
            # axis=0:according to 'col'
            centroids[cent, :] = mean(ptsInClust, axis=0)
    return centroids, clusterAssment

def biKmeans(dataMat, k, distMeans=distEclud):
    row = shape(dataMat)[0]
    clusterAssment = mat(zeros((row, 2)))
    # initialize a cluster
    centroid0 = mean(dataMat, axis=0).tolist()[0]  # [[]] [0]
    centList = [centroid0]
    for j in range(row):
        clusterAssment[j, 1] = distMeans(mat(centroid0), dataMat[j, :])**2
    while len(centList) < k:
        lowestSSE = inf
        for i in range(len(centList)):
            # split some cluster
            ptsInCurrCluster = dataMat[nonzero(clusterAssment[:, 0].A == i)[0], :]
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2)
            sseSplit = sum(splitClustAss[:, 1])
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:, 0].A != i)[0], 1])
            print("sseSplit, and sseNotSplit: ", sseSplit, sseNotSplit)
            if (sseSplit + sseNotSplit) < lowestSSE:
                lowestSSE = sseSplit + sseNotSplit
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
        # assign the NO. of cluster
        bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList)
        bestClustAss[nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit
        print("the bestCentToSplit is: ", bestCentToSplit)
        print("the len of bestClustAss is: ", len(bestClustAss))
        centList[bestCentToSplit] = bestNewCents[0, :]
        centList.append(bestNewCents[1, :])
        clusterAssment[nonzero(clusterAssment[:, 0].A == bestCentToSplit)[0], :] = bestClustAss
    return centList, clusterAssment

dataMat = loadDataSet('testSet2.txt')
dataMat = mat(dataMat)
centList, clusterAssment = biKmeans(dataMat, 3)
print(centList)