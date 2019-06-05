# Android

> 一直到这次校赛才开始学习Android， 唉tcltcl

## 常用的工具

`apktool.bat`& `apktool.jar`

比如得到`smali`文件 `apktool.bat d apkName`

打包成apk文件 : `apktools.bat b apkName`
v
应该算是最常用的工具了

当然还有一些比如`android killer`， 但是没用成功过

反编译apk文件用 `jeb`就行了， 也不用去瞎折腾`dex2jar`这些东西

## Android studio

玩Android最重要的就是配置环境， 其中Android studio是最难搞的， 又是`grandle`又是 `android sdk`

完整搞下来估计还要花上不少时间

对于一个Android 工程，有以下几个文件比较重要

### AndroidManifest.xml

这个是应用程序的清单文件，描述了应用程序的基础特性，定义它的各种组件。

无论你开发什么组件用作应用程序中的一部分，都需要在应用程序项目根目录下的manifest.xml文件中声明所有的组件。这个文件是Android操作系统与你的应用程序之间的接口，因此，如果没有在这个文件中声明你的组件，将无法被操作系统所识别。



### strings.xml文件

strings.xml文件在res/value文件夹下，它包含应用程序使用到的所有文本。例如，按钮、标签的名称，默认文本，以及其他相似的strings。这个文件为他们的文本内容负责。



### R 文件

这个文件是自动生成的
活动的Java文件，如MainActivity.java的和资源如strings.xml之间的胶水



### activity_main文件 

是一个在res/layout目录下的layout文件。当应用程序构建它的界面时被引用。你将非常频繁的修改这个文件来改变应用程序的布局。



一般情况下：
在新建一个activity后，为了使intent可以调用此活动，我们要在androidManifest.xml文件中添加一个\<activity>标签，\<activity>标签的一般格式如下

```html
<activity
            android:name="my.test.intents.MainActivity"
            android:label="@string/app_name" >
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
```

* "android:name"是活动对应的类名称
* "android:label"是活动标题栏显示的内容
* \<intent-filter>是意图筛选器
* \<action>是动作名称，是指intent要执行的动作
* \<category>是类别名称

## Android 程序的入口

主要是activity类， 

在 Activity 的生命周期中，系统会按类似于阶梯金字塔的顺序调用一组核心的生命周期方法。 也就是说，Activity 生命周期的每个阶段就是金字塔上的一阶。 当系统创建新 Activity 实例时，每个回调方法会将 Activity 状态向顶端移动一阶。 金字塔的顶端是 Activity 在前台运行并且用户可以与其交互的时间点。

有三种静止状态：继续， 暂停和停止

当用户开始离开 Activity 时，系统会调用其他方法在金字塔中将 Activity 状态下移，从而销毁 Activity。 在有些情况下，Activity 将只在金字塔中部分下移并等待（比如，当用户切换到其他应用时），Activity 可从该点开始移回顶端（如果用户返回到该 Activity），并在用户停止的位置继续。 

当窗体进入暂停状态的时候，系统会回调Activity的onPause()方法，在这个方法中，你可以停止不应该在暂停时继续运行的动作或持久化相关信息在用户离开应用时。如果用户在 Activity 暂停状态下返回，系统会恢复 Activity 并调用 onResume() 方法。

(其实和python和php中的魔术函数很有相似的地方)



至于具体的mobile题目， 只能边做边分析了









