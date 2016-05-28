#coding=utf-8



class TreeNode(object):



    def __init__(self):
        self.value = value 
        self.left_leaf = None
        self.right_leaf = None
        self.split_value = None 

class RegressionTree(object):

    


    def __init__(self):
        self.tree = TreeNode()

    


    def train(self , datasets , targets):
        feature_split_values = self.init_split_value(datasets , targets)
        

    def loss(self , datasets , labels , attr , split_value):
        """回归树的损失函数
            param:datasets:class 训练数据集
            param:labels:list target目标训练值
            param:attr:int 训练属性坐标
            param:split_value:float 属性分裂值
            return:error :如果训练数据集没有出错则返回损失值，否则返回None
            raise:None 
        """
        c1 , c2 = self.get_target_avg(datasets , attr , split_value)
        if c1 is None or c2 is None:
            return None
        error = None 
        for i in xrange(len(datasets)):
            if datasets[i][attr] is None:
                continue
            if error is None:
                error = 0.
            if datasets[i][attr] > split_value:
                error += (labels[i] - c1) ** 2
            else:
                error += (labels[i] - c2) ** 2
        return error


    def get_target_avg(self , datasets ,targets , attr , split_value):
        """根据分裂点，得到两个部分的target目标值
            param:datasets:class 训练数据集
            param:targets:list 训练数据对应的目标值list
            param:attr:int 训练属性坐标
            param:split_value:float 属性分裂值
            return:数据集中大于split_value值属性的训练target目标平均值c1 , 数据集attr属性中小于等于spliit_value属性的训练target目标平均值c2
            raise:None
        """
        c1 , c2 = 0., 0.
        c1_count , c2_count = 0, 0
        for i in xrange(len(datasets)):
            if datasets[i][attr] is None:
                continue
            if datasets[i][attr] > split_value:
                c1 += targets[i]
                c1_count++
            else:
                c2 += targets[i]
                c2_count++
        return c1 / c1_count , c2/ c2_count if c1 == 0 or c2 == 0 else None,None

    def _get_split_point(self , datasets ,labels, attr):
        split_value
        for i in xrange(len(datasets)):
            
    def get_best_split_attr_value(self , datasets , targets):
          
