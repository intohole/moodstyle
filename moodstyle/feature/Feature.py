#coding=utf-8



import bisect


class Binning(object):
   
    def __init__(self,k,box = None):
        self.k = k
        if box is None:
            self._box = [0.] * (k - 1)
        elif isinstance(box,(list),tuple):
            if len(box) != self.k - 1:
                raise ValueError("input box number not equal k, please recheck")
            self._box = box
 
   
    def train(self,features):
        pass
    

    def predict(self,feature):
        if feature is None:
            raise TypeError
        return bisect.bisect(self._box,feature) 

    
    def _sort(self,array):
        return sorted(array,reversed = False)



class EqualRate(Binning):
    
    
    def train(self,features):
        features = self._sort(features)
        for i in range(0,len(features),len(features) / self.k):
            pass

class EqualLength(Binning):
    """equal length excute feature
       
        >>> f = EqualLength(5)
        >>> from random import randint
        >>> array = [randint(0,100000) for i in range(10000)]
        >>> f.train(array) 
        >>> f.predict(899)
        0
    """ 
    
    def train(self,features):
        min_value = min(features)
        max_value = max(features)
        length = (max_value - min_value) / self.k
        for i in range(self.k - 1):
            self._box[i] = min_value + length * (i + 1)        
