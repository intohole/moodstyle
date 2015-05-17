#coding=utf-8




class LinerModel(object):





    def train(self , datas , labels , item_len , learn_rate ):
        self.weights = [1.] *  item_len
        self.offset = 1.  
        for i in range(len(labels)):
            l = self.predict(datas[i])
            self.update_weight( l , labels[i] , datas[i] , learn_rate)



    def update_weight(self , l , target , data , learn_rate):
        for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] - learn_rate *(l - target) * data[i]
        self.offset = self.offset - learn_rate * (l - target)



    def predict(self , data):
        if data and len(data) == len(self.weights):
            return sum([ data[i] *self.weights[i]  for i in range(len(self.weights))]) + self.offset


if __name__ == '__main__':
    l = LinerModel()
    from random import random
    datas = [ [random() * 10 ] for i in range(10000)]
    labels = [ 1 if data[0] >= 5 else 0 for data in  datas]
    l.train(datas , labels , 1 , 0.01)
    print l.weights
    print l.offset
    print l.predict([6.])