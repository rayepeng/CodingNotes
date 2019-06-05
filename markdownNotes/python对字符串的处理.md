# python对字符串的处理

```python
In [1]: str = "abcdefg"

In [2]: str[::-1]
Out[2]: 'gfedcba'
```

字符串和列表的切片都是支持三个数字的，也就是两个冒号
a:b:c
代表了提取从 a 到 b(不包括b)
后一个c代表间隔，如果是负数代表反向提取

省略a和b不写，代表从字符串首提取到末尾


# python tuple

tuple也是支持切片操作的

同样是[]运算符，因为其实现了__getitem__魔术方法

