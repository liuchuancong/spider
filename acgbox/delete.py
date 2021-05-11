import os
 
image_path = 'E:/persion/python/acgbox/'
#  删掉小于1000字节的图片
def get_filelist(file):
    count = 1
    for root, dirs, files in os.walk(file):
        for dir in dirs:
           if os.path.getsize(os.path.join(root, dir)) < 1000:
               os.rmdir(os.path.join(root, dir))
           for s in os.listdir(os.path.join(root, dir)):
                if os.path.getsize(os.path.join(root, dir,s)) < 1000:
                    count+=1
                    os.remove(os.path.join(root, dir,s))   #删除小于1000字节的文件
    print(count)

get_filelist(image_path)
