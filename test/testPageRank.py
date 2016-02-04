#coding=utf-8


from testDataSet import DataSet

class Graph(object):


    def __init__(self , point_len ):
        self.weights = [1.] * point_len
        self.data = DataSet(point_len , True)
        for i in range(point_len):
            self.data.append()
        self._keys = xrange(point_len)
        self._len = point_len
    
    def __len__(self):
        return self._len

    def add_edge(self , point_a , point_b):
        """添加point_a 指向 point_b
            param: point_a              图点a -> b 
            param: point_b              图被指向点
            return 
        """
        self.data[point_a][point_b] = 1
   
    def keys(self):
        return self._keys

    def in(self , point):
        if point and isinstance(point , (int , long)):
            if point >=  0 and point < self._len:
                return self.data[point].keys()
    def out(self , point):
        if point and isinstance(point , (int , long)):
            if point >=  0 and point < self._len:
                return for i in self.keys():

class PageRank(object):


    def __init__(self):
        pass


    def rank(self , graph ):
        for i in keys 

if __name__ == "__main__":
    graph = Graph(10)
    graph.add_edge(1 , 9)


