# coding=utf-8

import math
import numpy as np
from scipy.sparse import csc_matrix


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


 
def pageRank(G, s = .85, maxerr = .001):
    """
    Computes the pagerank for each of the n states.
 
    Used in webpage ranking and text summarization using unweighted
    or weighted transitions respectively.
 
 
    Args
    ----------
    G: matrix representing state transitions
       Gij can be a boolean or non negative real number representing the
       transition weight from state i to j.
 
    Kwargs
    ----------
    s: probability of following a transition. 1-s probability of teleporting
       to another state. Defaults to 0.85
 
    maxerr: if the sum of pageranks between iterations is bellow this we will
            have converged. Defaults to 0.001
    """
    n = G.shape[0]
 
    # transform G into markov matrix M
    M = csc_matrix(G,dtype=np.float)
    rsums = np.array(M.sum(1))[:,0]
    ri, ci = M.nonzero()
    M.data /= rsums[ri]
 
    # bool array of sink states
    sink = rsums==0
 
    # Compute pagerank r until we converge
    ro, r = np.zeros(n), np.ones(n)
    while np.sum(np.abs(r-ro)) > maxerr:
        ro = r.copy()
        # calculate each pagerank at a time
        for i in xrange(0,n):
            # inlinks of state i
            Ii = np.array(M[:,i].todense())[:,0]
            # account for sink states
            Si = sink / float(n)
            # account for teleportation to state i
            Ti = np.ones(n) / float(n)
 
            r[i] = ro.dot( Ii*s + Si*s + Ti*(1-s) )
 
    # return normalized pagerank
    return r/sum(r)
 
 
 
 
if __name__=='__main__':
    # Example extracted from 'Introduction to Information Retrieval'
    G = np.array([[0,0,1,0,0,0,0],
                  [0,1,1,0,0,0,0],
                  [1,0,1,1,0,0,0],
                  [0,0,0,1,1,0,0],
                  [0,0,0,0,0,0,1],
                  [0,0,0,0,0,1,1],
                  [0,0,0,1,1,0,1]])
 
    print pageRank(G,s=.86)
        
                
        
    
