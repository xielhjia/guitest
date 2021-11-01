import sys
import pyautogui
import win32gui, win32ui, win32con, win32api
from PIL import Image
from TestCase import TestCase, Page, Element, Action
import json
import numpy as np
import time

import winsound
import operator
# from pymouse import PyMouse
# import requests
# import base64
# import os
# import json
# import time

hwnd_title = dict()

#获取当前屏幕分辨率
# screenWidth, screenHeight = pyautogui.size()

# print('screenwidth:', screenWidth, ', screenHeight:', screenHeight)

#获取当前鼠标位置
# currentMouseX, currentMouseY = pyautogui.position()

#2秒钟鼠标移动坐标为100,100位置， 绝对移动
# pyautogui.moveTo(x=100, y=100, duration=2, tween=pyautogui.linear)

#鼠标移动到屏幕中央
# pyautogui.moveTo (screenWidth / 2, screenHeight / 2)

#鼠标双击
def doubleClick():
    pyautogui.doubleClick()

#鼠标点击一次
def click():
    pyautogui.click()

#grab a screeen shot with width and height, and save image to file pcname
# screenshot area of window by pyautogui but cannot capture active window
def getScreenShot(pcname,x, y, w,h):
    img = pyautogui.screenshot(region=[x,y,w,h])
    img.save(pcname)

#grab the active window shot by using win32gui lib
def getActiveWindowShot(picname, w, h):
    hwnd = win32gui.GetActiveWindow()
    # hwnd =  win32gui.GetDesktopWindow()
    print('hwnd:', hwnd)
    r = win32gui.GetWindowRect(hwnd)
    bmpFileName = 'screenshot.bmp'

    hwin = win32gui.GetDesktopWindow()
    # 图片最左边距离主屏左上角的水平距离
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    # 图片最上边距离主屏左上角的垂直距离
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, r[2] - r[0], r[3] - r[1])
    memdc.SelectObject(bmp)
    memdc.BitBlt((-r[0], top - r[1]), (r[2], r[3] - top), srcdc, (left, top), win32con.SRCCOPY)
    bmp.SaveBitmapFile(memdc, bmpFileName)

    im = Image.open(bmpFileName)
    im = im.convert('RGB')
    im.save(picname)

def call_ai(img):
    print('call ai function to calc elements coordinate in test_case')
    aiResultDict = {}
    with open("./ai_result.json", 'r') as load_f:
        aiResultDict = json.load(load_f)
    return aiResultDict

# def callAIMethod(picname):
def _get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

def __enum_all_wnd():
    win32gui.EnumWindows(_get_all_hwnd, 0)
    print('1111111111111111111111')
    print(hwnd_title.items())
    for wnd in hwnd_title.items():
        print(wnd)



if __name__ == "__main__":
    time.sleep(5)
    pic_name_step1 = "pic_name_step1.jpg"
    __enum_all_wnd()
    img = getActiveWindowShot(pic_name_step1, 0, 0)

    load_dict = {}
    with open("./test_case1.json", 'r') as load_f:
        load_dict = json.load(load_f)
    print(load_dict)
    testCase = TestCase(load_dict)

    #跳转到Test case 所在页面
    #turn_to_pageId:()

    #对test_case的起始页面截屏，调用AI算法，解析该页面下所有的元素 （x,y,w,h）,赋值给test_case中的相应element
    aiResultDict = call_ai(img)
    for action in testCase.actions:
        elementID = action.element.ID
        for aiResult in aiResultDict['shapes']:
            if aiResult['elementId'] == elementID:
                points = np.array(aiResult['points'])
                start_cor_x = points[0][0]
                end_cor_x = points[1][0]
                start_cor_y = points[0][1]
                end_cor_y = points[1][1]
                width = end_cor_x - start_cor_x
                height = end_cor_y - start_cor_y
                action.element.x = start_cor_x
                action.element.y = start_cor_y
                action.element.w = width,
                action.element.h = height,
                print(start_cor_x, start_cor_y, end_cor_x, end_cor_y, width, height, action.element.w[0])
                continue

    #开始执行测试用例中的所有actions
    for action in testCase.actions:
        print(action)
        print("action:", action.actionType, ", elementType:", action.element.type, ",elementContent:", action.element.element_content, ",element x, y, w, h:", action.element.x, action.element.y, action.element.w, action.element.h)
        if action.element.type == 'input':
            # 鼠标移动到element位置
            pyautogui.moveTo(x=(action.element.x + action.element.w[0] /2 ), y=(action.element.y + action.element.h[0]/2), duration=1, tween=pyautogui.linear)
            # 输入
            pyautogui.click()
            pyautogui.typewrite(action.element.element_content)
        if action.element.type == 'button':
            # 鼠标移动到element位置
            pyautogui.moveTo(x=(action.element.x + action.element.w[0] /2 ), y=(action.element.y + action.element.h[0]/2), duration=1, tween=pyautogui.linear)
            click()
    ### ai result

    # sleep(1)
    # pic_name_step2 = '2.jpg'
