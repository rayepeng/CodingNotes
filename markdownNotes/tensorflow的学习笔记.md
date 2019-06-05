# tensorflow的学习笔记

## numpy相关

## panda相关



## 开始！

### 创建图， 启动图



按照惯例

```python
import tensorflow as tf
```



#### 常量op

```python
m1 = tf.constant([[3,3]])
m2 = tf.constant([[2],[3]])
```



这个时候只是创建了两个op， 但是并没有得到计算结果

这是`print(m1)`的结果



```python
Tensor("Const_2:0", shape=(1, 2), dtype=int32)
```



如果是直接输入m1， 得到的结果是：

```python
<tf.Tensor 'Const_8:0' shape=(1, 2) dtype=int32>
```

或者我们直接 `type(m1)`

得到的结果：

```python
tensorflow.python.framework.ops.Tensor
```

（所以只要我们没有启动一个会话， 就无法得到结果）

我们可以对`op`进行操作

```python
product = tf.matmul(m1,m2)
print(product)
```

这个时候得到的结果是：

```python
Tensor("MatMul_1:0", shape=(1, 1), dtype=int32)
```



#### 启动会话

如果我们要得到结果：

那就启动一个会话吧！

```python
with tf.Session() as sess:
    # 使用sess的run方法来执行矩阵乘法op
    result = sess.run(product)
print(result)
print(type(result))
```



这个时候我们就得到结果了：

```python
[[15]]
<class 'numpy.ndarray'>
```



### 变量

之前我们用 `tf.constant()`创建了常量op

我们可以使用 `tf.Variable()`创建变量

```python
x = tf.Variable([1,2])
a = tf.constant([3,3])
```

同样的我们打印一下看一看

```python
<tf.Variable 'Variable_2:0' shape=(2,) dtype=int32_ref>
```

我们看到是 `Variable`类型的



### 函数的op(不是很理解)

```python
# 增加一个减法op
sub = tf.subtract(x,a)
# 增加一个加法op
add = tf.add(a,sub)
```



我们打印一下试试看？

`print(add)`的结果如下：

```python
Tensor("Add_2:0", shape=(2,), dtype=int32)
```





#### 全局初始化函数



引入了变量我们自然就需要进行初始化了

使用这个函数

```python
tf.global_variables_initializer()
```



同样的我们开始：



#### 启动会话

```python
with tf.Session() as sess:
    sess.run(init)
    print(x.value)
    print(sess.run(sub))
    print(sess.run(add))
```



注意到这里有一个 `sess.run(init)`进行初始化的操作

得到的结果如下：

```python
<bound method Variable.value of <tf.Variable 'Variable_1:0' shape=(2,) dtype=int32_ref>>
[-2 -1]
[1 2]
```

