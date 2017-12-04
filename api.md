API
=========

+ moodstyle.classifier.LinerModel.LinerModel
    - 参数:
        - w 参数个数／训练数据／测试数据个数
        - learn_rate 学习率，默认值0.1
        - labels label,默认[1,-1] 
    - train(datas,labels)
        - datas 训练数据,[[0,1],[1,2]]
        - labels 打标数据,[1,-1]
    - predict
        - data 预测数据，数据形式为[0,1]


+ moodstyle.alg.Bandit.Greedy 
    
    - 参数(Paramters):
        - e 探测率(explor rate); e 在(in) (0,1)
        - N 需要探测桶数(the number of explor bucket)

    - 函数(Function):
        - getIndex()
            - 获得运行的桶号(get index of bucket)
        - process(label)
            - 获得标注 


+ moodstyle.common.DDistance
    - 计算两个数据之间距离(caculate distance of input data)
    - 函数(Function)
        - distance(data1,data2)
            - data1 输入数据(input data); 例如（example）: [1,2]
            - data2 输入数据(input data); 例如 （example）:[2,3]
            - warn: length of data1 is equal to the length of data2 
    - moodstyle.common.DDistance.Manhattan
        - 曼哈顿距离
    - moodstyle.common.DDistance.Chebyshev
        - 切比雪夫距离
    - moodstyle.common.DDistance.Cosine
        - 余弦距离
    - moodstyle.common.DDistance.Hamming
        - 海明距离
    - moodstyle.common.DDistance.Eucliden
        - 欧式距离 

+ moodstyle.alg.PageRank
    - moodstyle.alg.PageRank.GraphV2
        - 建立图关系(build data graph) 
        - 构造函数(init function):
            - GraphV2(N)
                - N the number of node;
            - add_edge(n1 , n2)
                - n1 node point to another; intger
                - n2 node which n1 point to;  intger
    - moodstyle.alg.PageRank.PageRank
        - 计算图的page rank（caculate graph）
        - 函数(Function) 
            - rank
                - param: graph GraphV2 model，build node relation
                - return: weight array,weight of the nodes
