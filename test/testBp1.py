#coding=utf-8

import math
import random


class Neroun(object):


    def __init__(self , weight_len , rate = 0.1 , delta = random.uniform(1 , -1)):
        self.weights = self.init_weights(weight_len)                
        self.delta = delta  
        self.weight_len = weight_len
        self.weight_range = range(weight_len)
        self.rate = rate 

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

    def update(self , target, predict):
        error = target - predict
        for i in self.weight_range:
            self.weights[i] += self.rate * error
        return error 

class Layer(object):



    def __init__(self , inputs_len ,neroun_len , learn_rate = 0.1):
        self.nerouns = [ Neroun(inputs_len , rate = learn_rate)  for i in range(neroun_len)]
        self.nerouns_len = neroun_len
    
    def predict(self , inputs ):
        return [self.nerouns[i].predict(inputs) for i in range(self.nerouns_len)]

    def update(self , targets , predicts):
        return [ self.nerouns.update(targets[i] - predicts[i]) for i in range(self.nerouns_len)]

    def get_delta(self , vtargets , predicts):
        


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
        hidden_outputs = self.hidden_layer.predict(inputs)
        outputs = self.output_layer.predict(hidden_outputs)
        return outputs


    def update(self , predicts ,targets ):
        errors = [ (pre - tar) for pre , tar in zip(predicts , targets)]
        self.output_layer.update( targets , errors)
    
        return  


if __name__ == "__main__":

    bp = Bp(3 , 4 , 4)
    print bp.predict([2. , 3. ,1.])
