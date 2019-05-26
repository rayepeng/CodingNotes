# php 函数记录

## explode函数

```php
<?php
$str = 'one,two,three,four';

// 零 limit
print_r(explode(',',$str,0)); 
```

explode函数将字符串打散为数组

同时通过第三个参数来控制返回的数组，举例来说
```php
print_r(explode(',', $str, 0)) //Array ( [0] => one,two,three,four )
print_r(explode(',', $str, 2)) //Array ([0] => one [1] => two,three,four )

print_r(explode(',', $str, -1)) //Array([0] => three [1] => two [2] => one)
```

## $_SERVER数组


```php
array(
'DOCUMENT_ROOT' => '当前运行脚本所在的文档根目录。在服务器配置文件中定义。'
'SCRIPT_NAME' => '包含当前脚本的路径。这在页面需要指向自己时非常有用。__FILE__ 常量包含当前脚本(例如包含文件)的完整路径和文件名。'
'PHP_AUTH_USER' =>  '当 PHP 运行在 Apache 或 IIS（PHP 5 是 ISAPI）模块方式下，并且正在使用 HTTP 认证功能，这个变量便是用户输入的用户名。'


)

```
# php命名空间

php中可以通过三种方式使用命名空间


```php
// file1.php

<?php
namespace Foo\Bar\subnamespace; 

const FOO = 1;
function foo() {}
class foo
{
    static function staticmethod() {}
}
?>
```
在file1.php文件中定义了常量，同名的函数和类

```php
//file2.php
//

<?php
namespace Foo\Bar; 
include 'file1.php';

const FOO = 2;
function foo() {}
class foo
{
    static function staticmethod() {}
}

/* 非限定名称 */
foo(); // 解析为函数 Foo\Bar\foo
foo::staticmethod(); // 解析为类 Foo\Bar\foo ，方法为 staticmethod
echo FOO; // 解析为常量 Foo\Bar\FOO

/* 限定名称 */
subnamespace\foo(); // 解析为函数 Foo\Bar\subnamespace\foo
subnamespace\foo::staticmethod(); // 解析为类 Foo\Bar\subnamespace\foo,
                                  // 以及类的方法 staticmethod
echo subnamespace\FOO; // 解析为常量 Foo\Bar\subnamespace\FOO
                                  
/* 完全限定名称 */
\Foo\Bar\foo(); // 解析为函数 Foo\Bar\foo
\Foo\Bar\foo::staticmethod(); // 解析为类 Foo\Bar\foo, 以及类的方法 staticmethod
echo \Foo\Bar\FOO; // 解析为常量 Foo\Bar\FOO
?>
```


全局的命名空间就是 \
```php
<?php
namespace Foo;

function strlen() {}
const INI_ALL = 3;
class Exception {}

$a = \strlen('hi'); // 调用全局函数strlen
$b = \INI_ALL; // 访问全局常量 INI_ALL
$c = new \Exception('error'); // 实例化全局类 Exception
?>
```



# define()函数

定义常量
```php
define('APP_PATH', __DIR__.'/../application/');
```

# require函数


