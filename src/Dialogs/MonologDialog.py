# bplate

import wx
from ArtRegistry.ArtRegistry import ART
from wx.lib.evtmgr import eventManager

# ---------------------------- MonologDialog ----------------------
# ---------------------------- MonologDialog ----------------------
# ---------------------------- MonologDialog ----------------------
class MonologDialog(wx.Dialog):
    def __init__(self, parent, text, hdr='GSMPlayer, Attention'):
        wx.Dialog.__init__(self,
                           parent,
                           -1,
                           hdr,
                           style = wx.DIALOG_MODAL|wx.CAPTION)
        
        # the text field
        textStatic = wx.StaticText(self, -1, text)

        # OK button
        okBtn = wx.Button(self, wx.ID_CLOSE, "Close", (80, 20))
        okBtn.SetFocus()

        bmp = ART['32x32info']        
        wPic = wx.StaticBitmap(self,
                               -1,
                               bmp,
                               size=(bmp.GetWidth(), bmp.GetHeight()))
        
        contentsBox = wx.BoxSizer(wx.HORIZONTAL)
        contentsBox.Add(wPic, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        contentsBox.Add(textStatic, 1, wx.ALIGN_CENTER|wx.ALL, 5)
        
        line = wx.StaticLine(self, -1, size=(150, -1), style=wx.LI_HORIZONTAL)        
        allBox = wx.BoxSizer(wx.VERTICAL)
        allBox.Add(contentsBox, 1, wx.ALIGN_CENTER|wx.EXPAND|wx.ALL, 5)
        allBox.Add(line, 0, wx.ALIGN_CENTER|wx.EXPAND|wx.ALL, 5)
        allBox.Add(okBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        allBox.Fit(self)
        self.SetSizer(allBox)
        self.SetAutoLayout(True)

        self.Centre(wx.BOTH)
        
        eventManager.Register(self.Close, wx.EVT_BUTTON, okBtn)
        eventManager.Register(self.OnKeyDown, wx.EVT_KEY_DOWN, self)
        
    def OnKeyDown(self, evt):
        """ handle enter key  """
        
        key = evt.GetKeyCode()        
        if key == wx.WXK_RETURN:
            self.Close(evt)
        else:            
            evt.Skip()


    def Close(self, evt):        
        self.EndModal(wx.ID_OK)
