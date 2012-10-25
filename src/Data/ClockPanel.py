"""
analog clock
"""

import wx
from wx.lib import analogclock as ac

from Registry import Registry


class ClockPanel(wx.Panel):
    """Clock"""
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)

        Registry.add("CLOCK", self)

        self.aclock = ac.AnalogClockWindow(self, -1, style=wx.SUNKEN_BORDER)
        self.aclock.SetTickSizes(h=5, m=2)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.aclock, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)

        self.SetSizer(sizer)
