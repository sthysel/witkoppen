# bplate

from Universe.Universe import *
from wx.lib.evtmgr import eventManager
#import wx.lib.masked as masked


class TMGauge(wx.Window):
    """ composite window used to manage gauges"""

    def __init__(self, parent, ID, name):
        wx.Window.__init__(self, parent, ID)        

        self.range = 0 # max range of this gauge
        self.progres = 0 # progress
        
        self.gauge = wx.Gauge(self, -1, 0, size=(250,-1))
        self.gauge.SetBezelFace(3)
        self.gauge.SetShadowWidth(3)

        box = wx.StaticBoxSizer(wx.StaticBox(self, -1, name), wx.HORIZONTAL)
        box.Add(self.gauge, 1, wx.ALIGN_CENTER)
        
        self.SetSizer(box)
        self.SetAutoLayout(True)

        self.Layout()
        wx.EVT_SIZE(self, self.OnSize)        
        
        
    def update(self, evt):
        """ update the current value """
        
        msg = evt.msg
        if msg.range == -1 or msg.progvalue == -1: return

        range = msg.range
        if self.range != range:
            self.range = range
            self.gauge.SetRange(msg.range)
            
        if self.progres != msg.progvalue:
            self.progres = msg.progvalue
            self.gauge.SetValue(msg.progvalue)

        
        
    def OnSize(self, evt):
        self.SetSize(evt.GetSize())
        evt.Skip()
        self.Layout()

