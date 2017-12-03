#coding=utf-8    


from moodstyle.PageRank import PageRank
from moodstyle.PageRank import GraphV2

graph = GraphV2(10)
graph.add_edge(1 , 9)
graph.add_edge(3 , 4)
graph.add_edge(6 , 8)
graph.add_edge(7 , 8)
graph.add_edge(0,1)
pagerank = PageRank()
print pagerank.rank(graph )

