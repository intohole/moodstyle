# coding=utf-8

from collections import Counter


class ClassItem(object):

    pass


class KdNode(object):
    def __init__(self, split, left_child, right_child, data, parrent_node):
        self.split = split  # 切分点
        self.left = left  # 左子树
        self.right = right  # 右子树
        self.data = data  # 数据点
        self.parrent = pattern_node


class KdTree(object):
    def create_kd_tree(self, datas, k, feature_len, depth):
        if datas == None or len(datas) == 0:
            return KdNode(None, None, None, None, None)

        split_index = self.get_split_index(datas, k, feature_len, depth)
        datas = sorted(datas, key=lambda x: x[split_index], reverse=True)
        split_data_index = len(datas) / 2
        data = datas[split_data_index]

    def get_split_index(self, datas, k, feature_len, depth):
        data_sum = [0] * feature_len
        # 计算方差，找到方差最大的列，方差越大，证明点越分散，越具有可区分度

        for data in datas:
            for i in range(feature_len):
                data_sum[i] += data[i]
        data_avg = [data_sum[i] / len(datas) for i in range(feature_len)]
        data_chi = [0] * feature_len
        for data in datas:
            for i in range(len(data)):
                data_chi[i] += (data[i] - data_avg[i])**2

        return sorted(
            [(data_chi[i], i) for i in range(feature_len)],
            key=lambda x: x[0],
            reverse=True)[0][1]


class Knn(object):
    def __init__(self, train_data, labels, top_n):
        self.train_data = train_data
        self.labels = labels
        self.top_n = top_n

    def classify(self, data):
        label_orders = sorted(
            [(self.distance(data, self.train_data[i]), labels)
             for i in range(len(self.train_data))],
            key=lambda x: x[1])
        return Counter(
            label for data, label in label_orders[:self.top_n]).most_common(1)
