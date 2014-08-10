# coding=utf-8
#!/usr/bin/env python

from random import randint
from math import sqrt
import re

'''
处理数据的格式 [数据1,数据2]
但是必须要改写 def distance(data1,data2) 数据距离函数
数据转换格式 {分类:{数据的位置:数据距离}}
'''


class KMeans(object):

    def rand_seed(self, k, data):
        k_seed = {}
        for _ in range(k):
            _find = False
            while not _find:
                r = randint(0, len(data) - 1)
                if not k_seed.has_key(r):
                    k_seed[r] = {}
                    k_seed[r][r] = 0.
                    _find = True
        return k_seed

    def distance(self, data1, data2):
#         return abs(data1-data2)
        return sqrt((data1[0] - data2[0]) * (data1[0] - data2[0]) + (data1[1] - data2[1]) * (data1[1] - data2[1]))

    # 聚类
    # 循环每个元素找到距离最近的元素
    # 将元素添加到分类中
    def cluster(self, central, data):
        for i in range(len(data)):
            if i not in central.keys():  # 分组中心肯定不能分到其它类别 所以跳过
                _min_value = None  # 最小值
                _index = None  # 最小值的数据位置
                for _key in central.keys():  # 循环每个分类中心
                    _dis = self.distance(data[_key], data[i])  # 计算距离
                    # 如果第一次 或者 距离小于最小值 ,记录
                    if not _min_value or _dis < _min_value:
                        _index = _key
                        _min_value = _dis
                central[_index][i] = _min_value  # 保存最小距离 , 方便 find_central计算
        return central  # 返回新聚类中心

    # 找到每个分类中中心 -> min(abs(每个距离值 - 中心值))
    # 步骤:
    #   计算分类中的距离 {分类中心的序号:{数据序号:距分类中心距离}}
    #   找到每个分类元素 离中心最近的元素
    #   返回分类中心 {}
    def find_central(self, cluster_result):
        _seed = {}
        for _key, _val in cluster_result.items():
            _central = 0.
            # 计算分类中所有距离平均数
            for _v in _val.values():
                _central = _central + _v
            _central = _central / len(_val.values())
            # 找到平均值，将平均值作为新的中心
            _min = None
            _mindex = _key
            for _index, _v in _val.items():
                if not _min or abs(_v - _central) < _min:
                    _min = abs(_v - _central)
                    _mindex = _index
            _seed[_mindex] = {}
            _seed[_mindex][_mindex] = 0.
        return _seed

    # 对数据进行排序，比较
    #
    def have_chage(self, oldcluster, clusterresult):
        if len(oldcluster.keys()) == 0:  # 第一次时,则返回
            return True
        old_list = [_val.keys() for _val in oldcluster.values()]  # 将数据位置提出
        cluster_list = [_val.keys() for _val in clusterresult.values()]
        old_list.sort()  # 排序
        cluster_list.sort()
        if len(old_list) != len(cluster_list):  # 如果长度不同肯定是不同的
            return True
        for i in range(len(old_list)):
            if not (old_list[i] == cluster_list[i]):  # 如果结果不同
                return True  # 则是有改变的
        return False

    def k_means(self, k, data, times=100000):
        if k >= len(data):
            raise Exception("K is bigger than data")
        _randseed = self.rand_seed(k, data)
        isOver = False
        _oldcluster = {}
        time_count = 0  # 迭代次数 ,
        while not isOver:
            _cluster = self.cluster(_randseed, data)  # 把每个元素 分到最近的分类中
            # 是否没有改变 , 或者超过迭代次数 聚类终止条件
            if not self.have_chage(_oldcluster, _cluster) or time_count > times:
                result = {}
                count = 1
                for _, _val in _cluster.items():
                    result[count] = []
                    for _key in _val.keys():
                        result[count].append(data[_key])
                    result[count].sort()  # 分类中心排序
                    count = count + 1  # 分类元素
                return result
            _oldcluster.clear()  # 清空数据
            for _key, _val in _cluster.items():
                _oldcluster[_key] = _val
            _randseed = self.find_central(_oldcluster)  # 找到分类中心 算数中心
            time_count = time_count + 1  # 迭代次数+1


class ClusterItem:

    '''
    这个记录每个数据分别属于的类别和数据
    data　元素值
    '''

    def __init__(self, item, lable=None):
        if not item or not isinstance(item , list):
            raise TypeError , 'item type is list'
        self.item = item
        self.lable = lable

    def __str__(self):
        return '%s : %s' % (self.lable, str(self.item))

from collections import defaultdict
import copy

class NewKmeans(object):

    def cluster(self, items, k, iter_count):
        '''
        ｋmeans聚类
        '''
        if len(items) > 0:
            if isinstance(items, list):
                # items = [ClusterItem(data) for data in datas]  # 生成可以通用的聚类数据
                centres = self.random_seed(items, k)  # 随机生成中心点
                __iter = 0  # 迭代轮数
                item_len = len(items[0].item)
                while __iter < iter_count:
                    for i in range(len(items)):  # 循环每个元素
                        __min = None
                        __lable = -1
                        # 循环每个中心　，　迭代查找最近的一个中心
                        for centre in centres:
                            __distance = self.distance(
                                items[i], centre, item_len)
                            if not __min or __min < __distance:
                                __min = __distance
                                __lable = centre.lable
                        items[i].lable = __lable
                    centres = self.find_centre(items, centres, item_len)
                    __iter += 1
                return items , centres

    def find_centre(self, items, centres, feature_len):

        '''
        items  ClusterItem ，　聚类元素
        centres 聚类中心
        feature_len 聚类元素中每个元素的向量长度　即　len(ClusterItem.item)
        找到kmeans再次聚类中心点　，　是一个虚拟的中心点
        现在的算法是计算每个数据的平均数
        '''
        lable_count = defaultdict(int)
        for i in range(len(centres)): #清空聚类中心
            for j in range(feature_len):
                centres[i].item[j] = 0
        for i in range(len(items)):
            for j in range(feature_len):
                centres[items[i].lable].item[j] += items[i].item[j]
            lable_count[items[i].lable] += 1
        for i in range(len(centres)):
            for j in range(feature_len):
                centres[i].item[j] /= lable_count[i]
        return centres

    def distance(self, item1, item2, item_len):
        return sqrt(sum([(item1.item[i] - item2.item[i]) * (item1.item[i] - item2.item[i]) for i in range(item_len)]))

    def random_seed(self, items, k):
        seeds = []
        __have = 0
        while __have < k:
            __index = randint(0, len(items) - 1)
            if not items[__index].lable:
                seeds.append(ClusterItem( copy.copy(items[__index].item ), __have))
                __have += 1
        return seeds




if __name__ == "__main__":
    k = NewKmeans()
    items = [ClusterItem([randint(0, 10) * 1.0 , randint(0, 10) * 1.0])
             for _ in range(10)]
    cluster_item , centres = k.cluster(items, 2, 3)
    for centre in centres:
        print centre
    for item in cluster_item:
        print item
