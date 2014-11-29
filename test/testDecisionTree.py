# coding=utf-8


from collections import defaultdict
from math import log


class DecisionTree(object):

    def train(self, datas, denseData=False):
        labels = [data[-1] for data in datas]
        if len(set(labels)) <= 1:
            return {'all': labels[1]}
        # return self.__getBestFeature(datas , denseData)

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

        gains = [( label_entropy -
                 sum([attr_value_count[attr][value] / data_num *
                      DecisionTree.entropy([attr_value_class_count[attr][value][label] / attr_value_count[attr][value] 
                        for label in attr_value_class_count[attr][value].keys() ]) 
                      for value in attr_value_count[attr].values()]) 
                 ,attr) for attr in attrs ]
        return gains

if __name__ == '__main__':
    # 测试数据
    # 是否必须水里 是否有脚蹼 属于鱼类
    data = [[1, 1, 1], [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 1, 0]]
    d = DecisionTree()
    d.train(data)
    print DecisionTree.entropy([0.333, 0.21])
    test = [1, 2, 3]
    print d.getBestFeature(data, [1, 2] , True)
