# Re1

![1555928821257](H:\workspace\code\markdown\picture\1555928821257.png)



一开始有一条call指令



经历过call指令之后





# IDA分析



![1555929166202](H:\workspace\code\markdown\picture\1555929166202.png)



![1555929603057](H:\workspace\code\markdown\picture\1555929603057.png)





![1555930014180](H:\workspace\code\markdown\picture\1555930014180.png)

这一段逻辑基本看懂了

`try_again()`函数和 `Judge_win()`函数



接下来重点看中间的几个函数

## 先看一下 `sub_4011B0()`函数

![1555930233736](H:\workspace\code\markdown\picture\1555930233736.png)



令人疑惑的是这个函数调用的时候就是纯粹的调用了。并没有返回什么东西



## `sub_401EF0()`函数

![1555930330858](H:\workspace\code\markdown\picture\1555930330858.png)

这个函数的三个参数如下， BYTE， char， 何一个有符号的int

传入的实参

![1555930374523](H:\workspace\code\markdown\picture\1555930374523.png)



也就是a1 = v3(指针传递), a2=0， a3=50



![1555930811010](H:\workspace\code\markdown\picture\1555930811010.png)





差点忘记了 `*v4++` 的意思了

v4存放的是v3的地址， 也就是先 `*v3`赋值为 0， 然后`v4++`指向了下一个地址

同时由于 50, 49, 48 

分别是 0010, 0001, 0000, 

所以第三次就直接跳出去了， 只执行了两次



![1555931240394](H:\workspace\code\markdown\picture\1555931240394.png)



这里还有一个逻辑没看懂

![1555931508781](H:\workspace\code\markdown\picture\1555931508781.png)

