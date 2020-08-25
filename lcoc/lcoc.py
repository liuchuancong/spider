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
import json
dir_name = 'E:/python/download/lcoc/'
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
categories = ['4K专区',
              '美女模特',
              '爱情美图',
              '风景大片',
              '小清新',
              '动漫卡通',
              '明星风尚',
              '萌宠动物',
              '游戏壁纸',
              '汽车天下',
              '炫酷时尚',
              '月历壁纸',
              '影视剧照',
              '节日美图',
              '军事天地',
              '劲爆体育',
              'BABY秀',
              '文字控']
categoriesValues = [36, 6, 30, 9, 15, 26, 11,
                    14, 5, 12, 10, 29, 7, 13, 22, 16, 18, 35]
pageUrl = 'http://www.lcoc.top/bizhi/api.php?'
# 定义连续下载的壁纸数目
iteratormax = 10
threadNum = 30

start_index = 0  # 设置起始页面ID

selectIndex = 0  # 选择的索引


gap = 30  # 一页三十


class spiders(threading.Thread):
    name = 1

    def __init__(self, queue, page,selectIndex):
        threading.Thread.__init__(self)
        self.queue = queue
        self.page = page
        self.selectIndex = selectIndex
    def run(self):      # 定义线程开始函数
        while not self.queue.empty():
            url = self.queue.get_nowait()
            self.request_url(url)

    def request_url(self, url):     # 爬取并存储每一页的图片
        response = requests.get(url, headers=headers1, timeout=20000)
        html1 = etree.HTML(response.text)
        dict_str = json.loads(response.text)
        errno = dict_str["errno"]
        if not errno == '0':
            print('发生错误')
            exit(0)

        dic_data = dict_str["data"]
        urlsLength = len(dic_data)
        if not urlsLength == 0:
            query = requests.utils.urlparse(url).query
            params = dict(x.split('=') for x in query.split('&'))
            if 'start' in params:
                index = int(int(params['start']) / gap)
                # widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ',FileTransferSpeed()]
                widgets = ['第' + str(index + 1) + '页'+'进度: ', Bar('☞'), ' ', Counter(), '/'+str(urlsLength), ' ', Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
                bar = ProgressBar(widgets=widgets, maxval=urlsLength)
                bar.start()
                folder = dir_name + str(categories[self.selectIndex]) + '/' + str(index + 1)
                if not os.path.exists(folder):
                    os.makedirs(folder)
                for i in range(urlsLength):
                    file_name = dic_data[i]['img_1600_900'].split(
                        '/')[-1]  # 提取照片格式
                    imageUrl = 'https://image.baidu.com/search/down?tn=download&word=download&ie=utf8&fr=detail&url=http://p9.qhimg.com/bdm/2560_1600_100/' + \
                        str(file_name)
                    if os.path.exists(folder + '/' + file_name):
                        continue
                    try:
                        responsegraph = requests.get(
                            imageUrl, headers=headers1, timeout=20000)
                        #有可能返回的是空  排除该图片  重新运行几次即可全部下载  这是爬取接口的问题
                        if not responsegraph.content == b'':
                            with open(folder + '/' + file_name, 'wb') as f:
                                f.write(responsegraph.content)
                                f.close()
                                bar.update(i + 1)
                        else:
                            try:
                                responsegraph = requests.get(
                                    imageUrl, headers=headers1, timeout=20000)
                                #有可能返回的是空  排除该图片  重新运行几次即可全部下载  这是爬取接口的问题
                                if not responsegraph.content == b'':
                                    with open(folder + '/' + file_name, 'wb') as f:
                                        f.write(responsegraph.content)
                                        f.close()
                                        bar.update(i + 1)
                                else:
                                    try:
                                        responsegraph = requests.get(
                                            imageUrl, headers=headers1, timeout=20000)
                                        #有可能返回的是空  排除该图片  重新运行几次即可全部下载  这是爬取接口的问题
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
                print('请输入1-18的整数')
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
        url = pageUrl + 'cid=' + \
            str(categoriesValues[selectIndex]) + \
            '&start=' + str(i * gap) + '&count=' + str(gap)
        url_queue.put(url)
    for i in range(threadNum):
        t = spiders(url_queue, i,selectIndex)
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(str(threadNum) + "线程用时：%f" % (time.time() - start_time))
