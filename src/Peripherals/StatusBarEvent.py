# bplate

""" custom status bar events """

import wx.lib.newevent
StatusBarEvent, EVT_STATUSBAR = wx.lib.newevent.NewEvent()

class StatusBarMessage:
    """ message sent to statusbar"""
    def __init__(self, txt="", pos=0, range=0, progvalue=0, color="", logtype=""):
        self.txt = txt
        self.pos = pos
        self.progvalue = progvalue
        self.range = range
        self.color = color
        self.logtype = logtype

    def __str__(self):
        st = self.txt + '\n' + self.pos + '\n' + self.progvalue
        return st


        
