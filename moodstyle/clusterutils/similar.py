# coding=utf-8

import math

from collections import defaultdict
from collections import Counter


def toVector(words):
    vector = defaultdict(int)
    for word in words:
        vector[word] += 1
    return vector


def similar(document1, document2, split_fun=lambda x: x.split()):
    '''
    计算两个文档 相似度
    通过余弦相似度　，　将句子构造成两个向量　，　通过计算向量之间的夹角　，　
    得到两句相似度　
    '''
    vector1 = toVector(split_fun(document1))
    vector2 = toVector(split_fun(document2))
    words_bag = []
    words_bag.extend(vector1.keys())
    words_bag.extend(vector2.keys())
    words_bag = set(words_bag)
    sum_word12 = 0
    sum_word1_distance = 0
    sum_word2_distance = 0
    for word in words_bag:
        w1 = vector1[word] if vector1.has_key(word) else 0
        w2 = vector2[word] if vector1.has_key(word) else 0
        sum_word12 = w1 * w2 + sum_word12  # x1*y1 + x2*y2 + ...+ xn*yn
        sum_word1_distance = w1 * w1 + sum_word1_distance
        sum_word2_distance = w2 * w2 + sum_word2_distance
        # x1*y1 + x2*y2 + ...+ xn*yn / sqrt(x1*x1 + x2*x2 + x3*x3 + ...+ xn*xn) * sqrt(y1*y1 + y2*y2 + y3*y3 + ... + yn*yn)
    return sum_word12 / \
        (math.sqrt(sum_word1_distance) * math.sqrt(sum_word2_distance))


def consine(sentence1, sentence2, split_function=lambda x: x.split()):
    vector1 = sentence_to_vector(sentence1, split_function)
    vector2 = sentence_to_vector(sentence2, split_function)
    words_bag = set(vector2.keys()) & set(vector2.keys())
    __up = sum([vector1[x] * vector2[x] for x in words_bag])
    __down = math.sqrt(sum([ vector1[word] ** 2 for word in vector1.keys()] ) ) * \
        math.sqrt(sum([vector2[word] ** 2 for word in vector2.keys()]))
    return float(__up) / __down


def sentence_to_vector(sentence, split_function):
    return Counter(split_function(sentence))

if __name__ == "__main__":
    import time
    print time.time()
    for i in range(5000):
        consine("我 不 爱 他妈 哈 哈 哈", "我 爱 天安门 ming 哈 哈 哈")
    print time.time()
    for i in range(5000):
        similar("我 不 爱 他妈 哈 哈 哈", "我 爱 天安门 ming 哈 哈 哈")
    print time.time()
