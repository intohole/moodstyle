# coding=utf-8
#!/usr/bin/env python

import math
from collections import defaultdict




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
        attr_index = attrs.index(attr_name)
        __attrs = attrs[:attr_index]
        __attrs.extend(attrs[attr_index+1:])
        __data = []
        attr_index += 1 # label in the every data first index 
        for dd in data:
            if dd[attr_index] == attr_value:
                d = dd[:attr_index]
                d.extend(attrs[attr_index + 1 :])
                __data.append(d)
        return __data , __cattrs

    def find_best_attr(self , data , attrs):
        pass


if __name__ == '__main__':
    t = TrainDT()
    attrs = [ 'a' , 'b' , 'c' ,'d' ,'e']
    print t.split_data(1 , 'e', 3, attrs)
    print attrs

