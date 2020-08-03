import pyautogui
import win32api
import win32con
from random import randint
from random import random
# --------------------------------基础动作-------------------------------------
# 左击
def leftClick(x, y):
    pyautogui.moveTo(x+randint(0,10), y+randint(0,10), duration=random())
    pyautogui.click(x, y, button='left',duration=random())
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    print('leftClick' ,x , y)


# 右击
def rightClick(x, y):
    pyautogui.moveTo(x+randint(0,10), y+randint(0,10), duration=random())
    pyautogui.click(x, y, button='right',duration=random())
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    print('rightClick', x, y)


# 拖拽
def drag(startx, starty, endx, endy):
    pyautogui.click(startx, starty, button='left',duration=random())
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    pyautogui.click(endx, endy, button='left', duration=random())
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    print('drag', startx, starty,endx,endy)

