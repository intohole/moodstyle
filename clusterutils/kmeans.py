#coding=utf-8
#!/usr/bin/env python

from random import randint
<<<<<<< HEAD:clusterutils/kmeans.py
from math import sqrt        
=======
import  re
>>>>>>> d0a83c9d3a2ecc3d207d5d89fea99284bde910d0:kmeans.py

'''
处理数据的格式 [数据1,数据2]
但是必须要改写 def distance(data1,data2) 数据距离函数
数据转换格式 {分类:{数据的位置:数据距离}}
'''       
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
#         return abs(data1-data2)
        return sqrt((data1[0]-data2[0])*(data1[0]-data2[0])+ (data1[1]-data2[1])*(data1[1]-data2[1]))
    
    #聚类
    #循环每个元素找到距离最近的元素
    #将元素添加到分类中
    def cluster(self,central,data):
        for i in range(len(data)):
            if i not in central.keys(): #分组中心肯定不能分到其它类别 所以跳过
                _min_value = None #最小值
                _index = None #最小值的数据位置
                for _key in central.keys(): #循环每个分类中心
                    _dis = self.distance(data[_key], data[i]) #计算距离
                    if not _min_value or _dis < _min_value: #如果第一次 或者 距离小于最小值 ,记录
                        _index = _key
                        _min_value = _dis
                central[_index][i] = _min_value #保存最小距离 , 方便 find_central计算
        return central #返回新聚类中心
    
                
    #找到每个分类中中心 -> min(abs(每个距离值 - 中心值))
    #步骤:
    #   计算分类中的距离 {分类中心的序号:{数据序号:距分类中心距离}}
    #   找到每个分类元素 离中心最近的元素
    #   返回分类中心 {}
    def find_central(self,cluster_result):
        _seed = {}
        for _key,_val in cluster_result.items():
            _central = 0.
            #计算分类中所有距离平均数
            for _v in _val.values():
                _central = _central + _v
            _central = _central / len(_val.values())
            #找到平均值，将平均值作为新的中心
            _min = None
            _mindex = _key
            for _index,_v in _val.items():
                if not _min or abs(_v - _central) <_min:
                    _min = abs(_v - _central)
                    _mindex = _index
            _seed[_mindex] = {}
            _seed[_mindex][_mindex] = 0.
        return _seed
    
    #对数据进行排序，比较
    #
    def have_chage(self,oldcluster,clusterresult):
        if len(oldcluster.keys()) == 0: #第一次时,则返回
            return True
        old_list = [_val.keys() for _val in oldcluster.values()] #将数据位置提出
        cluster_list = [ _val.keys() for _val in clusterresult.values()] 
        old_list.sort() #排序
        cluster_list.sort() 
        if len(old_list) != len(cluster_list): #如果长度不同肯定是不同的
            return True
        for i in range(len(old_list)): 
            if not (old_list[i] == cluster_list[i]): #如果结果不同
                return True  #则是有改变的
        return False #
                
                    
                
    
    def k_means(self , k , data , times = 100000):
        if k >= len(data):
            raise Exception("K is bigger than data")
        _randseed = self.rand_seed(k,data)
        isOver = False
        _oldcluster = {}
        time_count = 0 # 迭代次数 ,
        while not isOver: 
            _cluster = self.cluster(_randseed, data) #把每个元素 分到最近的分类中
            print 1
            if  not self.have_chage(_oldcluster, _cluster) or time_count > times: #是否没有改变 , 或者超过迭代次数 聚类终止条件
                result = {}
                count = 1
                for _,_val in _cluster.items():
                    result[count] = []
                    for _key in _val.keys():
                        result[count].append(data[_key])
                    result[count].sort() #分类中心排序
                    count = count + 1 #分类元素
                return result
            _oldcluster.clear() #清空数据
            for _key,_val in _cluster.items():
                _oldcluster[_key] = _val 
            _randseed = self.find_central(_oldcluster) #找到分类中心 算数中心
            time_count = time_count + 1 #迭代次数+1
            
        
        
    
    
    
        
                
    
    


if __name__ == "__main__":
    k = KMeans()
    print k.k_means(4, [(1,4),(5,2) ,(100,16),(8,9),(10,101),(150,1555),(177,120),(14,4),(5,99)])

        
