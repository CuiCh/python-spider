"""
Author:Cui Cheng
E-mail:cuic@lreis.ac.cn
Create_at:2017/11/27
Purpose: 抓取豆瓣的纪录片数据，写入csv文件
Tips:AJAX

"""
import re
import csv
import time
import random
import requests
from lxml import etree



writer = csv.writer(open("documentarydata.csv","w",encoding='utf-8'))
fields = ["ID","title","directors","screenwriters","casts","rate","url","country","language","publishdate","runtime","summary"]
writer.writerow(fields)

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

for i in range(0,500,20):
	target = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%BA%AA%E5%BD%95%E7%89%87&start={}".format(i)
	# 定期休眠，防止爬取速度过快被封禁
	# x = random.random()
	# time.sleep(1+x)
	req = requests.get(target,headers=headers)
	# 返回的为JSON数据
	documentaries = req.json()["data"]
	for documentary in documentaries:
		item = {}
		data = []

		# 判断是否为纪录片,如果不是则直接跳过
		url = documentary["url"]
		print(url)
		# x = random.random()
		# time.sleep(1+x)
		req = requests.get(url,headers=headers)
		html = etree.HTML(req.content)
		genre = html.xpath("//*[@id='info']/span[@property='v:genre']/text()") 
		if not genre:
			continue
		if genre[0]!="纪录片":
			continue

		# 获取关于该纪录片的信息
		screenwriters = html.xpath('//div[@id="info"]/span/span[text()="编剧"]/following-sibling::span/a/text()') or ""
		if screenwriters:
			screenwriters = "/".join(screenwriters)
		country = html.xpath('//div[@id="info"]/span[text()="制片国家/地区:"]/following-sibling::text()')
		if country:
			country = country[0].strip()
		language = html.xpath('//div[@id="info"]/span[text()="语言:"]/following-sibling::text()')
		if language:
			language = language[0].strip()
		publishdate = html.xpath('//div[@id="info"]/span[@property="v:initialReleaseDate"]/@content')
		if publishdate:
			publishdate = "".join(re.findall("\d+",publishdate[0]))
		
		# 不同类型的纪录片的时长不一致
		runtime = html.xpath('//*[@id="info"]/span[@property="v:runtime"]/@content')
		if not runtime:
			# 不同的网页有不同的结构
			runtime = html.xpath('//*[@id="info"]/span[text()="片长:"]/following-sibling::text()') or None
		if runtime:
			runtime = re.findall("\d+",runtime[0])
		if not runtime:
			# 集数
			episode_number = html.xpath('//div[@id="info"]/span[text()="集数:"]/following-sibling::text()')
			if not episode_number:
				runtime=""
				break
			episode_number = int(episode_number[0].strip())
			# 每一集长度
			episode_length = html.xpath('//div[@id="info"]/span[text()="单集片长:"]/following-sibling::text()')
			if not episode_length:
				runtime=""
				break
			episode_length = int("".join(re.findall("\d+",episode_length[0].strip()[:5])))
			runtime = episode_number*episode_length
		else:
			runtime = runtime[0]

		summary = html.xpath("//*[@id='link-report']/span[@property='v:summary']/text()") or html.xpath('//*[@id="link-report"]/span[@class="all hidden"]/text()')
		summary = "".join(summary).replace(' ','')


		ID = documentary["id"]
		title = documentary["title"]
		directors = "/".join(documentary["directors"])
		casts = "/".join(documentary["casts"])
		rate = documentary["rate"]

		# 将属性信息保存在csv文件中
		for field in fields:
			item[field] = eval(field)
		data = list(item.values())
		print(data)
		writer.writerow(data)


		# 将封面照片保存在photos/title.jpg下
		coverphoto = documentary["cover"]
		# x = random.random()
		# time.sleep(1+x)
		photo = requests.get(url=coverphoto,headers=headers).content
		with open('photos/%s.jpg' % title,'wb') as f:
			f.write(photo)