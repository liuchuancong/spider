import os, shutil
import urllib.request, urllib.error, requests
import threading
import queue
requests.packages.urllib3.disable_warnings()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}

threadNum = 10240
url_m3u8 = 'https://video.dious.cc/20210331/6jRjdZCT/1000kb/hls/index.m3u8'
path = r'E:/python/download/ts/'
# 打开并读取网页内容
def getUrlData(url):
    ts_url_list = []
    with open(r"E:\projects\spider\ts\index.m3u8", "r", encoding="utf-8") as f:
        m3u8Contents = f.readlines()
        for content in m3u8Contents:
            if content.endswith("ts\n"):
                ts_Url = content.replace("\n", "").replace("..", "")
                ts_url_list.append(ts_Url)
    return ts_url_list

class spiders(threading.Thread):
    def __init__(self, queue, page):
        threading.Thread.__init__(self)
        self.queue = queue
        self.page = page
    def run(self):      # 定义线程开始函数
        while not self.queue.empty():
            url = self.queue.get_nowait()
            self.request_url(url)

    def request_url(self, url):     # 爬取并存储每一页的图片
        query = requests.utils.urlparse(url).query
        params = dict(x.split('=') for x in query.split('&'))
        if 'index' in params:
            index = int(params['index']);
            response = requests.get(url, headers,stream=True, verify=False)
            if not response.content == b'':
                            ts_path = path + "\{}.ts".format(index)
                            with open(ts_path, 'wb') as f:
                                f.write(response.content)
                                f.close()
        # print('')



def main():
    url_queue = queue.Queue()
    thread_list = []    # 线程列表
    ts_url_list = getUrlData(url_m3u8)
    print(len(ts_url_list))
    for i in range(len(ts_url_list)):
        url = ts_url_list[i] + '?index=' + str(i)
        url_queue.put(url)
    for i in range(threadNum):
        t = spiders(url_queue, i)
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

if __name__ == '__main__':
    if not os.path.exists(path):
        os.makedirs(path)
    main()