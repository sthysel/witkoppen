# bplate

import wx

""" Global timer events """

# -------------------------------- TimeEvent -----------------------
# -------------------------------- TimeEvent -----------------------
# -------------------------------- TimeEvent -----------------------

nswsEVT_GLOBAL_TIME = wx.NewId()
def EVT_GLOBAL_TIME(win, func):
    win.Connect(-1, -1, nswsEVT_GLOBAL_TIME, func)


class TimeEvent(wx.PyEvent):
    def __init__(self, now, nowstr):
        wx.PyEvent.__init__(self)
        self.SetEventType(nswsEVT_GLOBAL_TIME)
        self.now = now
        self.nowstr = nowstr

