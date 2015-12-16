#coding=utf-8

import math
import random


class Neroun(object):


    def __init__(self , weight_len):
        self.weights = self.init_weights(weight_len)                
        self.delta = 0.
        self.weight_len = weight_len
        self.weight_range = range(weight_len)
        self.rate = rate 

    def init_weights(self , weight_len):
        weights = [0.] * weight_len
        for i in range(weight_len):
            weights[i] = random.random()
        return weights

    def get_value(self , inputs):
        return self.simgod( sum(inputs[i]  * self.weights[i] for i in self.weight_range) + self.delta)            

    def simgod(self , value):
        return 1. / ( 1 + math.exp(-value))

    def __len__(self):
        return self.weight_len 

    def update(self , target, predict):
        error = target - predict
        for i in self.weight_range:
            self.weights[i] += self.rate * error
        return error 

class Layer(object):



    def __init__(self , inputs_len ,neroun_len):
        self.nerouns = [ Neroun(inputs_len)  for i in range(neroun_len)]
        self.nerouns_len = neroun_len
    
    def predict(self , inputs ):
        return [self.nerouns[i].get_value(inputs) for i in range(self.nerouns_len)]

    def update(self , targets , predicts):
        return [ self.nerouns.update(targets[i] - predicts[i]) for i in range(self.nerouns_len)]




class Bp(object):



    def __init__(self , inputs_len , hidden_len , outputs_len):
        self.input_layer_len = inputs_len
        self.hidden_layer_len = hidden_len 
        self.output_layer_len = outputs_len
        self.hidden_layer = Layer(inputs_len , hidden_len)
        self.output_layer = Layer(hidden_len , outputs_len)

    
    def predict(self , inputs):
        if len(inputs)  != self.input_layer_len:
            raise Exception 
        hidden_outputs = self.hidden_layer.get_value(inputs)
        outputs = self.output_layer.get_value(hidden_outputs)
        return outputs


    def train(self , inputs ,targets ):
        predicts = self.predict(inputs)
        self.output_layer.update( targets , errors)



if __name__ == "__main__":

    bp = Bp(3 , 4 , 4)
    print bp.get_value([2. , 3. ,1.])
