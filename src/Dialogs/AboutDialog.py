# bplate
# -*- coding: UTF-8 -*-

import wx
from wx.lib.evtmgr import eventManager
from ArtRegistry.ArtRegistry import ART

from VersionReader import VERSION

bragList = ['WitkoppenPR %s' % VERSION
            ]

from pprint import pprint

# ---------------------------- AboutDialog ---------------------------
# ---------------------------- AboutDialog ---------------------------
# ---------------------------- AboutDialog ---------------------------
class AboutDialog(wx.Dialog):
    def __init__(self, parent, ID):
        wx.Dialog.__init__(self, parent, ID,
                           title = "Witkoppen Patient Registry",
                           style=wx.DIALOG_MODAL|wx.CAPTION|wx.CAPTION)


        txtStr = "\n".join(bragList)
        thetxt = wx.StaticText(self, -1, txtStr)
        
        okBtn = wx.Button(self, wx.ID_OK, "OK")
        eventManager.Register(self.ok, wx.EVT_BUTTON, okBtn)
        eventManager.Register(self.ok, wx.EVT_KEY_DOWN, okBtn)
        
        bmp = ART["48x48logo"]
        Pic = wx.StaticBitmap(self,
                              -1,
                              bmp,
                              size=(bmp.GetWidth(), bmp.GetHeight()))
        
        contentsBox = wx.BoxSizer(wx.HORIZONTAL)
        contentsBox.Add(Pic, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        contentsBox.Add(thetxt, 1, wx.ALIGN_CENTER|wx.ALL, 5)

        allBox = wx.BoxSizer(wx.VERTICAL)
        allBox.Add(contentsBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 5)
        allBox.Add(okBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        allBox.Fit(self)
        self.SetSizer(allBox)
        self.SetAutoLayout(True)

        self.Centre(wx.BOTH)


    def ok(self, evt):
        self.EndModal(wx.ID_OK)
        
