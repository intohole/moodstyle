# coding=utf-8


import math
from testBaseStrut import WeightArray



class HierarchicalClustering(object):

    def __init__(self):
        pass

    def cluster(self, datas, cluster_num,  threshold=0.03):
        '''

        '''

        no_change = False

        # 创建数据距离词典
        distance_map = WeightArray(datas, self.distance)
        # 创建一个cluster，每个数据都是一个cluster
        clusters = [[datas[i]] for i in range(len(datas))]

        # 如果聚类不小于要求聚类数目继续
        while len(clusters) > cluster_num:
            min_distance = None #最短距离保存值
            min_cluster_pair = None #最短距离所对应的数据
            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    d = self.get_cluster_distance(
                        clusters[i], clusters[j], distance_map)
                    if d < threshold and (min_distance is None or d < min_distance):
                        min_distance = d
                        min_cluster_pair = (i, j)
            if min_cluster_pair:
                clusters[min_cluster_pair[0]].extend(
                    clusters[min_cluster_pair[1]])
                del clusters[min_cluster_pair[1]]
            else:
                break
        return clusters

    def distance(self, data1, data2):
        '''
        function:
            计算两个数据的距离
        params:
            data1 第一个数据
            data2 第二个数据
        return 
            distance 两个数据的距离
        '''

        return math.sqrt(sum([(data1[i] - data2[i]) ** 2 for i in range(1, len(data1))]))

    def get_cluster_distance(self, cluster1, cluster2, distance_map):
        '''
        function
            实现类之间平均距离
        params:
            cluster1 簇1 
            cluster2 簇2
            distance_map DataDistance实例
        return 
            两个类之间平均距离
        '''
        raise NotImplementedError


class ALHierarchicalClustering(HierarchicalClustering):
    '''
    主要算法：
        计算cluster之间平均距离
    '''
    def get_cluster_distance(self, cluster1, cluster2, distance_map):
        return sum([sum(distance_map[(data1[0], data2[0])]for data2 in cluster2) for data1 in cluster1]) / float(len(cluster1) * len(cluster2))


class SLHierarchicalClustering(HierarchicalClustering):
    '''
    主要算法：
        两个cluster中最小的两个数据之间距离
    '''

    def get_cluster_distance(self, cluster1, cluster2, distance_map):

        return min([min(distance_map[(data1[0], data2[0])] for data2 in cluster2) for data1 in cluster1]) / float(len(cluster1) * len(cluster2))


class CLHierarchicalClustering(HierarchicalClustering):
    '''
    主要算法：
        两个cluster中距离最大两个数据距离
    '''

    def get_cluster_distance(self, cluster1, cluster2, distance_map):

        return max([max(distance_map[(data1[0], data2[0])] for data2 in cluster2) for data1 in cluster1]) / float(len(cluster1) * len(cluster2))


if __name__ == '__main__':

    hc = ALHierarchicalClustering()
    from random import randint
    datas = [[i, randint(1, 20), randint(1, 20)] for i in range(10)]
    clusters = hc.cluster(datas, 4,  100)
    for cluster in clusters:
        print cluster
