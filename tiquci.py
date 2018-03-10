# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import jieba
import jieba.posseg as psg
from copy import deepcopy
from jieba import analyse
# 引入TF-IDF关键词抽取接口
tfidf = analyse.extract_tags

#打开文件
data = pd.read_csv('rrr1200.csv')

wordflag = ['a','v','i','b']
keys = set()
iii = -1

for text in data['text']:
    try:
        li = tfidf(text)
    except Exception as e:
        print e
        print text,"iii",iii
    for a in li:
        if a not in keys:
            keys.add(a)
    try:
        li = [(x.word,x.flag) for x in psg.cut(text.strip().decode('utf-8'))]
    except Exception as e:
        print e
        print text,"iii",iii
    for a,b in li:
        if (b in wordflag) and (a not in keys):
            keys.add(a)
    iii += 1
    if iii%100 == 0:
        print iii

fw = open('keword_linux.txt','w')
for k in keys:
    try:
        st = k+"\n"
        fw.write(st.encode('utf-8'))
    except Exception as e:
        print e
        print k
fw.close()
