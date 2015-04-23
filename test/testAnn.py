#coding=utf-8
#文件功能：
#	感知器实现
#参考网页地址：
#	http://www.hankcs.com/ml/the-perceptron.html
#   http://zh.wikipedia.org/wiki/%E6%84%9F%E7%9F%A5%E5%99%A8
#   http://blog.csdn.net/cscmaker/article/details/8296171
#实现原理：
#	Min(loss(yi - yt)**2 ) 
#
#算法：
#	梯度下降
#



class Ann(object):



	def __init__(self , w , learn_rate = 0.1 , labels = [1 , -1 ]):
		self.ratios = [0] *w 
		self.b = 0 
		self.range = range(w)
		self.r = learn_rate 
		self.labels = labels



	def train(self , data , label):
		yt = self.classify(data)
		if yt == label:
			return 
		for i in self.range:
			self.ratios[i] += self.r * label * data[i]
		self.b += self.r * label



	def classify(self , data ):
		'''
		function：
			根据感知器，计算data数据值
		params:
			data 数据 [feature1 , feature2 , feature3 .... , featureN ]
		return 
			感知器结果
		'''
		yt = sum( self.ratios[i] * data[i] for i in self.range ) + self.b  
		return min([ ( (yt -label) ** 2 , label)  for label in self.labels])[1]


if __name__ == '__main__':
	a = Ann(2 , 0.1)
	datas = [[[3, 3], 1], [[4, 3], 1], [[1, 1], -1], [[2, 2], -1] , [[7,3] , 1 ] , [ [-1 , -1] , -1 ] ] 
	for data in datas:
		a.train(data[0] , data[1])
	print a.ratios
	print a.b 
	print a.classify(datas[-1][0])

