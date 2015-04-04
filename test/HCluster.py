#coding=utf-8


import math 


class DataDistance(object):

    def __init__(self , datas , distance_fun):
        print distance_fun(datas[0] , datas[1])
        self.lable_dict =  {index : datas[index][0]  for index in range(len(datas))}
        self.distance_map = self.create_distance_map(datas , distance_fun)


    def __getitem__(self , label_tuple ):
        label1 , label2 = label_tuple
        if self.lable_dict.has_key(label1) and self.lable_dict.has_key(label2):
            index1 = self.lable_dict[label1]
            index2 = self.lable_dict[label2]
            print index1 , index2 
            return self.distance_map[index1][index2] 
        raise IndexError , 'index : %s , index2 : %s  not in this distance_map'



    def create_distance_map(self , datas , distance_fun):
        '''
        function:
            创建数据距离map
        params:
            datas 数据，格式 [[label1 , x1 ,x2...,xN ] , [lable2 , x1 , x2 , ..., xN]....[labelN , x1, x2 , ...xN] ]
        return 
            datas_map 
        '''
        distance_map = []
        for i in range(len(datas)):
            tmp_distance = [] 
            for j in range(len(datas)):
                if i == j:
                    tmp_distance.append(0)
                else:
                    tmp_distance.append(distance_fun(datas[i] , datas[j]))
            distance_map.append(tmp_distance)
        return distance_map
        



class HierarchicalClustering(object):



    def __init__(self):
        pass



    def cluster(self , datas   , cluster_num ,  threshold = 0.03):
        '''
            
        '''


        no_change = False

        #创建数据距离词典
        distance_map = DataDistance(datas , self.distance)
        #创建一个cluster，每个数据都是一个cluster 
        clusters = [ [datas[i][1]] for i in range(len(datas))]
        
        #如果聚类不小于要求聚类数目继续
        while len(clusters) < cluster_num:
            tmp_clusters = []
            for i in range(len(clusters)):
                for j in range(len(clusters)):
                    if  i != j :
                        pass
                        



        return clusters


    
    def distance(self , data1 , data2 ):
        '''
        function:
            计算两个数据的距离
        params:
            data1 第一个数据
            data2 第二个数据
        return 
            distance 两个数据的距离
        '''

        return math.sqrt(sum([(data1[i] - data2[i]) ** 2    for i in range(1, len(data1))]))


if __name__ == '__main__':
    

    hc =HierarchicalClustering()
    from random import randint
    datas = [ [i , randint(1, 20) , randint(1,20)] for i in range(2) ]
    print datas
    hc.cluster(datas , 3 )