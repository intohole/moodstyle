#coding=utf-8


__ALL__ = ["DList" , "DenseData" , "SparseData" , "DataSet"] 

class DList(list):

    def items(self):
        return enumerate(self) 

    def has_key(self , value):
        if value and isinstance(value , (int , long)):
            if value > 0 and value < len(self):
                return True
            return False
        raise TypeError
    
    def update(self , data):
        if data and hasattr(data , "items"):
            for index , value in data.items():
                if index > len(self):
                    self.append(value)
                else:
                    self[index] = value  
        elif data and isinstance(data , (list , tuple)):
            for index , value in enumerate(data):
                if index > len(self):
                    self[index] = value
                
    def keys(self):
        return xrange(self._data_len)

    def values(self):
        return self



class DeseData(DList):

    def __init__(self , data  ,  default_value  ,  data_len  , *argv , **kw):
        if data is None:
            for i in xrange(data_len):
                self.append(default_value)
        elif isinstance(data , (list , tuple)) and len(data) == data_len:
            self.extend(data)
        elif isinstance(data , dict):
            for i in xrange(data_len):
                self.append(data.get( i , default_value))
        self._data_len = data_len 

    def __len__(self):
        return self._data_len
    
    def __setitem__(self , index , value ):
        if index  and index < self._data_len:
            super(DeseData , self).__setitem__(index , value)
        else:
            raise IndexError
    
class SparseData(dict):

    def __init__(self ,data , default_value , data_len , *argv , **kw):
        super(SparseData , self).__init__(*argv , **kw)
        self._default = default_value
        self.data_len = data_len 
        if data is not None:
            self.update(data)    
         
    def __getitem__(self , index ):
        return super(SparseData , self).__getitem__(index) if index in self else self._default

    def __setitem__(self , index , value):
        if index:
            if index < self.data_len:
                super(SparseData , self).__setitem__(index , value )
            else:
                raise IndexError
        else:
            raise ValueError

    def __len__(self):
        return self.data_len 

class DataSet(DList):
    """实现稀疏/非稀疏矩阵保存结构
    """

    def __init__(self ,data_len, dense_data , *argv , **kw):
        """初始化矩阵
            params:
                data_len                矩阵维数
                dense_data              是否为稀疏矩阵
            return 
                None
            raise 
                None 
        """
        super(DataSet , self).__init__(*argv , **kw)
        self._type = dense_data
        self._data_len = data_len  
        self._data_class = DeseData if dense_data is False else SparseData 
        self._range = xrange(self._data_len)

    def append(self , data = None):
        """增加数据
            params:
                data                需要增加的数据;类型：tuple,list,dict
            return
                True
            raise:
                data                类型不符合需求，抛出TypeError
        """
        if data is None or isinstance(data , (list , tuple , dict)) :
            super(DataSet , self).append(self._data_class(data ,-1 , self._data_len ))
            return True
        else:
            raise TypeError
         
    def extend(self , data):
        """增加同类型数据
        """
        if isinstance(data , DataSet):
            if data._data_len == self._data_len and data._type == self._type:
                super(DataSet , self).extend(data)
            else:
                raise ValueError
            return 
        raise TypeError
    

    def shape(self):
        return len(self) , self._data_len
   
    def data_range(self):
        return self._range

if __name__ == "__main__":
    d1 = DataSet(10 , False )
    d1.append({1 : "1" , 2:"3"})
    for d in d1:
        for i , value in d.items():
            print  i ,value
    d2 = DataSet(10 , False)
    d2.extend(d1)
    print d2
