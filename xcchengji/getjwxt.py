# -*- coding:utf-8 -*-
import requests
import re
from pyquery import PyQuery as pq

#头部信息
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Host':'zhjw.dlnu.edu.cn',
    'Referer':'http://zhjw.dlnu.edu.cn/menu/s_main.jsp',
    'User-Agent':'"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'
}

#数据爬去
def getTest(username,passward):
    r_session  = requests.Session()
    data = {
            "ldap" : 'auth',
            "zjh": username,
            "mm": passward
    }    
    r_session.post('http://zhjw.dlnu.edu.cn/loginAction.do', data=data,headers=headers)
    xx = r_session.get('http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=lnfaqk&flag=zx',headers=headers)
    patternx = re.compile(r'tree.add\((.*?)\);',re.S)
    xlist = patternx.findall(xx.text)
    
    ts = r_session.get('http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa',headers=headers)
    patternt = re.compile(r'href=\"(.*?)\"',re.S)
    subjectlist = patternt.findall(ts.text)
    url = 'http://zhjw.dlnu.edu.cn/'
    for i in subjectlist:
        if u'fajhh' in i:
            url += i
            break
            
    tslist = []
    ts = r_session.get(url,headers=headers)
    for item in pq(ts.text).find('.odd'):
        tsl = pq(item).text().split('\n')
        tslist.append(tsl)
    
    if 'init()' in xx.text:
        xlist = -1
        tslist = -1
    return xlist,tslist#.encode("utf-8") #unicode(s.text,"gb2312")

#数据处理
def deldata(xlist,tslist):
    #选修课处理
    xxlist = []
    patx = re.compile(r'''\[(.*?)\]''',re.S)
    for i in xlist:
        #if u'yxjg.gif' in i:
        xstr = i.split('\n')[0]
        slist = patx.findall(xstr)
        if len(slist) > 0:
            xxlist.append(slist[0])
    
    #处理通识课
    for item in tslist:
        if len(item) == 7:
            del item[3]
        del item[1]
    return xxlist,tslist


#分类
def classify(xlist,tslist):
    tsll = []
    xxll = []
    bxll = []
    for i in tslist:
        if i[0] not in xlist and u'必修' not in i:
            tsll.append(i)
        elif u'必修' not in i:
            xxll.append(i)
        else:
            bxll.append(i)
    
    return tsll,xxll,bxll

#输出
def cout(tsll,xxll,bxll):
    for i in tsll:
        for j in i:
            print j,
        print '\n'
    for i in xxll:
        for j in i:
            print j,
        print '\n'
    for i in bxll:
        for j in i:
            print j,
        print '\n'
    
def start(username,passward):
    #username = raw_input("请输入账号:")
    #passward = raw_input("请输入密码:")
    xlist,tslist = getTest(username,passward)
    if xlist == -1 and tslist == -1:
        print '登录失败！'
        return -1
    else:
        xlist,tslist = deldata(xlist,tslist)
        tsll,xxll,bxll = classify(xlist,tslist)
        return tsll+xxll+bxll



