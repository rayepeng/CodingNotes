from PIL import Image


def plus(str):
    # Python zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。
    return str.zfill(8) 

# print(plus("afaas"))

def get_key(strr):
    # 获取要隐藏的文件内容
    tmp = strr;
    f = open(tmp, "rb"); # rb 只读加二进制形式打开
    Str = ""
    s = f.read() # s 是 byte类型
    for i in s:
        Str = Str + plus(bin(i).replace('0b', ''))
    f.close()
    return Str

def mod(x, y):
    return x%y


def func(str1, str2, str3):  #接收三个参数 第一个str1是原来的图片，第二个str2是要隐写的数据，第三个是输出的图片
    im = Image.open(str1)  # 打开文件
    width = im.size[0]
    print("width:"+str(width)+"\n")
    height = im.size[1]
    print("hight:"+str(height)+"\n")
    count = 0

    key = get_key(str2)
    keylen = len(key)
    for h in range(0, height):
        for w in range(0, width):
            pixel = im.getpixel((w,h)) # 得到像素点 getpixel方法传入的是一个tuple 获取像素 返回三元组
            a = pixel[0]  # 获取r，g, b
            b = pixel[1]
            c = pixel[2]
            if count == keylen:
                break
            a = a-mod(a,2)+int(key[count])
            count += 1

            if count == keylen:
                im.putpixel((w,h),(a,b,c))  # 设置某个像素点的颜色
                break
            b = b - mod(b,2)+int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a,b,c))
                break
            if count % 3 ==0:
                im.putpixel((w,h), (a,b,c))
    im.save(str3)

old = "taxi.png"
new = "tttt.png"
enc = "abc.txt"

func(old, enc, new)





# print(get_key("abc.txt"))
# f = open("abc.txt", "rb") # 打开一个文件，返回一个文件对象
# Str = f.read() #调用read方法可以获得文件的内容
#
# bin_Str = ""
# for i in Str:
#     # print(bin(i), end=" ")  # 0b1100110
#     bin_Str += plus(bin(i)).replace('0b', '')
#
# print(bin_Str)


