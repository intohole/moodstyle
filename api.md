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
