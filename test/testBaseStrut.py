#coding=utf-8



class WeightArray(object):


    def __init__(self, datas, distance_fun):
        '''
        function:
            init 
        params:
            datas 数据
            distance_fun 计算两个数据之间的距离
        '''
        self.lable_dict = {datas[index][0]:index   for index in range(len(datas))}
        self.distance_map = self.create_distance_map(datas, distance_fun)
        self.data_len = len(datas)



    def __getitem__(self, label_tuple):
        label1, label2 = label_tuple
        if self.lable_dict.has_key(label1) and self.lable_dict.has_key(label2):
            index1 = self.lable_dict[label1]
            index2 = self.lable_dict[label2]
            return self.get_distance_by_index(index1 , index2)
        raise IndexError, 'index : %s , index2 : %s  not in this distance_map'



    def get_distance_by_index(self  , row , line ):
        '''
        function:
            下半角矩阵 ， 转换坐标

        '''
        if line > row :
            tmp = row 
            row = line 
            line = tmp  
        return self.distance_map[row][line]



    def create_distance_map(self, datas, distance_fun):
        '''
        function:
            创建数据距离map
        params:
            datas 数据，格式 [[label1 , x1 ,x2...,xN ] , [lable2 , x1 , x2 , ..., xN]....[labelN , x1, x2 , ...xN] ]
            distance_fun 距离公式 ， 参数是data1 ， data2 
                return distance
        return 
            datas_map 
        '''
        if distance_fun is None or not callable(distance_fun):
            raise ValueError , 'distance_fun is calc data distance function !'
        distance_map = []
        for i in range(len(datas)):
            tmp_distance = []
            for j in range(i + 1):
                if i == j:
                    tmp_distance.append(0)
                else:
                    tmp_distance.append(distance_fun(datas[i], datas[j]))
            distance_map.append(tmp_distance)
        return distance_map
