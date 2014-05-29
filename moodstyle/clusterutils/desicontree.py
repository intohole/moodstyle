# coding=utf-8
#!/usr/bin/env python

import math


class DecisionTree(object):

    __data = {'a': {'c': {1: 30, 2: 70}, 'd': {1: 20, 0: 80}, 'e': {1: 50, 0: 50} , 'count' : 100}, 'h': {'c': {1: 30, 2: 70}, 'd':
             {1: 20, 0: 80}, 'e': {1: 50, 0: 50} , 'count' : 100}, 'x': {'c': {1: 30, 2: 70}, 'd': {1: 20, 0: 80}, 'e': {1: 50, 0: 50} , 'count' : 100}}
        # 类别 -> 属性 -> {1 : 个数 , 0 : 个数}
    __data_count = 300.

    def tarin(self, data):
        pass

    def entropy(self, prob):
        if prob and isinstance(prob, float) and prob >= 0. and prob <= 1.:
            return (-prob) * math.log(prob, 2)

    def ig(self, cname, attrname):
        if self.__data.has_key(cname):
            if self.__data[cname].has_key(attrname):
                centropy = 0.
                for __val in self.__data.keys():
                    centropy += self.entropy(self.__data[__val]['count'] / self.__data_count)
                for __val in self.__data[cname][attrname].values():
                    centropy -= self.entropy(float(__val) / self.__data[cname]['count'])
                return centropy


if __name__ == '__main__':
    x = DecisionTree()
    print math.log(1, 2)
    print x.entropy(1.)
    print x.entropy(0.5)
    print x.ig('a', 'c')
    print x.ig('a', 'd')
    print x.ig('a', 'e')
