# coding=utf-8

from collections import Counter
from collections import defaultdict

class Bayes(object):

    def __init__(self):
        pass

    def classify(self, data):
        pass

    def train(self, datas, dense=True):
        '''
        P(C | I) = P(I | C ) * P(C) /  P(I)
        因为判断 I的存在这个类别概率大小 ， 所以I必然已经存在
        P(C|I) = P(I | C) * P(C) # I 是数据 ， C是类别
        '''


        class_disture = {data[-1] : data[-1] }
        for data in datas:

