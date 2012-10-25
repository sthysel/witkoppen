# bplate

import wx
from ArtRegistry.ArtRegistry import ART
from wx.lib.evtmgr import eventManager

# ---------------------------- ConfirmationDialog ---------------------------
# ---------------------------- ConfirmationDialog ---------------------------
# ---------------------------- ConfirmationDialog ---------------------------
class ConfirmationDialog(wx.Dialog):
    def __init__(self,
                 parent,
                 hdr="GSMPlayer, Confirmation",
                 msg="Confirm Action",
                 art="question"):

        # i shall have my way
        if hdr == '': hdr = "Confirmation"
        
        wx.Dialog.__init__(self,
                           parent,
                           -1,
                           title=hdr,
                           style=wx.DIALOG_MODAL|wx.CAPTION)
        
        qstTxt = wx.StaticText(self, -1, msg)

        yesBtn = wx.Button(self, wx.ID_OK, "Yes")
        yesBtn.SetFocus()
        noBtn = wx.Button(self, wx.ID_CANCEL, "No")

        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        btnBox.Add(yesBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        btnBox.Add(noBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        bmp = ART[art]
        qPic = wx.StaticBitmap(self,
                                 -1,
                                 bmp,
                                 size=wx.Size(bmp.GetWidth(), bmp.GetHeight()))        
        contentsBox = wx.BoxSizer(wx.HORIZONTAL)
        contentsBox.Add(qPic, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        contentsBox.Add(qstTxt, 1, wx.ALIGN_CENTER|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(150, -1), style=wx.LI_HORIZONTAL)        
        allBox = wx.BoxSizer(wx.VERTICAL)
        allBox.Add(contentsBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 5)
        allBox.Add(line, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        allBox.Add(btnBox, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        allBox.Fit(self)
        self.SetSizer(allBox)
        self.SetAutoLayout(True)

        self.Centre(wx.BOTH)

        eventManager.Register(self.Yes, wx.EVT_BUTTON, yesBtn)
        eventManager.Register(self.No, wx.EVT_BUTTON, noBtn)
        eventManager.Register(self.OnKeyDown, wx.EVT_KEY_DOWN, self)
        
        
    def OnKeyDown(self, evt):
        """ do a yes() if enter has been hit """

        key = evt.GetKeyCode()    
        if key == wx.WXK_RETURN: self.Yes()
        else: evt.Skip()

    def Yes(self, evt):
        self.EndModal(wx.ID_OK)

    def No(self, evt):
        self.EndModal(wx.ID_CANCEL)

