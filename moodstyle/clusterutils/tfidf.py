# coding=utf-8

import math
from collections import defaultdict


def tf(words , splitword=' '):
    '''
    tf = 文章中词数 / 文章总词数
    '''
    max_count = 0.
    word_count = defaultdict(float)
    for word in words.split(split_word):
        word_count[word] += 1.0
        if word_count[word] > max_count:
            max_count = word_count[word]
    if len(word_count):
        for word in word_count.keyset():
            word_count[word] /= max_count
    return word_count

   


def idf(wordslist , splitword=''):
    '''
    idf(逆文档率) = log(总文档数 / （该词所在文档数目 + 1）) 
    '''
    _doc = {} 
    #循环文档-》计算每个词 被多少文档包含
    for _words in wordslist:
        _tmpdoc = {}
        for _word in _words.split(splitword):
            _tmpdoc[_word] = 1
        for _key, _val in _tmpdoc.items():
            if _doc.has_key(_key):
                _doc[_key] = _doc[_key] + 1
                continue
            _doc[_key] = 1
    _idf = {}
    _docnum = len(wordslist)
    for _key, _val in _doc.items():
        _idf[_val] = math.log(float(_docnum) / float(_val + 1))
    return _idf



def tf_idf(words , idfdict , splitword):
    _tf = tf(words, splitword)
    _ti = {}
    for word in words.split():
        if idfdict.has_key(word):
            _ti [word] = _tf[word] * idfdict[word]
    return _ti

                
        
    
