#coding=utf-8


class ClusterItem(object):


    def __init__(self , data):
        self.data = data 
        self.neighbours = []



class DbScan(object):


    def cluster(self , datas , radius , minPoint):
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

        for data in dats:
            clutser = ClusterItem(data)
            #计算每个数据点的邻居
            neighbours = [ neighbour for neighbour in datas if self.distance(data , neighbour) < radius]
            if len(neighbours) > minPoint :
                clutser.neighbours.extend(neighbours)
        for clutser in cluters:



            



