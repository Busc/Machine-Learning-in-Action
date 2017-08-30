from math import exp
from numpy import *
import matplotlib.pyplot as plt

def loadDataset():
    '''
    open and interpreting 'testSet.txt'
    :return: inputing data samples/outputing labels
    '''
    # if use 'dataMat = labelMat = []', there is an error in line 42
    dataMat = [];  labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        # bias:1.0
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat

def sigmoid(Z):
    '''
    Sigmoid
    :param Z:samples*weights
    :return: probabilities
    '''
    return 1/(1+exp(-Z))

def gradAscent(dataMat, labelMat):
    '''
    Gradient ascent optimization
    :param dataMat:sample_x
    :param labelMat:label_y
    :return:weights
    '''
    dataMatrix = mat(dataMat)
    labelMatrix = mat(labelMat).transpose()
    row, col = shape(dataMatrix)
    alpha = 0.001  # learning rate
    maxCycles = 500
    weights = ones((col, 1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix*weights)
        # iteration formula: omitting the derivation about likelihood function and its derivative
        weights += alpha * dataMatrix.transpose() * (labelMatrix - h)
    # weights = [w_con;w_cord1;w_cord2]
    return weights

def stoGradAscent0(dataMat, labelMat):
    '''
    Stochastic gradient ascent optimization
    :param dataMat:sample_x
    :param labelMat:label_y
    :return:weights
    '''
    dataArr = array(dataMat)
    row, col = shape(dataArr)
    alpha = 0.01
    weights = ones(col)
    for k in range(row):
        # * in array == .* in matrix
        h = sigmoid(sum(dataArr[k]*weights))
        weights += alpha * dataArr[k] * (labelMat[k]-h)
    return weights

def plotBestFit(weights, dataMat, labelMat):
    dataArr = array(dataMat)
    rows = shape(dataArr)[0]
    x0_cord1 = []; x0_cord2 = []; x1_cord1 = []; x1_cord2 = []
    for row in range(rows):
        # dataArr[row,0]=1(bias)
        if int(labelMat[row]) == 1:
            x1_cord1.append(dataArr[row, 1]); x1_cord2.append(dataArr[row, 2])
        else:
            x0_cord1.append(dataArr[row, 1]); x0_cord2.append(dataArr[row, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # make a scatter plot of cord1 vs cord2
    ax.scatter(x1_cord1, x1_cord2, s=30, c='red', marker='s')
    ax.scatter(x0_cord1, x0_cord2, s=30, c='green')
    # WX = 0
    cord1 = arange(-3, 3, 0.1)
    cord2 = (-weights[0]-weights[1]*cord1)/weights[2]
    ax.plot(cord1, cord2)
    plt.xlabel('cord1'); plt.ylabel('cord2');
    plt.show()




dataMat, labelMat = loadDataset()

gradWeights = gradAscent(dataMat, labelMat)
print('gradWeights = ')
print(gradWeights)
# Figure 1
plotBestFit(gradWeights, dataMat, labelMat)

sto_gradWeights0 = stoGradAscent0(dataMat, labelMat)
print('sto_gradWeights0 = ')
print(sto_gradWeights0)
# Figure 2
plotBestFit(sto_gradWeights0, dataMat, labelMat)













