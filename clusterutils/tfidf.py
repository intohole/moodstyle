# coding=utf-8

import math



def tf(words , splitword=' '):
    '''
    tf = 文章中词数 / 文章总词数
    '''
    word = {}
    _count = 0
    for _w in words.split(splitword):
        _count = _count + 1
        if word.has_key(_w):
            word[_w] = word[_w] + 1
            continue
        word[_w] = 1 
    _tf = {}
    for _key, _val in word.items():
        _tf[_key] = float(_val) / float(_count)


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
    
        
                
        
    

if __name__ == "__main__":
    print tf("")
