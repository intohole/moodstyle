#coding=utf-8
import math
from collections import defaultdict


class Document(object):

    """文本属性统计文档与词的统计关系，主要为了提取文本特征使用
    """

    def __init__(self):
        self._word_class_count = defaultdict(lambda : defaultdict(int))  # word -> 分类 ->次数
        self.doc_count = 0  # 文档数目
        self._class_count = defaultdict(int) # 每个类别数目

    def insert_document(self, doc_type, document= []):
        """添加训练文档
            params:
                doc_type    文本分类名称
                document    文档词集合 
            return
                False   如果文档词为空，则返回False
                True
        """       
        if isinstance(document, (set, list)) is False:
            raise TypeError, 'document  must is list or set'
        if len(document) == 0:
            return False
        for word in document:
            if word:
                self._word_class_count[word][doc_type] += 1
        self._class_count[doc_type] += 1
        self.doc_count += 1
        return True
    # 获得word在所有文档的总数量

    def get_word_count(self, word):
        '''
        获得一个词在所有分类中的数目
        word -> (str , unicode)

        '''
        if word and isinstance(word , basestring):
            return sum(value for value in self._word_class_count[word].values())
        return 1 


    def get_type_word_count(self, doc_type, word):
        '''
        得到某个分类下　，　ｗｏｒｄ数目
        doc_type 分类名称
        word 词
        '''
        return self._word_class_count[word][doc_type]


    def get_doc_count(self, doc_type):
        '''
        某个分类的文档数目
        doc_type
        '''
        return self._class_count[doc_type]


    def get_word_set(self):
        '''
        得到所有词的ｓｅｔ
        '''
        return self._word_class_count.keys()

    def get_type_set(self):
        '''
        得到所有分类类别
        '''
        return self._class_count.keys()


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





class CreateDocument(object):
    doc = Document()

    def insert_document_list(self, doc_name, contents, word_term=1, word_split=' '):
        if doc_name and len(doc_name) > 0:
            if contents and isinstance(contents, (list, tuple)) and len(contents) > 0:
                for line in contents:
                    self.doc.insert_document(
                        doc_name, self.text_extract(line, word_term, word_split))
            elif isinstance(contents, (str, unicode)):
                self.doc.insert_document(
                    doc_name, self.text_extract(line, word_term, word_split))
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

    def __init__(self, min_word_count=0, filter_rate=0.003):
        self.filter_rate = filter_rate
        self.min_word_count = min_word_count

    def extract_feature(self, doc, top_word=0.01):
        """从文档统计集合中，抽取文本特征
            params: 
                doc 文本统计信息集合 Document类
                top_word    抽取文本特征词比例
            return
                文档分类 文档分类词集合
        """
        doc_word_score_map = defaultdict(
            lambda: defaultdict(float))  # 文档 -> 词 -> 分值
        for word in doc.get_word_set():
            for doc_type in doc.get_type_set():
                if self.filter(doc , doc_type , word):
                    continue
                score = self.text_feature_score(
                    doc.get_type_word_count(doc_type, word),
                    doc.get_doc_count(doc_type),
                    doc.get_word_count(word),
                    doc.doc_count
                )
                doc_word_score_map[doc_type][word] = score
        # 对所有按照分值大小排序
        for doc_type, word_score in doc_word_score_map.items():  
            sorted_doc_word_by_score = sorted(
                word_score.items(),  key=lambda x: x[1], reverse=True)
            get_top = len(sorted_doc_word_by_score) * top_word
            yield doc_type , [word[0]   for word in sorted_doc_word_by_score][0:int(get_top)]


    def text_feature_score(self, doc_word_count, doc_count, word_count, doc_sum):
        '''
        子类必须要实现的方法  对每个打分
        params:
            doc_word_count  存在特定词并同时为特定类别文档数目
            doc_count   属于特定类别文档总数
            word_count  特定词总数
            doc_sum     文档总数
        '''
        raise NotImplementedError

    def filter(self, doc , doc_type , word):
        word_count_doc = doc.get_type_word_count(doc_type, word)
        return word_count_doc <= self.min_word_count or word_count_doc < long(doc.get_doc_count(doc_type) * self.filter_rate)


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
