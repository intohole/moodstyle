# coding=utf-8


import math


class DataDistance(object):

    def __init__(self, datas, distance_fun):
        self.lable_dict = {datas[index][0]:index   for index in range(len(datas))}
        self.distance_map = self.create_distance_map(datas, distance_fun)
        self.data_len = len(datas)




    def __getitem__(self, label_tuple):
        label1, label2 = label_tuple
        if self.lable_dict.has_key(label1) and self.lable_dict.has_key(label2):
            index1 = self.lable_dict[label1]
            index2 = self.lable_dict[label2]
            return self.get_distance_by_index(index1 , index2)
        raise IndexError, 'index : %s , index2 : %s  not in this distance_map'



    def get_distance_by_index(self  , row , line ):
        '''
        function:
            下半角矩阵 ， 转换坐标

        '''
        if line > (row+ 1) / 2 :
            tmp = row 
            row = line 
            line = tmp  
        try:
            d = self.distance_map[row][line]
        except:
            print row , line 
        return self.distance_map[row][line]



    def create_distance_map(self, datas, distance_fun):
        '''
        function:
            创建数据距离map
        params:
            datas 数据，格式 [[label1 , x1 ,x2...,xN ] , [lable2 , x1 , x2 , ..., xN]....[labelN , x1, x2 , ...xN] ]
        return 
            datas_map 
        '''
        distance_map = []
        for i in range(len(datas)):
            tmp_distance = []
            for j in range(i + 1 ):
                if i == j:
                    tmp_distance.append(0)
                else:
                    tmp_distance.append(distance_fun(datas[i], datas[j]))
            print tmp_distance
            distance_map.append(tmp_distance)
        return distance_map

class HTree(object):


    def __init__(self , left_data , right_data , datas):
        self.left_data = left_data
        self.right_data = right_data 
        self.datas = datas

    


class HierarchicalClustering(object):

    def __init__(self):
        pass

    def cluster(self, datas, cluster_num,  threshold=0.03):
        '''

        '''

        no_change = False

        # 创建数据距离词典
        distance_map = DataDistance(datas, self.distance)
        # 创建一个cluster，每个数据都是一个cluster
        clusters = [[datas[i]] for i in range(len(datas))]

        # 如果聚类不小于要求聚类数目继续
        while len(clusters) > cluster_num:
            min_distance = None
            min_cluster_pair = None
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

    def get_cluster_distance(self, cluster1, cluster2, distance_map):
        return sum([sum(distance_map[(data1[0], data2[0])]for data2 in cluster2) for data1 in cluster1]) / float(len(cluster1) * len(cluster2))


class SLHierarchicalClustering(HierarchicalClustering):

    def get_cluster_distance(self, cluster1, cluster2, distance_map):

        return min([min(distance_map[(data1[0], data2[0])] for data2 in cluster2) for data1 in cluster1]) / float(len(cluster1) * len(cluster2))


class CLHierarchicalClustering(HierarchicalClustering):

    def get_cluster_distance(self, cluster1, cluster2, distance_map):

        return max([max(distance_map[(data1[0], data2[0])] for data2 in cluster2) for data1 in cluster1]) / float(len(cluster1) * len(cluster2))


if __name__ == '__main__':

    hc = ALHierarchicalClustering()
    from random import randint
    datas = [[i, randint(1, 20), randint(1, 20)] for i in range(5)]
    clusters = hc.cluster(datas, 3,  100)
    for cluster in clusters:
        print cluster
