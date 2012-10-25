import wx
from Registry import Registry

class ContactPanel(wx.Panel):
    """ANC"""
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)

        Registry.add("ANC", self)
        Result.addListener(self)