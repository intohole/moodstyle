# coding=utf-8

from testKmeans import Kmeans
from testKmeans import DKmeans
from random import randint
from random import random
from copy import copy


class KmeansPlusPlus(Kmeans):

    def rand_seed(self, datas, k):
        '''
        function:
            kmeans++与kmeans最大不同点就是种子生成算法不同
        params:
            datas 聚类数据
            k   聚类数目
        '''
        seeds = [(
            copy(datas[randint(0, len(datas) - 1)]), 0
        )] #初始化种子库 ，随机一个种子
        #获取剩余种子
        for k_iter in range(k - 1):
            ds = [] #种子距离
            for data in datas:
                ds.append(
                    min(self.distance(seed[0], data)
                        for seed in seeds))
            sum_distance = sum(ds)
            rand_distance = random() * sum_distance
            for i in range(len(ds)):
                rand_distance -= ds[i]
                if rand_distance <= 0:
                    seeds.append((copy(datas[i]), k_iter + 1))
                    break
        return seeds


class DKmeansPlusPlus(KmeansPlusPlus , DKmeans):

    pass



if __name__ == '__main__':
    k = DKmeansPlusPlus()
    datas = [[randint(0, 20) * 1.0, randint(0, 20) * 1.0] for _ in range(200)]
    labels = k.cluster(datas, 5, 200 , diff = 0.00001)
    print labels

