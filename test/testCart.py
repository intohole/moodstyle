#coding=utf-8


from collections import Counter
from collections import defaultdict



class Null(dict):
    pass
    


class Node(object):



    def __init__(self  ,  index , data_len , split_value ):
        self.index = index 
        self.split_value = split_value
        self.data_len = data_len
        self.left_tree = None 
        self.right_tree = None 


    def get_value(self , data ):
        '''
        得到
        '''
        if len(data) == self.data_len:
            if data[index] > split_value:
                if self.right_tree:
                    return self.right_tree
                else:
                    return 1
            else:
                if self.left_tree:
                    return self.left_tree
                else:
                    return 0 
        raise ValueError

class Cart(object):



    pass



def get_split_value(datas , split_index):
    '''
    得到cart树，分割数据点index，中位数
    '''
    if len(datas):
        return sum(data[split_index] for data in datas)/len(datas)
    raise ValueError



def calc_gini(datas , labels , index , split_value):

    labels_dict = Counter(labels)
    label_dist_dict = {label : defaultdict(int) for label in labels_dict.keys()}
    for i in range(len(labels)):
        if datas[i][index] > split_value:
            label_dist_dict[labels[i]][1] += 1
        else:
            label_dist_dict[labels[i]][0] += 1 
    gini = 0.
    for label in labels_dict.keys():
        prob = labels_dict[label] / len(labels)
        prob_label = label_dist_dict[label][1] / float(len(labels))  
        gini += (prob * 2 * prob_label * (1 - prob_label) )
    return gini


def get_best_split_feature(datas  , data_len , labels ):
    ginis = []
    for split_index in range(data_len):
        split_value = get_split_value(datas , split_index)
        ginis.append( ( calc_gini(datas , labels , split_index  , split_value) ,split_value , split_index ) )
    return max(ginis)








if __name__ == '__main__':
    from random import random
    from random import randint
    datas = [ [random()+0.1] for i in range(10) ] 
    print get_split_value(datas , 0)
    labels =[ 1 if datas[i] > 0.45 else 0 for i in range(len(datas))]
    print get_best_split_feature(datas , 1 , labels)
