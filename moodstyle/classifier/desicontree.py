# coding=utf-8
#!/usr/bin/env python

import math
from collections import defaultdict


class Node(object):



    def __init__(self):
        pass

    

class DefaultDecisionTree(object) :
    '''
    二分类决策树实现思路　
    找到一个信息增益最高的属性　
    按照属性进行切分数据


    '''

    def __init__(self):
        pass




class TrainDT(object):

    def __init__(self):
        pass


    def train(self , data , attrs ):
        '''
        data -> [label , data1 , data2 , ....., dataN]
        attrs -> [attr1 , attr2 , attr3 ,.....,attrN]
        '''
        dt = {}




    def split_data(self , data , attr_name , attr_value , attrs):
        '''
        split classifier data
        '''

        data_status = defaultdict(int) # label - > count 
        data_count = 0
        for data in datas:
            data_status[data['label']] += 1
            data_count += 1
        sys_info_gain =  0. #系统总信息熵
        for __label , __count in data_status.items():
            sys_info_gain += self.entropy(float(__count) / data_count)
        attr_label_count = dict() # attr_name - > attr_value - > label_count 
        for __key in attrs:
            attr_label_count[__key] = {}
        #循环数据　　，　计算每个属性
        #计算每个属性值的时候　分别计算
        for data in datas: #循环每个数组
            __data = data['data']
            __label = data['label']
            for i in range(__data):
                if not attr_label_count[attrs[i]].has_key(__data[i]):
                    attr_label_count[attrs[i]][__data[i]] = {}
                    for label in data_status.keys():
                        attr_label_count[attrs[i]][__data[i]][label] = 0 
                attr_label_count[attrs[i]][__data[i]][__label] += 1    


if __name__ == '__main__':
    x = DefaultDecisionTree()
    atrrs = {1 : '1' , 2 : '2' , 3: '3'}
    datas = [{'label' : 0 , 'data' :[0 , 1, 1]} , {'label' : 1 , 'data' : [1,2,3]} ]
    x.calc_info_gain(datas , set(['2','3']))
    print x.entropy(9.0 / 14) + x.entropy(5.0 / 14)
    print x.entropy(6.0 / 9) + x.entropy( 2.0 /5)
    print x.entropy(3.0 / 9) + x.entropy( 3.0 /5)

