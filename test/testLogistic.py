# coding=utf-8

from math import exp


class Logistic(object):

    def train(self, datas, labels, alpha=0.001):
        self.params = [1. for _ in range(len(datas[0]))]

        for i in range(len(datas)):
            h = self.sigmod(
                sum([datas[i][j] * self.params[j] for j in range(len(self.params))]))
            error = (labels[i] - h)
            for j in range(len(self.params)):
                self.params[j] += (alpha * self.classify(datas[i]) * error)

    def classify(self, datas):
        return sum([datas[i] * self.params[i] for i in range(len(self.params))])

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
            labels.append(-1)
    b = Logistic()
    b.train(data, labels)
    print b.classify([5, 1])
