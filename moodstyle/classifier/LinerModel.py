#coding=utf-8
#文件功能：
#    感知器实现
#参考网页地址：
#    http://www.hankcs.com/ml/the-perceptron.html
#   http://zh.wikipedia.org/wiki/%E6%84%9F%E7%9F%A5%E5%99%A8
#   http://blog.csdn.net/cscmaker/article/details/8296171
#实现原理：
#    Min(loss(yi - yt)**2 ) 
#
#算法：
#    梯度下降
#

import Interface
import DataSet
from b2 import exceptions2



class LinerModel(Interface.Classify):



    def __init__(self , w , learn_rate = 0.1 , labels = [1 , -1 ]):
        """liner model
            param:w:predict/train data len:int
        """
        self.ratios = [0.] * w 
        self.weight_len = xrange(w)
        self.b = 0 
        self.data_range = xrange(w)
        self.r = learn_rate 
        self.labels = labels

    def __train(self , data , label):
        yt = self.predict(data)
        if yt == label:
            return 
        for i in self.weight_len:
            self.ratios[i] += self.r * label * data[i]
        self.b += self.r * label



    def predict(self , data , *argv , **kw ):
        """线性模型进行预测
        param:data/预测数据:list/tuple/dict
        return:predict value:int:model predict label 
        raise:None
        test:
            >>> model = Ann(2,0.1)
            >>> datas = [[[3, 3], 1], [[4, 3], 1], [[1, 1], -1], [[2, 2], -1] , [[7,3] , 1 ] , [ [-1 , -1] , -1 ] ] 
            >>> datas = [ data[0] for data in datas]
            >>> labels = [ data[1] for data in datas]
            >>> model.train(datas , labels)
            >>> model.predict(datas[-1]) == -1
            True 
        """
        yt = sum( self.ratios[i] * data[i] for i in self.data_range ) + self.b  
        return min([ ( (yt -label) ** 2 , label)  for label in self.labels])[1]

    def train(self , datas , labels , *argv , **kw):
        exceptions2.judge_null(datas)
        exceptions2.judge_null(labels)
        exceptions2.judge_type(datas,(list,tuple,DataSet.DataSet))
        for data,label in zip(datas,labels):
            self.__train(data,label)
