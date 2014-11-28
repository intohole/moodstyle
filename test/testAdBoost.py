# coding=utf-8

import math


class BoostClassifier(object):

    def __init__(self, classifier, weight=None):
        if classifier and callable(classifier):
            self.classifier = classifier
            self.weight = weight
        else:
            raise TypeError, 'classifier has classify and is callable!'

    def __call__(self, data):
        return self.classifier(data)

    def __str__(self):
        return 'weight : %s' % self.weight


class BoostData(object):

    def __init__(self, data, weight=None):
        if data and isinstance(data, (list, tuple)) and len(data) >= 2:
            self.data = data
            self.weight = weight
        else:
            raise ValueError


class AdBoost(object):

    def __init__(self, classifiers=[]):

        self.__boost_classifier = [BoostClassifier(cl) for cl in classifiers]
        self.__labels = set()

    def train(self, datas):
        '''
        [[feature1 , feature2 ,....,featuren , label]]
        '''
        # 初始化权重, 每个数据初始化权重为 weight = ( 1.0 / 数据长度 )
        if len(datas) == 0 or len(self.__boost_classifier) == 0:
            raise ValueError 

        for data in datas:
            self.__labels.add(data[-1])
        trains = [BoostData(data, 1.0 / len(datas)) for data in datas]
        for _ in range(len(self.__boost_classifier)):
            best_classifier = self.__get_trainer(trains)[0]
            best_classifier[1].weight = math.log((1 - best_classifier[0]) /
                                                 best_classifier[0], math.e) / 2
            self.__update_data_weight(trains, best_classifier[1])

    def classify(self, data):
        weight = sum([classifier.weight * classifier(data)
                      for classifier in self.__boost_classifier if classifier.weight != None])
        return sorted([(abs(label - weight), label) for label in self.__labels], key=lambda x: x[0])[0][1]

    def __update_data_weight(self, trains, classifier):
        '''
        功能： 更新数据的权重 
        公式：

        '''
        zm = sum([data.weight * math.exp(-classifier.weight *
                                         data.data[-1] * classifier(data.data[:-1])) for data in trains])
        for data in trains:
            data.weight = data.weight * \
                math.exp(-classifier.weight *
                         data.data[-1] * classifier(data.data[:-1])) / zm

    def __str__(self):
        msg = []
        for i in range(len(self.__boost_classifier)):
            msg.append('%s : %s' % (i, self.__boost_classifier[i]))
        return '\t'.join(msg)

    def __get_trainer(self, trains):
        return sorted([(sum([bd.weight for bd in trains if cl(bd.data[:-1]) != bd.data[-1]]), cl)
                       for cl in self.__boost_classifier if cl.weight == None], key=lambda x: x[0], reverse=False)


if __name__ == '__main__':
    classifiers = [lambda x: -1 if x[0] > 2.5 else 1, lambda x:
                   1 if x[0] > 5.5 else -1, lambda x: 1 if x[0] < 8.5 else -1]
    a = AdBoost(classifiers)
    datas = [[0, 1], [1, 1], [2, 1], [3, -1], [4, -1],
             [5, -1], [6, 1], [7, 1], [8, 1], [9, -1]]
    a.train(datas)
    print a.classify([9])
    print a
