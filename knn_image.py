#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from kNN import *
from os import listdir
import numpy as np


# 将32x32的数据转换成一个1x1024的向量
def img2Vector(filePath):
    returnVec = np.zeros((1, 1024))
    fr = open(filePath)

    # 读取每一行文件的行数
    for i in range(32):
        lineStr = fr.readline()
        # 当前行加到向量中
        for ch in range(32):
            returnVec[0, 32*i + ch] = int(lineStr[ch])
    return returnVec


def createDateSetFromFile():
    files = listdir('./data/ch02/digits/trainingDigits/')
    fileNumber = len(files)
    # 创建fileNumber数组
    dataSet = np.zeros((fileNumber, 1024))
    file_labels = []

    i = 0
    for file in files:
        dataSet[i, :] = img2Vector('./data/ch02/digits/trainingDigits/%s' % file)
        # 获取当前文件的标签
        file_label = file.split('_')[0]
        file_labels.append(file_label)
        i += 1

    return dataSet, file_labels


def testDigintTest():
    # 获取测试数据
    dataSet, file_labels = createDateSetFromFile()
    test_files = listdir('./data/ch02/digits/testDigits')
    fileNumber = len(test_files)
    errorCount = 0
    for test_file in test_files:
        test_vec = img2Vector('./data/ch02/digits/testDigits/%s' % test_file)
        label = test_file.split("_")[0]
        test_label = classify0(test_vec, dataSet, file_labels, 3)
        if label != test_label:
            errorCount += 1

    print('total error percent is', (errorCount*1.0)/float(fileNumber))


if __name__ == '__main__':
    returnVec = img2Vector('./data/ch02/digits/trainingDigits/0_0.txt')
    print(returnVec)
    testDigintTest()
    # dataSet, file_labels = createDateSetFromFile()
    #
    # test_vec = img2Vector('./data/ch02/digits/testDigits/2_14.txt')
    # label = classify0(test_vec, dataSet, file_labels, 3)
    # print(label)