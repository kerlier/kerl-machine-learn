#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import operator
import matplotlib
import matplotlib.pyplot as plt


# 创建数据集和标签
def createDataSet():
    group = np.array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


# 求inX 跟每个矩阵中每个元素的距离，然后求出最高的标签
def classify0(inX, dataSet, labels, k):
    # 获取矩阵的行数(维数)
    dataSetSize = dataSet.shape[0]
    # 使用tile函数，将inx向量转换成矩阵
    inXmat = np.tile(inX, [dataSetSize, 1])
    # 求向量之间的差
    diffMat = inXmat - dataSet
    # 根据欧式距离公式进行求距离
    sqDiffMat = diffMat ** 2
    # 求每行的和
    sqDiffSum = sqDiffMat.sum(axis=1)
    # 求平方根
    sqDistance = sqDiffSum ** 0.5
    # 然后获取排序后的下标
    sortIndex = sqDistance.argsort()

    classCount = {}
    if k > dataSetSize:
        k = dataSetSize
    for i in range(k):
        # 获取比较向量的标签
        voteIlabel = labels[sortIndex[i]]
        # 计算标签的数量
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    # 对标签进行排序
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    # 返回最大值的标签
    return sortedClassCount[0][0]


def file2matrix(filepath):
    # 创建数组, 行数为文件中的内容行数, 列数是3
    returnMat = None
    with open(filepath, 'r') as f:
        lines = f.readlines()
        numberOfLines = len(lines)
        returnMat = np.zeros((numberOfLines, 3))
        index = 0

        #获取标签
        classLabelVector = []
        for line in lines:
            line = line.strip()
            # 将数据进行切分
            listFromLine = line.split('\t')
            returnMat[index, :] = listFromLine[0:3]
            # -1表示list最后一个元素
            classLabelVector.append(listFromLine[-1])
            index += 1
        return returnMat, classLabelVector


# 将数值归一化,就是将取值范围改为 0-1 或-1-1之间
# 0-1公式: (当前值-最小值)/(最大值-最小值)
# 使用numpy，必须不要使用for循环
def autoNorm(dataSet):
    # for y in range(dataSet.shape[1]):
    #     xVector = dataSet[:, y]
    #     print(xVector.max())
    #     for x in range(dataSet.shape[0]):
    #         oldValue = dataSet[x, y]
    #         newValue = (oldValue - xVector.min()) / (xVector.max() - xVector.min())
    #         dataSet[x, y] = newValue
    # 获取所有列的最小值, 这里求的都是近似值
    # print(dataSet.min(0))
    minVals = dataSet.min(0)
    # 获取所有列的最大值，求的都是近似值
    # print(dataSet.max(0))
    maxVals = dataSet.max(0)
    # 两个向量的减法, 获取取值范围
    ranges = maxVals - minVals
    # 获取矩阵的行数
    m = dataSet.shape[0]

    # 求两个矩阵的减法
    normDataSet = dataSet - np.tile(minVals, (m, 1))
    normDataSet = normDataSet / np.tile(ranges, (m, 1))

    return normDataSet, ranges, minVals


def datingClassTest():
    # 使用0.9的数据进行测试， 0.1的数据进行校验
    hoRatio = 0.10
    dataSet, labels = file2matrix('./data/ch02/datingTestSet2.txt')

    # 数据归一化
    normMat, ranges, datingLabels = autoNorm(dataSet)

    #获取行数
    m = normMat.shape[0]
    errorCount = 0.0
    numTestVecs = int(m*hoRatio)
    for i in range(numTestVecs):
        result = classify0(normMat[i, :], normMat[numTestVecs:m, :], \
                  labels[numTestVecs:m], 1)
        if result != labels[i]:
            print('this classifier is ', result, ', the real answer is ', labels[i])
            errorCount += 1.0

    print('total error rate is: %f' % (errorCount/float(numTestVecs)))


if __name__ == '__main__':
    # 创建数据集
    group, labels = createDataSet()
    # 目标向量
    inX = [1.0, 1.0]
    lable = classify0(inX, group, labels, 10)
    print(lable)
    # group, labels = createDataSet()
    # print(group)
    # print(labels)
    #
    # # 获取矩阵的shape. shape[0]表示矩阵的行数
    # print(group.shape)
    # print(group.shape[0])
    # print(np.zeros((3, 3)))
    dataSet, labels = file2matrix('./data/ch02/datingTestSet2.txt')
    print(dataSet.shape)
    print(len(labels))
    inX = [1.0, 1.0, 1.0]

    # 输入数据，然后输入标签
    lable = classify0(inX, dataSet, labels, 2)
    print(lable)

    datingClassTest()
    # 使用matplotlib创建散点图
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # # 使用np.array创建数据时，可以指定数据类型
    # # 使用scatter，指定两个轴
    # # [:, 0] 表示所有行，第1列，表示一个向量
    # ax.scatter(dataSet[:, 0], dataSet[:, 1], 15.0 * np.array(labels, dtype=np.float32),
    #            15.0 * np.array(labels, dtype=np.float32))
    # plt.show()
    newDataSet, ranges, minVals = autoNorm(dataSet)
    print(newDataSet)

    #
    # x = [2.2, 2.2]
    # # tile函数将数组重复m,n次
    # # m表示将变成m维数组, n表示数组内重复
    # print(np.tile(x, (4, 1)) - group)
    #
    # diffMat = np.tile(x, (4, 1)) - group
    # print(diffMat ** 2)
    # sqDiffMat = diffMat ** 2
    # print(sqDiffMat.sum(axis=1))
    # print(sqDiffMat.sum(axis=0))
    # sqlDistance = sqDiffMat.sum(axis=1) ** 0.5
    # print(sqlDistance)
    # print(sqlDistance.argsort())
    # sortedDist = sqlDistance.argsort()
    # # 获取距离最近的k个点
    # classCount = {}
    # for i in range(3):
    #     print(sortedDist[i])
    #     voteIlabel = labels[sortedDist[i]]
    #     print(voteIlabel)
    #     classCount[voteIlabel]= classCount.get(voteIlabel, 0) +1
    # print(classCount)
    #
    # l = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    # print(l)
    # print(l[0][0])
    # arrayLines = []
    # index = 0
    # arrayLines.append("1 1 1")
    # arrayLines.append("2 2 2 ")
    # returnMat = np.zeros((2, 3))
    # for line in arrayLines:
    #     line = line.strip()
    #     listFromLine = line.split(" ")
    #     print('format', listFromLine[0:3])
    #     returnMat[index, :] = listFromLine[0:3]
    #     index += 1
    #
    # print(returnMat)