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
'''
