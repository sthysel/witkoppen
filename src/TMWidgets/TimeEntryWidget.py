# bplate

from Universe.Universe import *
import wx.lib.masked as masked


class TimeEntryWidget(wx.Window):
    def __init__(self, parent, ID, label="TimeEntryWidget", size=(80, -1), fmt24hr=True, display_seconds=True):
        wx.Window.__init__(self, parent, ID)
        
        spin = wx.SpinButton(self, -1, style=wx.SP_VERTICAL)
        self.timeCtrl = masked.TimeCtrl(self,
                                        -1,
                                        display_seconds=display_seconds,
                                        fmt24hr=fmt24hr,
                                        size=size,
                                        spinButton=spin)
        # spin.SetSize((-1, self.timeCtrl.GetSize().height))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.timeCtrl, 1, wx.ALIGN_CENTRE)
        sizer.Add(spin, 0, wx.ALIGN_CENTRE)
                
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        sizer.Fit(self)
        self.Layout()

        self.sizer = sizer

        wx.EVT_SIZE(self, self.size)

    def size(self, evt):
        self.SetSize(evt.GetSize())
        self.sizer.Fit(self)
        self.Layout()


    def GetValue(self):
        """ return time value """
        return self.timeCtrl.GetValue()

    def SetValue(self, time_t):
        """ return time value """
        self.timeCtrl.SetValue(wx.DateTimeFromTimeT(time_t))
    
    
    
    def GetTicks(self):
        """ get the seconds value """
        
        tm = self.timeCtrl.GetMxDateTime().gmticks()
        # print "timeentry", tm
        return tm
        
