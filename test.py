#coding=utf-8






class Node(object):
    '''
    创建多叉树的过程 ，
    创建每个元素都是Node ， 每个Node 都有孩子节点(Node) 
    '''


    def __init__(self , data):
        self.data = data
        self.__child = {}



    def __getitem__(self , key):
        '''
        得到一个Node child节点
        '''
        if key in self.__child.keys():
            return self.__child[key]
        else:
            return None

    def __setitem__(self , key , value):
        if key:
            if key not in self.__child.keys() and isinstance(value , Node):
                self.__child[key] = value
                return
        raise TypeError , 'key is null or value is not Node or int string etc'







def create_tree(self , datas , attrs):
    '''
    
    '''
    attr = find_best_feather(datas , attrs)
    split_data(datas , attr )







if __name__ == '__main__':
    pass