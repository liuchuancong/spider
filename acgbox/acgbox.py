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
dir_name = 'E:/persion/python/download/'
cookie = '''__cfduid=d256797305602e2363ffebabbbca8a1241594915605; _ga=GA1.2.202326394.1594915637; _gid=GA1.2.830997817.1594915637; Hm_lvt_761a739b07691faaf387795b881a824f=1594573015,1594575128,1594743471,1594998827; _gat_gtag_UA_163211905_1=1'''
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie': cookie
}

pageUrl = 'https://tu.acgbox.org/index.php/archives/'
# 定义连续下载的写真集数目
iteratormax = 300
threadNum = 300

start_index = 0  # 设置起始页面ID


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
        response = requests.get(url, headers=headers1)
        html = (response.text)
        html1 = etree.HTML(html)
        urls = html1.xpath('//img/@data-original')
        urlsLength = len(urls)
        if not urlsLength == 0:
            # widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ',FileTransferSpeed()]
            widgets = ['进度: ', Bar('☞'), ' ', Counter(
            ), '/'+str(urlsLength), ' ', Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
            bar = ProgressBar(widgets=widgets, maxval=urlsLength)
            bar.start()
            # titles = re.findall('https://img.*?.jpg', html1)
            titles = html1.xpath(
                "//div[@class='post-item col-xs-6 col-sm-4 col-md-3 col-lg-2']/img/@title")
            index = re.findall(r'\d+', str(url))[0]
            folder = dir_name + str(index)
            if not os.path.exists(folder):
                os.makedirs(folder)
            for i in range(urlsLength):
                file_name = urls[i].split('.')[-1]  # 提取照片格式
                if os.path.exists(folder + '/' + titles[i]+'.' + file_name):
                    continue
                try:
                    responsegraph = requests.get(urls[i], headers=headers1, timeout=10)
                    with open(folder + '/' + titles[i]+'.' + file_name, 'wb') as f:
                            f.write(responsegraph.content)
                            f.close()
                            bar.update(i + 1)        
                except:
                        print('超时，下载下一张图片')
                        continue

                bar.finish()
            print('第' + str(index) + '页' + str(urlsLength) + '张')

# 创建多线程函数


def main():
    url_queue = queue.Queue()
    thread_list = []    # 线程列表
    for i in range(iteratormax):
        url = pageUrl + str(i) + '/'
        url_queue.put(url)
    for i in range(threadNum):
        t = spiders(url_queue, i)
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(str(threadNum) + "线程用时：%f" % (time.time() - start_time))
