#coding=utf-8


from DataSet import DataSet
from collections import Counter 
import copy


class Graph(object):


    def __init__(self , point_len , dense = True ):
        self.weights = [1.] * point_len
        self.data = DataSet(point_len , dense)
        for i in range(point_len):
            self.data.append()
        self._keys = xrange(point_len)
        self._len = point_len
        self.outs_counter = Counter() 
    
    def __len__(self):
        return self._len

    def add_edge(self , point_a , point_b):
        """添加point_a 指向 point_b
            param: point_a              图点a -> b 
            param: point_b              图被指向点
            return 
        """
        self.data[point_a][point_b] = 1
        self.outs_counter[point_a] += 1
   
    def keys(self):
        return self._keys

    def ins(self , point):
        """入链个数
        """
        if point and isinstance(point , (int , long)):
            if point >=  0 and point < self._len:
                for index in self.data.keys():
                    if self.data[index][point] > 0:
                        yield index 
                    

    def outs(self , point):
        if point and isinstance(point , (int , long)):
            if point >=  0 and point < self._len:
                for index in self.data[point].keys():
                    if self.data[point][index] > 0:
                        yield index 
    def outs_count(self , point):
        return self.outs_counter[point]

    def update(self , weights):
        if weights:
            for i in self.keys():
                self.weights[i] =  weights[i]

class PageRank(object):


    def __init__(self):
        pass


    def rank(self , graph ,iter_count = 1000, d = 0.85 , min_error = 0.001):
        for _ in xrange(iter_count):
            weights = copy.copy(graph.weights)
            for i in graph.keys():
                weights[i] =(1-d) + d * sum([ weights[point_in]/graph.outs_count(point_in) for point_in in graph.ins(i)]) 
            error = self.calc_error(weights ,graph ) 
            if error < min_error:
                break
            graph.update(weights)
        return copy.copy(graph.weights)
    
    def calc_error(self , weights , graph):
        return max(abs(weights[i] - graph.weights[i])  for i in graph.keys())

if __name__ == "__main__":
    graph = Graph(10)
    graph.add_edge(1 , 9)
    graph.add_edge(3 , 4)
    graph.add_edge(6 , 8)
    graph.add_edge(7 , 8)
    graph.add_edge(0,1)
    pagerank = PageRank()
    print pagerank.rank(graph )

