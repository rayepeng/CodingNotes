# python各种数据类型的抓换

list和str

list变成str

比如
str = "".join(list)

就是将list中的每个元素都进行合并，用""作为连接符

str变成list
可以直接 list(str)
也可以通过分隔符
str.split(" ") # 中间必须有值


# python3中的byte类型

python3中的文本总是Unicode，用str来表示
二进制数据流则由bytes类型表示

```python
In [28]: type(s)
Out[28]: str

In [29]: s.encode('utf-8')
Out[29]: b'\xe4\xb8\xad\xe6\x96\x87'

In [30]: b = s.encode('utf-8')

In [31]: b
Out[31]: b'\xe4\xb8\xad\xe6\x96\x87'

In [32]: b.decode('gbk')

# 报错

In [33]: b.decode('utf-16')
Out[33]: '룤\ue6ad螖'

In [34]: b.decode('utf-16be')
Out[34]: '\ue4b8귦隇'

In [35]: b.decode('utf-8')
Out[35]: '中文'

```

> 如果你用二进制方式去打开文件，那么调用read方法时返回的数据就是bytes类型的


# python 各种进制之间的转换

各种进制到十进制
```python
In [40]: int('0xf', 16)
Out[40]: 15

In [41]: int('00001111000', 2)
Out[41]: 120

In [42]: int('01237',8)
Out[42]: 671

In [43]: int('1237',8)
Out[43]: 671

In [44]: int('f', 16)
Out[44]: 15
```

十进制转十六进制可以用hex函数
二进制转十六进制就是先转十进制，再转成十六进制
八进制转十六进制，就是八进制先转十进制再转十六进制

oct可以将任意进制的数转八进制

```python
# ascii编码转换
In [47]: ord('a')
Out[47]: 97

In [48]: chr(97)
Out[48]: 'a'
```



