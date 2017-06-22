#coding=utf-8

from collections import defaultdict
import random



class Greedy(object):
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





if __name__ == "__main__":
    
    N = 100 
    p = [random.random() for i in range(N)]
    greedy = Greedy(0.3,N)
    TIMES = 100000
    COUNT = 0
    for _ in range(TIMES):
        index = greedy.getIndex()          
        prop = random.random()
        if prop <= p[index]:
            label = 1 
            COUNT += 1
        else:
            label = 0
        greedy.process(label)
    
    print COUNT / float(TIMES)
            
                         
