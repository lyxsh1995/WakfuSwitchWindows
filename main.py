# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

import win32gui, win32com.client

import WakfuWindowEntity

windows = []
colora = 6911105  # 底部箭头颜色
colorb = 8356608  # 中间奖励蓝色条
if __name__ == '__main__':
    while (win32gui.FindWindow(None, "沃土  WAKFU")):
        window = WakfuWindowEntity.WakfuWindow(win32gui.FindWindow(None, "沃土  WAKFU"))
        windows.append(window)
        win32gui.SetWindowText(window.hwnd, "Wakfu")
        print(vars(window))  # 打印所有变量

    for window in windows:`
        win32gui.SetWindowText(window.hwnd, "沃土  WAKFU")

    if len(windows) == 0:
        print("目前没有沃土运行")
        exit()


    def setfouces():
        shell = win32com.client.Dispatch("WScript.Shell")
        while (True):
            time.sleep(1)
            i = 0
            for window in windows:
                # 刷新点位颜色
                try:
                    window.refreshColor()
                except:
                    break
                # 判断是不是所有窗口都符合
                if window.color == colora:
                    i = i + 1
            # 符合条件窗口大于等于2个则在准备阶段,不进行操作
            if i >= 2:
                break

            for window in windows:
                if win32gui.GetForegroundWindow() == window:
                    # 如果当前窗口在最前里则不进行操作
                    break
                try:
                    if window.color == colora or window.color2 == colorb:
                        # 通过句柄将窗口放到最前
                        print("准备置顶")
                        shell.SendKeys('`')
                        win32gui.SetForegroundWindow(window.hwnd)
                        # 把当前窗口放到列表第一位
                        windows.remove(window)
                        windows.insert(0, window)
                        break
                    else:
                        print("颜色不同", window.color)
                except Exception as e:
                    print(e)


    setfouces()
