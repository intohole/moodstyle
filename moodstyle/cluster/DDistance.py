# coding=utf-8

import math


class DDdistance(object):

    def distance(self, data1, data2):
        raise NotImplementedError


class Manhattan(DDdistance):

    """
        算法实现曼哈顿距离
    """

    def distance(self, data1, data2):
        if len(data1) != len(data2):
            raise ValueError
        return sum([abs(data1[i] - data2[i]) for i in range(len(data1))])


class DefaultDistance(DDdistance):

    def distance(self, data1, data2):
        return math.sqrt(
            sum([
                (data1[i] - data2[i]) ** 2
                for i in range(len(data1))
            ])
        )


class Chebyshev(DDdistance):

    """
        切比雪夫距离
    """

    def distance(self, data1, data2):
        if len(data1) != len(data2):
            raise ValueError
        return max([abs(data1[i] - data2[i]) for i in range(len(data1))])


class Cosine(DDdistance):

    """
        余弦距离
    """

    def distance(self, data1, data2):
        if len(data1) != len(data2):
            raise ValueError

        return sum([data1[i] * data2[i] for i in range(len(data1))]) / (
            math.sqrt(sum([data ** 2 for data in data1])) +
            math.sqrt(sum([data ** 2 for data in data2]))
        )


class Hamming(DDdistance):

    """
        海明距离
    """

    def distance(self, data1, data2):
        return sum([1 if data1[i] == data2[i] else 0 for i in range(len(data1))]) / float(len(data1))


class Euclidean(DDdistance):

    """
        欧式距离
    """

    def distance(self, data1, data2):
        return math.sqrt(sum([(data1 - data2) ** 2 for i in range(len(data1))]))
