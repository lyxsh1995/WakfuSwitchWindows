# WakfuSwitchWindows
Wakfu自动切换当前回合的窗口
## 功能
### 切换窗口
把当前行动的游戏窗口放到最前
- 目前只支持原生主题
- 游戏窗口不能太小,底部按钮栏不能有形变缩小,不能被游戏内其他窗口遮挡
- 界面缩放要为默认的最小值
### 自动空格
每隔一秒向窗口发送空格的按键消息,支持后台,但任务栏图标会闪烁
## 实现
### 切换窗口
使用win32gui.GetPixel取特定点颜色
使用win32gui.SetForegroundWindow置顶窗口
### 自动空格
win32gui.SendMessage发送按键消息
Get/Set KeyboardState避免切换需要窗口
