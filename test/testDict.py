#coding=utf-8




import collections 

class Dictionary(dict):

    def __init__(self , **kw):
        if "dict_path" in kw:
            self.open_dict(kw["dict_path"]) 
        elif "words" in kw:
            self.update({word:word_seq for word_seq , word in enumerate(kw["words"])})
            
    def open_dict(self , dict_path):
        with open(dict_path) as f:
            for seq , word in enumerate(f.readlines()):
                self[word] = seq
    
    def __setitem__(self ,key, value):
        if key and  key not in self: 
            value = len(self)
            super(Dictionary , self).__setitem__(key , value)



    def to_vector(self , words):
        word_counter = collections.Counter(words.split())
        vector = [0] * len(self)
        for word,count in word_counter.items():
            vector[self[word]] = count
        return vector
    
    def to_one_hot(self , words):
        words = set(words.split())
        vector = [0] * len(self)
        for word in words:
            vector[self[word]] = count 
        return vector


if __name__ == "__main__":
    d = Dictionary(words = ["a" , "b" ,"c"])
    d['c'] = 5
    d['d'] = 6
    print d.to_vector("b b a")

