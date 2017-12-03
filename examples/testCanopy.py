#coding=utf-8





from random import randint
from moodstyle import Canopy


s = Canopy.CanopyCluster(120, 100)
datas = [[randint(0, 1000)] for i in range(100)]
for i in s.cluster(datas):
    print i
