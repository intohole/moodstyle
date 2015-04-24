#coding=utf-8



class WeightArray(object):


    def __init__(self, datas, distance_fun):
        '''
        function:
            init 
        params:
            datas 数据
            distance_fun 计算两个数据之间的距离
        '''
        self.lable_dict = {datas[index][0]:index   for index in range(len(datas))}
        self.distance_map = self.create_distance_map(datas, distance_fun)
        self.data_len = len(datas)



    def __getitem__(self, label_tuple):
        label1, label2 = label_tuple
        if self.lable_dict.has_key(label1) and self.lable_dict.has_key(label2):
            index1 = self.lable_dict[label1]
            index2 = self.lable_dict[label2]
            return self.get_distance_by_index(index1 , index2)
        raise IndexError, 'index : %s , index2 : %s  not in this distance_map'



    def get_distance_by_index(self  , row , line ):
        '''
        function:
            下半角矩阵 ， 转换坐标

        '''
        if line > row :
            tmp = row 
            row = line 
            line = tmp  
        return self.distance_map[row][line]



    def create_distance_map(self, datas, distance_fun):
        '''
        function:
            创建数据距离map
        params:
            datas 数据，格式 [[label1 , x1 ,x2...,xN ] , [lable2 , x1 , x2 , ..., xN]....[labelN , x1, x2 , ...xN] ]
            distance_fun 距离公式 ， 参数是data1 ， data2 
                return distance
        return 
            datas_map 
        '''
        if distance_fun is None or not callable(distance_fun):
            raise ValueError , 'distance_fun is calc data distance function !'
        distance_map = []
        for i in range(len(datas)):
            tmp_distance = []
            for j in range(i + 1):
                if i == j:
                    tmp_distance.append(0)
                else:
                    tmp_distance.append(distance_fun(datas[i], datas[j]))
            distance_map.append(tmp_distance)
        return distance_map



class Normalization(object):


	def __init__(self, *argv , **kw):
		pass


	def update(self , value):
		raise NotImplementedError


	def get_normalization(self ,value ):
		raise NotImplementedError



class MinMax(Normalization):
	'''
	类功能：
		通过最普通的方式，将数据归一化
	'''


	def __init__(self , max_value = None , min_value = None ) :
		'''
		function
			init
		params
			max_value 最大值 ， 默认值None
			min_value 最小值 ， 默认值None
		'''
		self.max = max_value 
		self.min = min_value


	def update(self , value):
		'''
		function
			将属性对应更新，获得数据最大值和最小值
		params
			value 属性值 ， value 类型(int , long , float)
		return 
			None
		raise
			当value无法转换为float值，抛出ValueError
		'''
		if value is not None:
			try:
				value = float(value)
			except Exception, e:
				raise ValueError , e 
			if self.max is None or self.max < value :
				self.max = value 
			if self.min is None or self.min > value :
				self.min = value 


	def get_normalization(self , value ):
		'''
		function
			将value 转换为归一化后的值
		params
			value 属性值
		return 
			[0,1]
		raise
			value == None ValueError
		'''
		if value is None :
			raise ValueError 
		if self.max == self.min:
			return 1
		return (float(value) - self.min) / (self.max - self.min )


import math 
class ZScore(Normalization):




	def __init__(self):
		self.avg_value = 0 #均值
		self.variance = 0 #方差均值



	def update(self , values):
		'''
		function
			计算数据的平均值和平均方差
		'''
		self.avg_value = sum(values) / float(len(values))
		self.variance = math.sqrt(sum( (value - self.avg_value) ** 2  for value in values ) ) 


	def get_normalization(self , value):
		if value is None :
			raise ValueError 
		if self.avg_value == 0:
			return 0 
		return ( float(value)  - self.avg_value ) / self.variance


class LogNormalization(Normalization):


	def __init__(self , base = 10 ):
		'''
		function
			init
		params
			base log基数，最好为最大值
		return 
			None 
		raise 
			None 
		'''
		self.base = base


	def get_normalization(self , value ):
		if value is None :
			raise ValueError 
		return math.log(value , self.base )

class Arccotx(Normalization):


	def get_normalization(self , value ):
		if value is None:
			raise ValueError
		return math.atan(float(value)) * 2 / math.pi 

if __name__ == '__main__':
	l = Arccotx()
	print l.get_normalization(10)



