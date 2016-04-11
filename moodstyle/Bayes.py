#coding=utf-8

from collections import Counter
from collections import defaultdict
import sys

class Bayes(object):
    

    def train(self, datas, attr_len, labels, dense=True):
        """贝叶斯训练函数 
            params:
                datas 训练数据 ， [[]]
                attr_len 属性长度
                labels 分类数组 ， 与datas对应
                dense 是否为稀疏矩阵，现在只支持dense=True
            return
                None
            raise 
                None
        """
        self.label_status = Counter(labels)
        self.default_prob = defaultdict(float)
        self.attr_status = {
            i: defaultdict(lambda: defaultdict(float)) for i in range(attr_len)}
        self.base_count = len(datas)
        self.attr_range = range(attr_len)
        for i in range(len(datas)):
            for j in range(attr_len):
                attr_val = datas[i][j]
                # 统计每个属性对应 p(I | C) , I < (v1 , v2 ,v3....,vn)
                self.attr_status[j][attr_val][labels[i]] += 1.
        # 计算每个属性出现val 时 ， P(v1|I,C)
        for feature, attr_label in self.attr_status.items():
            for attr_val, label in self.attr_status[feature].items():
                for cl in label.keys():
                    self.attr_status[feature][attr_val][
                        cl] /= ( self.label_status[cl] + self.base_count)
        for label in self.label_status.keys():
            self.default_prob[label] = 1. / ( self.label_status[label] + self.base_count)
        # 计算所有类别出现的概率 P(C) = sum(Cn) / sum(C) , n < (1,2,3,4,5....n)
        labels_count = float(sum(self.label_status.values()))
        for label, count in self.label_status.items():
            self.label_status[label] /= labels_count
    def _predict(self , data , label):
        prob = 1. 
        for i in self.attr_range:
            if data[i] == 0:
                continue
            prob *= self.get_prob(i , data[i], label)        
        return prob * self.label_status[label]

    def get_prob(self , attr_index , value ,label ):
        """得到在指定序号下value在特定类别下发生概率
            params
                attr_index 暂定为属性序号
                value   属性值
                label   类别
            return 
                prob    发生概率
            raise 
                None
        """
        if value in self.attr_status[attr_index]:
            if label in self.attr_status[attr_index][value]:
                return self.attr_status[attr_index][value][label]
        return self.default_prob[label] 

    
    
    def predict(self, data):
        """对输入数据进行预测
            params:
                data
            return 
                label 数据标记
            raise
                None
        """
        probs = [( self._predict(data , label),label ) for label in self.label_status.keys() ]
        return sorted(probs, key = lambda x:x[0] , reverse = True)[0]
 
    def predict_old(self, data):

        """对输入数据进行预测
            params:
                data
            return 
                label 数据标记
            raise
                None
        """
        return sorted([(
            reduce(lambda x, y:x * y,
                   [
                       self.attr_status[i][data[i]][label]
                       for i in range(len(data))
                       if self.attr_status[i][data[i]].has_key(label)
                   ]
                   )
            *
            self.label_status[label], label
        )
            for label in self.label_status.keys()
        ], reverse=True)

if __name__ == "__main__":
    b = Bayes()
    datas = [ [ 0 , 0 ] , [0 , 1] , [1 , 1]  ,[1 , 0]]
    labels = [ 0 , 1 , 0 , 1]
    b.train(datas , 2 ,labels = labels) 
    print b.predict([ 2 , 1])
