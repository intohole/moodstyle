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
class Ann(testInterface.Classify):



    def __init__(self , w , learn_rate = 0.1 , labels = [1 , -1 ]):
        self.ratios = [0.] * w 
        self.weight_len = xrange(w)
        self.b = 0 
        self.data_range = xrange(w)
        self.r = learn_rate 
        self.labels = labels

    def __train(self , data , label):
        yt = self.classify(data)
        if yt == label:
            return 
        for i in self.weight_len:
            self.ratios[i] += self.r * label * data[i]
        self.b += self.r * label



    def classify(self , data , *argv , **kw ):
        """ann算法进行分类
        params:data 数据源:class [list , tuple ,dict]
        return:1,-1默认值:value 
        raise:None
        test:
            >>> classify = Ann(2,0.1)
            >>> datas = [[[3, 3], 1], [[4, 3], 1], [[1, 1], -1], [[2, 2], -1] , [[7,3] , 1 ] , [ [-1 , -1] , -1 ] ] 
            >>> for data in datas:
            ...     classify.train(data[0] , data[-1])
            >>> classify.classify(datas[-1][0]) == -1
            True 
        """
        yt = sum( self.ratios[i] * data[i] for i in self.data_range ) + self.b  
        return min([ ( (yt -label) ** 2 , label)  for label in self.labels])[1]

    def train(self , datas , labels , *argv , **kw):
        if data is None:
            raise TypeError("datas is must be valuealbe")
        if isinstance(data , (list, tuple, testDataSet.DataSet)) is False:
            raise TypeError("datas type in [list , tuple , testDataSet.DataSet]")
        if len(datas) != len(labels):
            raise Exception("datas len must be equal labels")
        for i in xrange(datas):
            self.__train(datas[i] , labels[i])
