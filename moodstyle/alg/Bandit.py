#coding=utf-8

from collections import defaultdict
import random



class Greedy(object):
    """
    """
    EXPLORER = 1
    WORK = 0 
    
    def __init__(self,e,N):
        self.e = e
        self.p = [0.5] * N
        self._front = [0.] * N
        self._explor = [0.] * N 
        self.N = N
        self._max_index = 0
        # 1 explorer ; 0 work
        self._status = None
        self._last = None

    def _prop(self):
        for i in range(self.N):
            if self._explor[i] == 0.:
                continue
            self.p[i] = self._front[i] / self._explor[i]
            if self.p[self._max_index] < self.p[i]:
                self._max_index = i
            
    
    def getIndex(self):
        r = random.random()     
        index = None 
        if r < self.e:
            index = random.randint(0,self.N - 1)
            self._status = self.EXPLORER 
        else:
            self._status = self.WORK
            index = self._max_index 
        self._last = index
        return index

    
    def process(self,label):
        if self._status == self.EXPLORER:
            if label == 1:
                self._front[self._last] += 1.
            self._explor[self._last] += 1.
            self._prop()


#class UCB(object):
#    
#
#    def __init__(self,N,max_value):
#        self.N = N
#        self.max_value = max_value
#        self._count = 0
#        self._sub_count = [0.] * N
#        self._sub_sum = [0.] * N
#        self.p = [0.] * N
#        self._last = None
#    
#
#    def _prop(self):
#        for i in range(self.N):
#            if self._sub_count == 0:
#                continue
#            self.p[i] = self._sub_sum[i] / self._sub_count + math.sqrt( 2 * math.log(self._count) / self._sub_count[i])
#
#    def getIndex(self):
#        for i in range(self.N):
#            if self._sub_count[i] == 0:
#                self._last = i
#                return self._last            
#        self._last = max(enumerate(self.p),key = lambda x:x[1])[0] 
#        return self._last 
#
#    def process(self,label):
#        self._count += 1
#        self._sub_count[self._last] += 1 
#        self._sub_sum[self._last] += label
#
          
