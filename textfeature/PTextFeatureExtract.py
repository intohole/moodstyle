#!/usr/bin/env python
# coding:utf-8


import math


class Document(object):

    """
    整个是一个封装的 dict{}
    分别为  word - > 分类类别 -> 词数目
    """

    def __init__(self):
        self.__doc = {}　#所有词的ｓｅｔ
        self.doc_count = 0  # 文档数目
        self.__type_count = {} #　ｗｏｒｄ　-> 分类类别　-> 数目

    def insert_document(self, doc_type, document={}):
        '''
        插入一个ｄｏｃ
        doc_type (str , unicode ) 分类名称
        document (set) 一个文档所含有不重复词
        抛出异常　TypeError 
        '''
        if not isinstance(document, (set, list)):
            raise TypeError, 'document  must is list or set'
        for word in document:
            self.__insert_doc_dict(doc_type, word)
        self.__insert_type_dict(doc_type)
        self.doc_count = self.doc_count + 1
    # 获得word在所有文档的总数量

    def get_word_count(self, word):
        '''
        获得一个词在所有分类中的数目
        word -> (str , unicode)

        '''
        if not (word and isinstance(word, (str, unicode))):
            raise TypeError, 'word must be is str or unicode : %s' % word
        count = 0
        if self.__doc.has_key(word):
            for _key, _val in self.__doc[word].items():
                count = count + _val
        return count

    def __insert_type_dict(self, doc_type):
        count = 1
        if self.__type_count.has_key(doc_type):
            count = self.__type_count[doc_type] + 1
        self.__type_count[doc_type] = count

    def get_type_word_count(self, doc_type, word):
        '''
        得到某个分类下　，　ｗｏｒｄ数目
        doc_type 分类名称
        word 词
        '''
        if self.__doc.has_key(word):
            if self.__doc[word].has_key(doc_type):
                return self.__doc[word][doc_type]
        return 0

    def __insert_doc_dict(self, doc_type, word):
        __value = 1
        if self.__doc.has_key(word):
            if self.__doc[word].has_key(doc_type):
                __value = self.__doc[word][doc_type] + 1
        else:
            self.__doc[word] = {}
        self.__doc[word][doc_type] = __value

    def get_doc_count(self, doc_type):
        '''
        某个分类的文档数目
        doc_type
        '''
        if doc_type and isinstance(doc_type , (str , unicode)):
            if self.__type_count.has_key(doc_type):
                return self.__type_count[doc_type]
        return 0

    def get_word_set(self):
        '''
        得到所有词的ｓｅｔ
        '''
        return self.__doc.keys()

    def get_type_set(self):
        '''
        得到所有分类类别
        '''
        return self.__type_count.keys()


class ITextFeatureScore(object):

    '''
    doc_word_count , 特定文档中出现该词的文档数目
    doc_count , 特定类别的文档数目
    word_count , 特定存在文档总数目
    doc_sum , 文档总数目
    功能： 计算 每个词的分值
    返回: double

    '''

    def feature_socre(self, doc_word_count, doc_count, word_count, doc_sum):
        raise NotImplementedError


# class IM(ITextFeatureScore):

#     def feature_socre(self, doc_word_count, doc_count, word_count, doc_sum):
# return math.log(float(doc_sum * doc_word_count) / float(doc_count *
# word_count))


class CreateDocument(object):
    doc = Document()

    def insert_document_list(self, doc_name, contents, word_term=1, word_split=' '):
        if doc_name and len(doc_name) > 0:
            if contents and isinstance(contents, (list, tuple)) and len(contents) > 0:
                for line in contents:
                    self.doc.insert_document(
                        doc_name, self.text_extract(line, word_term, word_split))
            else if isinstance(contents , (str , unicode)):
                self.doc.insert_document(doc_name , self.text_extract(lien , word_term , word_split))
            return
        raise TypeError, 'doc_name is string and contents is list or tuple which element is string or unicode!'
    # 提取句子的几元文法

    def text_extract(self, line, word_count=2,  word_split=' '):
        if line and isinstance(line, (str, unicode)):
            lineArry = [word.strip()
                        for word in line.split(word_split) if word.strip() != '']
            return [' '.join(lineArry[i: i + word_count]) for i in range(len(lineArry) - 1)]
        else:
            raise TypeError


class TextFeature(object):

    def __init__(self,  min_word_count=0, filter_rate=0.003):
        self.filter_rate = filter_rate
        self.min_word_count = min_word_count
        self.createdoc = CreateDocument()

    def extract_feature_from_contents(self, top_word=0.01):
        doc = self.createdoc.doc
        doc_word_score_map = {}  # 文档 ——》 词 ——》分值
        for doc_type in doc.get_type_set():  # 初始化 分值dict 这样不用下面判断
            doc_word_score_map[doc_type] = {}
        for word in doc.get_word_set():
            for doc_type in doc.get_type_set():
                word_count_doc = doc.get_type_word_count(doc_type, word)
                # 现在简单的滤除低词频
                if word_count_doc <= self.min_word_count or word_count_doc < long(doc.get_doc_count(doc_type) * self.filter_rate):

                    continue
                score = self.text_feature_score(doc.get_type_word_count(
                    doc_type, word), doc.get_doc_count(doc_type), doc.get_word_count(word), doc.doc_count)
                doc_word_score_map[doc_type][word] = score
        for doc_type, word_score in doc_word_score_map.items():  # 对所有按照分值大小排序
            sorted_x = sorted(
                word_score.iteritems(),  key=lambda x: x[1], reverse=True)
            get_top = len(sorted_x) * top_word
            doc_word_score_map[doc_type] = [word[0]
                                            for word in sorted_x][0:get_top]
        return doc_word_score_map

    def text_feature_score(self, doc_word_count, doc_count, word_count, doc_sum):
        '''
        子类必须要实现的方法  对每个打分
        '''
        pass


class IM(TextFeature):

    '''
    互信息 方法计算 ——》 香浓熵

    '''

    def text_feature_score(self, doc_word_count, doc_count, word_count, doc_sum):

        return math.log(float(doc_sum * doc_word_count) / float(doc_count * word_count), 2)


class CHI(TextFeature):

    def text_feature_score(self, doc_word_count, doc_count, word_count, doc_sum):
        __A = doc_word_count
        __B = word_count - doc_word_count
        __C = doc_count - doc_word_count
        __D = doc_sum - (word_count + doc_count - doc_word_count)
        return (float((__A * __D - __B * __C) * (__A * __D - __B * __C)) / float(word_count * (doc_sum - word_count)))


class DF(TextFeature):

    '''
    文档率 计算 ===》 简单理解就是一个 去除高词频
    去除低词频 算法简单
    '''
    MAX_FILTER = 0.006

    def text_feature_score(self, doc_word_count, doc_count, word_count, doc_sum):
        # 去除一定的高词频
        if float(doc_word_count) / float(doc_count) > self.MAX_FILTER:
            return 0.
        return float(doc_word_count) / float(doc_count)


class WLLR(TextFeature):

    def text_feature_score(self, doc_word_count, doc_count, word_count, doc_sum):
        if word_count == doc_word_count:
            # 如果这个词只存在这个文本类别中，而且高过一定词频 是否要认为这个词具有代表性呢？ 我实验了一下 确实可以代表
            # 但是我的文本类别真的具有可行性吗 这里应该是多少 1 or 0
            return 1.
        __A = float(doc_word_count) / float(doc_count)
        __B = math.log(float(doc_word_count * (doc_sum - doc_count))
                       / float((word_count - doc_word_count) * doc_count))
        return __A * __B


class IG(TextFeature):
    # 信息增益

    pass


