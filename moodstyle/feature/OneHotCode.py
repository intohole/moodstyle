#coding=utf-8

from collections import defaultdict
from b2 import math2
import math



class OneHotCode(object):
    
    """feature one hot 
        Test:
            >>> ohc = OneHotCode()
            >>> ohc.train(0)
            >>> ohc.train(1)
            >>> ohc.train(2)
            >>> ohc.train(3)
            >>> ohc.train(4)
            >>> ohc.train(7)
            >>> ohc.predict(0)
            >>> ohc.predict(3)
            >>> ohc.predict(7)
    """

    def __init__(self):
        self._feature_map = {}
    
    def train(self,data):
        if data in self._feature_map:
            return
        self._feature_map[data] = len(self._feature_map) 

    def predict(self,data):
        array_len = int(math.ceil(math.sqrt(len(self._feature_map))))
        index = self._feature_map[data]
        features = math2.bitfield(index)
        features[:0] = [0 for _ in range(array_len - len(features))]
        return features
