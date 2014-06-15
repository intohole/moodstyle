# coding=utf-8
#!/usr/bin/env python


'''
Wi <- Wi + change Wi
z = w1 * x1 + w2 * x2 + b

'''

from math import exp
from random import randint
from random import random

a = [1, 1 , 1 ]
step = 0.1


def sigmod(x):
    return 1 / (1 + exp(x))

def cal1(x1 , x2):
    global a
    z =1 / (1 + exp( -(a[0] * x1 + a[1] * x2 ) ) )
    if z > 0.5 :
        return 1
    else:
        return 0

def update(x1, x2, label):
    global a
    z = cal1(x1 , x2)
    a[0] = a[0] + step * (- z + label) * x1
    a[1] = a[1] + step * (- z +label) * x2

def cal(x1 , x2):
    return x1 * a[0] + x2 * a[1] + a[2]
    


for i in range(2000000):
    if i % 2 == 0:
        update(-random() * 10, - random() * 10, 0)
        update(-random() * 10,  random() * 10, 0)
    else:
        update(random() * 10, random() * 10, 1)
        update(random() * 10, -random() * 10, 1)
print a
print cal1(-0.5 , 1)
print cal1(200 ,100)
print cal1(1000 , 2000)
print cal1(4500,-4500)
