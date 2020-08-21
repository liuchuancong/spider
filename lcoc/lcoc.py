# -*- coding: utf-8 -*-
"""
Created on Sun May 24 09:21:10 2020

@author: CILENCE_AIR
"""

import requests
import re
import time
import os
import time
import threading
import queue
from progressbar import Bar, Counter, Timer, ETA, FileTransferSpeed, ProgressBar
from pyprobar.styleString import rgb_str
from lxml import etree
dir_name = 'E:/python/download/lcoc/'
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

pageUrl = 'http://www.lcoc.top/bizhi/'
# 定义连续下载的壁纸数目
iteratormax = 10
threadNum = 8

start_index = 1  # 设置起始页面ID


class spiders(threading.Thread):
    name = 1
    def __init__(self, queue, page):
        threading.Thread.__init__(self)
        self.queue = queue
        self.page = page
    def run(self):      # 定义线程开始函数
        while not self.queue.empty():
            url = self.queue.get_nowait()
            self.request_url(url)

    def request_url(self, url):     # 爬取并存储每一页的图片
        response = requests.get(url, headers=headers1, timeout=20000)
        html1 = etree.HTML(response.text)
        urls = html1.xpath(".//li//a[@class='preview']/@href")  # 获取到跳转页面
        files = html1.xpath("//figure/img/@data-src")  # 获取到跳转页面
        urlsLength = len(urls)
        if not urlsLength == 0:
            index = re.findall(r'\d+', str(url))[0]
            # widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ',FileTransferSpeed()]
            widgets = ['第' + str(index) + '页'+'进度: ', Bar('☞'), ' ', Counter(
            ), '/'+str(urlsLength), ' ', Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
            bar = ProgressBar(widgets=widgets, maxval=urlsLength)
            bar.start()
            folder = dir_name + str(index)
            if not os.path.exists(folder):
                os.makedirs(folder)
            for i in range(urlsLength):
                file_name = files[i].split('/')[-1]  # 提取照片格式
                if os.path.exists(folder + '/' + file_name):
                    continue
                try:
                    res = requests.get(urls[i], headers=headers1, timeout=50000)
                    html = etree.HTML(res.text)
                    img_src = html.xpath(".//img[@id='wallpaper']/@src")
                    dowmloadPath = img_src[0]
                    try:
                        responsegraph = requests.get(dowmloadPath, headers=headers1, timeout=50000)
                        with open(folder + '/' + file_name, 'wb') as f:
                                f.write(responsegraph.content)
                                f.close()
                                bar.update(i + 1)
                    except:
                        print('超时')
                except:
                        print('打开' + urls[i] + '失败')
                        continue
                bar.finish()
# 创建多线程函数
def main():
    while True:
        try:
            num = int(input("请输入你想下载的页数："))
            break
        except:
            print("请输入整数!")
    url_queue = queue.Queue()
    thread_list = []    # 线程列表
    for i in range(start_index,num + 1):
        url = pageUrl + str(i)
        url_queue.put(url)
    for i in range(threadNum):
        t = spiders(url_queue, i)
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:0
        t.join()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(str(threadNum) + "线程用时：%f" % (time.time() - start_time))
