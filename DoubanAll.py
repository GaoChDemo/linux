# -*- coding:utf-8 -*-
import requests
from pyquery import PyQuery as pq
import re
import pandas as pd
import time

cookies = {' _pk_id.100001.8cb4': 'cc198f3080a707b3.1516623466.3.1516850773.1516800492.', ' dbcl2': '"173064118:yk185kPPZw0"', ' _ga': 'GA1.2.94774273.1516623251', ' ap': '1', ' as': '"https://www.douban.com/"', ' ps': 'y', ' _pk_ref.100001.8cb4': '%5B%22%22%2C%22%22%2C1516850569%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D', 'bid': '1GOJr_Lieng', ' ll': '"118129"', ' _gid': 'GA1.2.597574385.1516800005', ' push_doumail_num': '0', ' _pk_ses.100001.8cb4': '*', ' _gat_UA-7019765-1': '1', ' __utmz': '30149280.1516850569.10.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)', ' __utmt': '1', ' __utmv': '30149280.17306', ' _vwo_uuid_v2': 'A94552B113E5975C0F717A522B7286E0|ec873e50152013af2b8584596dce6dc6', ' __yadk_uid': 'fTPbQVg9N7wstTyIKWCuon2ZI8les44I', ' __utma': '30149280.94774273.1516623251.1516800000.1516850569.10', ' push_noty_num': '0', ' __utmc': '30149280', ' __utmb': '30149280.8.10.1516850569'}

dataframe = pd.DataFrame()

'''name = raw_input("请输入电影名字")

url = "https://movie.douban.com/subject_search?search_text="+ name +"&cat=1002"

r = requests.get(url)

print r.text
print url
'''
'''
for i in range(0,250,25):
	#待爬取的网址
	url = 'https://movie.douban.com/top250?start=%d&filter='%i
	#爬取url，获取内容
	r = requests.get(url)

	#遍历
	for movie in pq(r.text).find('.item'):
		print pq(movie).find('.title').html(),"  ",
		print pq(movie).find('.rating_num').html(),
		#print pq(movie).find('.bd').html()'''

class Douban_url:
	"""获取所有 """
	def __init__(self):
		self.url_list = []
	def get_url(self,page,url):
		#print pq(page).find('.next').attr('href')
		return url + pq(page).find('.next').find('a').attr('href')
	def downloader(self,url):
		r = requests.get(url,cookies=cookies)
		return r.text
	def html_paser(self,page):
		for item in pq(page).find('.item'):
			url = pq(item).find('.pic').find('a').attr('href') + 'comments?status=P'
			#print url
			self.url_list.append(url)
	def start(self):
		url_start = 'https://movie.douban.com/top250'
		url_root = url_start.split('?')[0]
		#print url_root
		url = url_start
		while(True):
			#print url
			try:
				page = self.downloader(url)
				self.html_paser(page)
				url = self.get_url(page,url_root)
			except Exception as e:
				#print e
				break
	def get_list(self):
		return self.url_list

class Douban:
	"""demo """
	def __init__(self,url_start):
		self.url_start = url_start
		self.data = []
	def get_url(self,page,url):
		#print pq(page).find('.next').attr('href')
		return url + pq(page).find('.next').attr('href')
	def downloader(self,url):
		r = requests.get(url,cookies=cookies)
		return r.text
	def html_paser(self,page,movie):
		for item in pq(page).find('.comment-item'):
			user = pq(item).find('.comment-info').find('a').html()
			rating = pq(item).find('.rating').attr('title')
			time = pq(item).find('.comment-time').attr('title')
			text = pq(item).find('.comment').find('p').html()
			self.data.append({'movie':movie,'user':user,'rating':rating,'time':time,'text':text})
	def output(self):
		for item in self.data:
			#dataframe = pd.DataFrame({'title':item['title'],'rating':item['rating']})
			print item['title'],"  ",item['rating']
		#dataframe.to_csv("test.csv",sep=',')
	def writefile(self):
		global num
		df = pd.DataFrame(self.data,columns=['movie','user','rating','time','text'])
		df.to_csv('d.csv', sep=',', header=False, index=False,encoding='utf-8',mode='a')
	def start(self,num=250):
		url_root = self.url_start.split('?')[0]
		#print url_root
		url = self.url_start
		while(True):
			time.sleep(1)
			print url
			try:
				page = self.downloader(url)
				movie = pq(page).find('#content').find('h1').html()
				movie = movie.split(' ')[0]
				#print movie
				self.html_paser(page,movie)
				url = self.get_url(page,url_root)
			except Exception as e:
				#print e
				break
			
		self.writefile()
	
'''	
		for url in self.get_url(num):
			page = self.downloader(url)
			self.html_paser(page)
		self.output()
		self.writefile()'''

#d = Douban()
#d.start()
u = Douban_url()
u.start()
url_list = u.get_list()
df = pd.DataFrame(columns=['movie','user','rating','time','text'])
df.to_csv('d.csv', sep=',', header=True, index=False,encoding='utf-8',mode='a')
while(len(url_list)>0):
	d = Douban(url_list.pop())
	d.start()
	time.sleep(5)

#print cookies
