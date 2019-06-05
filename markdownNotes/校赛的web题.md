# 校赛的web题

## waf

这题其实还是要靠抓包， 多分析包中的数据， 就能看到一个`360webscan`的东东

然后就是如何绕过`360webscan`了

[参考](<https://www.leavesongs.com/penetration/360webscan-bypass.html>)

p牛分析了一下`cmseasy`中的`360webscan`

```php
/**
 *  拦截目录白名单
 */
function webscan_white($webscan_white_name,$webscan_white_url_t=array()) {
  $url_path=$_SERVER['PHP_SELF'];
  $url_var=$_SERVER['QUERY_STRING'];
  if (preg_match("/".$webscan_white_name."/is",$url_path)==1) {
    return false;
  }
  foreach ($webscan_white_url_t as $webscan_white_url) {
	  foreach ($webscan_white_url as $key => $value) {
		if(!empty($url_var)&&!empty($value)){
		  if (stristr($url_path,$key)&&stristr($url_var,$value)) {
			return false;
		  }
		}
		elseif (empty($url_var)&&empty($value)) {
		  if (stristr($url_path,$key)) {
			return false;
		  }
		}

	  }
  }
  return true;
}
```

问题的关键在于`$url_path=$_SERVER['PHP_SELF'];`上

PHP_SELF指当前的页面绝对地址

只需要PHP_SELF中含有白名单字段即可绕过

具体到这个waf这个题目上来， 初看起来觉得过滤很严格

其实只要`/index.php/admin/id=3`这样构造就行了。 至于为什么需要加`index.php`那就不是很清楚了



## flask SSTI

这算是一个新姿势了

我们先看一段代码

```python
from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/index')
def index():
    return "hello world"


@app.errorhandler(404)
def page_not_found(e):
    template = '''
{%% block body %%}
    <div class="center-content error">
        <h1>Oops! That page doesn't exist.</h1>
        <h3>%s</h3>
    </div>
{%% endblock %%}
''' % (request.url)
    return render_template_string(template), 404

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')

```

唉，开发者为了省事直接将用户的输入插入到了jinja的模板中

因为jinja只能执行有限地python函数， 所以这种题目和沙箱绕过有很大的关系

### python沙箱逃逸

这个要分版本的

#### python2

