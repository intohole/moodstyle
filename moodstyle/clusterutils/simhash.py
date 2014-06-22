# coding=gbk
#!/usr/bin/env python


from collections import defaultdict


class SimHash(object):

    __seg = None
    __word_hash = defaultdict()

    def __init__(self, segfun=None):
        self.__seg = segfun

    def figureprint(self, document):
        if document:
            if isinstance(document, (str, unicode)):
                words = self.__seg(document)
                wm = defaultdict(int)
                for word in words:
                    print word
                    if not self.__word_hash.has_key(word):
                        self.__word_hash[word] = self.hash(word)
                    wm[self.__word_hash[word]] += 1
                hash_arry = [0 for i in range(64)]
                for __hash , __weight in wm.items():
                    self.__array_add(hash_arry , self.__toarry(__hash , __weight))
                print hash_arry
                return self.__toint(hash_arry)

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
        if word:
            if isinstance(word, (str, unicode)):
                return hash(word)
        return None

    @staticmethod
    def distance(sh1 , sh2):
        h = sh1 ^ sh2
        d = 0
        while h:
            h = h & (h - 1)
            d += 1
        return d


if __name__ == '__main__':
    f = SimHash(lambda x : x.split())
    print f.figureprint('i have a box !') ^ f.figureprint('i have a cat !')
    print SimHash.distance(f.figureprint('i have a cat !')  , f.figureprint('i have a cat !'))
    # print f.hash('a')
