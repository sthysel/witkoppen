# bplate

import wx
from Registry import Registry

class TMPanel(wx.Panel):
    """ TM General panel"""
    def __init__(self, parent, ID, name="", style=wx.TAB_TRAVERSAL, registrykey="", size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, ID, name="", style=style, size=size)
        
        if registrykey: Registry.add(registrykey, self)

        
    def GetName(self):
        """ returns docstring """
        return self.__doc__


    def getChildren(self):
        """ returns dict of children with name keys"""

        data = {}
        children = self.GetChildren()
        for child in children:
            name = child.GetName()
            if name not in ['', 'message']:
                data[name] = child

        return data

