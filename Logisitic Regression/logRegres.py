from math import exp
from numpy import *

def loadDataSet():
    '''
    打开数据文件并逐行读取
    :return:输入数据列表/输出标签列表
    '''
    dataMat = labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()  # 去掉每行头尾的障碍字符并分解数据行
        # 每个输入样本中加的1.0为偏置项
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat

def sigmoid(Z):
    '''
    sigmoid函数映射
    :param Z:所有数据样本*所有权值向量
    :return: 映射的概率值
    '''
    return 1.0/(1+exp(-Z))

def gradAscent(dataMat, labelMat):
    '''
    梯度上升优化算法
    :param dataMat:输入数据
    :param labelMat:输出标签
    :return:权值向量的训练结果
    '''
    dataMat = mat(dataMat)
    labelMat = mat(labelMat).transpose()
    row, col = shape(dataMat)
    alpha = 0.001  # 学习率(步长)
    maxCycles = 500
    weights = ones((col, 1))
    for k in range(maxCycles):
        h = sigmoid(dataMat*weights)
        # 参数迭代公式:略去了似然函数及求偏导部分
        weights += alpha * dataMat.transpose() * (labelMat - h)
    return weights








