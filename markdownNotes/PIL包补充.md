# 记录一下python的PIL包

## 常用方法

from PIL import Image

获取图片的宽度和高度
    width = im.size[0]
    height = im.size[1]

获得指定位置的像素点

    pixel = im.getpixel((w,h)) # 得到像素点 getpixel方法传入的是一个tuple 获取像素 返回三元组

设置指定像素点的值
    im.putpixel((w, h), (a,b,c))

保存
    im.save(str3) # str3是路径


# 实现LSB隐写的方法

LSB的想法很简单，就是修改每一个像素点的最后一位

问题： 怎么修改二进制数的最后一位改成我们想要的

```python
def leastBit(intDec):
	# 得到其最后一位
	# strBin = str(intbin)
	# return int(strBin[-1])
	strBin = bin(intDec)
	strBin.replace('0b', '')
	return int(strBin[-1])


# 对最后一位进行设置
def InsertBit(SingleBit, intDec):
	# strBin = str(intbin)
	# strBin[-1] = SingleBit
	# return int(strBin)
	# 
	# strBinList = list(strBin)
	# strBinList[-1] = SingleBit
	# rtnStrBin = ""
	# rtnStrBin.join(strBinlist)	
	strBin = bin(intDec)
	strBin.replace('0b', '')
	strBin[-1] = SingleBit
	return int(strBin, 2)	 #返回的是十进制

```
这样之后我尝试修改代码

```python
def myfunc(str1, str2, str3):
    im = Image.open(str1)  # 打开文件
    width = im.size[0]
    print("width:"+str(width)+"\n")
    height = im.size[1]
    print("hight:"+str(height)+"\n")

    key = get_key(str2)
	keylen = len(key)
	count = 0
	for h in range(0, height):

		for w in range(0,width):
			pixel = im.getpixel((w,h))
            r = pixel[0]  # 获取r，g, b
            g = pixel[1]
            b = pixel[2]
            if count == keylen:
                break

            InsertBit(key[count], r)
            count += 1
            if count == keylen:
                im.putpixel((w,h),(a,b,c))  # 设置某个像素点的颜色
                break

            InsertBit(key[count], g)
            count += 1
            if count == keylen:
                im.putpixel((w,h),(a,b,c))  # 设置某个像素点的颜色
                break

            InsertBit(key[count], b)
            count += 1
            if count == keylen:
                im.putpixel((w,h),(a,b,c))  # 设置某个像素点的颜色
                break

            if count % 3 == 0:
                im.putpixel((w,h),(a,b,c))  # 设置某个像素点的颜色

    im.save(str3)



