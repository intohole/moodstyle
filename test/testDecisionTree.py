# coding=utf-8


from collections import defaultdict
from math import log


class Node(object):

    def __init__(self, attr):
        pass


class DecisionTree(object):

    def train(self, datas, attrs, denseData=False):
        labels = [data[-1] for data in datas]
        if len(set(labels)) <= 1:
            return {'all': labels[1]}
        # return self.__getBestFeature(datas , denseData)

        # for data , attrs ,

    @staticmethod
    def entropy(probs):
        return sum([-prob * log(prob, 2) for prob in probs])

    def getBestFeature(self, datas, attrs, denseData):
        '''
        通过算法获得最好分类的属性 ；
        思想：
            1.  信息增益 
            2.  信息增益率
        参数：
            datas 训练的数据
            attrs 属性列表
            deseData 是否为密集型数据 ， == True [[v1 , v2 ,v3 ,v4 .... vn , label]]
                                         == False [({f1 : v1 , f2:v2...fn:vn} , label1)]
        '''
        label_dict = defaultdict(float)
        for data in datas:
            label_dict[data[-1]] += 1
        data_num = len(datas)  # 计算此次计算信息增益的数据长度 ， 样本大小
        label_entropy = DecisionTree.entropy(
            [label_count / data_num for label_count in label_dict.values()])  # 计算整个系统的熵
        # 计算每个属性的熵
        # 声明一个属性列表 ， {属性 ： {属性值 ： 出现的次数}}
        attr_value_count = {attr: defaultdict(float) for attr in attrs}
        # 声明属性->属性值->类别->数量
        attr_value_class_count = {attr: defaultdict(dict) for attr in attrs}
        iter_index = range(len(attrs))
        for data in datas:
            if denseData:
                for i in iter_index:
                    # 计算每个属性下不同值数量 ， 此处必要转换为离散变量
                    attr_value_count[attrs[i]][data[i]] += 1
                    if not attr_value_class_count[attrs[i]][data[i]].has_key(data[-1]):
                        attr_value_class_count[attrs[i]][data[i]][
                            data[-1]] = 0.
                    attr_value_class_count[attrs[i]][data[i]][data[-1]] += 1.0
        # 信息增益计算公式分析
        #     H(D) - H(D|A)
        #     系统熵 - 每个属性下 ， 存在这个类别的信息熵
        #
        gains = [(attr,
                  label_entropy -
                  sum(
                      [
                          attr_value_count[attr][value] / data_num *
                          DecisionTree.entropy(
                              [
                                  #计算每个属性在特定属性值时 ， 发生的概率
                                  # p(DA1)/A
                                  attr_value_class_count[attr][value][
                                      label] / attr_value_count[attr][value]
                                  #循环每个属性值在特定label产生
                                  for label in attr_value_class_count[attr][value].keys()
                              ]
                          )
                          for value in attr_value_count[attr].values() if attr_value_class_count[attr].has_key(value)]
                  ),
                  attr_value_count[attr].keys() )
                 for attr in attr_value_count.keys()]
        return sorted(gains, key=lambda x: x[1], reverse=True)

    def splitDataByAttr(self, datas, attr, atrr_value, denseData=True):
        dump_datas = []
        for data in datas:
            dump = []
            if data[attr] == attr_value:
                dump = data[:attr]
                dump.extend(data[attr:])
                dump_datas.append(dump)
        return dump_datas


if __name__ == '__main__':
    # 测试数据
    # 是否必须水里 是否有脚蹼 属于鱼类
    data = [[1, 1, 1], [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 1, 0]]
    d = DecisionTree()
    # d.train(data)
    print DecisionTree.entropy([0.333, 0.21])
    test = [1, 2, 3]
    print d.getBestFeature(data, [1, 2], True)
