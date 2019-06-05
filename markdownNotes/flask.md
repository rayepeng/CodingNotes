# flask

## request

可用的一些属性

### form

一个从POST和PUT请求解析的 MultiDict

### args

MultiDict，要操作 URL （如 ?key=value ）中提交的参数可以使用 args 属性

### values

CombinedMultiDict，内容是`form`和`args`。 
可以使用values替代form和args。

### cookies

类型是dict

### headers

请求头，字典类型。

### data

包含了请求的数据

### files 

### environ

### method

### path

### script_root

### url

### base_url

### url_root

[【Flask】关于Flask的request属性](<https://blog.csdn.net/yannanxiu/article/details/53116652>)



