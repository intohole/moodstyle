#coding=utf-8

from moodstyle.classifier.Knn import KdTree

kd = KdTree()
datas = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
print kd.get_split_index(datas, 3, 2, 1)
