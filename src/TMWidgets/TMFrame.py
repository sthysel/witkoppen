# bplate

import wx
from Registry import Registry


class TMFrame(wx.Frame):
    """TM Frame widget"""
    
    def __init__(self, parent, ID, title=None, 
                 style=wx.TAB_TRAVERSAL, 
                 size=wx.DefaultSize, fosterchild=None):
        wx.Frame.__init__(self, parent, ID, title=title, style=style, size=size)
        #ResponseHandler.__init__(self)
        
        self.parent = parent
        self.fosterchild = fosterchild

        self.Center(wx.BOTH)
        
        wx.EVT_CLOSE(self, self.OnClose)
        wx.EVT_SIZE(self, self.OnSize)        
        
    def OnSize(self, evt):
        self.SetSize(evt.GetSize())
        evt.Skip()
        
    def OnClose(self, evt):
        """ panel is being closed"""

        if self.fosterchild:
            parent = self.fosterchild.oldparent
            self.fosterchild.Reparent(parent)
            parent.AddPage(self.fosterchild, self.fosterchild.__doc__)
            self.fosterchild.Show()
            self.Destroy()

