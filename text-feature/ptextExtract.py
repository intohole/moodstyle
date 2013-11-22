# coding=utf-8
#!/usr/bin/env python


class DF(object):

    def __init__(self):
        self.doc_word_num = {}
        self.doc_num = 0
        self.word_set = {}
        self.min_filter = 0.00001
        self.max_filter = 0.005

    def insert_word(self, doctype, word_list={}):
        for word in word_list:
            if not self.doc_word_num.has_key(doctype):
                self.doc_word_num[doctype] = {}
            if not self.doc_word_num[doctype].has_key(word):
                self.doc_word_num[doctype][word] = 1
            self.doc_word_num[doctype][
                word] = self.doc_word_num[doctype][word] + 1
        self.doc_num = self.doc_num + 1


    def extact_df(self, doc_word_num, doc_num, min_filter):
        if not isinstance(doc_word_num, dict):
            raise TypeError
        word_doc_df = {}
        for doctype in doc_word_num.keyset():
            word_doc_df[doctype] = {}
        for doctype, word_num in doc_word_num.items():
            for word, times in word_num.items():
                df_score = float(times) / float(doc_num)
                if df_score < min_filter:
                    continue
                word_doc_df[doctype][word] = df_score
        return word_doc_df

    def filter(self,word_set ,word_doc_df, max_filter):
    	doc_type_list = [doctype for doctype in word_doc_df.keyset()]
    	for word in word_set:
    		word_df = [ 0 for _ in range(len(doc_type_list))]
    		for i in range(len(doc_type_list)):
    			df = 0.
    			if word_doc_df[doc_type_list[i]].has_key[word]:
    				df = word_doc_df[doc_type_list[i]][word]
    			word_df[i] = df
    		max_count = 0 
    		for df in word_df:
    			if df > max_filter:
    				max_count = max_count + 1
    		if max_count >= 2:
    			for doctype in word_doc_df.keyset():
    				if word_doc_df[doctype].has_key(word):
    					del word_doc_df[doctype][word]
    	return word_doc_df

    def parser(self , doc):
    	raise NotImplementedError

    def get_text_feature(self , docs = []):
    	for doc in docs:
    		doctype , word_set = self.parser(doc)
    		self.insert_word(doctype , word_set)

    	word_doc_df = self.extact_df(self.doc_word_num , self.doc_num , self.min_filter)
    	self.filter(self.word_set , self.word_doc_df , self.max_filter)





if __name__ == '__main__':
    pass
