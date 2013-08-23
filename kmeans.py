#coding=utf-8
#!/usr/bin/env python

from random import randint


        
        
class KMeans(object):
    
    def rand_seed(self , k , data):
        k_seed = {}
        for _ in range(k):
            _find = False 
            while not _find:
                r = randint(0,len(data))
                if not k_seed.has_key(r):
                    k_seed[r] = [(r,0)]
                    _find = True
        return k_seed
    
    
    def distance(self,data1,data2):
        return long(data1)-long(data2)
    
    
    def cluster(self,central,data):
        for i in range(len(data) - 1 ):
            if i not in central.keys():
                _min_value = None
                _index = None
                for _key in central.keys():
                    _dis = self.distance(data[_key], data[i])
                    if not _min_value or _dis < _min_value:
                        _index = _key
                central[_key].append((i,_min_value))
        return central
    
                
    
    def find_central(self,cluster_result):
        _seed = {}
        for _key,_val in cluster_result.items():
            _central = 0
            for _v in _val:
                _central = _central + _v[1]
            _central = _central / len(_val)
    
    
    def _find_central_in(self , ):
        pass
                
    
    


if __name__ == "__main__":
    k = KMeans()
    print k.cluster(k.rand_seed(3, [1,4,5,2,1,4,9,10]), [1,4,5,2,1,4,9,10])
        