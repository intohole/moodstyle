#coding=utf-8


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

    def __init__(self , data , data_range  ,  default_value  ,  data_len  , *argv , **kw):
        if isinstance(data , (list , tuple)) and len(data) == data_len:
            self.extend(data)
        elif isinstance(data , dict):
            for i in xrange(data_len):
                self.append(default_value)
            for i , value in data:
                self[i] = value 
        self._data_len = data_len 
        self._data_range = data_range

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
        return self.data_len 

class DataSet(DList):


    def __init__(self ,data_len, dense_data , *argv , **kw):
        super(DataSet , self).__init__(*argv , **kw)
        self._type = dense_data
        self._data_len = data_len  
        self._data_class = DeseData if dense_data else SparseData 
        self._range = xrange(self._data_len)

    def append(self , data):
        if isinstance(data , (list , tuple , dict)) :
            super(DataSet , self).append(self._data_class(data ,-1 , self._data_len ))
            return True
        else:
            raise TypeError
         
    def extend(self , data):
        if isinstance(data , DataSet):
            if data._data_len == self._data_len and data._type == self._type:
                super(DataSet , self).extend(data)
            else:
                raise ValueError
            return 
        raise TypeError
   
    
if __name__ == "__main__":
    d1 = DataSet(10 , False )
    d1.append({1 : "1" , 2:"3"})
    for d in d1:
        for i , value in d.items():
            print  i ,value
    d2 = DataSet(10 , False)
    d2.extend(d1)
    print d2
