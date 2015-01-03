#!/coding=utf-8

from collections import defaultdict
from copy import deepcopy


class Classifier(object):

    def __init__(self, classifier):
        if classifier and (callable(classifier)):
            self.classifier = classifier
        else:
            raise TypeError, 'classifier must be  callable and valuable !'
        # label   ,    ( fit value sum , count )
        self.__weights = defaultdict(float)
        self.__count = defaultdict(int)

    def clear(self):
        self.__weights.clear()
        self.__count.clear()

    def update_fit_value(self, data, value):
        label = self.classifier(data)
        self.__weights[label] += value
        self.__count[label] += 1.

    def updates_fit_values(self, datas, values):
        for i in range(len(datas)):
            self.update_fit_value(datas[i], values[i])

    def sync(self):
        '''
        计算每个分类器需要拟合误差值
        '''
        for label in self.__weights.keys():
            self.__weights[label] /= self.__count[label]

    def classify(self, data):
        label = self.classifier(data)
        return self.__weights[label] if self.__weights.has_key(label) else None


    def __str__(self):
        return str(self.__weights)






class AdTree(object):

    def __init__(self):
        #定义分类器集合
        self.classifiers = []

    def train(self, datas, weights, classifiers, diff=0.2):
        '''
        datas
        weights , 每个数据需要拟合的数值
        F0(x) = 0
        F1(x) = F0(x) + 树的分值
        FN(x) = FN(x) + 树(N-1)
        r(x) = sum ( yi - F
        '''
        r = deepcopy(weights)

        for _ in range(len(classifiers)):
            _classifiers = [Classifier(classifier) for classifier in classifiers]
            # 更新每个分类器 ， 与上轮的
            # 残差 ， 计算需要拟合的weight
            for _classifier in _classifiers:
                _classifier.updates_fit_values(datas, r)
                _classifier.sync()
            #计算损失函数值 ， 分类器的标记
            loss, ci = self.find_min_loss(datas, r, _classifiers)
            self.classifiers.append(deepcopy(_classifiers[ci]))
            #更新下一轮残差是当前一轮分类器拟合上一轮残差剩余的残差
            #所以更新残差的时候是分类器，而不是所有分类器都参加更正
            r = self.update_residual(datas, r , _classifiers[ci])
            #损失数值小于要求值之后 ， 会跳出方程
            if loss < diff:
                break

    def find_min_loss(self, datas, residuals, classifiers):
        '''
        每一轮迭代迭代 ， 只需要拟合上一轮的残差值
        datas : 数据
        residuals ： 上一轮的残差表
        return :
            (最小损失函数值 ， 分类器序号)

        '''

        return min([
            (
                sum(
                    [
                        (classifiers[j].classify(datas[i]) - residuals[i]) ** 2
                        for i in range(len(datas))
                    ]
                ), j)
            for j in range(len(classifiers))
        ])

    def update_residual(self, datas, residuals , classifier):
        '''
        返回一个参差表 ， 通过生成的分类器 ， 计算下一轮需要拟合的残差表
        Rn-1,i = yi - fn-1(xi)
        '''
        return [
            residuals[i] - classifier.classify(datas[i])
            for i in range(len(datas))
        ]

    def classify(self, data):
        return sum([classifier.classify(data) for classifier in self.classifiers]) if len(self.classifiers) > 0 else 0


if __name__ == '__main__':
    datas = [i for i in range(1, 11)]
    weights = [5.56, 5.70, 5.91, 6.40, 6.80, 7.05, 8.90, 8.70, 9.00, 9.05]

    at = AdTree()
    classifiers = [lambda x: 1 if x >= 1.5 else 0, lambda x: 1 if x >= 2.5 else 0, lambda x: 1 if x >= 3.5 else 0, lambda x: 1 if x >= 4.5 else 0, lambda x:
                   1 if x >= 5.5 else 0, lambda x: 1 if x >= 6.5 else 0, lambda x: 1 if x >= 7.5 else 0, lambda x: 1 if x >= 8.5 else 0, lambda x: 1 if x >= 9.5 else 0]

    at.train(datas, weights, classifiers)
    print at.classify(8)
