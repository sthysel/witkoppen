# bplate

import wx
from Registry import Registry
from Peripherals.StatusBarEvent import *

""" writes to the statusbar in a thread save manner """

class BarWriter:
    def __init__(self):
        self.statusbar = None 

    def getBar(self):
        """ get a reference to the status bar, it might not exist in the beginning """
        if self.statusbar == None:
            try:
                self.statusbar = Registry.get('APPFRAME').GetStatusBar()
                return self.statusbar
            except AttributeError:
                return None
        else:
            return self.statusbar

        
    def write(self, txt="", pos=0, range=0, progvalue=0, color="", logtype="LOG"):
        """ write a message to the status bar """
        
        bar = self.getBar()
        if bar:
            # send the message to the status bar
            msg = StatusBarMessage(txt=txt,
                                   pos=pos,
                                   range=range,
                                   progvalue=progvalue,
                                   color=color,
                                   logtype=logtype)
            
            evt = StatusBarEvent(msg=msg)
            wx.PostEvent(self.statusbar, evt)


    def stopGauge(self):
        """ stop the gauge"""
        pass

    def rewindGauge(self):
        """ rewind the gauge to 0"""
        pass

    def startGauge(self, interval):
        """ start the gauge"""
        pass
        
        
    def setProgres(self, val):
        """ set the bar's progress value"""
        pass

        
BARWRITER = BarWriter()
