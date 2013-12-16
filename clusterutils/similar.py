#coding=utf-8

import math



  
def toVector(words1,words2):
    wordmap = {}
    wordVector1 = {}
    wordVector2 = {}
    for word in words1.split(" "):
        wordmap[word] = 1
        if wordVector1.has_key(word):
            wordVector1[word] = wordVector1[word] + 1
        else:
            wordVector1[word] = 1
    for word in words2.split(" "):
        wordmap[word] = 1
        if wordVector2.has_key(word):
            wordVector2[word] = wordVector2[word] + 1
        else:
            wordVector2[word] = 1
    return (wordmap,wordVector1,wordVector2)
  
  
  
def similar(words1,words2):
    '''
    计算两个文档 相似度
    '''
    _vector = toVector(words1, words2)
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
        sum_word12 = _w1 * _w2 + sum_word12 # x1*y1 + x2*y2 + ...+ xn*yn
        sum_word1_distance = _w1*_w1 + sum_word1_distance
        sum_word2_distance = _w2*_w2 + sum_word2_distance
        # x1*y1 + x2*y2 + ...+ xn*yn / sqrt(x1*x1 + x2*x2 + x3*x3 + ...+ xn*xn) * sqrt(y1*y1 + y2*y2 + y3*y3 + ... + yn*yn)
    _similar = sum_word12 / (math.sqrt(sum_word1_distance) * math.sqrt(sum_word2_distance))
    return _similar


if __name__ == "__main__":
    print similar("我 不 爱 他妈 哈 哈 哈", "我 爱 天安门 ming 哈 哈 哈")