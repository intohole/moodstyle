# coding=utf-8

from math import exp


class Logistic(object):

    def train(self, datas, labels, alpha=0.001):
        self.params = [1. for _ in range(len(datas[0]))]
        self.labels = set(labels)

        for i in range(len(datas)):
            h = self.sigmod(self.classify(datas[i]))
            #L(a) = error , 已知损失数值 ， 需要求更新权重的
            error = (labels[i] - h)
            for j in range(len(self.params)):
                self.params[j] += (alpha * datas[i][j] * error)

    def classify(self, data):
        _val = sum([data[i] * self.params[i] for i in range(len(self.params))]) 
        return min([abs(label - _val  , label) for label in self.labels ])
    def sigmod(self, x):

        return 1. / (1 + exp(-x))



if __name__ == '__main__':
    data = []
    labels = []
    from random import randint
    for _ in range(10000):
        x = randint(1 , 10)
        y = randint(1 , 10)
        data.append((x,y))
        if x <= y:
            labels.append(1)
        else:
            labels.append(0)
    b = Logistic()
    b.train(data, labels)
    print b.classify([2, 5])
