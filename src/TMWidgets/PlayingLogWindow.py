# bplate

from Universe.Universe import *
from wx.lib.evtmgr import eventManager


class PlayingLogWindow(TMPanel):
    """ Impliments current playing log and information """
    def __init__(self, parent, ID):
        TMPanel.__init__(self, parent, -1, registrykey="PLAYINGLOG")        
        
        # the log control
        self.logCtrl = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        font = wx.Font(-1,
                       wx.ROMAN,
                       wx.NORMAL,
                       wx.NORMAL,
                       False,
                       "courier",
                       wx.FONTENCODING_SYSTEM)        
        self.logCtrl.SetFont(font)
        self.logCtrl.SetBackgroundColour(COLORS['INFO BACKGROUND'])
        
        # self.logCtrl.SetBackgroundColour(COLORS['INFO BACKGROUND'])
        logBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Play Log"), wx.HORIZONTAL)
        logBox.Add(self.logCtrl, 1, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 3)


        sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(topBox, 0, wx.ALIGN_CENTRE|wx.GROW|wx.ALL)
        sizer.Add(logBox, 1, wx.ALIGN_CENTRE|wx.GROW|wx.ALL)
        
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.Fit()

        EVT_LOG(self, self.OnLogEvent)
        EVT_INFO(self, self.OnInfoEvent)
        
    def addLog(self, txt):
        """ add the log text"""

        try:
            self.logCtrl.AppendText(txt)
        except UnicodeDecodeError:
            self.logCtrl.AppendText("SMS Undisplayable\n")

    def errLog(self, txt):
        """ write a error log to the log """

        curcol = self.logCtrl.GetForegroundColour()
        self.logCtrl.SetForegroundColour(wx.RED)
        self.logCtrl.AppendText(txt)
        self.logCtrl.SetForegroundColour(curcol)

        
    def OnLogEvent(self, evt):
        """ a log arrived, update the log window"""

        txt = evt.msg.txt
        errFlag = evt.msg.errorFlag
        if errFlag:
            self.errLog(str(txt) + '\n')
        else:
            self.addLog(str(txt) + '\n')        

    def OnInfoEvent(self, evt):
        """ a info event arrived, update the info fields"""


        info = evt.msg
        
        try:
            clear = info.clear
            return
        except AttributeError:
            pass
        
        
        self.addLog("Encoding: %s\n" % info.encoding)
        self.addLog("Rate: %s\n" % info.rate)
        self.addLog("Left: %s\n" % info.leftsource)
        self.addLog("Right: %s\n" % info.rightsource)
        
        

