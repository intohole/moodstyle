# coding=utf-8

import math

from collections import defaultdict


def toVector(words1, words2 , split_word ):
    '''

    '''
    wordmap = {}
    wordVector1 = defaultdict(int)
    wordVector2 = defaultdict(int)
    for word in words1.split(split_word):
        wordmap[word] = 1
        wordVector1[word] += 1
    for word in words2.split(split_word):
        wordmap[word] = 1
        wordVector2[word] += 1
    return (wordmap, wordVector1, wordVector2)


def similar(words1, words2　,split_word = ' '):
    '''
    计算两个文档 相似度
    通过余弦相似度　，　将句子构造成两个向量　，　通过计算向量之间的夹角　，　
    得到两句相似度　
    '''
    _vector = toVector(words1, words2 , split_word)
    sum_word12 = 0
    sum_word1_distance = 0
    sum_word2_distance = 0
    for _word in _vector[0].keys():
        _w1 = 0
        _w2 = 0
        if _vector[1].has_key(_word):
            _w1 = _vector[1][_word]
        if _vector[2].has_key(_word):
            _w2 = _vector[2][_word]
        sum_word12 = _w1 * _w2 + sum_word12  # x1*y1 + x2*y2 + ...+ xn*yn
        sum_word1_distance = _w1 * _w1 + sum_word1_distance
        sum_word2_distance = _w2 * _w2 + sum_word2_distance
        # x1*y1 + x2*y2 + ...+ xn*yn / sqrt(x1*x1 + x2*x2 + x3*x3 + ...+ xn*xn) * sqrt(y1*y1 + y2*y2 + y3*y3 + ... + yn*yn)
    __similar = sum_word12 / \
        (math.sqrt(sum_word1_distance) * math.sqrt(sum_word2_distance))
    return __similar


if __name__ == "__main__":
    print similar("我 不 爱 他妈 哈 哈 哈", "我 爱 天安门 ming 哈 哈 哈")
