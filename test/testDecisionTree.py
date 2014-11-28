# coding=utf-8


from collections import defaultdict
from math import log


class DecisionTree(object):

    def train(self, datas):
        labels = [data[-1] for data in datas]
        if len(set(labels)) <= 1:
            return {'all': labels[1]}
        return self.__getBestFeature(datas)

    @staticmethod
    def entropy(probs):
        return sum([-prob * log(prob, 2) for prob in probs])

    def __getBestFeature(self, datas):
        label_dict = defaultdict(float)
        for data in datas:
            label_dict[data[-1]] += 1
        data_num = sum(label_dict.values())
        label_entropy = DecisionTree.entropy( [ cc / data_num for cc in label_dict.values() ])
        attrs = [0. for _ in range(len(datas[0][:-1]))]
        



if __name__ == '__main__':
    # 测试数据
    # 是否必须水里 是否有脚蹼 属于鱼类
    data = [[1, 1, 1], [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 1, 0]]
    d = DecisionTree()
    d.train(data)
    print DecisionTree.entropy([0.333, 0.21])
