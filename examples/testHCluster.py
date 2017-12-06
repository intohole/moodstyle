#coding=utf-8


from moodstyle import HCluster
from random import randint




hc = HCluster.ALHierarchicalClustering()
datas = [[i, randint(1, 20), randint(1, 20)] for i in range(10)]
clusters = hc.cluster(datas, 4,  100)
for cluster in clusters:
    print cluster
