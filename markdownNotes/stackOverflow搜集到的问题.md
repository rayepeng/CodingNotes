# 从StackOverflow上搜集到的问题

## python3的str

```python
AttributeError: 'str' object has no attribute 'decode'
```

python3中是Unicode编码的， 不需要decode('utf-8')了



```python
import imaplib
from email.parser import HeaderParser

conn = imaplib.IMAP4_SSL('imap.gmail.com')
conn.login('example@gmail.com', 'password')
conn.select()
conn.search(None, 'ALL')
data = conn.fetch('1', '(BODY[HEADER])')
header_data = data[1][0][1].decode('utf-8')
```



## endswith first arg must be str or a tuple of str, not bool



代码如下：

```python
s = 'like go goes likes liked liked liking likes like'
lst = s.split()
suffixes = ['s', 'es', 'ies', 'ed', 'ing']

counter = 0
prompt = 'like'
for x in lst:
    if x.startswith(prompt) and x.endswith(any(suffix for suffix in suffixes)):
         counter += 1
```



最佳回答是：

```python
x.endswith(tuple(suffixes))
```