# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

import WakfuWindowEntity
import ctypes
import win32com.client
import win32con
import win32gui
import win32api

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
        #历遍所有Wakfu窗口
        window = win32gui.FindWindowEx(0, window, None, "沃土  WAKFU")
        if window == 0:
            break
        else:
            wakfuwindow = WakfuWindowEntity.WakfuWindow(window)
            print(vars(wakfuwindow))
            windows.append(wakfuwindow)

    # while (win32gui.FindWindowEx(None, "Wakfu")):
    #     window = WakfuWindowEntity.WakfuWindow(win32gui.FindWindow(None, "沃土  WAKFU"))
    #     windows.append(window)
    #     win32gui.SetWindowText(window.hwnd, "Wakfu")
    #     print(vars(window))  # 打印所有变量``
    #
    # for window in windows:
    #     win32gui.SetWindowText(window.hwnd, "沃土  WAKFU")

    if len(windows) == 0:
        print("目前没有沃土运行")
        exit()


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


    def setFouces():
        """
        当前回合按空格
        :return:
        """
        while (True):
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
                if win32gui.GetForegroundWindow() == window:
                    # 如果当前窗口在最前里则不进行操作
                    break
                try:
                    if window.color == colora or window.color2 == colorb:
                        # 通过句柄将窗口放到最前
                        print("准备置顶")
                        sendKey(window.hwnd, SPACE)
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
        while True:
            time.sleep(1)
            for window in windows:
                sendKey(window.hwnd, SPACE)

    # setfouces()

    whileSpace()
