# -*- coding: utf-8 -*-

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
import json
# dir_name = 'E:/python/download/lcoc/'
dir_name = 'E:/极简/'
headers1 = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'content-type': 'application/json'
}
categories = ['人物',
              '精选',
              '二次元']
categoriesValues = ['people', 'index', 'anime']
pageUrl = 'https://api.zzzmh.cn/bz/getJson'

# 线程数
threadNum = 1000

start_index = 1  # 设置起始页面ID

selectIndex = 0  # 选择的索引



class spiders(threading.Thread):
    name = 1

    def __init__(self, queue, page, selectIndex,pageNum):
        threading.Thread.__init__(self)
        self.queue = queue
        self.page = page
        self.selectIndex = selectIndex
        self.pageNum = pageNum
    def run(self):      # 定义线程开始函数
        while not self.queue.empty():
            url = self.queue.get_nowait()
            self.request_url(url)

    def request_url(self, url):     # 
        print(self.pageNum)
        data = {"target":categoriesValues[self.selectIndex],"pageNum":self.pageNum }
        response = requests.post(url, headers=headers1,json=data,timeout=30000)
        html1 = etree.HTML(response.text)
        dict_str = json.loads(response.text)
        errno = dict_str["msg"]
        if not errno == 'success':
            print('发生错误')
            exit(0)

        dic_data = dict_str["result"]['records']
        urlsLength = len(dic_data)
        if not urlsLength == 0:
            # widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ',FileTransferSpeed()]
            widgets = ['第' + str(self.pageNum) + '页'+'进度: ', Bar('☞'), ' ', Counter(), '/'+str(
                urlsLength), ' ', Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
            bar = ProgressBar(widgets=widgets, maxval=urlsLength)
            bar.start()
            # folder = dir_name + str(categories[self.selectIndex]) + '/' + str(index + 1)
            folder = dir_name
            if not os.path.exists(folder):
                os.makedirs(folder)
            for i in dic_data:
                isJpg = '.jpg' if i['t'] == 'j' else'.png'
                file_name = i['i'] + isJpg
                path_folder = str(i['i'])[0:2]
                # url = 
                imageUrl = 'https://w.wallhaven.cc/full/' + path_folder + '/' + 'wallhaven-' + str(file_name)
                if os.path.exists(folder + '/' + file_name):
                    continue
                try:
                    responsegraph = requests.get(
                        imageUrl, headers=headers1, timeout=30000)
                    # 有可能返回的是空  排除该图片  重新运行几次即可全部下载  这是爬取接口的问题
                    if not responsegraph.content == b'':
                        with open(folder + '/' + file_name, 'wb') as f:
                            f.write(responsegraph.content)
                            f.close()
                            bar.update(i + 1)
                    else:
                        try:
                            responsegraph = requests.get(
                                imageUrl, headers=headers1, timeout=30000)
                            # 有可能返回的是空  排除该图片  重新运行几次即可全部下载  这是爬取接口的问题
                            if not responsegraph.content == b'':
                                with open(folder + '/' + file_name, 'wb') as f:
                                    f.write(responsegraph.content)
                                    f.close()
                                    bar.update(i + 1)
                            else:
                                try:
                                    responsegraph = requests.get(
                                        imageUrl, headers=headers1, timeout=30000)
                                    # 有可能返回的是空  排除该图片  重新运行几次即可全部下载  这是爬取接口的问题
                                    if not responsegraph.content == b'':
                                        with open(folder + '/' + file_name, 'wb') as f:
                                            f.write(responsegraph.content)
                                            f.close()
                                            bar.update(i + 1)
                                except:
                                    print('打开' + imageUrl + '失败')
                                    continue
                        except:
                            print('打开' + imageUrl + '失败')
                            continue
                except:
                    print('打开' + imageUrl + '失败')
                    continue
                bar.finish()
# 创建多线程函数


def main():
    categoriesStr = ''  # 分类字符
    for i in range(len(categories)):
        categoriesStr += str(i+1)+' ' + categories[i] + '\n'
    print(categoriesStr)
    while True:
        try:
            category = int(input("请输入你想下载的分类："))
            if category >= 1 and category <= 18:
                selectIndex = category - 1
                break
            else:
                print('请输入1-3的整数')
        except:
            print("请输入整数!")
    while True:
        try:
            num = int(input("请输入你想下载的页数："))
            break
        except:
            print("请输入整数!")
    url_queue = queue.Queue()
    thread_list = []    # 线程列表
    for i in range(start_index, num + 1):
        url = pageUrl
        url_queue.put(url)
        for j in range(threadNum):
            t = spiders(url_queue, j, selectIndex,i)
            thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
        


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(str(threadNum) + "线程用时：%f" % (time.time() - start_time))
