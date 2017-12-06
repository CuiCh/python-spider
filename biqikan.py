"""
Author: Cuicheng
E-mail:cuic@lreis.ac.cn
Created:2017-11-12
Purpose:参考Jack-Cui的代码重新学习爬虫，抓取静态页面
"""
import os
import sys
import requests
from lxml import etree

class downloader(object):
	"""
	类说明：获取笔趣看小说《一念永恒》
	Modify:2017-11-12
	"""
	def __init__(self):
		self.serversite = "http://www.biqukan.com"
		self.target = "http://www.biqukan.com/1_1094/"
		self.filepath = "一念永恒.txt"
		self.names = []
		self.urls = []
		self.num = 0

	def get_download_urls(self):
		"""
		函数说明：获取每个章节的名字和下载地址
		Parameters:
			无
		Returns:
			无
		Modify:
			2017-11-12
		"""
		req = requests.get(url=self.target)
		html = etree.HTML(req.content) 
		# 解析HTML获取章节名称和下载链接
		names  = html.xpath("/html/body/div[@class='listmain']//dt[2]/following-sibling::dd/a/text()")
		urls = html.xpath("/html/body/div[@class='listmain']//dt[2]/following-sibling::dd/a/@href")
		self.num = len(urls)
		self.names = names
		self.urls = [self.serversite+url for url in urls]

		print("目前共有%s章" % len(urls))
			
	def get_content(self,target):
		"""
		函数说明：获取每一章的具体内容
		Parameters:
			target-下载链接
		Returns:
			content-每一章的具体内容
		Modify:
			2017-11-12
		"""
		req = requests.get(url=target)
		html = etree.HTML(req.content)
		# 获取小说内容
		content = html.xpath("//*[@id='content']/text()")
		# 多个空格替换为回车
		content = ''.join(content).replace('        ','\n\n')
		# content = ''.join(content).replace('\a0'*8,'*********************')
		# print(content)
		return content

	def write_to_file(self,path,name,content):
		"""
		函数说明：获取所有章节的内容并保存
		Parameters:
			 path-保存的路径,将所有章节保存到同一文件
			 name-每一章节的名字
			 content-每一章的内容
		Returns:
			 
		Modify:
			2017-11-12
		"""
		with open(path,'a',encoding='utf-8') as f:
			f.write(name+"\n")
			f.writelines(content)
			f.write("\n\n\n\n")

	def download(self):
		"""
		函数说明：获取所有章节的内容并保存
		Parameters:
			 
		Returns:
			 
		Modify:
			2017-11-12
		"""
		self.get_download_urls()
		# 若已经存在文件"一念永恒.txt"，则删除
		if os.path.exists(self.filepath):
			os.remove(self.filepath)
		for (i,name,url) in zip(range(self.num),self.names,self.urls):
			content = self.get_content(url)
			self.write_to_file(self.filepath,name,content)
			sys.stdout.write("已下载%.3f %% \r" % float(i/self.num*100))
			sys.stdout.flush()
			

def main():
	print("开始下载《一念永恒》")
	dl = downloader()
	dl.download()
	print("《一年永恒》下载完成！")


if __name__ == '__main__':
	main()