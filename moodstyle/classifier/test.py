# coding=utf-8
#!/usr/bin/env python

from moodstyle.textfeature.PTextFeatureExtract import IM
from moodstyle.textfeature.PTextFeatureExtract import Document
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CreateDoc(object):

    __split = re.compile('[\\s]+').split
    doc = Document()

    def __init__(self, min_split=1, max_split=5):
        self.__min_split = min_split
        self.__max_split = max_split

    def insert_doc(self, type_name, content):
        if type_name and content:
            if isinstance(content, (str, unicode)):
                content = self.__split(content)
            elif not isinstance(content, (str, unicode)):
                raise TypeError, 'content is list or string'
            items = []
            for line in content:
                for __i in range(self.__min_split, self.__max_split):
                    items.extend(self.__gram(line , __i))
            self.doc.insert_document(type_name , items)

    def __gram(self, line, split_num):
        if line:
            # if not isinstance(line, unicode):
            #     line = line.decode('utf-8')
            return [line[i:i + split_num] for i in range(len(line) - split_num + 1)]


if __name__ == '__main__':
    import os
    root = '/home/lixuze/Data/ClassFile'
    create = CreateDoc()
    count = 1
    for d in os.listdir(root):
        for f in os.listdir('%s/%s' % (root , d)):
            with open('%s/%s/%s' % (root , d , f)) as f:
                create.insert_doc(d ,''.join([line.strip() for line in f.readlines()]))
            if count % 100 == 0 :
                break
            count = count + 1
    im = IM()
    sc = im.extract_feature(create.doc)
    for __key , __val in sc.items():
        print __key 
        for __word in __val:
            print __word


