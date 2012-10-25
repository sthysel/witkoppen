# bplate

import wx
from Registry import Registry
from TMEvents.LEDEvent import *
from twisted.internet import reactor

FONTSIZE = 8

class LEDWindow(wx.Window):
    def __init__(self, parent, service=""):
        wx.Window.__init__(self, parent, -1, size=(20, -1))
        Registry.addList("LEDS", self)

        self.service = service
        self.SetToolTip(wx.ToolTip(str(service)))
        
        self.defcolour = self.GetBackgroundColour()
                
        self.serviceColors = {'LOG':wx.GREEN,
                              'WATCH':wx.BLUE}
        
        self.serviceColor = self.serviceColors[self.service]

        font = wx.Font(FONTSIZE, wx.NORMAL, wx.NORMAL, wx.LIGHT)
        self.SetFont(font)
        
        EVT_LED(self, self.handleLEDEvt)

    def handleLEDEvt(self, evt):
        """ handle the LED evt """
        
        action = evt.action
        service = evt.service

        if service == self.service:                   
            if action == "on":
                self.on()
            elif action == "off":
                self.off()


    def flashOnce(self):
        """ flash the LED once"""

        self.powerOn()
        reactor.callLater(1, self.powerOff)
        

    def powerOn(self):
        """ switch the LED on"""
        
        thedc = wx.PaintDC(self)
        thedc.SetBackground(wx.Brush(self.serviceColor))
        thedc.Clear()

    def powerOff(self):
        """ switch the LED off"""
        
        thedc = wx.PaintDC(self)
        thedc.SetBackground(wx.Brush(self.defcolour))
        thedc.Clear()
