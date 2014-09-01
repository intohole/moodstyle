# coding=utf-8
#!/usr/bin/env python


from collections import defaultdict


class SimHash(object):
    '''
    simhash 海明距离计算
    词——》 hash
    数字权重计算
    逐位计算
    取反取距离
    '''

    __seg = None #分词藉口
    __word_hash = defaultdict() #word——hash 保存

    def __init__(self, segfun=None):
        self.__seg = segfun

    def figureprint(self, document):
        '''
        计算海明编码
        '''
        if document:
            if isinstance(document, (str, unicode)):
                words = self.__seg(document) #
                wm = defaultdict(int) #词hash->出现次数
                for word in words: #循环分词
                    if not self.__word_hash.has_key(word):
                        self.__word_hash[word] = self.hash(word)
                    wm[self.__word_hash[word]] += 1
                hash_arry = [0 for i in range(64)] #所有ｈａｓｈ值相加减数组
                for __hash , __weight in wm.items():#循环数组　权重
                    self.__array_add(hash_arry , self.__toarry(__hash , __weight))
                return self.__toint(hash_arry) #转换为数字

    def __toint(self , hash_arry):
        __h = 0 
        for i in range(len(hash_arry)):
            if hash_arry[i] > 0:
                __h += (1 << i)
        return __h


    def __array_add(self, arry1, arry2):
        for i in range(len(arry1)):
            arry1[i] += arry2[i]


    def __toarry(self, h, weight):
        __hash = [(h >> i) & 1 for i in range(64)]
        for i in range(64):
            if __hash[i]:
                __hash[i] = weight
            else:
                __hash[i] = -1 * weight
        return __hash

    def hash(self, word):
        '''
        对字符串ｈａｓｈ作用

        '''
        if word:
            if isinstance(word, (str, unicode)):
                return hash(word)
        return None

    @staticmethod
    def distance(sh1 , sh2):
        if not (isinstance(sh1 , int ) and isinstance(sh2 , int)):
            raise TypeError , '参数必须为整数 !'
        h = (sh1 ^ sh2 ) & ( 1 << 64 - 1)
        d = 0
        while h:
            h = h & (h - 1)
            d += 1
        return d


if __name__ == '__main__':
    f = SimHash(lambda x : x.split())
    print f.figureprint('hello')
    print f.figureprint('i have a box !') ^ f.figureprint('i have a cat !')
    print f.figureprint('he have cat')
    print f.figureprint('i have a cat !')
    print SimHash.distance(f.figureprint('he have cat !')  , f.figureprint('i have a cat !'))
    print f.hash('a')
