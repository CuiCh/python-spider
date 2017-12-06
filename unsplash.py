"""
Author: Cuicheng
E-mail:cuic@lreis.ac.cn
Created:2017-11-12
Purpose:参考Jack-Cui的代码重新学习爬虫，抓取动态反爬页面
"""
import sys
import time
import json
import random
import requests
from lxml import etree


class GetPhotos(object):
	"""
	类说明：获取https://unsplash.com上的图片
	"""
	def __init__(self):
		self.ids = []
		self.target = "https://unsplash.com/napi/feeds/home"
		self.download_server = "https://unsplash.com/photos/xxxxx/download?force=true"
		# authorization 是此网站中是重要的验证
		self.headers = {
		'authorization':"Client-ID c94869b36aa272dd62dfaeefed769d4115fb3189a9d1ec88ed457207747be626",
		'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
		}
		self.download_delay = 1 
	
	def get_photoids(self):
		"""
		函数说明：获取图片的id
		Parameters:
			无
		Returns:
			无
		Modify:
			2017-11-12
		"""
		req = requests.get(url=self.target,headers=self.headers,verify=False)
		# html = json.loads(req.content)
		# 使用requests自带的json解码器
		html = req.json()
		next_page = html["next_page"]
		for each in html["photos"]:
			self.ids.append(each['id'])
		# 适当休眠
		time.sleep(self.download_delay + random.random())

		# 再抓取4页，一共有50张图片
		for i in range(4):
			req = requests.get(url=next_page,headers=self.headers,verify=False)
			html = req.json()
			next_page = html["next_page"]
			for each in html["photos"]:
				self.ids.append(each['id'])
			time.sleep(self.download_delay + random.random())
		print(self.ids)

	def download_photo(self,photo_id,photo_name):
		"""
		函数说明：下载每一张图片
		Parameters:
			photo_id-图片的ID
			photo_name-图片的名字
		Returns:
			无
		Modify:
			2017-11-12
		"""
		target = self.download_server.replace("xxxxx",photo_id)
		photo = requests.get(url=target,headers=self.headers,verify=False).content
		with open('%s.jpg' % photo_name,'wb') as f:
			f.write(photo)

	def download_all(self):
		"""
		函数说明：下载所有图片
		Parameters:
			无
		Returns:
			无
		Modify:
			2017-11-12
		"""
		print("开始获取图片链接")
		self.get_photoids()
		print("开始下载图片")
		for i,id in enumerate(self.ids):
			print("正在下载第%i张图片" % (i+1))
			self.download_photo(id,(i+1))


def main():
	gp = GetPhotos()
	gp.download_all()


if __name__ == '__main__':
	main()