#coding=utf-8
#!/usr/bin/env python

from random import randint


        
        
class KMeans(object):
    
    def rand_seed(self , k , data):
        k_seed = {}
        for _ in range(k):
            _find = False 
            while not _find:
                r = randint(0,len(data)-1)
                if not k_seed.has_key(r):
                    k_seed[r] = {}
                    k_seed[r][r] = 0.
                    _find = True
        return k_seed
    
    
    def distance(self,data1,data2):
        return abs(long(data1)-long(data2))
    
    
    def cluster(self,central,data):
        for i in range(len(data)):
            if i not in central.keys():
                _min_value = None
                _index = None
                for _key in central.keys():
                    _dis = self.distance(data[_key], data[i])
                    if not _min_value or _dis < _min_value:
                        _index = _key
                        _min_value = _dis
                central[_index][i] = _min_value
        return central
    
                
    
    def find_central(self,cluster_result):
        _seed = {}
        for _key,_val in cluster_result.items():
            _central = 0.
            #计算分类中所有距离平均数
            for _index,_v in _val.items():
                _central = _central + _v
            _central = _central / len(_val)
            #找到平均值，将平均值作为新的中心
            _min = None
            _mindex = _key
            for _index,_v in _val.items():
                if not _min or _v <_min:
                    _min = _v
                    _mindex = _index
            _seed[_mindex] = {}
            _seed[_mindex][_mindex] = 0.
        return _seed
    
    def have_chage(self,oldcluster,clusterresult):
        for _oc , _ov in oldcluster.items():
            isSameLine = True
            for _c , _v in clusterresult.items():
                isSameLine = True
                for _index in _ov.keys():
                    if not _v.has_key(_index):
                        isSameLine = False
                        break
            if not isSameLine:
                return False
        return True
                    
                
    
    def k_means(self , k , data):
        if k >= len(data):
            raise Exception("K is bigger than data")
        _randseed = self.rand_seed(k,data)
        isOver = False
        _oldcluster = {}
        while not isOver:
            _cluster = self.cluster(_randseed, data)
            print 1
            if not self.have_chage(_oldcluster, _cluster):
                break
            _oldcluster.clear()
            _oldcluster = None
            _oldcluster = _cluster
            _randseed = None
            _randseed = self.find_central(_cluster)
        
        result = {}
        count = 1
        for _,_val in _oldcluster.items():
            result[count] = []
            for _key in _val.keys():
                result[count].append(data[_key])
            count = count + 1
        return result
    
    
            
        
        
    
    
    
        
                
    
    


if __name__ == "__main__":
    k = KMeans()
    print k.k_means(3, [1,4,5,2 ,100,16,8,9,10,101,150,1555,177,120,14,4,5])
        