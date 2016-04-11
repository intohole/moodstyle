# coding=utf-8


from Kmeans import Kmeans
from Kmeans import Center
from DDistance import DefaultDistance
from random import randint
import random
from collections import Counter
from collections import defaultdict
from math import sqrt
from Kmeans import DKmeans
from copy import copy
import sys


class MiniBatchKmeans(Kmeans):

    def cluster(self, datas, k, iter_count=10000, diff=0.00001):
        """
            k center count 
        """
        if k > len(datas):
            return datas
        centers = self.rand_seed(datas, k)
        center_range = range(k)
        data_range = range(len(datas))
        sample_rate = 0.3
        sample_data_count = int(len(datas) * sample_rate)
        sample_data_range = range(sample_data_count)
        for _ in range(iter_count):
            sample_data = random.sample(datas, sample_data_count)
            distance_vector = [-1] * sample_data_count
            center_counts = [0] * k
            for i in sample_data_range:
                mini_distance, bestlabel = min(
                    [
                        (
                            self.distance(
                                datas[i],
                                centers[j]
                            ), j
                        )
                        for j in center_range
                    ]
                )
                distance_vector[i] = bestlabel
            for i in sample_data_range:
                data_label = distance_vector[i]
                center_counts[data_label] += 1
                eta = 1.0 / center_counts[data_label]
                centers[data_label] = self.add(
                    centers[data_label],
                    sample_data[i],
                    eta,
                    len(sample_data[i])
                )
        return centers

    def rand_seed(self, datas, k):
        return [copy(data) for data in random.sample(datas, k)]

    def add(self, center, data, eta, data_len):
        _center = [i * (1.0 - eta) for i in center]
        _data = [eta * i for i in data]
        return [_center[i] + _data[i] for i in range(data_len)]


class DMiniBatchKmeans(MiniBatchKmeans, DefaultDistance):
    pass


if __name__ == '__main__':
    k = DMiniBatchKmeans()
    datas = [[randint(1, 20), randint(1, 20), randint(
        1, 20), randint(1, 20), randint(1, 20)] for _ in range(100)]
    labels = k.cluster(datas, 5, 200, diff=0.00001)
    print labels
