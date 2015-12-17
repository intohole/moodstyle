# coding=utf-8
from collections import defaultdict

class MissingValue(object):

    def get_value(self, feature):
        raise NotImplementedError


class ArvgMissingValue(object):

    def __init__(self, feature_len):
        self.default_values = [None for i in range(feature_len)]

    def add(self, feature, value):
        
        self.default_values[feature] = value
        #if self.default_values[feature] is None
        #else (self.default_values[feature] + value)
        
