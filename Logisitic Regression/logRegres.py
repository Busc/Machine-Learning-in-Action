from math import exp
from numpy import *
import matplotlib.pyplot as plt

def loadDataset():
    '''
    open and interpreting 'testSet.txt'
    :return: inputing data samples/outputing labels
    '''
    # if use 'dataMat = labelMat = []', there is an error in line 42
    dataMat = []
    labelMat = []
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
    return weights

def stocGradAscent0(dataMat, labelMat):
    pass


def plotBestFit(weights):
    pass


# print(gradAscent(dataMat, labelMat))











