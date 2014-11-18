# coding=utf-8


from collections import defaultdict
from copy import copy


class PageRank(object):

    def __init__(self, vectors):
        '''
        edges : 横列是 eg. 纵列 对 a入链数目
        '''
        self.edges = [[0 for _ in range(vectors)] for _ in range(vectors)]
        self.weights = [1. for _ in range(vectors)]
        self.__iter = range(vectors)

    def add_edage(self, a, in_b, ins):
        '''
        参数:
             a  为图上一个点 ， 数组计数从0开始
             in_b 为图上例外的点 ， 数组计数从0开始
             ins a点对in_b点的入链数目
        '''
        if a and in_b and weight:
            if a != in_b:
                self.edges[a][in_b] = ins
            else:
                raise ValueError, 'a coudln\'t  point to self ! '

        raise TypeError, 'a and in_b \'s type is int and weight\'s type is float !'

    def calc(self, iters, d=0.85, maxerr=0.00001):
        for _ in range(iters):
            tmp_weights = copy(self.weights)
            cur_max_diff = 0.
            for i in self.__iter:
                for j in self.__iter:
                    #如果边 j 对 i 没有入链 或者两个点相同 ， 则不处理
                    if self.edges[i][j] == 0 or i == j :
                        continue
                    weight = 0. 
                    for in_j in self.__iter:
                        weight[in_j][i]



                self.weights[i] = (1 - d) *


if __name__ == '__main__':
    p = PageRank(5)
