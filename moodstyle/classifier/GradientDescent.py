#coding:utf-8
#梯度下降法的简单示例
#已知拟合的曲线形式：Y = θ0 * X0 + θ1 * X1
#现在有一组数据（X0，X1，Y），保存在train_list中
 
alpha = 0.006555#步长
train_list = [(1,0,1),(1,1,3),(1,2,5),(1,3,7),(1,4,9),
              (1,5,11),(1,6,13),(1,7,15)]#训练集，X0,X1,Y
theta = [0,0]#初始化θ0、θ1
 
#计算Loss Function J(θ)的偏导数,
#param取值0、1，分别对应求θ0、θ1偏导数
#PDJ为J(θ)的偏导数partial derivative
def PDJ(param):
    sum = 0
    for item in train_list:
        hx = theta[0] * item[0] + theta[1] * item[1]#估计函数
        sum += (hx - item[2]) * item[param]
    return sum
 
#θ0、θ1属于[0,2.0],每隔0.1运行一次梯度下降法
for i in range(21):
    i = float(i)/10
    for j in range(21):
        j = float(j)/10
        theta  = [i,j]
        for count in range(1000):
            pdJ0, pdJ1 = PDJ(0), PDJ(1)#参数θ0、θ1的偏导数，注：(pdJ0,pdJ1)为梯度
            pdJ0, pdJ1 = pdJ0 * alpha, pdJ1 * alpha#朝偏导数方向移动长度为alpha的距离
             
            if abs(pdJ0) < 0.000001 and abs(pdJ1) < 0.000001:
                break
            theta[0] -= pdJ0#更新theta
            theta[1] -= pdJ1
        print i,j,count,theta[0],theta[1]