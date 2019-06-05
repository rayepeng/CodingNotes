分析一下flask的模板有哪些可以利用的全局变量和上下文



# g

这个全局变量是与请求绑定的



![1555919465859](H:\workspace\code\markdown\picture\1555919465859.png)

# config





![1555919600741](H:\workspace\code\markdown\picture\1555919600741.png)







# request





![1555919664638](H:\workspace\code\markdown\picture\1555919664638.png)



`request.data`得到数据



![1555919695425](H:\workspace\code\markdown\picture\1555919695425.png)







![1555919799266](H:\workspace\code\markdown\picture\1555919799266.png)





# session



![1555919869920](H:\workspace\code\markdown\picture\1555919869920.png)





# url_for()函数

![1555919921843](H:\workspace\code\markdown\picture\1555919921843.png)









# get_flashed_message()

![1555919977419](H:\workspace\code\markdown\picture\1555919977419.png)







但是这些都被过滤了， 也就是说， 要用到python沙箱逃逸的知识



很痛苦对不对， 真不知道别人是怎么构造出来的





# 过滤器相关



![1555920279598](H:\workspace\code\markdown\picture\1555920279598.png)



过滤器似乎可以绕过





常用的内置过滤器有哪些呢？



1. default 设置默认值
2. escape() 转义html文本 也就是将其转化为html实体
3. first() 返回序列的第一个元素
4. last() 返回序列的最后一个元素
5. length() 长度
6. random() 返回序列中的随机元素
7. safe() 标记为安全，避免转义
8. trim() 清除变量前后的空格



但是部分过滤器都有括号。

不过过滤器是不是可以有 **两种使用方式** ？ 

一种是 `{{movie|length}}`

另一种是 `{{movie.length()}}`





szf的博客中写过如果过滤了`[]`的办法， 应该可以参考





我还需要查一下哪些上下文或者全局变量是可以用的



