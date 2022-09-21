# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# from mainUI import Ui_MainWindow
# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow

import ctypes
import threading
import time
import tkinter.messagebox

import pystray
import win32api
import win32com.client
import win32con
import win32gui
from PIL import Image

import WakfuWindowEntity

TITLE = "沃土切换器"
isRun = True
windows = []
colora = 6911105  # 底部箭头颜色
colorb = 8356608  # 中间奖励蓝色条
SPACE = 0x20  # 空格
shell = win32com.client.Dispatch("WScript.Shell")
_user32 = ctypes.WinDLL("user32")
AttachThreadInput = _user32.AttachThreadInput
GetKeyboardState = _user32.GetKeyboardState
SetKeyboardState = _user32.SetKeyboardState
MapVirtualKeyA = _user32.MapVirtualKeyA
PBYTE256 = ctypes.c_ubyte * 256
oldKeyboardState = PBYTE256()
keyboardStateBuffer = PBYTE256()
GetKeyboardState(ctypes.byref(oldKeyboardState))
current = win32api.GetCurrentThreadId()

if __name__ == '__main__':
    window = 0
    while True:
        window = win32gui.FindWindowEx(0, window, None, "沃土  WAKFU")
        if window == 0:
            break
        else:
            wakfuwindow = WakfuWindowEntity.WakfuWindow(window)
            print(vars(wakfuwindow))
            windows.append(wakfuwindow)

    if len(windows) == 0:
        print("目前没有沃土运行")
        # exit()


    def sendKey(hwnd, key):
        """
        后台发送按键
        :param hwnd:窗口句柄
        :param key:按键值
        :return:
        """
        lparam = win32api.MAKELONG(0, MapVirtualKeyA(key, 0)) | 0x00000001
        win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        AttachThreadInput(current, hwnd, True)
        GetKeyboardState(ctypes.byref(oldKeyboardState))
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, lparam)
        time.sleep(0.1)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, lparam | 0xC0000000)
        time.sleep(0.1)
        SetKeyboardState(ctypes.byref(oldKeyboardState))
        time.sleep(0.1)
        AttachThreadInput(current, hwnd, False)


    def switchwindows():
        """
        当前回合切换
        :return:
        """
        while isRun:
            time.sleep(1)
            i = 0
            for window in windows:
                # 刷新点位颜色
                try:
                    window.refreshColor()
                except:
                    print("取色错误")
                # 判断是不是所有窗口都符合
                if window.color == colora:
                    i = i + 1
            # 符合条件窗口大于等于2个则在准备阶段,不进行操作
            if i >= 2:
                continue

            for window in windows:
                if window.isswitch:
                    if win32gui.GetForegroundWindow() == window:
                        # 如果当前窗口在最前里则不进行操作
                        break
                    try:
                        if window.color == colora or window.color2 == colorb:
                            # 通过句柄将窗口放到最前
                            print("准备置顶")
                            sendKey(window.hwnd, 0x60)
                            win32gui.SetForegroundWindow(window.hwnd)
                            break
                        else:
                            print("颜色不同", window.color)
                    except Exception as e:
                        print(e)


    def whileSpace():
        """
        一直按空格
        :return:
        """
        while isRun:
            time.sleep(1)
            for window in windows:
                if window.iswhilepass:
                    sendKey(window.hwnd, SPACE)


    def About(icon, item):
        tkinter.messagebox.showinfo(TITLE, "https://github.com/lyxsh2016/WakfuSwitchWindows\r\rby:zhuaizhuai")


    def Exit(icon, item):
        global isRun
        isRun = False
        icon.stop()


    def isswitch(window):
        def inner(item):
            return window.isswitch

        return inner


    def iswhilepass(window):
        def inner(item):
            return window.iswhilepass

        return inner


    def click_switch(x):
        def inner(icon, item):

            for window in windows:
                if str(x.hwnd) == str(window.hwnd):
                    window.isswitch = not window.isswitch

        return inner


    def click_whilepass(x):
        def inner(icon, item):
            for window in windows:
                if str(x.hwnd) == str(window.hwnd):
                    window.iswhilepass = not window.iswhilepass

        return inner


    Items = []
    for window in windows:
        Items.append(pystray.MenuItem(str(window.hwnd), pystray.Menu(
            pystray.MenuItem("切换窗口", click_switch(window),
                             checked=isswitch(window)),
            pystray.MenuItem("自动空格", click_whilepass(window),
                             checked=iswhilepass(window))
        )))
    Items.append(pystray.MenuItem("关于", About))
    Items.append(pystray.MenuItem("退出", Exit))
    menu = pystray.Menu(*Items)

    notify = pystray.Icon(TITLE, Image.open("icon.png"), TITLE, menu)

    thread = threading.Thread(target=switchwindows)
    thread.start()
    thread = threading.Thread(target=whileSpace)
    thread.start()
    notify.run()
