# coding=utf-8
#!/usr/bin/env python


'''
Wi <- Wi + change Wi
z = w1 * x1 + w2 * x2 + b

'''

from math import exp
from random import randint
from random import random

a = [1, 1 , 1 ]
step = 0.1



class Logistic(object):

    __weights = None
    __datalen = 0
    __rate = 0.01

    def __init__(self , rate = 0.01):
        if rate:
            if isinstance(rate , float):
                if rate > 0 :
                    self.__rate = rate


    def __sigmod(self , x):
        return 1 / (1 + exp(-x))


    def __initweights(self , l):
        if not self.__weights:
            if l and isinstance(l , int ) and l > 0:
                self.__weights = []
                [self.__weights.append(1) for i in range(l)]
                self.__datalen = l
                return 
            raise TypeError , '数组长度不正确　必须是整数'



    def train(self , datas):
        if datas:
            if isinstance(datas , (list , tuple)):
                for i in range(len(datas)):
                    self.update(data[i][0] , data[i][1])

    def update(self , data , label):
        if data:
            if isinstance(data , (tuple , list)):
                self.__initweights(len(data))
                for i in range(self.__datalen):
                    self.__weights[i] = self.__weights[i] + self.__rate * (label - self.predict(data)) * data[i]


    def predict( self , data):
        if self.__predict(data) > 0.5:
            return 1
        else:
            return 0

    def __predict(self , data):
        if data:
            if isinstance(data , (list , tuple)):
                __x = 0.
                for i in range(self.__datalen):
                    __x += data[i] * self.__weights[i]
                return self.__sigmod(__x)


lg = Logistic()
    


for i in range(20000):
    if i % 2 == 0:
        lg.update([-random() * 20, - random() * 20] , 0)
        lg.update([-random() * 20, random() * 20] , 0)
    else:
        lg.update([random() * 20, random() * 20], 1)
        lg.update([random() * 20, - random() * 20] , 1)
print a
print lg.predict([-0.5 , 1])
print lg.predict((20 ,10))
print lg.predict((10 , 20))
print lg.predict((4,-4.5))
