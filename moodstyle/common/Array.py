#coding=utf-8
'''
因为对数据进行训练的时候，需要采取抽样方式，让数据更加随机，比如gbdt/随机森林训练的时候；
会采用随机抽样方式进行训练
PoolArray :蓄水池抽样方法
WaterSample :流式抽样方法
SampleArray : 抽样方法的工厂类
'''
from random import randint
from random import random

class PoolArray(objects):


    def __init__(self , objects , sample_rate ):
        self.sample_rate = sample_rate
        self.objects = objects
        self.data_len = len(objects)
        self.sample_num = int( self.data_len * sample_rate )
        self.rand_index = self.create_rand_list()
        self.index = -1 


    def create_rand_list(self):
        index = 0 
        sample_list = []
        while index < self.data_len:
            if index < self.sample_num:
                sample_list.append(index)
            else:
                rand_index = randint(0 , index)
                if rand_index < self.sample_num:
                    sample_list[rand_index] = index 
            index += 1
        return sample_list

    def next(self):
        self.index += 1 
        if self.index < self.data_len:
            return self.objects[self.index]
        else:
            raise StopIteration


class WaterSample(object):


    def __init__(self , objects , sample_rate):
        self.sample_rate = sample_rate
        self.objects = objects
        self.data_len = len(objects)
        self.index = 0


    def get_rand_score(self ):
        return random(0 , 1)

    def next(self):
        while self.get_rand_score() > sample_rate:
            self.index += 1 
        if self.index < self.data_len:
            return self.objects[self.index]
        raise StopIteration
        



        




class SampleArray(object):


    def __init__(self , objects , sample_class = WaterSample):
    	if objects is not None and hasattr(objects , '__iter__') and not isinstance(objects ,basestring):
            self.objects = objects
            self.data_len = len(self.objects)
        else:
            raise ValueError


    def __iter__(self):
        return  sample_class(self.objects , self.sample_rate)




    def __getitem__(self , index ):
        if isinstance(index , (int , long)) and index >= 0 and index < self.data_len:
            return self.objects[index]
        else:
            raise ValueError


