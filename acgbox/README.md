
# 多线程抓取acgbox的妹子图片

抓取网址:`https://tu.acgbox.org/`

密码:acgbox

## 设置

`dir_name`: 文件夹名称自行设置(默认:E:/persion/python/download/)

`cookie`: 自己登录网址然后F12复制cookie

`iteratormax`: 网址的页码(估计只有不到300)

`threadNum`: 线程数(开了300个 8.5G图片用了10minutes)

`folder`:文件夹名称(index = re.findall(r'\d+', str(url))[0]) 数字

### 运行

`python acgbox.py`
