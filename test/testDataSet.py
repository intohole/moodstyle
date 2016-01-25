#coding=utf-8


class DList(List):

    def items(self):
        return enumerate(self) 


class DeseData(DList):
    pass 

class SparseData(dict):

    def __init__(self ,data , default_value , data_len , *argv , **kw)
        super(SparseData , self).__init__(*argv , **kw)
        self._default = default_value
        self.data_len = data_len 
        self.update(data)    
         
    def __getitem__(self , index ):
        if index in self:
            return self[index]
        else:
            return self._default

    def __setitem__(self , index , value):
        if index:
            if index < self.data_len:
                super(SparseData , self).__setitem__(index , value )
            else:
                raise IndexError
        else:
            raise ValueError

    def __len__(self):
        return data_len 

class DataSet(DList):


    def __init__(self ,data_len, dense_data , *argv , **kw):
        super(DataSet , list).__init__(*argv , **kw)
        self._type = dense_data
        self._data_len = data_len  
        self._data_class = DeseData if dense_data else SparseData 

    def append(self , data):
        if isinstance(data , (list , tuple)) and self._type:
            
        elif isinstance(data , dict):
            pass
        else:
            raise TypeError
        super(DataSet , self).append(self._data_class(data , ))
    
    def extrend(self , data):
        if isinstance(data , DataSet):
            if len(data) == len(self):
                super(DataSet , self).extrend(data)
