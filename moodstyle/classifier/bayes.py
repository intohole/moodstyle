# coding=utf-8
#!/usr/bin/env python

from collections import defaultdict
import json
import re
import os


class Classify(object):

    def save(self):
        pass

    def train(self, datas):
        pass

    def classof(self, data):
        pass


class NaiveBayes(Classify):

    '''
    max(P(C|d)) 
    p(c|d) = p(cd) / p(d) = p(d|c) * p(c) / p(d) = p(t1 | c ) * p(t2 | c) ...* p(t3 | c) * p(c)
    p(d) = 1
    p(d|c) 是后验概率 
    '''

    __class = defaultdict(float)  # 计算各个类别的
    __attributes = {}  # 属性在各个分类出现的概率 属性 -> 属性值　－＞　类别 - > 概率
    __cc = 0
    __attr = None
    __split = re.compile('[ \t\r\n]+').split

    def train(self, **kw):
        if len(kw) < 0:
            raise TypeError, '**kw is empty !'
        __datas = None
        for __key, __val in kw.items():
            if __key == 'trainFile':
                if not (__val and isinstance(__val, (str, unicode))):
                    raise Exception, 'trainFile type is string or unicode'
                if not (os.path.isfile(__val) and os.path.exists(__val)):
                    raise Exception, 'trainFile isn\'t file or exists!'
                __datas = []
                with open(__val) as f:
                    content = f.readlines()
                    attrs = self.__split(content[0].strip())
                    for i in range(1, len(content)):
                        if len(content[i]) > 0:
                            __cl = content[i].strip().split('\t')
                            if len(__cl) == 2:
                                __tmp = {}
                                __attr = __cl[1].split()
                                if len(__attr) == len(attrs):
                                    for i in range(len(__attr)):
                                        __tmp[attrs[i]] = long(__attr[i])
                                    __datas.append((__cl[0], __tmp))

            elif __key == 'datas':
                if datas:
                    if __val and isinstance(__val , (list , tuple)):
                        __datas.append(val)
                    else:
                        raise TypeError , 'datas value type must be list or tuple'
        if __datas:
            print __datas
            for data in __datas:
                __cl = data[0]
                self.__class[__cl] += 1.
                self.__cc += 1
                for __attr, __val in data[1].items():
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

        for __attr, __attrval in self.__attributes.items():
            for __val in __attrval.keys():
                for __cl in self.__class.keys():
                    if self.__attributes[__attr][__val].has_key(__cl):
                        self.__attributes[__attr][
                            __val][__cl] /= float(self.__cc)
                    else:
                        self.__attributes[__attr][__val][__cl] = 0.

    def classof(self, data):
        if data:
            if isinstance(data, dict):
                cl = []
                for __cl in self.__class.keys():
                    prob = 1.
                    for __attr, __val in data.items():
                        if self.__attributes[__attr][__val][__cl] != 0.:
                            prob *= self.__attributes[__attr][__val][__cl]
                        else:
                            prob *= 0.0001

                    cl.append((__cl, prob))
                return sorted(cl, key=lambda x: x[1], reverse=True)
        raise TypeError


if __name__ == '__main__':
    n = NaiveBayes()
    # d = [(
    #     1, {'a': 1, 'b': 0, 'c': 0}), (2, {'a': 0, 'b': 1, 'c': 0}),
    #     (2, {'a': 0, 'b': 0, 'c': 0}), (1, {'a': 0, 'b': 1, 'c': 1})]
    n.train(trainFile='/home/lixuze/test.dat')
    print n.classof({'a': 0, 'b': 0, 'c': 0})
