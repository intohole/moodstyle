#coding=utf-8
#!/usr/bin/env python

from collections import defaultdict
import json

class Classify(object):


    def save(self):
        pass


    def train(self , datas):
        pass

    def classof(self , data):
        pass



class NaiveBayes(Classify):
    '''
    max(P(C|d)) 
    p(c|d) = p(cd) / p(d) = p(d|c) * p(c) / p(d) = p(t1 | c ) * p(t2 | c) ...* p(t3 | c) * p(c)
    p(d) = 1
    p(d|c) 是后验概率 
    '''

    __class = defaultdict(float) #计算各个类别的
    __attributes = {} #属性在各个分类出现的概率 属性 -> 属性值　－＞　类别 - > 概率
    __cc = 0
    __attr = None


    def train(self , datas):
        if datas:
            if isinstance(datas , (str , unicode)):
                pass
            elif not isinstance(datas , dict):
                raise TypeError
            for __cl , __attrs in datas.items():
                self.__class[__cl] += 1.
                self.__cc += 1
                for __attr , __val in __attrs.items():
                    if not self.__attributes.has_key(__attr):
                        self.__attributes[__attr] = {}

                    if not self.__attributes[__attr].has_key(__val):
                        self.__attributes[__attr][__val] = {}

                    if not self.__attributes[__attr][__val].has_key(__cl):
                        self.__attributes[__attr][__val][__cl] = 0


                    self.__attributes[__attr][__val][__cl] += 1
            self.__topro()
            print self.__attributes

    def save(self):
        pass
    
    
    def __topro(self):

        for __cl in self.__class.keys():
            self.__class[__cl] /= self.__cc

        for __attr , __attrval in self.__attributes.items():
            for __val  in __attrval.keys():
                for __cl in self.__class.keys():
                    if self.__attributes[__attr][__val].has_key(__cl):
                        self.__attributes[__attr][__val][__cl] /= float(self.__cc)
                    else:
                        self.__attributes[__attr][__val][__cl] = 0.

    def classof(self , data):
        if data:
            if isinstance(data , dict):
                cl = []
                print 'x'
                print self.__class
                for __cl in self.__class.keys():
                    prob = 0.
                    for __attr ,__val in data.items():
                        print __attr , __cl , __val
                        prob *=self.__attributes[__attr][__val][__cl]
                    cl.append((__cl , prob))
                return sorted(cl , key = lambda x : x[1] , reverse = True )
        raise TypeError











if __name__ == '__main__':
    n = NaiveBayes()
    d = {1: {'a' : 1 , 'b' : 0 , 'c' : 1 } , 2: {'a':1 , 'b': 1 , 'c' : 0 } }
    n.train(d)
    print n.classof({'a' : 1 , 'b' : 0 , 'c' : 0})