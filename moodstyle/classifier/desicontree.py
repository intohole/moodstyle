# coding=utf-8
#!/usr/bin/env python

import math
from collections import defaultdict

class Node(object):



    def __init__(self):
        pass

    def __

class DefaultDecisionTree(object) :
    '''
    二分类决策树实现思路　
    找到一个信息增益最高的属性　
    按照属性进行切分数据


    '''

    def __init__(self):
        pass



    def predict(self , data):
        pass



    def train(self , datas):
        pass



    def split_datas_by_attr(self , datas , attr , attsed ):
        '''
        将数据按照某个属性进行split动作　，　决策树计算流程　，　按照某个属性对系统的增益最大（最能确定分类元素）　，
        建立节点按照
        '''
        tree_root = {}



    def entropy(self , prob ):
        if prob and isinstance(prob, float) and prob >= 0. and prob <= 1.:
            return (-prob) * math.log(prob, 2)


    def calc_info_gain(self , datas , attrs ):
        '''
        数据形如　：　[{'lable' : 1  , 'data' : [1 , 2 , 3]]
        attrsed set类型　为已经计算完的属性名称
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
