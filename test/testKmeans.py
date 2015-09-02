# coding=utf-8
#!/usr/bin/env python

from random import randint
from random import sample
from collections import Counter
from collections import defaultdict
from math import sqrt
import re
from testDDistance import Manhattan
from testDDistance import Hamming
from testDDistance import Cosine
from testDDistance import Euclidean
from copy import copy
import sys

'''
处理数据的格式 [数据1,数据2]
但是必须要改写 def distance(data1,data2) 数据距离函数
数据转换格式 {分类:{数据的位置:数据距离}}
'''


class Kmeans(object):

    def cluster(self, datas, k, iter_count=10000, diff=0.00001):
        '''
        函数功能：
               对数据进行聚类 ， 通过kmeans 算法


        过程：
             随机从数据选出centers （一个随机过程）
             开始迭代
                 循环每个数据：
                     计算数据与每个中心距离 ， 找到一个最小值
                     如果 数据原有label 和现有label 不同：
                          diff_labels += 1
                 计算数据label变化比率 ， 如果超出diff设置值 ， 继续下轮迭代
                 否则 ， 跳出循环
            返回数据labels
        '''

        centers = self.rand_seed(datas, k)
        center_range = range(len(centers))
        data_range = range(len(datas))
        labels = [-1 for i in data_range]
        for _ in range(iter_count):
            diff_labels = 0
            for i in data_range:
                bestlabel = min(
                    [(self.distance(datas[i], centers[j][0]), centers[j][1])
                     for j in center_range])
                if labels[i] != bestlabel[1]:
                    diff_labels += 1
                    labels[i] = bestlabel[1]
            if float(diff_labels) / len(datas) < diff:
                break
            centers = self.update_centers(datas, labels, centers)
            print _, 'iter'
        return labels, centers

    def rand_seed(self, datas, k):
        rand_seeds = sample(datas, k)
        rand_seeds = [(copy(rand_seeds[i]), i) for i in range(len(rand_seeds))]
        return rand_seeds

    def update_centers(self, datas, labels, centers):
        centers_dict = {
            center[1]: [0 for i in range(len(center[0]))] for center in centers}
        label_dict = Counter(labels)
        for i in range(len(datas)):
            for j in range(len(datas[i])):
                centers_dict[labels[i]][j] += datas[i][j]
        for label in label_dict.keys():
            for i in range(len(centers_dict[label])):
                centers_dict[label][i] /= label_dict[label]
        return sorted([(center, label) for label, center in centers_dict.items()], key=lambda x: x[1], reverse=False)


class DKmeans(Kmeans):

    def distance(self, data1, data2):
        return sqrt(
            sum([
                (data1[i] - data2[i]) ** 2
                for i in range(len(data1))
            ])
        )


class ManhattanKmeans(Kmeans, Manhattan):

    pass


class HammingKmeans(Kmeans, Hamming):

    pass


class CosineKmeans(Kmeans, Cosine):
    pass


class EuclideanKmeans(Kmeans, Euclidean):
    pass


if __name__ == '__main__':
    k = HammingKmeans()
    datas = [[randint(1, 20), randint(1, 20), randint(
        1, 20), randint(1, 20),randint(1, 20)] for _ in range(100)]
    labels = k.cluster(datas, 5, 200, diff=0.00001)
    print labels
