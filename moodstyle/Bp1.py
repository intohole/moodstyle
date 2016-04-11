#coding=utf-8

import math
import random


class Neroun(object):


    def __init__(self , weight_len , learn_rate = 0.1 , delta = random.uniform(1 , -1)):
        self.weights = self.init_weights(weight_len)                
        self.delta = delta  
        self.weight_len = weight_len
        self.weight_range = xrange(weight_len)
        self.learn_rate = learn_rate 

    def init_weights(self , weight_len  , weight_max = 0.5 , weight_min = -0.5):
        return [ random.uniform(weight_max , weight_min) for i in range(weight_len)]

    def predict(self , inputs):
        return self.simgod( sum( value * weight for value , weight in zip(inputs ,self.weights)) + self.delta)            

    def simgod(self , value):
        return 1. / ( 1 + math.exp(-value))
    
    def disgod(self , target):
        return target * (1 - target)
    
    def __len__(self):
        return self.weight_len 

    def __getitem__(self , index):
        return self.weights[index]

    def __setitem__(self , index , value):
        self.weights[index] = self.weights[index] + self.learn_rate * value 

    def update(self , target, predict):
        error = target - predict
        for i in self.weight_range:
            self.weights[i] += self.rate * error
        return error 

class Layer(object):



    def __init__(self , inputs_len ,neroun_len , learn_rate = 0.1):
        """神经元层初始化
            params:
                inputs_len                  神经元输入数目
                neroun_len                  神经元个数
                learn_rate                  学习率 
            return
                None 
            raise 
                None
        """
        self.nerouns = [ Neroun(inputs_len , learn_rate = learn_rate)  for i in range(neroun_len)]
        self.nerouns_len = neroun_len 
        self.nerouns_range = xrange(self.nerouns_len)
        self.output = [ 0.] * self.nerouns_len

    def predict(self , inputs ):
        return [self.nerouns[i].predict(inputs) for i in self.nerouns_range ]
    
    def train_predict(self , inputs):
        for i in self.nerouns_range:
            self.output[i] = self.nerouns[i].predict(inputs)
        return self.output[:]

    def update(self , deltas):
        for i in self.nerouns_range:
            for j in xrange(len(self.nerouns[i])):
                self.nerouns[i][j] = deltas[i]

    def get_delta(self ,errors):
        raise NotImplemetion 

class OutPutLayer(Layer):

    def get_delta(self , errors ):
        return [self.output[i] * (1 - self.output[i]) * errors[i] for i in self.nerouns_range ]

class HiddenLayer(Layer):
    
    def __init__(self , inputs_len ,neroun_len  , next_layer, learn_rate = 0.1):
        super(HiddenLayer  , self).__init__(inputs_len ,neroun_len , learn_rate)
        self.next_layer = next_layer

    def get_delta(self , errors ):
        delta = [0.] * self.nerouns_len 
        for i in self.nerouns_range:
            error = sum( errors[j] * self.next_layer.nerouns[j][i] for j in self.next_layer.nerouns_range)
            delta[i] = self.output[i] * (1 - self.output[i])*error 
        return delta

class Bp(object):



    def __init__(self , inputs_len , hidden_len , outputs_len):
        self.input_layer_len = inputs_len
        self.hidden_layer_len = hidden_len 
        self.output_layer_len = outputs_len
        self.output_layer = OutPutLayer(hidden_len , outputs_len)
        self.hidden_layer = HiddenLayer(inputs_len , hidden_len , self.output_layer)

    
    def predict(self , inputs):
        if len(inputs)  != self.input_layer_len:
            raise Exception 
        hidden_outputs = self.hidden_layer.predict(inputs)
        outputs = self.output_layer.predict(hidden_outputs)
        return outputs
    
    def _train_predict(self , inputs):
        if len(inputs)  != self.input_layer_len:
            raise Exception 
        hidden_outputs = self.hidden_layer.train_predict(inputs)
        outputs = self.output_layer.train_predict(hidden_outputs)
        return outputs


    def train(self , inputs ,targets ):

        #calc output errors 
        predicts = self._train_predict(inputs)
        errors = [ pre - tar   for pre , tar in zip(predicts , targets)]
        output_deltas = self.output_layer.get_delta(errors)
        hidden_deltas = self.hidden_layer.get_delta(output_deltas)
        self.output_layer.update(output_deltas) 
        self.hidden_layer.update(hidden_deltas)
        return sum((pre - tar) ** 2  for pre , tar in zip(predicts , targets))


if __name__ == "__main__":

    bp = Bp(2 , 2 , 1)
    print bp.train([ 1 , 0 ] , [1. , 1. ,1.,1.])
