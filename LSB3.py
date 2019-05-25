ef plus(str):
    # Python zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。
    return str.zfill(8)

def get_key(strr):
    # 获取要隐藏的文件内容
    tmp = strr;
    f = open(tmp, "rb");
    Str = ""
    s = f.read() # s 是 byte类型
    for i in s:
        Str = Str + plus(bin(i).replace('0b', ''))
    f.close()
    return Str


def InsertBit(SingleBit, intDec):
    strBin = bin(intDec)
    strBin.replace('0b', '')
    strBinList = list(strBin)
    strBinList[-1] = SingleBit
    rtnStrBin = "".join(strBinList)
    return int(rtnStrBin, 2)


def myfunc(str1, str2, str3):
    im = Image.open(str1)  # 打开文件
    width = im.size[0]
  
    height = im.size[1]
  

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
                im.putpixel((w,h),(r,g,b))  # 设置某个像素点的颜色
                break

            InsertBit(key[count], g)
            count += 1
            if count == keylen:
                im.putpixel((w,h),(r,g,b))  # 设置某个像素点的颜色
                break

            InsertBit(key[count], b)
            count += 1
            if count == keylen:
                im.putpixel((w,h),(r,g,b))  # 设置某个像素点的颜色
                break

            if count % 3 == 0:
                im.putpixel((w,h),(r,g,b))  # 设置某个像素点的颜色

    im.save(str3)

old = "taxi.png"
new = "tttt.png"
enc = "abc.txt"
func(old, enc, new)
