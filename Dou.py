# -*- coding:utf-8 -*-
import requests
from pyquery import PyQuery as pq
import re
import pandas as pd
import time
import random
import string
import json


USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]



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

class Douban:
	"""demo """
	def __init__(self):
		self.url_list = []
		self.url_start = ''
		self.data = []
		self.headers = {}
	def get_headers(self):
		self.headers = {
	        "User-Agent": random.choice(USER_AGENTS),
	        "Host": "movie.douban.com",
	        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	        "Accept-Encoding": "gzip, deflate, sdch, br",
	        "Accept-Language": "zh-CN, zh; q=0.8, en; q=0.6",
	        "Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
    	}

	def downloader_movie_list(self,url,number):
		r = requests.get(url,headers=self.headers,allow_redirects=False)
		print 'download'
		while r.status_code != 200:
			print 'download failed, wait for 10 minutes %d' % number
			time.sleep(600)
			r = requests.get(url,headers=self.headers,allow_redirects=False)
		return json.loads(r.text)

	def get_movie(self):
		url_start = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,5&tags=&start=%d'
		for i in range(200,600,20):
			url = url_start % i
			self.get_headers()
			urllist = self.downloader_movie_list(url,i)['data']
			self.url_list += urllist


	def get_url(self,page,url,num):
		#print pq(page).find('.next').attr('href')
		url = url + '?start=%d&limit=20&sort=new_score&status=P&percent_type=' % num
		return url
	def downloader(self,url,movie):
		r = requests.get(url,headers=self.headers,allow_redirects=False)
		while r.status_code != 200:
			print 'download failed, wait for 10 minutes'
			time.sleep(600)
			r = requests.get(url,headers=self.headers,allow_redirects=False)
		return r.text
	def html_paser(self,page,movie):
		for item in pq(page).find('.comment-item'):
			user = pq(item).find('.comment-info').find('a').html()
			rating = pq(item).find('.rating').attr('title')
			time = pq(item).find('.comment-time').attr('title')
			text = pq(item).find('.comment').find('p').html().split('<a class="source-icon"')[0].strip().replace('"', '').replace('\n', '')
			self.data.append({'movie':movie,'user':user,'rating':rating,'time':time,'text':text})
	def output(self):
		for item in self.data:
			#dataframe = pd.DataFrame({'title':item['title'],'rating':item['rating']})
			print item['title'],"  ",item['rating']
		#dataframe.to_csv("test.csv",sep=',')
	def writefile(self):
		df = pd.DataFrame(self.data,columns=['movie','user','rating','time','text'])
		df.to_csv('rrrl200-600.csv', sep=',', header=False, index=False,encoding='utf-8',mode='a')
		self.data = []
	def start(self):
		df = pd.DataFrame(columns=['movie','user','rating','time','text'])
		df.to_csv('rrrl200-600.csv', sep=',', header=True, index=False,encoding='utf-8',mode='w')
		self.get_headers()
		self.get_movie()
		while(len(self.url_list) > 0):
			time.sleep(10)
			smovie = self.url_list.pop()

			url = smovie['url']+'comments?status=P'
			url_root = url.split('?')[0]
			#print url_root	
			print url
			for i in range(0,200,20):
				
				time.sleep(2)
				try:
					self.get_headers()
					movie = smovie['title']
					page = self.downloader(url,movie)
					#print movie
					self.html_paser(page,movie)
					url = self.get_url(page,url_root,i)
				except Exception as e:
					#print e
					print e
					break
			
			self.writefile()
			'''
		url_root = self.url_start.split('?')[0]
		#print url_root
		url = self.url_start
		while(True):
			time.sleep(1)
			print url
			try:
				self.get_headers()
				page = self.downloader(url)
				#print movie
				self.html_paser(page,movie)
				url = self.get_url(page,url_root)
			except Exception as e:
				#print e
				break
			
		self.writefile()'''
	
'''	
		for url in self.get_url(num):
			page = self.downloader(url)
			self.html_paser(page)
		self.output()
		self.writefile()'''

#d = Douban()
#d.start()
u = Douban()
u.start()
'''
for lis in u.get_movie():
	while(len(lis['data']) > 0):
	    movie = lis['data'].pop()
	    print movie['title'],movie['url']


url_list = u.get_list()
df = pd.DataFrame(columns=['movie','user','rating','time','text'])
df.to_csv('rrr.csv', sep=',', header=True, index=False,encoding='utf-8',mode='a')
for i in range(2):
#while(len(url_list)>0):
	d = Douban(url_list.pop())
	d.start()
	time.sleep(5)

#print cookies'''

