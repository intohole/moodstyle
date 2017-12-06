#coding=utf-8





from moodstyle.alg import Bandit
import random



N = 100 
# 随机生成N个概率
p = [random.random() for i in range(N)]

# 0.1 进行explor 
greedy = Bandit.Greedy(0.05,N)
# 重复实验次数
TIMES = 100000
COUNT = 0
for _ in range(TIMES):
    index = greedy.getIndex()          
    prop = random.random()
    if prop <= p[index]:
        label = 1 
        COUNT += 1
    else:
        label = 0
    greedy.process(label)
print greedy.p
print p
print COUNT / float(TIMES)
 
