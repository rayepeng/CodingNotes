# ASP.NET语法快速入门

## 三种顺序结构

for 循环 和 foreach循环

```asp
@for(var i = 10; i < 21; i++)
{
<p>Line @i</p>
}
```



```asp
@foreach (var x in Request.ServerVariables)
    {<li>@x</li>}
```



可以猜测`Request`应该是一个对象

程序运行的结果如下：猜测应该是`Request`的服务变量

```
ALL_HTTP
ALL_RAW
APPL_MD_PATH
APPL_PHYSICAL_PATH
AUTH_PASSWORD
AUTH_TYPE
AUTH_USER
CERT_COOKIE
CERT_FLAGS
CERT_ISSUER
CERT_KEYSIZE
CERT_SECRETKEYSIZE
CERT_SERIALNUMBER
CERT_SERVER_ISSUER
CERT_SERVER_SUBJECT
CERT_SUBJECT
CONTENT_LENGTH
CONTENT_TYPE
GATEWAY_INTERFACE
HTTPS
HTTPS_KEYSIZE
HTTPS_SECRETKEYSIZE
HTTPS_SERVER_ISSUER
HTTPS_SERVER_SUBJECT
INSTANCE_ID
INSTANCE_META_PATH
LOCAL_ADDR
LOGON_USER
PATH_INFO
PATH_TRANSLATED
QUERY_STRING
REMOTE_ADDR
REMOTE_HOST
REMOTE_USER
REQUEST_METHOD
SCRIPT_NAME
SERVER_NAME
SERVER_PORT
SERVER_PORT_SECURE
SERVER_PROTOCOL
SERVER_SOFTWARE
URL
HTTP_ACCEPT
HTTP_HOST
```



while 循环

```asp
@{
var i = 0;
while (i < 5)
    {
    i += 1;
    <p>Line @i</p>
    }
}
```



if判断

```asp
@if (price>30)
  {
  <p>The price is too high.</p>
  }
```



if-else判断

```asp
@if (price>30)
    {
    <p>The price is too high.</p>
    }
    else
    {    
    <p>The price is OK.</p>
    }
```

switch语句也很类似

```asp
@{
var message="";
var weekday=DateTime.Now.DayOfWeek;
var day=weekday.ToString()
}
@switch(day)
{
case "Monday":
    message="This is the first weekday.";
    break;
case "Thursday":
    message="Only one day before weekend.";
    break;
case "Friday":
    message="Tomorrow is weekend!";
    break;
default:
    message="Today is " + day;
    break;
```





## 数据类型

最常用的就是数组啦， 还有整形， 字符，字符串类型等

```asp
string[] members = {"Jani", "Hege", "Kai", "Jim"};
int i = Array.IndexOf(members, "Kai")+1;
int len = members.Length;
string x = members[2-1];
```

之后调用`foreach`循环就可以遍历数组了

```asp
@foreach (var person in members)
{
<p>@person</p>
}
```



变量声明可以直接用`var`，是不是也可以用`int`或者`string`等

## 时间和日期

```asp
@DateTime.Now
```



## 进阶语法

### 数据库

首先要连接数据库，然后查询，返回数值并打印出来

```asp
@{
var db = Database.Open("SmallBakery"); 
var query = "SELECT * FROM Product"; 
}

@foreach(var row in db.Query(query))
{
<tr> 
<td>@row.Id</td> 
<td>@row.Name</td> 
<td>@row.Description</td> 
<td align="right">@row.Price</td> 
</tr> 
```

可以看到`Database`调用了`Open`方法， 打开一个数据库， 之后还会调用`Query`方法，返回一个对象

# ASP.NET结合C#学习

## HttpContext 学习

> HttpContext类对Request、Respose、Server等等都进行了封装,并保证在整个请求周期内都可以随时随地的调用

	生存周期：从客户端用户点击并产生了一个向服务器发送请求开始---服务器处理完请求并生成返回到客户端为止。针对每个不同用户的请求，服务器都会创建一个新的HttpContext实例直到请求结束,服务器销毁这个实例



## NameValueCollection集合类(C#)

> 该类在一个键下存储多个字符串值（就是键相同，值就连接起来如下例子）。该类可用于标头、查询字符串和窗体数据。



