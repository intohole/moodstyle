#coding=utf-8



from moodstyle.cluster.DbScan import DbScan
from random import randint


t = DbScan(0.5,10)


datas = [[ _ , randint(0, 20) * 1.0, randint(0, 20) * 1.0] for _ in range(100)]
t.cluster(datas)
print datas


