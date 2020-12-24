#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 使用正则表达式切分句子
import bayes
import numpy as np


def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 0]
    # regEx = re.compile('\\W+')
    # mySent = 'This book is the book on python or M.L. I have ever laid eyes upon.'
    # words = regEx.split(mySent)
    # # 去除空格, 需要将每个单词改为小写
    # newWords = [word.lower() for word in words if len(word) > 0]
    # print(newWords)


# 测试垃圾邮件
def spamTest():
    docList = []; classList = []; fullText = []
    # 读取spam下面的26个文件
    for i in range(1, 26):
        # 垃圾邮件的分类
        wordList = textParse(open('./data/spam/%d.txt' % i).read())
        # 添加到docList中
        docList.append(wordList)
        # extend是将list1的元素添加进来
        fullText.extend(wordList)
        classList.append(1)

        # 正常邮件的分类
        wordList = textParse(open('./data/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)

    # 创建词汇表：需要文档列表 postingList。 读取所有的txt并进行词汇切分
    vocabList = bayes.createVocabList(docList)

    docMartix = np.zeros((50, len(vocabList)))
    i = 0
    for document in docList:
        # 需要将每个文档进行转换成向量
        docVec = bayes.setOfWords2Vec(vocabList, document)
        # 添加类别
        docMartix[i, :] = docVec
        i += 1
    print('词汇表长度：', len(vocabList))
    print('词汇表内容：', vocabList)
    print('文档内容：', docList[0], '\n词汇数', len(docList[0]))
    print('文档矩阵：', docMartix[0], '\n词汇数', sum(docMartix[0]))

    # 训练贝叶斯
    p0Vec, p1Vec, pAbusive = bayes.trainNBC(docMartix, classList)
    # print(p1Vec)
    # print(p0Vec)
    # print(pAbusive)
    # 测试函数
    i = 0
    errorCount = 0
    for document in docList:
        testVec = bayes.setOfWords2Vec(vocabList, document)
        testClass = bayes.classifyNBC(np.array(testVec), p0Vec, p1Vec, pAbusive)
        if testClass != classList[i]:
            errorCount += 1
        i += 1
    print('error percent: ', errorCount/float(len(docList)))


spamTest()
