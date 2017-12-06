#coding=utf-8

from random import randint
from ..common.BaseStrut import WeightArray
from b2 import exceptions2
import DDistance


class ClusterItem(object):


    def __init__(self , data):
        self.data = data 
        self.neighbours = []
        self.visited = False
        self.cluster = 0 


class DbScan(object):

    def __init__(self,radius,minPoint,distance = DDistance.DefaultDistance()):
        exceptions2.judge_type(distance,DDistance.DDdistance)
        exceptions2.judge_null(radius)
        exceptions2.judge_null(minPoint)
        self.distance = distance
        self.radius = radius
        self.minPoint = minPoint

    def cluster(self, datas):
        '''
        算法：DBSCAN
        参数：
            radius 半径
            minPoint 给定点在radius领域内成为核心对象的最小领域点数
        输出：目标类簇集合
        方法：
        repeat
            1)       判断输入点是否为核心对象
            2)       找出核心对象的E领域中的所有直接密度可达点
        util 所有输入点都判断完毕
        
        repeat
            针对所有核心对象的E领域所有直接密度可达点找到最大密度相连对象集合，
            中间涉及到一些密度可达对象的合并。
        Util 所有核心对象的E领域都遍历完毕
        '''
        cluters = []
        weight_map = WeightArray(datas , self.distance.distance)
        items = [ ClusterItem(data) for data in datas ] 
        k = 1 
        for i in range(len(items)):
            if items[i].visited == False:
                neighbours = [ items[j]  for j in range(len(items)) if i != j and  weight_map[(i,j)] < self.radius ]
                if len(neighbours) >= self.minPoint:
                    items[i].visited = True
                    items[i].cluster = k
                    for neighbour in neighbours:
                        if neighbour.visited == False or neighbour.cluster == -1:
                            neighbour.cluster = k 
                            neighbour.visited = True
                            items[i].data.append(neighbour)

                        elif neighbour.visited == True and neighbour.cluster != -1:
                            neighbour.cluster = k
                            for item in neighbour.data:
                                item.cluster = k
                            items[i].data.extend(neighbour.data)
                            del neighbour.data[:]
                    k += 1 
                else:
                    items[i].visited = True
                    items[i].cluster = -1
