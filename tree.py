#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
决策树
1. 离散变量
    X是随机变量
    x1, x2, x3 ... xk是所有可能取值
    p1, p2, p3 ... pk是所有可能取值发生的概率
    那么离散变量的期望： E(x) =  x1*p1 + x2*p2 + x3*p3 + ... + xk*pk

2. 信息量
    信息量和概率是负相关的:即概率越大,信息量越小
    比如 下雨天，没有太阳是必然事件，从中得到的信息量就越小
        p(没有太阳,下雨天)=1 , 信息量就越小

        信息量 = -log2(p(x))

3. 信息熵
    X所有取值的信息量的期望
    即 E(x) = -(p1*log(p1) + p2*log(p2) + p3*log(p3) + ... + pk*log(pk))

4. 信息增益
    划分数据之前之后，信息发生的变化叫做信息增益。
    我们可以计算每个特征值划分后前后获得的信息增益。然后信息增益最高的特征值就是数据集最好的选择

    计算信息增益就是计算信息熵. 信息增益就是熵的减少
'''
from math import log
import json
import operator

# 计算信息熵
def calcShannonEnt(dataSet):
    # 先计算概率
    numEntries = len(dataSet)
    lableCounts = {}
    for featVec in dataSet:
        # 获取最后一个标签
        currentLable = featVec[-1]
        if currentLable not in lableCounts.keys():
            lableCounts[currentLable] = 0
        lableCounts[currentLable] += 1
    # 计算熵
    shannoEnt = 0.0
    for key in lableCounts:
         # 计算每个元素的count
         prob = float(lableCounts[key])/numEntries
         shannoEnt -= prob * log(prob, 2)

    return shannoEnt


def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def chooseBestFeatureToSplit(dataSet):
    # 先计算原本数据集dataSet的信息熵
    baseEntropy = calcShannonEnt(dataSet)

    # 当前信息增益为0.0
    bestInfoGain = 0.0

    # 定义bestFeature
    bestFeature = -1

    # 获取数据集特征数量
    # [1, 1, 'yes']
    numFeature = len(dataSet[0]) - 1

    # 计算每个特征
    for i in range(numFeature):
        featList = [line[i] for line in dataSet]
        # 去重
        uniFeatList = set(featList)
        # 计算这个特征的每个值的信息熵
        newEntropy = 0.0
        for value in uniFeatList:
            subDataSet = splitDataSet(dataSet, i, value)
            # 计算子数据集在原来数据集的概率
            prob = len(subDataSet)/float(len(dataSet))
            # 计算当前特征值的信息熵
            newEntropy += prob * calcShannonEnt(subDataSet)

        # 计算信息增益, 信息增益就是熵的减少
        newInfoGain = baseEntropy - newEntropy

        if newInfoGain > bestInfoGain:
            bestInfoGain = newInfoGain
            bestFeature = i
    return bestFeature


def majorityCnt(dataSet):
    classCount = {}
    for vote in dataSet:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount =  sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


# 创建数
def createTree(dataSet, labels):
    # 获取dataSet中所有的分类
    classList = [example[-1] for example in dataSet]

    # 如果剩下的分类和总数一样的话,直接返回第一个分类
    if classList.count(classList[0]) == len(classList):
        return classList[0]

    # 如果就剩下一个分类的话,返回最多的类别
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)

    # 选择最好的特征值
    bestFeature = chooseBestFeatureToSplit(dataSet)
    bestLabel = labels[bestFeature]

    myTree = {bestLabel:{}}
    # 删除已经筛选过的标签
    del(labels[bestFeature])

    featValues = [example[bestFeature] for example in dataSet]
    uniqueValues = set(featValues)
    for value in uniqueValues:
        # 复制整个label
        subLabels = labels[:]
        myTree[bestLabel][value] = createTree(splitDataSet(dataSet, bestFeature, value), subLabels)
    return myTree


def createDataSet():
    dataSet = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no'],
        [0, 1, 'maybe'],
    ]

    labels = ['no surfacing', 'flippers']
    return dataSet, labels


# 使用决策树的分类函数
def classify(inputTree, featLables, testVec):
    # 获取树的根节点
    keys = inputTree.keys()
    # 取树的根节点
    for key in keys:
        firstStr = key
        break

    # 获取根节点的子树
    secondDict = inputTree[firstStr]
    featIndex = featLables.index(firstStr)

    for key in secondDict.keys():
        if testVec[featIndex] == key:
            # 继续迭代
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key],  featLables, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel


# 计算矩阵的信息熵, 熵越高，表示混合的数据也越多
myDat, labels = createDataSet()

treeLabels = labels[:]
# 根据每个特征进行创建树
myTree = createTree(myDat, treeLabels)
print(labels)
#
result = classify(myTree, labels, [1, 0])
print(result)
# 获取当前数据中所有标签的信息熵