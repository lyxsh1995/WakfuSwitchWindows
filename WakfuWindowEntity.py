import time

import win32gui


class WakfuWindow:
    w: int
    h: int
    hwnd = None
    hwndDC = None
    color: int  # 底部调整方向箭头点位
    color2: int  # 中间3回合奖励点位
    checked: bool = False #当前窗口在托盘中是否被选中

    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        self.w = right - left
        self.h = bot - top
        self.color = win32gui.GetPixel(self.hwndDC, int(self.w / 2) - 20, self.h - 25)
        self.color2 = win32gui.GetPixel(self.hwndDC, int(self.w / 2), int(self.h / 2) + 120)
        self.checked = False

    def refreshColor(self):
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        self.w = right - left
        self.h = bot - top
        self.color = win32gui.GetPixel(self.hwndDC, int(self.w / 2) - 20, self.h - 25)
        self.color2 = win32gui.GetPixel(self.hwndDC, int(self.w / 2), int(self.h / 2) + 120)

    def ischecked(self):
        return self.checked
