Forked from [genshin-lyre-auto-play](https://github.com/Misaka17032/genshin-lyre-auto-play)

## 简介

根据midi文件生成演奏“风物之诗琴”的Auto.js脚本

## 使用方法


### 运行环境

```
python 3.x
numpy
Auto.js  // Android
```

### 1. 安装Python

去Python官网下载然后安装

### 2.安装模块

安装并配置好python环境后使用`pip install -r requirements.txt`命令安装模块。

国内可以使用：

```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### 3.配置

开启Android设备的开发者选项，并开启开发者选项中的“指针位置”选项，可参考[文章](https://www.jianshu.com/p/5e58de76b581)

在游戏界面中使用风物之琴，确定高音Do的XY坐标和低音Ti的XY坐标，对应修改`config.py`中的坐标

### 4.生成

使用管理员权限运行`python android.py`生成指定Midi的Auto.js脚本文件

### 5.安装Auto.js

Auto.js 4.1.1 Alpha2 (461) -> armeabi-v7a [版本下载](https://github.com/Ericwyn/Auto.js/releases/tag/V4.1.1.Alpha2)

### 6.运行

将生成的演奏歌曲的js文件放入Android设备的`/sdcard/脚本`目录下

在Android设备上运行Auto.js，开启**无障碍服务**和**悬浮窗权限**后，进入游戏演奏界面，运行生成的音乐脚本