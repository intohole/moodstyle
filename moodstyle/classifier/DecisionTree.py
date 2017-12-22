# coding=utf-8

from collections import defaultdict
from collections import Counter
from math import log


class Node(object):
    def __init__(self, attr_name=None, label=None):
        self.attr_name = attr_name
        self.label = label
        self.child = {}

    def __str__(self):
        child = '\t'.join(
            ['%s %s' % (val, str(node)) for val, node in self.child.items()])
        return 'attr: %s \t label : %s \t childs : [ %s ] ' % (self.attr_name,
                                                               self.label,
                                                               self.child)


class DecisionTree(object):
    def __init__(self):
        self.tree = None
        self.attrs = None

    def train(self, datas, attrs, threshold=0.01, denseData=True, tree=None):
        if self.attrs == None:
            self.attrs = attrs
        node = Node()
        if self.tree == None:
            self.tree = node
        label_dict = Counter([data[-1] for data in datas])
        if len(label_dict.keys()) == 1:
            node.label = datas[0][-1]
            return node  # 如果都输于同一类 ， 则返回树
        if len(attrs) == 0:
            node.label = label_dict.most_common()[0][0]
            return node  # 如果属性为空 ， 则返回绝大数的类标记
        attr, attr_gain, attr_val = self.getBestFeature(
            datas, attrs, denseData)[0]  # 得到最好信息增益的属性
        if attr_gain < threshold:
            node.label = label_dict.most_common()[0][0]
            return node
        node.attr_name = attr
        for val in attr_val:
            #按照属性不同value 区分这个
            #取得最好分类属性 ， 按照不同该属性不同val 区分数据 ；
            node.child[val] = self.train(
                self.splitDataByAttr(datas, attrs, attr, val),
                self.getSplitAttrs(attrs, attr), threshold, denseData, node)
        return node

    @staticmethod
    def entropy(probs):
        if probs:
            if isinstance(probs, (list, tuple)):
                return sum([-prob * log(prob, 2) for prob in probs])
            elif isinstance(probs, (int, float)):
                return -probs * log(probs, 2)

    def getSplitAttrs(self, attrs, attr):
        split_attrs = []
        index = attrs.index(attr)
        split_attrs.extend(attrs[:index])
        split_attrs.extend(attrs[index + 1:])
        return split_attrs

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
        label_entropy = DecisionTree.entropy([
            label_count / data_num for label_count in label_dict.values()
        ])  # 计算整个系统的熵
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
                    if not attr_value_class_count[attrs[i]][data[i]].has_key(
                            data[-1]):
                        attr_value_class_count[attrs[i]][data[i]][data[
                            -1]] = 0.
                    attr_value_class_count[attrs[i]][data[i]][data[-1]] += 1.0
        # 信息增益计算公式分析
        #     H(D) - H(D|A)
        #     系统熵 - 每个属性下 ， 存在这个类别的信息熵
        #
        # gains = [(属性名称 ， 信息增益 ， (属性值))......(属性名称n , 信息增益n ， (f1 ...fn))]
        gains = [
            (
                attr,
                label_entropy - sum([
                    attr_value_count[attr][value] / data_num *
                    DecisionTree.entropy([
                        # 计算每个属性在特定属性值时 ， 发生的概率
                        # p(DA1)/A
                        attr_value_class_count[attr][value][label] /
                        attr_value_count[attr][value]
                        # 循环每个属性值在特定label产生
                        for label in attr_value_class_count[attr][value]
                        .keys()
                    ]) for value in attr_value_count[attr].values()
                    if attr_value_class_count[attr].has_key(value)
                ]),
                attr_value_count[attr].keys())
            for attr in attr_value_count.keys()
        ]
        return sorted(gains, key=lambda x: x[1], reverse=True)

    def splitDataByAttr(self,
                        datas,
                        attrs,
                        attr_name,
                        attr_value,
                        denseData=True):
        '''
        切割训练集为了下一步
        datas :训练的数据 [[data]]
        attrs 属性名称列表
        attr_val 属性值
        denseData 是否是密集型数据 , 暂时废弃
        '''
        dump_datas = []
        index = attrs.index(attr_name)
        for data in datas:
            dump = []
            if data[index] == attr_value:
                dump = data[:index]
                dump.extend(data[index + 1:])
                dump_datas.append(dump)
        return dump_datas

    def classify(self, data):
        '''
        功能： 用于分类模型
        参数 ：
            data 待分析的数据 ， list
        返回:
            返回决策树的label
        '''
        if self.tree == None:
            raise Exception, 'no model !'
        node = self.tree
        if node.label != None:
            return node.label
        for _ in range(len(data)):
            index = self.attrs.index(node.attr_name)
            node = self.tree.child[data[index]]
            if node.label != None:
                return node.label
        return None


if __name__ == '__main__':
    # 测试数据
    # 是否必须水里 是否有脚蹼 属于鱼类
    data = [[1, 0, 1], [0, 1, 0], [1, 1, 1]]
    d = DecisionTree()
    d.train(data, [1, 2])
    print d.classify([1, 0])
