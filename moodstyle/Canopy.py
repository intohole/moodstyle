# coding=utf-8
#!/usr/bin/env python

from random import randint
from random import sample
from b2 import exceptions2
import DDistance


class Canopy(object):

    def __init__(self, centre):
        self.centre = centre  # 中心点
        self.datas = []  # 涵盖的数据 , 如果在class下直接声明　，　会造成多个类公用一个list

    def __str__(self):
        return '%s : [ %s ]' % (
            str(self.centre), ','.join([str(data) for data in self.datas]))


class CanopyCluster(object):
    """canopy 是一个粗聚类算法
    主要是两个值确定：
    t1 外围圈子
    t2 内部圈子
    过程　：
    　　　判断数据ｌｉｓｔ是否为空
    　　　　　随机一个数据元素作为中心　，　建立canopy
             删除这个元素
            循环每个数据每个元素　，　计算它与ｃａｎｏｐｙ中心的距离
            　　如果　距离小于　< t1
               　　canopy 加入此数据
            　　如果　距离小于　< t2
               　　在数据中删除这个元素　
        　　将canopy 加入到聚类中心处
    思想：
    　　减少计算　，　通过两个半径有效的去除元素
    　　可以为kmeans方法　，　提供ｋ值参考
    """
    def __init__(self, t1, t2, calc_distance = DDistance.DefaultDistance()):
        exceptions2.judge_null(calc_distance) 
        exceptions2.judge_type(calc_distance,DDistance.DDdistance)
        exceptions2.judge_type(t1,(int,float))
        exceptions2.judge_type(t2,(int,float))
        exceptions2.judge_smaller(t2,t1)
        self.t1 = t1
        self.t2 = t2
        self._calc_distance = calc_distance

    def cluster(self, datas):
        canopys = []
        while len(datas) > 0:
            rand_center = randint(0, len(datas) - 1)
            canopy = Canopy(datas[rand_center])
            del datas[rand_center] 
            index = 0
            # 这里有个操作　，　因为for i in range(9) 这样是在一个ｌｉｓｔ，删除元素无用
            while index < len(datas):
                distance = self._calc_distance.distance(canopy.centre, datas[index])
                if distance < self.t1:
                    canopy.datas.append(datas[index])
                if distance < self.t2:
                    del datas[index]
                    index = index - 1
                index = index + 1
            canopys.append(canopy)
        return canopys
