# coding=gbk
#!/usr/bin/env python

from moodstyle.textfeature.PTextFeatureExtract import IM
from moodstyle.textfeature.PTextFeatureExtract import Document
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class CreateDoc(object):

    __split = re.compile(ur'[^\u4e00-\u9fa5]+').split
    doc = Document()

    def __init__(self, min_split=1, max_split=5):
        self.__min_split = min_split
        self.__max_split = max_split

    def insert_doc(self, type_name, content):
        if type_name and content:
            if isinstance(content, (str, unicode)):
                if not isinstance(content, unicode):
                    try:
                        content = content.decode('utf-8')
                    except Exception , e:
                        print e
                        return 
                content = self.__split(content)

            elif not isinstance(content, (str, unicode)):
                raise TypeError, 'content is list or string'
            items = []
            for line in content:
                if line and len(line):
                    for __i in range(self.__min_split, self.__max_split):
                        items.extend(self.__gram(line, __i))
            self.doc.insert_document(type_name, items)

    def __gram(self, line, split_num):
        if line:
            if not isinstance(line, unicode):
                line = line.decode('utf-8')
            return [line[i:i + split_num] for i in range(len(line) - split_num + 1)]


if __name__ == '__main__':
    import os
    root = '/home/lixuze/Data/ClassFile'
    create = CreateDoc(min_split = 2 , max_split = 4)
    count = 1
    for d in os.listdir(root):
        if count >= 9000:
            break

        for f in os.listdir('%s/%s' % (root, d)):
            with open('%s/%s/%s' % (root, d, f)) as f:
                create.insert_doc(
                    d, ''.join([line.strip() for line in f.readlines()]))
            if count % 4500 == 0:
                count = count + 1
                break
            count = count + 1
            print count


    im = IM(filter_rate = 0.004)
    sc = im.extract_feature(create.doc)
    for __key, __val in sc.items():
        f = open('/home/lixuze/%s' % __key, 'w')
        for __word in __val:
            f.write(__word + '\n')
        f.close()
