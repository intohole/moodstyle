# coding=utf-8


from collections import defaultdict
from collections import Counter
from math import log
import json



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
        with open(model_path, 'w') as f:
            f.write(json.dumps(self.tree))

    def __train(self, datas , labels , attrs, threshold=0.01, dense_data=True):
        
        label_dict = Counter(labels)
        if len(label_dict.keys()) == 1:
            return label_dict.keys()[0]
        
        if len(attrs) == 0:
            return label_dict.most_common()[0][0]
        
        attr, attr_gain, attr_val = self.get_best_feature(
            datas , labels , attrs, dense_data)[0]  # 得到最好信息增益的属性
        
        if attr_gain < threshold:
            return label_dict.most_common()[0][0]
        
        node = Node()
        node[attr] = {}
        child_attr = self.get_split_attr(# 为下轮切割属性
            attrs, attr
        )
        
        for val in attr_val:
            # 按照属性不同value 区分这个
            # 取得最好分类属性 ， 按照不同该属性不同val 区分数据 ；
            child_datas , child_labels = self.split_data_by_attr(
                    datas , labels , attrs, attr, val
                )
            node[attr][val] = self.__train(
                child_datas,
                child_labels,
                child_attr,
                threshold,
                dense_data)
        return node

    def train(self, datas , labels , attrs, threshold=0.01, dense_data=True):
        self.attrs = attrs
        self.tree = self.__train(datas , labels , attrs, threshold, dense_data)

    @staticmethod
    def entropy(probs):
        if probs:
            if isinstance(probs, (list, tuple)):
                return sum([-prob * log(prob, 2) for prob in probs])
            elif isinstance(probs, (int, float)):
                return -probs * log(probs, 2)

    def get_split_attr(self, attrs, attr):
        split_attrs = []
        index = attrs.index(attr)
        split_attrs.extend(attrs[:index])
        split_attrs.extend(attrs[index + 1:])
        return split_attrs

    def get_best_feature(self, datas, labels, attrs, dense_data):
        raise NotImplementedError, '【获得最好属性方法没有实现】'

    def split_data_by_attr(self, datas , labels , attrs, attr_name, attr_value, dense_data=True):
        '''
        切割训练集为了下一步
        datas :训练的数据 [[data]]
        attrs 属性名称列表
        attr_val 属性值
        dense_data 是否是密集型数据 , 暂时废弃
        '''
        dump_datas = []
        dump_labels = []
        attr_index = attrs.index(attr_name)
        for i in range(len(datas)):
            dump = []
            data = datas[i]
            if data[attr_index] == attr_value:
                dump_labels.append(labels[i])
                dump = data[:attr_index]
                dump.extend(data[attr_index + 1:])
                dump_datas.append(dump)
        return dump_datas, dump_labels

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

    def get_best_feature(self, datas , labels , attrs, dense_data):
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
        label_dict = Counter(labels)
        data_num = float(len(datas))  # 计算此次计算信息增益的数据长度 ， 样本大小
        label_entropy = DecisionTree.entropy(
            [label_count / data_num for label_count in label_dict.values()])  # 计算整个系统的熵
        # 计算每个属性的熵
        # 声明一个属性列表 ， {属性 ： {属性值 ： 出现的次数}}
        attr_value_count = {attr: defaultdict(float) for attr in attrs}
        # 声明属性->属性值->类别->数量
        attr_value_class_count = {attr: defaultdict(lambda : defaultdict(float)) for attr in attrs}
        iter_index = range(len(attrs))
        for i in range(len(datas)):
            for j in iter_index:
                    # 计算每个属性下不同值数量 ， 此处必要转换为离散变量
                    data = datas[i]
                    attr_value_count[attrs[j]][data[j]] += 1
                    attr_value_class_count[attrs[j]][data[j]][labels[i]] += 1.0
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
        # return attr_name , gains , attr value 
        return sorted(gains, key=lambda x: x[1], reverse=True)


class C45(ID3):

    def get_best_feature(self, datas , labels, attrs, dense_data):

        label_dict = Counter(labels)
        data_num = float(len(datas))  # 计算此次计算信息增益的数据长度 ， 样本大小
        label_entropy = DecisionTree.entropy(
            [label_count / data_num for label_count in label_dict.values()])  # 计算整个系统的熵
        # 计算每个属性的熵
        # 声明一个属性列表 ， {属性 ： {属性值 ： 出现的次数}}
        attr_value_count = {attr: defaultdict(float) for attr in attrs}
        # 声明属性->属性值->类别->数量
        attr_value_class_count = {attr: defaultdict(lambda : defaultdict(float)) for attr in attrs}
        iter_index = range(len(attrs))
        for i in range(len(datas)):
            for j in iter_index:
                    # 计算每个属性下不同值数量 ， 此处必要转换为离散变量
                    data = datas[i]
                    attr_value_count[attrs[j]][data[j]] += 1
                    attr_value_class_count[attrs[j]][data[j]][labels[i]] += 1.0
                    
        attr_count = {attr : sum(attr_value_count[attr].values())  for attr in attrs}

        h_v = { attr : 
                sum(
                    DecisionTree.entropy(val / attr_count[attr]) 
                    for val in value_count_dict.values()
                   ) 
               for attr, value_count_dict in attr_value_count.items()}  # 算出信息增益比 ， 分子， 每个属性的值熵
        
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
                  )) / h_v[attr],
                  attr_value_count[attr].keys())
                 for attr in attr_value_count.keys()]
        return sorted(gains, key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    # 测试数据
    # 是否必须水里 是否有脚蹼 属于鱼类
    datas = [[1, 0, 0, 0],
             [1, 0, 0, 1],
             [1, 1, 0, 1],
             [1, 1, 1, 0],
             [1, 0, 0, 0],
             [2, 0, 0, 0],
             [2, 0, 0, 1],
             [2, 1, 1, 1],
             [2, 0, 1, 2],
             [2, 0, 1, 2],
             [3, 0, 1, 2],
             [3, 0, 1, 1],
             [3, 1, 0, 1],
             [3, 1, 0, 2],
             [3, 0, 0, 0]]
    labels = [0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    d = C45()
    d.train(datas, labels , [1, 2, 3, 4])
    print d.tree
    print d.classify([1 , 1, 1, 1])
    
