# coding=utf-8

from collections import Counter
from collections import defaultdict


class Bayes(object):

    def __init__(self):
        pass

    def classify(self, data):
        pass

    def train(self, datas, labels, dense=True):
        '''
        P(C | I) = P(I | C ) * P(C) /  P(I)
        因为判断 I的存在这个类别概率大小 ， 所以I必然已经存在
        P(C|I) = P(I | C) * P(C) # I 是数据 ， C是类别
        '''

        self.label_status = Counter(labels)
        self.attr_status = {i: {} for i in range(len(datas[0]))}
        for i in range(len(datas)):
            for j in range(len(datas[i])):
                attr_val = datas[i][j]
                # 统计每个属性对应 p(I | C) , I < (v1 , v2 ,v3....,vn)
                if not self.attr_status[j].has_key(attr_val):
                    self.attr_status[j][attr_val] = defaultdict(float)
                self.attr_status[j][attr_val][labels[i]] += 1.
        # 计算每个属性出现val 时 ， P(v1|I,C)
        for feature, attr_label in self.attr_status.items():
            for attr_val, label in self.attr_status[feature].items():
                for cl in label.keys():
                    self.attr_status[feature][attr_val][
                        cl] /= self.label_status[cl]
        # 计算所有类别出现的概率 P(C) = sum(Cn) / sum(C) , n < (1,2,3,4,5....n)
        labels_count = float(sum(self.label_status.values()))
        for label, count in self.label_status.items():
            self.label_status[label] /= labels_count

    def classify(self, data):
        '''
        P(I | C ) * P(C) /  P(I)
        data : list , tuple -> [v1n , v2n ,v3n]
        返回：
            [(类别概率,类别1) , (类别概率 ， 类别2).....(类别概率 ， 类别n)] ， 降序
        '''
        return sorted([(
            sum(
                [
                    self.attr_status[i][data[i]][label]
                    for i in range(len(data))
                    if self.attr_status[i][data[i]].has_key(label)
                ]
            )
            *
            self.label_status[label], label
        )
            for label in self.label_status.keys()
        ], reverse=True)


if __name__ == '__main__':
    data = [[1, 0], [0, 1], [1, 1]]
    labels = [1, 0, 1]
    b = Bayes()
    b.train(data, labels)
    print b.classify([1, 1])
