Title: 关于moodstyle 使用方法  
Slug: six god  
Date: 2013-12-16 19:39:38  
Tags: 情感分析   
Category:  算法 python  
Author:  泽  
Lang:  zh  
Summary: 一个辅助工具集  

moodstyle工具集介绍  
============

PTextFeatureExtract  
----------------------------------
:::python

                    from PTextFeatureExtract import *  
                    text_feature_extract = IM() #基于互信息 可选择种类为：CHI () DF WLLR  
                    contents = []  
                    with open('/home/xxxx/fenlei/all.txt') as f:  
                    contents = [line.strip() for line in f.readlines()]  
                    for doc_type, word_list in s.extract_feature_from_contents(100, contents , 2).items():  
                        print doc_type  
                        for i in word_list:   
                            print i  
用于已经分好类别的数据，进行提取特征词  

clusterutils/kmeans.py  
---------------------------
基于kmeans分类算法实现   
:::python

              k = KMeans() #但是要继承 def distance(self,data1,data2)： 计算分类距离   
              print k.k_means(4, [(1,4),(5,2) ,(100,16),(8,9),(10,101),(150,1555),(177,120),(14,4),(5,99)])  


clusterutils/levenshtein.py
-------------------------------------------------
字符串编辑距离 及字符串相似度  
:::python

             str_similarity('asds', 'acbccc')  # 0.17  

clusterutils/similar.py  
------------------------------------------
两个（句子，段落）之间相似度    
:::python

             print similar("我 不 爱 他妈 哈 哈 哈", "我 爱 天安门 ming 哈 哈 哈") # 0.846153846154 两个句子向量相似度  



clusterutils/HMM.py
-------------------------------------------------
隐士马尔夫实现 hmm 维特比实现
:::python

             states = ('Healthy', 'Fever') 

            observations = ('normal', 'cold', 'dizzy')

            start_probability = {'Healthy': 0.6, 'Fever': 0.4}
            transition_probability = {
                'Healthy': {'Healthy': 0.7, 'Fever': 0.3},
                'Fever': {'Healthy': 0.4, 'Fever': 0.6},
            }
            emission_probability = {
                'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
                'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6},
            }
            print viterbi(observations , states , start_probability , transition_probability , emission_probability)
              



 

   
