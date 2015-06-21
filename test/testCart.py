# coding=utf-8


from collections import Counter
from collections import defaultdict
import cPickle
import copy 


class Node(object):

    def __init__(self, split_attr, split_value):
        self.split_attr = split_attr
        self.split_value = split_value
        self.left_tree = None
        self.right_tree = None

    def __str__(self):
        return '[split_attr : %s split_value : %s ] [left tree %s] [right tree %s ] ' % (self.split_attr, self.split_value , self.left_tree , self.right_tree)


class CartTree(object):

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
        with open(model_path, 'w') as f:
            f.write(cPickle.dumps(self.tree))

    def __train(self, datas, labels, attrs, threshold=0.01):

        label_dict = Counter(labels)

        if len(label_dict.keys()) == 1:

            return float(label_dict.keys()[0])

        if len(attrs) == 0:
            return sum(label for label in labels) / float(len(labels))

        attr_gain, attr, split_value, left_data, left_label, right_data, right_label = self.get_best_feature(
            datas, labels, attrs)  # 得到最好信息增益的属性
        if attr_gain < threshold:
            return sum(label for label in labels) / float(len(labels))
        node = Node(attr, split_value)
        child_attr = self.get_split_attr(# 为下轮切割属性
            attrs, attr
        )
        #创建左子树
        node.left_tree = self.__train(
            self.split_data_by_attr(left_data , attrs , attr) , left_label, child_attr, threshold)
        #创建
        node.right_tree = self.__train(
            self.split_data_by_attr(right_data , attrs , attr), right_label, child_attr, threshold)
        return node



    
    def split_data_by_attr(self, datas, attrs, attr_name):
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
            dump = data[:index]
            dump.extend(data[index + 1:])
            dump_datas.append(dump)
        return dump_datas
    
    def train(self, datas, attrs, labels, threshold=0.01):
        self.attrs = attrs
        self.tree = self.__train(datas, labels, attrs, threshold)

    def get_split_attr(self, attrs, attr):
        split_attrs = []
        index = attrs.index(attr)
        split_attrs.extend(attrs[:index])
        split_attrs.extend(attrs[index + 1:])
        return split_attrs

    def get_split_value(self, datas, split_index):
        '''
        得到cart树，分割数据点index，中位数
        '''
        if len(datas):
            return sum(data[split_index] for data in datas) / float(len(datas))
        raise ValueError

    def calc_gini(self, datas, labels, split_index, split_value):
        """计算属性值gini值
        参数：
            datas   数据集合
            labels  label集合，与datas集合对应

        """
        labels_dict = Counter(labels)
        label_dist_dict = {
            label: defaultdict(int) for label in labels_dict.keys()}
        left_data = []
        left_label = []
        right_data = []
        right_label = []
        for i in range(len(labels)):
            if datas[i][split_index] > split_value:
                label_dist_dict[labels[i]][1] += 1.
                right_data.append(datas[i])
                right_label.append(labels[i])
            else:
                label_dist_dict[labels[i]][0] += 1.
                left_data.append(datas[i])
                left_label.append(labels[i])
        gini = 0.
        for label in labels_dict.keys():
            prob = labels_dict[label] / float(len(labels))
            prob_label = label_dist_dict[label][1] / float(len(labels))
            gini += (prob * 2 * prob_label * (1 - prob_label))
        return gini, left_data, left_label, right_data, right_label

    def get_best_feature(self, datas, labels, attrs):
        gini_min = float('inf')
        left_data = None
        left_label = None
        right_data = None
        right_label = None
        split_attr = None
        split_value = None
        for split_index in range(len(attrs)):
            _split_value = self.get_split_value(datas, split_index)
            gini, _left_data, _left_label, _right_data, _right_label = self.calc_gini(
                datas, labels, split_index, _split_value)
            if gini < gini_min:
                gini_min = gini
                split_attr = attrs[split_index]
                left_data = _left_data
                left_label = _left_label
                right_data = _right_data
                right_label = _right_label
                split_value = _split_value
        return gini_min, split_attr, split_value, left_data, left_label, right_data, right_label

    def _classify(self, data, attrs, node):
        '''
        功能： 用于分类模型
        参数 ：
            data 待分析的数据 ， list
        返回:
            返回决策树的label
        思想 ： 每层树的节点 {节点1：{val1 ：节点2：{val3 ：{。。。。{valn ： label }}}
        第一层是key 下一层是val 第三层是key 第四层是val 。。。。 直到出现val
        '''
        if not isinstance(node, Node):
            return node
        print attrs 
        value = data[attrs.index(node.split_attr)]
        del data[attrs.index(node.split_attr)]
        del attrs[node.split_attr]
        if value > node.split_value:
            return self._classify(data, attrs, node.right_tree)
        else:
            return self._classify(data, attrs, node.left_tree)

    def classify(self, data):
        return self._classify(copy.copy(data), copy.copy(self.attrs) , self.tree)


if __name__ == '__main__':
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
    d = CartTree()
    d.train(datas, [1, 2, 3, 4], labels)
    print d.tree
    print d.classify([1, 0])
    print d.attrs
