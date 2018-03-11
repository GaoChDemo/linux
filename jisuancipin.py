# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import jieba
import jieba.posseg as psg
from copy import deepcopy
import collections

dic = collections.OrderedDict()
dic['flag'] = False
fw = open('key20w.txt','r')
for line in fw:
    dic[line.decode('utf-8').replace("\n", "")] = False
fw.close()
print len(dic)
data = pd.read_csv('rrr1200oko.csv')

nplis = []
jj = 0
xj = 0
for i in range(0,len(data)):
    print i
    text = data['text'][i]
    keym = deepcopy(dic)
    try:
        past = [(x.word,x.flag) for x in psg.cut(text.strip().decode('utf-8'))]
    except Exception as e:
        print e
        continue
    for k,v in past:
    	#print k
        if k in keym:
            keym[k] = True
    if True in keym.values():
    	print "true"
        #if data['rating'][i] in ['力荐','推荐','还行']:
        if data['flag'][i] == 1:
            keym['flag'] = True
            df = pd.DataFrame.from_dict(keym,orient='index').T
            df.to_csv('20wokojj.csv', sep=',', header=False, index=False,encoding='utf-8',mode='a')
            jj += 1
            print "jj+1"
        #elif data['rating'][i] in ['很差','较差']:
    	elif data['flag'][i] == 0:
            keym['flag'] = False
            df = pd.DataFrame.from_dict(keym,orient='index').T
            df.to_csv('20wokoxj.csv', sep=',', header=False, index=False,encoding='utf-8',mode='a')
            xj += 1
            print "xj+1"
        #li.insert(0,data['flag'][i])
    else:
        continue

print "jj:"+jj
print "xj:"+xj
print "jj:"+jj
print "xj:"+xj
