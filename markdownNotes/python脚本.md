# python小脚本



##  request包

```python
r = request.session() #开启一个session
s = r.post(url, data=)  # post,s是获得的响应


# 比如这个
import requests
import base64
 
s =requests.Session()
headers =s.get("http://123.206.87.240:8002/web6/").headers
str1 = base64.b64decode(headers['flag'])
str2 = base64.b64decode(repr(str1).split(':')[1]) #repr() 函数将对象转化为供解释器读取的形式
data= {'margin':str2}
flag = s.post("http://123.206.87.240:8002/web6/",data=data)
print(flag.text)

```



## 加解密



```python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2018/12/23 09:55:19
@Author  :   HeliantHuS 
@Version :   1.0
@Contact :   1984441370@qq.com
'''

string = input("输入:")
frequency = [] # 获得栅栏的栏数
result_len = len(string)        # 栅栏密码的总长度  25
for i in range(2, result_len):   # 最小栅栏长度为2   逐个测试2,3,4....
    if(result_len % i == 0):        # 当栅栏密码的总长度 模 i 余数为0  则这个i就是栅栏密码的长度
        frequency.append(i)

for numberOfColumn in frequency:   # 循环可能分的栏数
    RESULT = []                 #  保存各栏数的结果
    for i in range(numberOfColumn):     #   i : 开始取值的位置
        for j in range(i, result_len, numberOfColumn):  # 开始取值， 隔栏数取一个值， 起始位置是i
            RESULT.append(string[j])
    print("".join(RESULT))
```



```python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2018/12/23 09:56:53
@Author  :   HeliantHuS 
@Version :   1.0
@Contact :   1984441370@qq.com
'''


import string

inputStr = input("输入:").lower()
caseS1 = string.ascii_lowercase * 2
# caseS1 = string.ascii_uppercase * 2

for j in range(26):
    result_list = []
    for i, num in zip(inputStr, range(len(inputStr))):
        status = caseS1.find(i)
        if status != -1:
            result_list.append(caseS1[status + j])
        else:
            result_list.append(inputStr[num])
    print("".join(result_list), "向右偏移了{}位".format(j))
```




## 杂项
用python分析图片

```python
from PIL import Image
import re

x = 503 #x坐标 通过对txt里的行数进行整数分解
y = 122 #y坐标 x*y = 行数

im = Image.new("RGB",(x,y))#创建图片
file = open('misc80.txt') #打开rbg值文件

#通过一个个rgb点生成图片
for i in range(0,x):
	for j in range(0,y):
        line = file.readline()#获取一行
        rgb = line.split(",")#分离rgb
        im.putpixel((i,j),(int(rgb[0]),int(rgb[1]),int(rgb[2])))#rgb转化为像素
im.show()
```

```python
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'NSimSun,Times New Roman'

x, y = np.loadtxt('1.txt', delimiter=',', unpack=True)
plt.plot(x, y, '.', label='Data', color='black')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Data')
plt.legend()
plt.show()
```

用python实现盲水印：
```python
#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import random

cmd = None
debug = False
seed = 20160930
alpha = 3.0

if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) < 2:
        print 'Usage: python bwm.py <cmd> [arg...] [opts...]'
        print '  cmds:'
        print '    encode <image> <watermark> <image(encoded)>'
        print '           image + watermark -> image(encoded)'
        print '    decode <image> <image(encoded)> <watermark>'
        print '           image + image(encoded) -> watermark'
        print '  opts:'
        print '    --debug,          Show debug'
        print '    --seed <int>,     Manual setting random seed (default is 20160930)'
        print '    --alpha <float>,  Manual setting alpha (default is 3.0)'
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd != 'encode' and cmd != 'decode':
        print 'Wrong cmd %s' % cmd
        sys.exit(1)
    if '--debug' in sys.argv:
        debug = True
        del sys.argv[sys.argv.index('--debug')]
    if '--seed' in sys.argv:
        p = sys.argv.index('--seed')
        if len(sys.argv) <= p+1:
            print 'Missing <int> for --seed'
            sys.exit(1)
        seed = int(sys.argv[p+1])
        del sys.argv[p+1]
        del sys.argv[p]
    if '--alpha' in sys.argv:
        p = sys.argv.index('--alpha')
        if len(sys.argv) <= p+1:
            print 'Missing <float> for --alpha'
            sys.exit(1)
        alpha = float(sys.argv[p+1])
        del sys.argv[p+1]
        del sys.argv[p]
    if len(sys.argv) < 5:
        print 'Missing arg...'
        sys.exit(1)
    fn1 = sys.argv[2]
    fn2 = sys.argv[3]
    fn3 = sys.argv[4]

import cv2
import numpy as np
import matplotlib.pyplot as plt

# OpenCV是以(BGR)的顺序存储图像数据的
# 而Matplotlib是以(RGB)的顺序显示图像的
def bgr_to_rgb(img):
    b, g, r = cv2.split(img)
    return cv2.merge([r, g, b])

if cmd == 'encode':
    print 'image<%s> + watermark<%s> -> image(encoded)<%s>' % (fn1, fn2, fn3)
    img = cv2.imread(fn1)
    wm = cv2.imread(fn2)

    if debug:
        plt.subplot(231), plt.imshow(bgr_to_rgb(img)), plt.title('image')
        plt.xticks([]), plt.yticks([])
        plt.subplot(234), plt.imshow(bgr_to_rgb(wm)), plt.title('watermark')
        plt.xticks([]), plt.yticks([])

    # print img.shape # 高, 宽, 通道
    h, w = img.shape[0], img.shape[1]
    hwm = np.zeros((int(h * 0.5), w, img.shape[2]))
    assert hwm.shape[0] > wm.shape[0]
    assert hwm.shape[1] > wm.shape[1]
    hwm2 = np.copy(hwm)
    for i in xrange(wm.shape[0]):
        for j in xrange(wm.shape[1]):
            hwm2[i][j] = wm[i][j]

    random.seed(seed)
    m, n = range(hwm.shape[0]), range(hwm.shape[1])
    random.shuffle(m)
    random.shuffle(n)
    for i in xrange(hwm.shape[0]):
        for j in xrange(hwm.shape[1]):
            hwm[i][j] = hwm2[m[i]][n[j]]

    rwm = np.zeros(img.shape)
    for i in xrange(hwm.shape[0]):
        for j in xrange(hwm.shape[1]):
            rwm[i][j] = hwm[i][j]
            rwm[rwm.shape[0] - i - 1][rwm.shape[1] - j - 1] = hwm[i][j]

    if debug:
        plt.subplot(235), plt.imshow(bgr_to_rgb(rwm)), \
            plt.title('encrypted(watermark)')
        plt.xticks([]), plt.yticks([])

    f1 = np.fft.fft2(img)
    f2 = f1 + alpha * rwm
    _img = np.fft.ifft2(f2)

    if debug:
        plt.subplot(232), plt.imshow(bgr_to_rgb(np.real(f1))), \
            plt.title('fft(image)')
        plt.xticks([]), plt.yticks([])

    img_wm = np.real(_img)

    assert cv2.imwrite(fn3, img_wm, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    # 这里计算下保存前后的(溢出)误差
    img_wm2 = cv2.imread(fn3)
    sum = 0
    for i in xrange(img_wm.shape[0]):
        for j in xrange(img_wm.shape[1]):
            for k in xrange(img_wm.shape[2]):
                sum += np.power(img_wm[i][j][k] - img_wm2[i][j][k], 2)
    miss = np.sqrt(sum) / (img_wm.shape[0] * img_wm.shape[1] * img_wm.shape[2]) * 100
    print 'Miss %s%% in save' % miss

    if debug:
        plt.subplot(233), plt.imshow(bgr_to_rgb(np.uint8(img_wm))), \
            plt.title('image(encoded)')
        plt.xticks([]), plt.yticks([])

    f2 = np.fft.fft2(img_wm)
    rwm = (f2 - f1) / alpha
    rwm = np.real(rwm)

    wm = np.zeros(rwm.shape)
    for i in xrange(int(rwm.shape[0] * 0.5)):
        for j in xrange(rwm.shape[1]):
            wm[m[i]][n[j]] = np.uint8(rwm[i][j])
    for i in xrange(int(rwm.shape[0] * 0.5)):
        for j in xrange(rwm.shape[1]):
            wm[rwm.shape[0] - i - 1][rwm.shape[1] - j - 1] = wm[i][j]

    if debug:
        assert cv2.imwrite('_bwm.debug.wm.jpg', wm)
        plt.subplot(236), plt.imshow(bgr_to_rgb(wm)), plt.title(u'watermark')
        plt.xticks([]), plt.yticks([])

    if debug:
        plt.show()

elif cmd == 'decode':
    print 'image<%s> + image(encoded)<%s> -> watermark<%s>' % (fn1, fn2, fn3)
    img = cv2.imread(fn1)
    img_wm = cv2.imread(fn2)

    if debug:
        plt.subplot(231), plt.imshow(bgr_to_rgb(img)), plt.title('image')
        plt.xticks([]), plt.yticks([])
        plt.subplot(234), plt.imshow(bgr_to_rgb(img_wm)), plt.title('image(encoded)')
        plt.xticks([]), plt.yticks([])

    random.seed(seed)
    m, n = range(int(img.shape[0] * 0.5)), range(img.shape[1])
    random.shuffle(m)
    random.shuffle(n)

    f1 = np.fft.fft2(img)
    f2 = np.fft.fft2(img_wm)

    if debug:
        plt.subplot(232), plt.imshow(bgr_to_rgb(np.real(f1))), \
            plt.title('fft(image)')
        plt.xticks([]), plt.yticks([])
        plt.subplot(235), plt.imshow(bgr_to_rgb(np.real(f1))), \
            plt.title('fft(image(encoded))')
        plt.xticks([]), plt.yticks([])

    rwm = (f2 - f1) / alpha
    rwm = np.real(rwm)

    if debug:
        plt.subplot(233), plt.imshow(bgr_to_rgb(rwm)), \
            plt.title('encrypted(watermark)')
        plt.xticks([]), plt.yticks([])

    wm = np.zeros(rwm.shape)
    for i in xrange(int(rwm.shape[0] * 0.5)):
        for j in xrange(rwm.shape[1]):
            wm[m[i]][n[j]] = np.uint8(rwm[i][j])
    for i in xrange(int(rwm.shape[0] * 0.5)):
        for j in xrange(rwm.shape[1]):
            wm[rwm.shape[0] - i - 1][rwm.shape[1] - j - 1] = wm[i][j]
    assert cv2.imwrite(fn3, wm)

    if debug:
        plt.subplot(236), plt.imshow(bgr_to_rgb(wm)), plt.title(u'watermark')
        plt.xticks([]), plt.yticks([])

    if debug:
        plt.show()
```


这个GitHub上涵盖了很多python工具[链接](https://github.com/dloss/python-pentest-tools)
