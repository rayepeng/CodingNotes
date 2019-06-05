# google ctf2018

## js is_safe

从入门开始调试JavaScript代码

这个题目里面有几个关键的函数

```javascript
            function x(х) {
                ord = Function.prototype.call.bind(''.charCodeAt);
                chr = String.fromCharCode;
                str = String;
                function h(s) {
                    for (i = 0; i != s.length; i++) {
                        a = ((typeof a == 'undefined' ? 1 : a) + ord(str(s[i]))) % 65521;
                        b = ((typeof b == 'undefined' ? 0 : b) + a) % 65521
                    }
                    return chr(b >> 8) + chr(b & 0xFF) + chr(a >> 8) + chr(a & 0xFF)
                }
                function c(a, b, c) {
                    for (i = 0; i != a.length; i++)
                        c = (c || '') + chr(ord(str(a[i])) ^ ord(str(b[i % b.length])));
                    return c
                }
                for (a = 0; a != 1000; a++)
                    debugger ;
                x = h(str(x));
                source = /Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/;
                source.toString = function() {
                    return c(source, x)
                }
                ;
                try {
                    console.log('debug', source);
                    with (source)
                        return eval('eval(c(source,x))')
                } catch (e) {}
            }
```

和一个验证函数`open_safe()`

```javascript
            function open_safe() {
                keyhole.disabled = true;
                password = /^CTF{([0-9a-zA-Z_@!?-]+)}$/.exec(keyhole.value);
                if (!password || !x(password[1]))
                    return document.body.className = 'denied';
                document.body.className = 'granted';
                password = Array.from(password[1]).map(c=>c.charCodeAt());
                encrypted = JSON.parse(localStorage.content || '');
                content.value = encrypted.map((c,i)=>c ^ password[i % password.length]).map(String.fromCharCode).join('')
            }
            function save() {
                plaintext = Array.from(content.value).map(c=>c.charCodeAt());
                localStorage.content = JSON.stringify(plaintext.map((c,i)=>c ^ password[i % password.length]));
            }
```



当我们填写表单的时候就会调用`open_safe()`函数

```javascript
<input id="keyhole" autofocus onchange="open_safe()" placeholder="🔑">
```

当我们输入`CTF{AAAABBBB}`的时候，

在`<input id="keyhole" autofocus onchange="open_safe()" placeholder="🔑">`加断点

在`console`开启`debugger`模式，由于不是很熟悉JavaScript的数据类型所以先看了一下几个变量的值

```javascript
> password
(2) ["CTF{AAAABBBB}", "AAAABBBB", index: 0, input: "CTF{AAAABBBB}", groups: undefined]
> password[1]
"AAAABBBB"
> keyhole
<input id="keyhole" autofocus onchange="open_safe()" placeholder="🔑" disabled>
> keyhole.value
"CTF{AAAABBBB}"
```



之后调用了`x`函数， JavaScript有一个比较神奇的特性

```javascript
                ord = Function.prototype.call.bind(''.charCodeAt);
                chr = String.fromCharCode;
                str = String;
//这样就得到了函数
```

但是之后就进入了死循环

```javascript
                for (a = 0; a != 1000; a++)
                    debugger ;
```



ok那我们就直接把这段循环给变成空的， 但是问题来了， 注意到

```javascript
 function h(s) {
                    for (i = 0; i != s.length; i++) {
                        a = ((typeof a == 'undefined' ? 1 : a) + ord(str(s[i]))) % 65521;
                        b = ((typeof b == 'undefined' ? 0 : b) + a) % 65521
                    }
```

其实a这个变量是没有用`var`关键字来定义的， 所以一旦有了值之后就应该是全局的了， 所以这个循环完成之后a的值应该是1000



