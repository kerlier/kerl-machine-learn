#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
朴素贝叶斯
使用(x,y)表示数据点
使用p(x,y)表示数据点的概率

同一个数据点(x,y)的情况下:
如果p1(x,y) > p2(x,y),那么(x,y)属于类别1
如果p1(x,y) < p2(x,y),那么(x,y)属于类别2

贝叶斯理论的核心思想：选择高概率的类别
    p(类别|特征) = p(特征|类别) * p(类别) / p(特征)

朴素贝叶斯： 朴素的意思是每个特征之间相互独立(这个在现实生活中几乎是不可能的，但是仍对大多数事件起作用)

1. 首先确认类别以及特征。 一个类别会拥有很多个特征
   比如确认 这个文档是否是敏感文档
   类别就是 敏感以及不敏感
   特征就是 敏感文档中含有的敏感词

   那么上面的公式就改为了
     p(敏感|词条) = p(词条|敏感) * p(敏感) / p(词条)


2. 确认每个词汇在文档中出现的概率(p1, p2, p3... pk),
   然后计算每个文档的类别概率: p(class) = p1 * p2 * p3 ... * pk

3. 在相乘的时候，会出现两个问题
    (1)即 有可能某一个pn的概率为0，导致最后的乘机为0， 解决方案：每个词汇表出现的次数初始化为1,分母为2
    (2) 可能会出现多个小数相乘，会出现四舍五入为0的情况，解决方案：使用log(),公式 log(ab) = log(a) + log(b)

4. 词集模型和词袋模型：
    词集模型： 词汇在文档出现的次数只能是0或1, 即使同一个词汇在文档中出现多次
    词袋模型： 词汇在文档出现的总次数。 多次出现会多次计算
'''
import numpy as np


def loadDataSet():
    postingList = [
        ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
    ]
    # 1代表侮辱性文字，0表示正常言论
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec


# 创建词汇表(去重)
def createVocabList(postingList):
    vocabSet = set([])
    for document in postingList:
        # 操作符 | 表示求两个集合的并集
        vocabSet = vocabSet | set(document)
    # 将set转换成list
    return list(vocabSet)


# 将每个文档都转换成向量
def setOfWords2Vec(vocabList, setOfWords):
    returnVec = [0] * len(vocabList)
    for word in setOfWords:
        if word in vocabList:
            # 这里使用的是词集模型
            returnVec[vocabList.index(word)] = 1
        else:
            print('this word is not in vocab list')
    return returnVec


# 将文档列表转换成矩阵
def createMatrix(postingList, vocabList):
    returnMat = []
    for document in postingList:
        returnMat.append(setOfWords2Vec(vocabList, document))
    return returnMat


def trainNBC(trainMatrix, trainCategory):
    # 判断非敏感词汇以及敏感词汇的概率
    # 需要计算每个词汇在敏感以及非敏感文档出现的概率
    numTrainDocs = len(trainMatrix)

    numOfWords = len(trainMatrix[0])

    # 计算敏感文档出现的概率
    pAbusive = sum(trainCategory) / float(numTrainDocs)

    # 计算每个词汇占所有词汇的概率
    # p0Num表示词汇在正常文档中出现的概率
    p0Num = np.ones(numOfWords)
    p0Denom = 2.0

    # p1Num 表示词汇在敏感文档中出现的概率
    p1Num = np.ones(numOfWords)
    p1Denom = 2.0
    for i in range(numTrainDocs):
        # 如果类别是敏感词汇的话，计算p1Num
        if trainCategory[i] == 1:
            # 单个词汇数相加
            p1Num += trainMatrix[i]
            # 所有词汇数相加
            p1Denom += sum(trainMatrix[i])
        else:
            # 计算正常文档，词汇数
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    # p0Vec表示每个词汇在正常文档出现的概率
    p0Vec = np.log(p0Num / p0Denom)
    # p1Vec表示每个词汇在敏感文档中出现的概率
    p1Vec = np.log(p1Num / p1Denom)

    return p0Vec, p1Vec, pAbusive


def classifyNBC(classifyVec, p0Vec, p1Vec, pclass):
    # 敏感文档分类的概率
    p1 = sum(p1Vec * classifyVec) + np.log(pclass)
    # 正常文档分类的概率
    p0 = sum(p0Vec * classifyVec) + np.log(1.0 - pclass)
    if p1 > p0:
        return 1
    else:
        return 0


def testNBC():
    # 加载数据
    postingList, classVec = loadDataSet()
    # 创建词汇表
    vocabList = createVocabList(postingList)
    # 创建向量矩阵
    vocabMatrix = createMatrix(postingList, vocabList)
    # 计算每个词汇的概率
    p0Vec, p1Vec, pAbusive = trainNBC(vocabMatrix, classVec)
    # 计算每个词汇在文档中的概率的乘机。获取某个类别的概率
    print('词汇表:', vocabList)
    print('敏感文档出现的概率:', pAbusive)
    print('每个词汇在正常文档出现的概率:', p0Vec)
    print('每个词汇在敏感文档出现的概率:', p1Vec)

    # 测试向量
    testEntry = ['love', 'my', 'dalmation']
    # 将文字转换成向量
    thisDoc = np.array(setOfWords2Vec(vocabList, testEntry))
    classifyClass = classifyNBC(thisDoc, p0Vec, p1Vec, pAbusive)
    print(classifyClass)

    testEntry1 = ['stupid', 'garbage']
    thisDoc1 = np.array(setOfWords2Vec(vocabList, testEntry1))
    classifyClass1 = classifyNBC(thisDoc1, p0Vec, p1Vec, pAbusive)
    print(classifyClass1)


testNBC()
