# bplate
# -*- coding: UTF-8 -*-

import wx
import os
import sys
from VersionReader import VERSION
from Registry import Registry

from Search.SearchPanel import SearchPanel
from Data.DataNoteBook import DataNoteBook

from ArtRegistry.ArtRegistry import ART

from Peripherals.StatusBar import StatusBar
from Peripherals.MenuBar import *

# ----------------------------- AppFrame ------------------------------------
# ----------------------------- AppFrame ------------------------------------
# ----------------------------- AppFrame ------------------------------------
class AppFrame(wx.Frame):        
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self,
                          parent,
                          ID,
                          title,
                          wx.DefaultPosition,                          
                          #size=(500, 600),
                          style=wx.DEFAULT_FRAME_STYLE)

        Registry.add("APPFRAME", self)
        self.parent = parent
        self.splitter = wx.SplitterWindow(self, -1, 
                                          style=wx.CLIP_CHILDREN| 
                                          wx.SP_LIVE_UPDATE|
                                          wx.SP_3D)
        

        self.searchpanel = SearchPanel(self.splitter, -1)                                      
        self.dataNB = DataNoteBook(self.splitter, -1)

        self.splitter.SplitVertically(self.searchpanel, self.dataNB)                
        self.splitter.SetSashPosition(260, True)
        self.splitter.SetMinimumPaneSize(20)

        # application peripherals
        self.makeStatusBar()
        self.makeMenuBar()
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.searchpanel, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        sizer.Add(self.dataNB, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.Fit()        

        # self.SetSize(self.GetClientSize())
        # self.SetSize((1000, 800))
        self.Maximize(True)
        
        # event handler
        self.Bind(wx.EVT_CLOSE, CLEANUP.Quit)
        wx.EVT_SIZE(self, self.OnSize)

        self.Centre(wx.BOTH)

        self.SetIcon(self.__getIcon())

    def makeStatusBar(self):
        """ make a status bar """
        
        bar = StatusBar(self, -1)
        self.SetStatusBar(bar)

    def makeMenuBar(self):
        """ Instantiate menubar object and add it to self. """
        
        mb = MenuBar(self, -1)
        self.SetMenuBar(mb)


        
    def __getIcon(self):
        """ convert the logo to a usable icon"""

        from wx import EmptyIcon
        
        icon = EmptyIcon()
        icon.CopyFromBitmap((ART["48x48logo"]))
        return icon

        
    def OnSize(self, evt):
        """ app size change """        

        self.splitter.SetSize(self.GetClientSize())
        #self.SetSize(self.GetClientSize())