from random import randint, random
from time import sleep, time

import cv2
import pyautogui
import win32api
import win32con
from PIL import ImageGrab
from pykeyboard import PyKeyboard
from pymouse import PyMouse
from pynput.mouse import Controller

from imginit import ImgInit
from action import *
from numpy import where, hstack

mouse = Controller()
m = PyMouse()
k = PyKeyboard()

# --------------------------位置信息----------------------
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
imgPos['myHero'] = (419, 308, 1458, 623)  # 半张棋盘 红框
imgPos['start'] = (X_START, Y_START, X_END, Y_END)  # 客户端
imgPos['rightClick'] = (450, 172, 1419, 725)  # 捡球坐标 黑框


# --------------------------计时参数----------------------
startTime = time()  # 游戏开始时间
lastDTime = time()  # 上一次D人的时间
lastFTime = time()  # 上一次上人口的时间
lastEquipTime = time()  # 上次装备时间
lastBallTime = time()  # 上次捡球时间


# --------------------------启动标识----------------------
# 点击接受比赛后，启动标识重置为1,第一次开始己方回合，startTime更新
start_flag = 1


# --------------------------加载图片资源----------------------
startIcon, ChooseHeroIcon, rightClickIcon, leftClickDelayIcon, judgeHeroIcon, flags = ImgInit()


# --------------------------------调试-------------------------------------
# 方便看执行到哪一步了
debug_flag = 1


def show_action(info):
    if debug_flag:
        print(info)


# --------------------------------识别-------------------------------------
# 抓图
def grabRaw(imgKey):
    pic = ImageGrab.grab(imgPos[imgKey])
    pic.save("target.jpg")
    target = cv2.imread("target.jpg")
    show_action('抓图' + imgKey)
    return target


# 评价模块
def judge(target, source):
    result = cv2.matchTemplate(target, source, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return min_val, min_loc


# 判断是否在游戏中 || 用是否有D F来判断
def judgeInGame():
    target = grabRaw('inGame')
    min_val, min_loc = judge(target, flags['in_game_flag'])  # 检测是否在游戏中
    if min_val < 0.25:
        return True
    min_val, min_loc = judge(target, flags['in_game_flag2'])  # 检测是否在游戏中
    if min_val < 0.25:
        return True
    return False


# 判断是否是己方回合 || 用是否有友方血条和地方血条判断
def judgeMyTurn():

    target = grabRaw('myTurn')

    # 开局五分钟后再判断是否有敌方血条，要不然开局都是野怪，会愣着不动
    if (time() - startTime) > 180:
        min_val, min_loc = judge(target, flags['fighting_flag3'])  # 没有敌方血条
        if min_val < flags['threshold']:
            return False
    min_val, min_loc = judge(target, flags['fighting_flag'])  # 有友方血条
    if min_val < flags['threshold']:
        return True
    min_val, min_loc = judge(target, flags['fighting_flag2'])  # 有友方血条
    if min_val < flags['threshold']:
        return True
    return False


# 判断选中的是哪个英雄
def judgeHero(singlePos):
    hero = -1
    rightClick(singlePos[0], singlePos[1])  # 右键点击，呼出英雄界面
    sleep(0.7)
    pic = ImageGrab.grab(
        (singlePos[0] - 500,
         singlePos[1] - 400,
         singlePos[0] + 500,
         singlePos[1] + 400))  # 以点击处为中心，截取附近的图像，保证英雄信息可以被截取
    pic.save("target.jpg")
    target = cv2.imread("target.jpg")

    # 遍历，找匹配解
    for key in list(judgeHeroIcon.keys())[:-2]:
        min_val, min_loc = judge(target, judgeHeroIcon[key])
        if min_val < ChooseHeroIcon['threshold']:
            hero = list(judgeHeroIcon.keys()).index(key)
            break
    show_action('识别英雄' + str(hero))
    return hero


# --------------------------------命令执行-------------------------------------
# 执行按键命令
def doKey(key_dir, LorR):

    target = grabRaw(key_dir['name'])
    key_list = list(key_dir.keys())

    for key in key_list[:-2]:
        t_height, t_width = key_dir[key].shape[:2]
        min_val, min_loc = judge(target, key_dir[key])
        if min_val < key_dir['threshold']:
            show_action('执行' + key[:-4])

            if LorR == 'L':
                leftClick(
                    imgPos[key_dir['name']][0] + min_loc[0] + t_width // 2,
                    imgPos[key_dir['name']][1] + min_loc[1] + t_height // 2)
            if LorR == 'R':
                rightClick(
                    imgPos[key_dir['name']][0] + min_loc[0] + t_width // 2,
                    imgPos[key_dir['name']][1] + min_loc[1] + t_height // 2)
            sleep(0.1)


# 给重开单独做一个按键函数，提高效率
def startKey():
    key_dir = startIcon

    target = grabRaw(key_dir['name'])
    key_list = list(key_dir.keys())

    for key in key_list[:-2]:
        t_height, t_width = key_dir[key].shape[:2]
        min_val, min_loc = judge(target, key_dir[key])
        if min_val < key_dir['threshold']:
            if key == 'accept_match.png':
                show_action('--------------开始新游戏------------------')
                global start_flag
                start_flag = 1
            show_action('执行' + key[:-4])
            leftClick(
                imgPos[key_dir['name']][0] + min_loc[0] + t_width // 2,
                imgPos[key_dir['name']][1] + min_loc[1] + t_height // 2)
            sleep(0.1)

# 执行D命令 D命令有两种


def D():
    # 两费D的图标
    t_height, t_width = leftClickDelayIcon['d1.png'].shape[:2]
    target = grabRaw('inGame')
    min_val, min_loc = judge(target, leftClickDelayIcon['d1.png'])
    if min_val < leftClickDelayIcon['threshold']:
        show_action('D')
        leftClick(
            imgPos['inGame'][0] + min_loc[0] +
            t_width //
            2,
            imgPos['inGame'][1] + min_loc[1] +
            t_height //
            2)
        sleep(0.1)
        return

    # 零费D的图标
    t_height, t_width = leftClickDelayIcon['d2.png'].shape[:2]
    target = grabRaw('inGame')
    min_val, min_loc = judge(target, leftClickDelayIcon['d1.png'])
    if min_val < leftClickDelayIcon['threshold']:
        show_action('D')
        leftClick(
            imgPos['inGame'][0] + min_loc[0] +
            t_width //
            2,
            imgPos['inGame'][1] + min_loc[1] +
            t_height //
            2)
        sleep(0.1)


# 执行F命令
def F():
    t_height, t_width = leftClickDelayIcon['f.png'].shape[:2]
    target = grabRaw('inGame')
    min_val, min_loc = judge(target, leftClickDelayIcon['f.png'])
    if min_val < leftClickDelayIcon['threshold']:
        show_action('F')
        leftClick(
            imgPos['inGame'][0] + min_loc[0] +
            t_width //
            2,
            imgPos['inGame'][1] + min_loc[1] +
            t_height //
            2)
        sleep(0.1)


# 购买英雄
def ChooseHero():
    # 开局3分钟保护
    if (time() - startTime) < 180:
        if random() > 0.7:
            leftClick(589, 984)  # 购买左一英雄，防止打野打不过
    doKey(ChooseHeroIcon, 'L')


# 获得英雄位置
def getHeroPos():
    try:
        # 多目标匹配，以英雄血条为基准，向右向下平移40，70像素，找到英雄的中心
        target = grabRaw('myHero')
        temp_HeroPos = []

        template = flags['fighting_flag']
        ret = cv2.matchTemplate(target, template, cv2.TM_CCORR_NORMED)
        index = where(ret > 0.9)
        for i in zip(*index[::-1]):
            temp_HeroPos.append((i[0] + 40, i[1] + 70))

        template = flags['fighting_flag2']
        ret = cv2.matchTemplate(target, template, cv2.TM_CCORR_NORMED)
        index = where(ret > 0.9)
        for i in zip(*index[::-1]):
            temp_HeroPos.append((i[0] + 40, i[1] + 70))

        # 因为截过图，转化为绝对坐标
        HeroPos = []
        done_flag = 0
        HeroPos.append((temp_HeroPos[0][0] + imgPos['myHero'][0],
                        temp_HeroPos[0][1] + imgPos['myHero'][1]))

        # 多目标可能会对同一英雄多次识别，因此把太接近的位置合并
        for singlePos in temp_HeroPos:
            for donePos in HeroPos:
                if abs(
                        singlePos[0] + imgPos['myHero'][0] -
                        donePos[0]) < 15 and abs(
                        singlePos[1] + imgPos['myHero'][1] -
                        donePos[1]) < 15:

                    done_flag = 0
                    break
                done_flag = 1
            if done_flag:
                HeroPos.append(
                    (singlePos[0] + imgPos['myHero'][0],
                     singlePos[1] + imgPos['myHero'][1]))
        return HeroPos

        # 调试函数，取消注释可绘图，未来希望能在lol顶层绘制动态图框
        # 记得把上面的return也注释掉
        # draw_img = target.copy()
        # for test in temp_HeroPos:
        #     rect = cv2.rectangle(draw_img, test, (test[0] - 40, test[1] - 70), (0, 0, 255), 1)
        #
        # cv2.imshow('rect', hstack((target, rect)))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print(HeroPos)

    except BaseException:
        return False


# 卖掉英雄
def sellHero(singlePos):
    show_action('卖掉英雄')
    drag(singlePos[0], singlePos[1], 940 + randint(-30, 30), 993)
    sleep(random() / 3)


# 调整英雄站位
def moveHero(aimPos, hero):
    # 移动前后相近，就不动了
    if abs(
            aimPos[0] -
            heroPosX[hero]) < 55 and abs(
            aimPos[1] -
            heroPosY[hero]) < 55:
        pass
    else:
        drag(aimPos[0], aimPos[1], heroPosX[hero], heroPosY[hero])
    show_action(str(hero) + '号英雄就位')
    sleep(random() / 3)


# 装备
def moveEquip():
    rand_equip = randint(0, len(equipPosX) - 1)
    # 重点关照的英雄，这里选的是1号 3号 4号 6号
    hero_index = [0, 2, 3, 5]
    choose_hero = hero_index[randint(0, len(hero_index) - 1)]
    drag(
        equipPosX[rand_equip],
        equipPosY[rand_equip],
        heroPosX[choose_hero],
        heroPosY[choose_hero])
    show_action(str(rand_equip + 1) + '装备到' + str(choose_hero + 1) + '号英雄')
    sleep(random() / 3)

# 新开游戏


def startNewGame():
    print("-----------------------------------------")
    print("新的一局")
    print("-----------------------------------------")


# 设置D的开始时间和间隔
def D_set(nowtime, begin, gap):
    global lastDTime
    if (nowtime - startTime) > begin:
        if (nowtime - lastDTime) > gap:
            D()
            lastDTime = time()


# 设置F的开始时间和间隔
def F_set(nowtime, begin, gap):
    global lastFTime
    if (nowtime - startTime) > begin:
        if (nowtime - lastFTime) > gap:
            F()
            lastFTime = time()


# 设置装备的开始时间和间隔
def equip_set(nowtime, begin, gap):
    global lastEquipTime
    if (nowtime - startTime) > begin:
        if (nowtime - lastEquipTime) > gap:
            moveEquip()
            lastEquipTime = time()


# 设置装备的开始时间和间隔
def ball_set(nowtime, begin, gap):
    global lastBallTime
    if (nowtime - startTime) > begin:
        if (nowtime - lastBallTime) > gap:
            getBall()
            lastBallTime = time()


# 捡球
def getBall():
    doKey(rightClickIcon, 'R')


if __name__ == '__main__':
    print(" ________  _____ ")
    print(r"|__  / _ \| ____|")
    print("  / / | | |  _|  ")
    print(" / /| |_| | |___ ")
    print(r"/____\___/|_____|")
    print("")
    print("----作者:星†空----")
    print("免费软件，切勿用作商业目的!!!!!!")
    print("原作者: https://github.com/zhouxingkong/LOL-yunding")

    print("灰烬猫猫 学习重构")
    print('fork: https://github.com/AshenNeko/LOL-yunding')
    print("-----------------------------------------")
    print("脚本已启动，请转到游戏界面")
    print("-----------------------------------------")
    while True:
        # ----------------------在游戏中---------------------------
        while judgeInGame():
            if start_flag:
                start_flag = 0
                startTime = time()
                show_action(
                    '----------------------游戏开始，开始计时---------------------------')

            ChooseHero()  # 买英雄

            # ----------------------己方回合---------------------------
            if judgeMyTurn():
                show_action(
                    '----------------------进入己方回合---------------------------')
                PosList = getHeroPos()  # 获得英雄位置
                # 获得位置失败
                if not PosList:
                    continue
                # 获得成果
                for singlePos in PosList[:]:  # 逐个遍历
                    hero = judgeHero(singlePos)  # 当前位置英雄ID

                    # 再判别一遍，要不然非己方无法移动
                    if judgeMyTurn():
                        if hero >= 0:  # 是想要的
                            moveHero(singlePos, hero)
                        else:  # 不是想要的
                            # 大于600s才开始卖英雄，防止前期无英雄可用
                            if (time() - startTime) > 600:
                                sleep(1)
                                # 再判断一遍，防止误删
                                if judgeHero(singlePos) < 0:
                                    sellHero(singlePos)
                    else:
                        break
                sleep(3)

            # ----------------------敌对回合---------------------------
            show_action(
                '----------------------进入对敌回合---------------------------')
            # 480s后开始装装备，10s一次尝试
            equip_set(time(), 480, 10)
            # 700s后开始D，30s一次尝试
            D_set(time(), 700, 30)
            # 700s后开始D，60s一次尝试
            F_set(time(), 700, 60)
            # 200s后开始找球，30s一次尝试
            ball_set(time(), 200, 30)
            ChooseHero()  # 买英雄
            sleep(3)

        # ----------------------不在游戏中---------------------------
        show_action('----------------------不在游戏里---------------------------')
        startKey()  # 执行开始游戏控件，保证游戏不断

        # 太久不动，可能是客户端有部分显示错误，尝试救赎
        if (time() - startTime) > 2400:
            leftClick(949, 785)
