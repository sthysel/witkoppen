# bplate
# -*- coding: UTF-8 -*-

""" statusbar """

import wx
import time
# from twisted.internet import reactor

from StatusBarEvent import  EVT_STATUSBAR

from Timer import TimeRegistry
from Timer.TimeEvent import *
from TMWidgets.LEDWindow import LEDWindow

from ArtRegistry.ArtRegistry import ART
from Registry import Registry

from Timer import Timer

# ----------------------------- StatusBar ----------------------------------
# ----------------------------- StatusBar ----------------------------------
# ----------------------------- StatusBar ----------------------------------
class StatusBar(wx.StatusBar):
    """ a statusbar """
    def __init__(self, parent, ID):
        wx.StatusBar.__init__(self, parent, ID, style=wx.GA_SMOOTH)

        TimeRegistry.add('STATUSBAR', self)
        Registry.add("STATUSBAR", self)

        self.barrange = 0
        self.barvalue = 0
        
        # hart
        hartbmp = ART['24x24hart']
        self.hartPic = wx.StaticBitmap(self,
                                       -1,
                                       hartbmp,
                                       size=(hartbmp.GetWidth(), hartbmp.GetHeight()))
        self.hartPic.Show(False)

        # the gauge
        self.gauge = wx.Gauge(self, -1, 0)
        self.gauge.SetBezelFace(3)
        self.gauge.SetShadowWidth(3)
        
        fieldlengths = [400, -1, 20, 20, 160, hartbmp.GetWidth() + 6]        
        self.SetFieldsCount(len(fieldlengths))
        self.SetStatusWidths(fieldlengths)

        self.write('Witkoppen Registry GUI Initialized ...')

        # network access flashers
        self.LOGLED = LEDWindow(self, service="LOG")
        self.WATCHLED = LEDWindow(self, service="WATCH")
        
        self.position() # position the various wigets on the bar
        
        EVT_GLOBAL_TIME(self, self.clockDisplay)
        EVT_STATUSBAR(self, self.OnBarMessage)        
        wx.EVT_SIZE(self, self.OnSize)

        
    def flashHart(self, ontime=1):
        """ flash hart for ontime period"""
        self.hartPic.Show(True)
        reactor.callLater(ontime, self.hartOff)

    def hartOff(self):
        """ turn hart off"""
        self.hartPic.Show(False)

        
    def OnBarMessage(self, evt):
        """ a status bar event arrived """

        msg = evt.msg
        txt = msg.txt
        pos = msg.pos
        color = msg.color
        logtype = msg.logtype
        
        # set the progress bar values
        if self.barrange != msg.range:
            self.barrange = msg.range
            self.gauge.SetRange(self.barrange)

        if self.barvalue != msg.progvalue:
            self.SetGaugeProgres(msg.progvalue)
            
        if txt: 
            self.write(txt, pos)
            # set last message as tooltip
            self.SetToolTip(wx.ToolTip(txt))

        # flash the LEDS
        if logtype == "LOG":
            self.LOGLED.flashOnce()
        elif logtype == "WATCH":
            self.WATCHLED.flashOnce()

        
    def OnSize(self, evt):
        self.position()  # for normal size events

        # Set a flag so the idle time handler will also do the repositioning.
        # It is done this way to get around a buglet where GetFieldRect is not
        # accurate during the EVT_SIZE resulting from a frame maximize.
        self.sizeChanged = True


    def position(self):
        """ position the widgets on the bar """

        # gauge
        rect = self.GetFieldRect(1)
        self.gauge.SetPosition(wx.Point(rect.x+2, rect.y+2))
        self.gauge.SetSize(wx.Size(rect.width-4, rect.height-4))

        # LOG led
        rect = self.GetFieldRect(2)
        self.LOGLED.SetPosition(wx.Point(rect.x+2, rect.y+2))
        self.LOGLED.SetSize(wx.Size(rect.width-4, rect.height-4))

        # WATCH led
        rect = self.GetFieldRect(3)
        self.WATCHLED.SetPosition(wx.Point(rect.x+2, rect.y+2))
        self.WATCHLED.SetSize(wx.Size(rect.width-4, rect.height-4))

        # hart pic
        rect = self.GetFieldRect(5)
        self.hartPic.SetPosition(wx.Point(rect.x+2, rect.y+2))
        self.hartPic.SetSize(wx.Size(rect.width-5, rect.height-5))
        
        self.sizeChanged = False
        
        
    def write(self, txt, i=0):
        """ write text to the bar at position i"""
        self.SetStatusText(str(txt), i)

    def clockDisplay(self, evt):
        """ displays the time """
        self.write(evt.nowstr, 4)

    def SetTotal(self, total):
        """ set the total value"""
        self.gauge.SetRange(total)
        
    def SetGaugeProgres(self, count):
        """ set the progres value"""

        range = self.gauge.GetRange()
        if count < range:
            self.barvalue = count
            self.gauge.SetValue(count)
        else:
            self.barvalue = 0

    def SetProgresText(self, txt):
        """ write text to index """
        self.write(txt)


