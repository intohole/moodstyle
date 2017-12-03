API
=========

+ moodstyle.LinerModel.LinerModel
    - 参数:
        - w 参数个数／训练数据／测试数据个数
        - learn_rate 学习率，默认值0.1
        - labels label,默认[1,-1] 
    - train(datas,labels)
        - datas 训练数据,[[0,1],[1,2]]
        - labels 打标数据,[1,-1]
    - predict
        - data 预测数据，数据形式为[0,1]


+ moodstyle.Bandit.Greedy 
    
    - 参数(Paramters):
        - e 探测率(explor rate); e 在(in) (0,1)
        - N 需要探测桶数(the number of explor bucket)

    - 函数(Function):
        - getIndex()
            - 获得运行的桶号(get index of bucket)
        - process(label)
            - 获得标注 


+ moodstyle.DDistance
    - 计算两个数据之间距离(caculate distance of input data)
    - 函数(Function)
        - distance(data1,data2)
            - data1 输入数据(input data); 例如（example）: [1,2]
            - data2 输入数据(input data); 例如 （example）:[2,3]
            - warn: length of data1 is equal to the length of data2 
    - moodstyle.DDistance.Manhattan
        - 曼哈顿距离

    - moodstyle.DDistance.Chebyshev
        - 切比雪夫距离
   
    - moodstyle.DDistance.Cosine
        - 余弦距离
    
    - moodstyle.DDistance.Hamming
        - 海明距离
    
    - moodstyle.DDistance.Eucliden
        - 欧式距离 
