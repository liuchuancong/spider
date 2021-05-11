# -*- coding: utf-8 -*-
from webbrowser import open as webopen
import requests
import re
import os
import threading
import queue
from lxml import etree
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
dir_name = ''

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
threadNum = 300

start_index = 0  # 设置起始页面ID

selectIndex = 0  # 选择的索引


gap = 30  # 一页三十


class spiders(threading.Thread):
    name = 1

    def __init__(self, queue, page, selectIndex,calc_count):
        threading.Thread.__init__(self)
        self.queue = queue
        self.page = page
        self.selectIndex = selectIndex
        self.calc_count = calc_count

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
            exit(0)
        dic_data = dict_str["data"]
        urlsLength = len(dic_data)
        if not urlsLength == 0:
            query = requests.utils.urlparse(url).query
            params = dict(x.split('=') for x in query.split('&'))
            if 'start' in params:
                index = int(int(params['start']) / gap)
                # folder = dir_name + str(categories[self.selectIndex]) + '/' + str(index + 1)
                folder = dir_name
                if not os.path.exists(folder):
                    os.makedirs(folder)
                for i in range(urlsLength):
                    file_name = dic_data[i]['img_1600_900'].split(
                        '/')[-1]  # 提取照片格式
                    imageUrl = 'https://image.baidu.com/search/down?tn=download&word=download&ie=utf8&fr=detail&url=http://p9.qhimg.com/bdm/0_0_100/' + \
                        str(file_name)
                    if os.path.exists(folder + '/' + file_name):
                        continue
                    try:
                        responsegraph = requests.get(
                            imageUrl, headers=headers1, timeout=20000)
                        # 有可能返回的是空  排除该图片  重新运行几次即可全部下载  这是爬取接口的问题
                        if not responsegraph.content == b'':
                            with open(folder + '/' + file_name, 'wb') as f:
                                f.write(responsegraph.content)
                                f.close()
                            self.calc_count()
                        else:
                            try:
                                responsegraph = requests.get(
                                    imageUrl, headers=headers1, timeout=20000)
                                # 有可能返回的是空  排除该图片  重新运行几次即可全部下载  这是爬取接口的问题
                                if not responsegraph.content == b'':
                                    with open(folder + '/' + file_name, 'wb') as f:
                                        f.write(responsegraph.content)
                                        f.close()
                                    self.calc_count()
                                else:
                                    try:
                                        responsegraph = requests.get(
                                            imageUrl, headers=headers1, timeout=20000)
                                        # 有可能返回的是空  排除该图片  重新运行几次即可全部下载  这是爬取接口的问题
                                        if not responsegraph.content == b'':
                                            with open(folder + '/' + file_name, 'wb') as f:
                                                f.write(responsegraph.content)
                                                f.close()
                                            self.calc_count()
                                    except:
                                        continue
                            except:
                                continue
                    except:
                        continue
# 创建多线程函数


class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("壁纸下载")
        self.init_window_name.geometry('500x500')

        #链接
        self.text_link_label=tk.Label(self.init_window_name,width=10, text="电脑壁纸:")
        self.text_link_label.place(x=10, y=10)

        self.text_link=tk.Label(self.init_window_name, text="http://www.lcoc.top/bizhi",fg = "#1989fa")
        self.text_link.bind('<Button-1>', lambda x: webopen('http://www.lcoc.top/bizhi',2))
        self.text_link.place(x=80, y=10)
        
        #按钮
        self.directory_button_label= tk.StringVar()
        self.directory_button_label.set("") 
        
        self.directory_button = tk.Button(self.init_window_name, text="选择下载目录", bg="#1989fa",fg="#fff", width=10,command=self.getDownLoadDirectory)  # 调用内部方法  加()为直接调用
        self.directory_button.place(x=20, y=40)

        #标签
        self.result_directory_name_label = tk.Label(self.init_window_name, textvariable=self.directory_button_label,font=('microsoft yahei',10))
        self.result_directory_name_label.bind('<Button-1>', lambda x: self.open_directory())
        self.result_directory_name_label.place(x=120, y=42)

        # 指定Radiobutton的事件处理函数

        self.radio_value = tk.IntVar()
        self.radio_value.set(0)
        self.getLoopRadio()
        #页数

                
        entry_input_Label = tk.Label(self.init_window_name, text='请输入下载页数：')
        entry_input_Label.place(x=20, y=300)

        self.pageNum = tk.StringVar()   # 这即是输入框中的内容
        self.pageNum.set(1)
        self.entry_input = tk.Entry(self.init_window_name, textvariable= self.pageNum,width=10)  # 设置"文本变量"为var
        self.entry_input.place(x=120, y=302)

        
        #按钮
        self.directory_button = tk.Button(self.init_window_name, text="下载", bg="#1989fa",fg="#fff", width=8,command=self.down_file)  # 调用内部方法  加()为直接调用
        self.directory_button.place(x=200, y=298)

        #页数

                
        down_count_Label = tk.Label(self.init_window_name, text='已下载：')
        down_count_Label.place(x=20, y=340)

        self.down_count = tk.IntVar()   # 这即是输入框中的内容
        self.down_count.set(0)
        self.down_count_label = tk.Label(self.init_window_name, textvariable= self.down_count,width=10)  # 设置"文本变量"为var
        self.down_count_label.place(x=120, y=340)

        
        self.directory_button = tk.Label(self.init_window_name, text="张")  # 调用内部方法  加()为直接调用
        self.directory_button.place(x=200, y=340)
    #功能函数

    def calc_count(self):
        count = self.down_count.get()
        count = count + 1
        self.down_count.set(count)
    def open_directory(self):
        if not dir_name == '':
            os.startfile(dir_name)
    def getDownLoadDirectory(self):
        '''打开选择文件夹对话框'''
        global dir_name
        dir_name = filedialog.askdirectory()  # 获得选择好的文件夹
        if dir_name == '':
            result =  messagebox.showwarning('警告','请先选择下载目录')
        else:
            self.directory_button_label.set(dir_name)

    def getLoopRadio(self):
        for i in range(len(categories)):
            rb_function_Label = tk.Label(self.init_window_name, text=str(i + 1) + '.',anchor='se')
            rb_function = tk.Radiobutton(self.init_window_name, variable= self.radio_value,  text=categories[i], value = i)
            if i % 2 == 0:
                rb_function_Label.place(x=80, y=72 + 10 * (i + 1))
                rb_function.place(x=100, y=72 + 10 * (i + 1))
            else:
                rb_function_Label.place(x=80 + 100, y=72 + 10 * i)
                rb_function.place(x=100 +  100, y=72 + 10 * i)

    def down_file(self):
        self.down_count.set(0)
        if dir_name == '':
            messagebox.showwarning('警告','请先选择下载目录')
        else:
            try:
                num = int(self.pageNum.get())
                down_load(self.radio_value.get(),num,self.calc_count)
            except:
                messagebox.showwarning('警告','下载页数大于0')

def main():
    gui_start()



def gui_start():
    init_window  = tk.Tk()
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

def down_load(selectIndex,num,calc_count):
    url_queue = queue.Queue()
    thread_list = []    # 线程列表
    for i in range(start_index, num):
        url = pageUrl + 'cid=' + \
            str(categoriesValues[selectIndex]) + \
            '&start=' + str(i * gap) + '&count=' + str(gap)
        url_queue.put(url)
    for i in range(threadNum):
        t = spiders(url_queue, i, selectIndex,calc_count)
        thread_list.append(t)
    for t in thread_list:
        t.setDaemon(True) 
        t.start()

if __name__ == '__main__':
    main()
