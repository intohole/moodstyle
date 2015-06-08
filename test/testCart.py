# coding=utf-8


from collections import Counter
from collections import defaultdict
import cPickle


class Node(object):

    def __init__(self,  index, split_value):
        self.index = index
        self.split_value = split_value
        self.left_tree = None
        self.right_tree = None
        self.val = None


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
            self.tree = cPickle.loads(f.readline().strip())

    def save(self, model_path):
        if not self.tree:
            raise ValueError, 'no model can save!'
        with open(file_path, 'w') as f:
            f.write(cPickle.dumps(self.tree))

    def __train(self, datas, attrs, threshold=0.01):

        if self.attrs is None:
            self.attrs = attrs

        label_dict = Counter([data[-1] for data in datas])

        if len(label_dict.keys()) == 1:
            return float(datas[0][-1])

        if len(attrs) == 0:
            return sum(data[-1] for data in datas) / len(datas)

        attr, attr_gain, attr_val = self.get_best_feature(
            datas, attrs)[0]  # 得到最好信息增益的属性

        if attr_gain < threshold:
            return sum(data[-1] for data in datas) / len(datas)

        node = Node(self.attrs.index(attr) , )
        node[attr] = {}
        child_attr = self.get_split_attr(  # 为下轮切割属性
            attrs, attr
        )
        for val in attr_val:
            # 按照属性不同value 区分这个
            # 取得最好分类属性 ， 按照不同该属性不同val 区分数据 ；
            node[attr][val] = self.__train(
                self.split_data_by_attr(
                    datas, attrs, attr, val
                ),
                child_attr,
                threshold
            )
        return node

    def train(self, datas, attrs, threshold=0.01):
        self.tree = self.__train(datas, attrs, threshold)

    def get_split_attr(self, attrs, attr):
        split_attrs = []
        index = attrs.index(attr)
        split_attrs.extend(attrs[:index])
        split_attrs.extend(attrs[index + 1:])
        return split_attrs


    def split_data_by_attr(self, datas, attrs, attr_name, attr_value=True):
        '''
        切割训练集为了下一步
        datas :训练的数据 [[data]]
        attrs 属性名称列表
        attr_val 属性值
       是否是密集型数据 , 暂时废弃
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

    def get_split_value(self, datas, split_index):
        '''
        得到cart树，分割数据点index，中位数
        '''
        if len(datas):
            return sum(data[split_index] for data in datas) / len(datas)
        raise ValueError

    def calc_gini(self, datas, index, split_value):
        """计算属性值gini值
        参数：
            datas   数据集合
            labels  label集合，与datas集合对应

        """
        labels = [data[-1] for data in datas]
        labels_dict = Counter(labels)
        label_dist_dict = {
            label: defaultdict(int) for label in labels_dict.keys()}
        for i in range(len(labels)):
            if datas[i][index] > split_value:
                label_dist_dict[labels[i]][1] += 1
            else:
                label_dist_dict[labels[i]][0] += 1
        gini = 0.
        for label in labels_dict.keys():
            prob = labels_dict[label] / len(labels)
            prob_label = label_dist_dict[label][1] / float(len(labels))
            gini += (prob * 2 * prob_label * (1 - prob_label))
        return gini

    def get_best_feature(self, datas, attrs, labels):
        ginis = []
        data_len = len(attrs)
        for split_index in range(data_len):
            split_value = get_split_value(datas, split_index)
            gini = calc_gini(datas, labels, split_index, split_value)
            ginis.append(
                (gini , split_value, split_index))
        return max(ginis)

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


if __name__ == '__main__':
    from random import random
    from random import randint
    datas = [[random() + 0.1] for i in range(10)]
    print get_split_value(datas, 0)
    labels = [1 if datas[i] > 0.45 else 0 for i in range(len(datas))]
    print get_best_split_feature(datas, 1, labels)
