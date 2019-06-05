# python沙箱逃逸



python2和python3的区别



在python2中， 可以直接使用 `__builtin__`

而在python3中， 必须先手动导入 `import builtins`

并且python3中， `'str' object has no attribute 'decode`



## reload

如果是在python2中， 可以直接使用内置的函数

```
__builtin__.open()
__builtin__.int()
__builtin__.chr()
```



`del`可以删除掉内置的函数

但是`reload`又可以重新加载一遍



但是把`reload`干掉就没法用了

在python中,有一个模块叫做imp,是有关引入的一个模块
我们可以使用

```
import imp
imp.reload(__builtin__)
```



## sys

通过`sys.path`可以获知相关路径

如下是我在Windows下的python3

>  ['',
>  'E:\\ProgramFiles\\python\\Scripts\\ipython.exe',
>  'E:\\ProgramFiles\\python\\Scripts',
>  'e:\\programfiles\\python\\python35.zip',
>  'e:\\programfiles\\python\\DLLs',
>  'e:\\programfiles\\python\\lib',
>  'e:\\programfiles\\python',
>  'e:\\programfiles\\python\\lib\\site-packages',
>  'e:\\programfiles\\python\\lib\\site-packages\\turtle-0.0.2-py3.5.egg',
>  'e:\\programfiles\\python\\lib\\site-packages\\pyyaml-4.2b4-py3.5-win-amd64.egg',
>  'e:\\programfiles\\python\\lib\\site-packages\\wc_socket-1.0.0-py3.5.egg',
>  'e:\\programfiles\\python\\lib\\site-packages\\socket_executor-0.1-py3.5.egg',
>  'e:\\programfiles\\python\\lib\\site-packages\\scrapy-1.5.0-py3.5.egg',
>  'e:\\programfiles\\python\\lib\\site-packages\\win32',
>  'e:\\programfiles\\python\\lib\\site-packages\\win32\\lib',
>  'e:\\programfiles\\python\\lib\\site-packages\\Pythonwin',
>  'e:\\programfiles\\python\\lib\\site-packages\\IPython\\extensions',
>  'C:\\Users\\zz\\.ipython']



如果是在Linux环境下

```
In [8]: sys.path
Out[8]: 
['',
 '/usr/local/bin',
 '/usr/lib/python2.7',
 '/usr/lib/python2.7/plat-x86_64-linux-gnu',
 '/usr/lib/python2.7/lib-tk',
 '/usr/lib/python2.7/lib-old',
 '/usr/lib/python2.7/lib-dynload',
 '/home/centurio/.local/lib/python2.7/site-packages',
 '/usr/local/lib/python2.7/dist-packages',
 '/usr/lib/python2.7/dist-packages',
 '/usr/lib/python2.7/dist-packages/gtk-2.0',
 '/usr/lib/python2.7/dist-packages/IPython/extensions']
```

则同样可以看到系统包的路径



`sys.modules`可以查看哪些包

比如在Windows环境下



>{'IPython': <module 'IPython' from 'e:\\programfiles\\python\\lib\\site-packages\\IPython\\__init__.py'>,
> 'IPython.core': <module 'IPython.core' from 'e:\\programfiles\\python\\lib\\site-packages\\IPython\\core\\__init__.py'>,
> 'IPython.core.alias': <module 'IPython.core.alias' from 'e:\\programfiles\\python\\lib\\site-packages\\IPython\\core\\alias.py'>,
> 'IPython.core.application': <module 'IPython.core.application' from 'e:\\programfiles\\python\\lib\\site-packages\\IPython\\core\\application.py'>,
> 'IPython.core.async_helpers': <module 'IPython.core.async_helpers' from 'e:\\programfiles\\python\\lib\\site-packages\\IPython\\core\\async_helpers.py'>,
> 'IPython.core.autocall': <module 'IPython.core.autocall' from 'e:\\programfiles\\python\\lib\\site-packages\\IPython\\core\\autocall.py'>,
> 'IPython.core.builtin_trap': <module 'IPython.core.builtin_trap' from 'e:\\programfiles\\python\\lib\\site-packages\\IPython\\core\\builtin_trap.py'>,
>
>.......

我们可以通过对`sys.modules`进行相关的设置

```
>>> sys.modules['os']=None
>>> import os
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named os
>>> __import__('os')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named os
>>> import importlib
>>> importlib.import_module('os')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "importlib/__init__.py", line 37, in import_module
    __import__(name)
ImportError: No module named os
```



当我们把 `sys.modules['os']`设置为`None`时， 无法导入这个模块了



这时候你肯定疑惑， python导入包的机制是怎样的？



### python如何导入包

> Python import 的步骤
> python 所有加载的模块信息都存放在 sys.modules 结构中，当 import 一个模块时，会按如下步骤来进行
> 如果是 import A，检查 sys.modules 中是否已经有 A，如果有则不加载，如果没有则为 A 创建 module 对象，并加载 A
> 如果是 from A import B，先为 A 创建 module 对象，再解析A，从中寻找B并填充到 A 的 **dict** 中

那么删掉之后， 我们再加回来就是了

```
>>> import sys
>>> sys.modules['os']='/usr/lib/python2.7/os.py'
>>> import os
>>>
```

## impot进阶





## 参考资料

[Python沙箱逃逸的n种姿势](<https://xz.aliyun.com/t/52#toc-4>)

