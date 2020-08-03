# LOL云顶之弈自动化脚本

版本|日期|作者
--|---|--
1.0|2020.8.3|灰烬猫猫

## 说明

原作者：https://github.com/zhouxingkong/LOL-yunding

原作者代码清晰，学会了很多，结合自己理解，写了一版自己的脚本

目前脚本支持的功能[原作者都基本实现]:

+ 自动寻找并接受对局，在死亡后自动退出
+ 自动拿牌(目前策略是只拿暗星)
+ 自动在对敌回合升人口
+ 自动在对敌回合刷英雄
+ 自动在对敌回合捡装备
+ 自动在己方回合识别场上英雄信息
+ 自动在己方回合给特定英雄上装备
+ 自动在己方回合卖英雄
+ 自动在己方回合布局站位
+ 前期打野保护，避免前三局落败

存在的问题:
+ 仍存在未知bug，运行若干局后可能会闪退

## 使用方法


首先修改系统和游戏设置，修改成如下参数:
+ LOL客户端分辨率:1280x720
+ 屏幕分辨率:1920x1080
+ 云顶棋盘建议用S1最老的浅绿色的那款

运行前首先要保证pic文件夹和main.exe在同一个路径中

`以管理员权限`运行main.exe，打印出脚本成功运行这句话说明脚本运行成功
点开下图所示的云顶客户端界面，脚本会自动进行点击操作

![client_ui](https://github.com/AshenNeko/LOL-yunding/blob/master/assets/client_ui.png)

转到该界面后，程序会自动进行寻找对局等一系列流程[昨天连败，心态崩了，游戏删掉了，客户端截图来源于原作者]

大概打了10局，第7-8名4次，第3-6名4次，第2名1次

## 脚本编译

安装所需依赖环境

在main.py目录中执行下面的语句将程序打包成exe文件

``` shell
pyinstaller -F main.py
```

## 程序简介

简单介绍下程序逻辑，具体程序分析见https://ashenneko.github.io/

##### 棋盘划分

![区域划分](https://github.com/AshenNeko/LOL-yunding/blob/master/assets/区域划分.png)

方框特征如图

```python
# 装备位置 紫框
equipPosX = [298, 342, 317, 351, 320, 334, 401, 380, 390, 440]
equipPosY = [765, 729, 691, 666, 633, 595, 663, 634, 595, 633]

# 英雄位置 红字标注
heroPosX = [782, 582, 707, 838, 901, 1218, 1019, 1350]
heroPosY = [444, 676, 676, 676, 444, 676, 444, 676]

# 观众席坐标 棕框
watcherPosX = [446, 555, 674, 790, 906, 1022, 1137, 1253, 1366]
watcherPosY = [744, 739, 742, 743, 743, 744, 743, 744, 743]

# 选择客户端
X_START = 240
X_END = 1700
Y_START = 200
Y_END = 1080
size = (X_START, Y_START, X_END, Y_END)

# 小图坐标
imgPos = {}
imgPos['ChooseHero'] = (476, 900, 1493, 1072)  # 英雄购买框 粉框
imgPos['inGame'] = (263, 875, 468, 1074)  # DF框 绿框
imgPos['myTurn'] = (399, 82, 1528, 626)  # 整个棋盘 蓝框
imgPos['myHero'] = (419,308,1458,623) # 半张棋盘 红框
imgPos['start'] = (X_START, Y_START, X_END, Y_END)  # 客户端
imgPos['rightClick'] = (450, 172, 1419, 725)  # 捡球坐标 黑框
```

##### 程序流程

![流程图](https://github.com/AshenNeko/LOL-yunding/blob/master/assets/流程图.png)

###### 英雄编号

![英雄编号](https://github.com/AshenNeko/LOL-yunding/blob/master/assets/英雄编号.PNG)

###### 英雄站位

![英雄站位](https://github.com/AshenNeko/LOL-yunding/blob/master/assets/英雄站位.png)

###### 英雄位置识别

![英雄位置识别](https://github.com/AshenNeko/LOL-yunding/blob/master/assets/英雄位置识别.PNG)

## 功能扩展

原作者的pic目录未动，可以在imginit.py实现自由扩展

字典名|功能
--|--
startIcon|实现自动化重开游戏的图标
ChooseHeroIcon|底端购买英雄的图标
rightClickIcon|掉落装备的图标
leftClickDelayIcon|D 和 F 的图标
judgeHeroIcon|右键点击场上英雄后的英雄图标
flags|英雄血条图标与D和F的图标

可以直接在imginit.py里重构字典，自由添加图标

## 未来优化方向

- [ ] 程序里import 整个包的情况比较多，在编译时，让整个exe臃肿不堪，可以针对性的import所需函数
- [ ] 程序封装较差，需要手动键入的部分较多，可对通用参数封装
- [ ] 设计GUI，避免每次更改参数就要重新编译exe的麻烦
- [ ] 实现至少两种分辨率，800×600分辨率可以有效资源占用，而且识别也更加轻松
- [ ] 从API层次读取信息，cv2识别还是比较占用资源

