# coding=utf-8


from collections import defaultdict
from collections import Counter
from math import log
import json


# class Node(object):

#     def __init__(self, attr_name=None, label=None):
#         self.attr_name = attr_name
#         self.label = label
#         self.child = {}

#     def __str__(self):
#         child = '\t'.join(['%s %s' % (val , str(node)) for val , node in self.child.items()])
# return 'attr: %s \t label : %s \t childs : [ %s ] ' % (self.attr_name,
# self.label, self.child)

class Node(dict):
    pass


class DecisionTree(object):

    def __init__(self):
        self.tree = None
        self.attrs = None

    def load_model(self, file_path):
        '''
        加载模型  
        file_path : 模型加载地址 
        功能 ： 不管是否成功都会覆盖model 
        '''
        with open(file_path) as f:
            self.tree = json.loads(f.readline().strip())

    def save(self, model_path):
        if not self.tree:
            raise ValueError, 'no model can save!'
        with open(file_path, 'w') as f:
            f.write(json.dumps(self.tree))

    def __train(self, datas, attrs, threshold=0.01, dense_data=True):
        if self.attrs == None:
            self.attrs = attrs
        label_dict = Counter([data[-1] for data in datas])
        if len(label_dict.keys()) == 1:
            return datas[0][-1]
        if len(attrs) == 0:
            return label_dict.most_common()[0][0]
        attr, attr_gain, attr_val = self.get_best_feature(
            datas, attrs, dense_data)[0]  # 得到最好信息增益的属性
        if attr_gain < threshold:
            return label_dict.most_common()[0][0]
        node = Node()
        node[attr] = {}
        sublables = self.getSplitAttrs(  # 为下轮切割属性
            attrs, attr
        )
        for val in attr_val:
            # 按照属性不同value 区分这个
            # 取得最好分类属性 ， 按照不同该属性不同val 区分数据 ；
            node[attr][val] = self.__train(
                self.splitDataByAttr(
                    datas, attrs, attr, val
                ),
                sublables,
                threshold,
                dense_data)
        return node

    def train(self, datas, attrs, threshold=0.01, dense_data=True):
        self.tree = self.__train(datas, attrs, threshold, dense_data)

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

    def get_best_feature(self, datas, attrs, dense_data):
        raise NotImplementedError, '【获得最好属性方法没有实现】'

    def splitDataByAttr(self, datas, attrs, attr_name, attr_value, dense_data=True):
        '''
        切割训练集为了下一步
        datas :训练的数据 [[data]]
        attrs 属性名称列表
        attr_val 属性值
        dense_data 是否是密集型数据 , 暂时废弃
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
        思想 ： 每层树的节点 {节点1：{val1 ：节点2：{val3 ：{。。。。{valn ： label }}}
        第一层是key 下一层是val 第三层是key 第四层是val 。。。。 直到出现val
        '''
        if self.tree == None:
            raise Exception, 'no model !'
        node = self.tree
        if not isinstance(node, dict):
            return node
        for _ in range(len(data)):
            val = data[self.attrs.index(node.keys()[0])]  # 得到第n%2层val
            node = node[node.keys()[0]][val]
            if not isinstance(node, dict):
                return node
        raise 'DecisionTree is wrong !', self.tree


class ID3(DecisionTree):

    def get_best_feature(self, datas, attrs, dense_data):
        '''
        通过算法获得最好分类的属性 ；
        思想：
            1.  信息增益 
            2.  信息增益率
        参数：
            datas 训练的数据
            attrs 属性列表
            dense_data 是否为密集型数据 ， == True [[v1 , v2 ,v3 ,v4 .... vn , label]]
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
            if dense_data:
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
        # gains = [(属性名称 ， 信息增益 ， (属性值))......(属性名称n , 信息增益n ， (f1 ...fn))]
        # 以上运算是这样的；
        #   当查看每个属性 ， 在各个值中是否很大概率偏向一方 ， 这样造成整体信息增益最大 ， 因为整体的信息增益肯定为正的 ，
        #   减去一个越小的数 ， 数值反而越大 ， 就是说明属性是比较稳定的（比较有分类信息的）
        gains = [(attr,
                  label_entropy -
                  sum(
                      [
                          attr_value_count[attr][value] / data_num *
                          DecisionTree.entropy(
                              [
                                  # 计算每个属性在特定属性值时 ， 发生的概率
                                  # p(DA1)/A
                                  attr_value_class_count[attr][value][
                                      label] / attr_value_count[attr][value]
                                  # 循环每个属性值在特定label产生
                                  for label in attr_value_class_count[attr][value].keys()
                              ]
                          )
                          for value in attr_value_count[attr].values() if attr_value_class_count[attr].has_key(value)]
                  ),
                  attr_value_count[attr].keys())
                 for attr in attr_value_count.keys()]
        return sorted(gains, key=lambda x: x[1], reverse=True)


class C45(ID3):

    def get_best_feature(self, datas, attrs, dense_data):

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
            if dense_data:
                for i in iter_index:
                    # 计算每个属性下不同值数量 ， 此处必要转换为离散变量
                    attr_value_count[attrs[i]][data[i]] += 1
                    if not attr_value_class_count[attrs[i]][data[i]].has_key(data[-1]):
                        attr_value_class_count[attrs[i]][data[i]][
                            data[-1]] = 0.
                    attr_value_class_count[attrs[i]][data[i]][data[-1]] += 1.0
        attr_count = {attr : sum(attr_value_count[attr].values())  for attr in attrs}

        h_v = { attr : 
        sum(DecisionTree.entropy( val / attr_count[attr]) for val in value_count_dict.values() ) 
        for attr,value_count_dict in attr_value_count.items()} # 算出信息增益比 ， 分子， 每个属性的值熵
        
        # 信息增益计算公式分析
        #     H(D) - H(D|A)
        #     系统熵 - 每个属性下 ， 存在这个类别的信息熵
        #
        # gains = [(属性名称 ， 信息增益 ， (属性值))......(属性名称n , 信息增益n ， (f1 ...fn))]
        # 以上运算是这样的；
        #   当查看每个属性 ， 在各个值中是否很大概率偏向一方 ， 这样造成整体信息增益最大 ， 因为整体的信息增益肯定为正的 ，
        #   减去一个越小的数 ， 数值反而越大 ， 就是说明属性是比较稳定的（比较有分类信息的）
        gains = [(attr,
                  
                ( 
                label_entropy -
                  sum(
                      [
                          attr_value_count[attr][value] / data_num *
                          DecisionTree.entropy(
                              [
                                  # 计算每个属性在特定属性值时 ， 发生的概率
                                  # p(DA1)/A
                                  attr_value_class_count[attr][value][
                                      label] / attr_value_count[attr][value]
                                  # 循环每个属性值在特定label产生
                                  for label in attr_value_class_count[attr][value].keys()
                              ]
                          )
                          for value in attr_value_count[attr].values() if attr_value_class_count[attr].has_key(value)]
                  ) ) / h_v[attr],
                  attr_value_count[attr].keys())
                 for attr in attr_value_count.keys()]
        return sorted(gains, key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    # 测试数据
    # 是否必须水里 是否有脚蹼 属于鱼类
    data = [[1, 0, 'man'], [1, 1, 'man'], [0, 1, 'man'], [0, 0, 'woman'] , [3 , 0  , 'woman']]
    d = C45()
    d.train(data, [1, 2])
    print d.classify([0, 0])
