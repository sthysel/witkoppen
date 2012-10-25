#!/usr/bin/env python2.4
# -*- coding: UTF-8 -*-

# bplate

"""
graphical interface for Witkoppen 
"""

import wxversion
wxversion.select('2.6')
from VersionReader import VERSION

from twisted.internet import threadedselectreactor
threadedselectreactor.install()

# attempt to load the psyco optimizer
try:
    import psyco
    psyco.full()
except ImportError, x:
    print x
    pass

import wx
from AppFrame import AppFrame




class App(wx.App):
    def OnInit(self):
        
        frame = AppFrame(None, -1, U"Witkoppen Patient Register %s" % VERSION)        
        self.SetTopWindow(frame)
        frame.Show()
        frame.ShowFullScreen(wx.FULLSCREEN_NOBORDER)
        return True
    
def main():
    app = App(False)
    app.SetVendorName('AgeOfWant')
    app.MainLoop()    
        
if __name__ == '__main__':
    main()
