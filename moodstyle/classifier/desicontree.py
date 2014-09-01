# coding=utf-8
#!/usr/bin/env python

import math






from collections import defaultdict
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


    def calc_info_gain(self , datas  , attrsed):
        '''
        数据形如　：　[{'label' : 1 , 'data' : {}} , {'label' : 0  , 'data' : {}}]
        attrsed set类型　为已经计算完的属性名称
        '''
        data_status = defaultdict(int) # label - > count 
        data_count = 0
        attr_have = {}
        for data in datas:
            if set(data['data'].keys()) != attrsed:
                data_status[data['label']] += 1
                data_count+= 1 
        sys_info_gain =  0. #系统总信息熵
        for __label , __count in data_status:
            sys_info_gain += self.entropy(float(__count) / data_count)


        attr_label_count = {} # attr_name - > attr_value - > label_count 
        #循环数据　　，　计算每个属性
        #计算每个属性值的时候　分别计算

        








class DecisionTree(object):

    __data = {'a': {'c': {1: 30, 2: 70}, 'd': {1: 20, 0: 80}, 'e': {1: 50, 0: 50} , 'count' : 100}, 'h': {'c': {1: 30, 2: 70}, 'd':
             {1: 20, 0: 80}, 'e': {1: 50, 0: 50} , 'count' : 100}, 'x': {'c': {1: 30, 2: 70}, 'd': {1: 20, 0: 80}, 'e': {1: 50, 0: 50} , 'count' : 100}}
        # 类别 -> 属性 -> {1 : 个数 , 0 : 个数}
    __data_count = 300.

    def tarin(self, data):
        pass

    def entropy(self, prob):
        if prob and isinstance(prob, float) and prob >= 0. and prob <= 1.:
            return (-prob) * math.log(prob, 2)

    def ig(self, cname, attrname):
        if self.__data.has_key(cname):
            if self.__data[cname].has_key(attrname):
                centropy = 0.
                for __val in self.__data.keys():
                    centropy += self.entropy(self.__data[__val]['count'] / self.__data_count)
                for __val in self.__data[cname][attrname].values():
                    centropy -= self.entropy(float(__val) / self.__data[cname]['count'])
                return centropy


if __name__ == '__main__':
    x = DefaultDecisionTree()
    datas = [{'label' : 0 , 'data' : {'1' : 0 , '2' : 0 , '3' : 0 }} , {'label' : 1 , 'data' : {'1' : 1 , '2' : 2 , '3' : 0 }} ]
    x.calc_info_gain(datas , set(['2','3']))
    print x.entropy(9.0 / 14) + x.entropy(5.0 / 14)
    print x.entropy(6.0 / 9) + x.entropy( 2.0 /5)
    print x.entropy(3.0 / 9) + x.entropy( 3.0 /5)
