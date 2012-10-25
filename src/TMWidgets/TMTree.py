# bplate

import wx
from Registry import Registry


class TMTree(wx.TreeCtrl):
    """ tree ctrl """
    def __init__(self, parent, ID, name="",
                 style=wx.TR_HAS_BUTTONS,
                 size=wx.DefaultSize,
                 registrykey=None):

        wx.TreeCtrl.__init__(self, parent, ID, name="", style=style, size=size)
        
        if registrykey: Registry.add(registrykey, self)


    def OnExpandAll(self, evt):
        """ expand all nodes """

        root = self.GetRootItem()
        self.traverse(root, self.Expand)

    def OnCollapseAll(self, evt):
        """ collapse all nodes of the tree """

        root = self.GetRootItem()
        self.traverse(root, self.Collapse)
        
    def traverse(self, traverseroot, function, cookie=0):
        """ recursivly walk tree control """

        # step in subtree if there are items or ...
        if self.ItemHasChildren(traverseroot):
            firstchild, cookie = self.GetFirstChild(traverseroot, cookie)
            function(firstchild)
            self.traverse(firstchild, function, cookie)

        # loop siblings
        child = self.GetNextSibling(traverseroot)
        if child:
            function(child)
            self.traverse(child, function, cookie)
                        

    def GetFirstChild(self, id):
        """ api change between 2.4 and 2.5"""

        if wxver.isver('2.4'):
            return wx.TreeCtrl.GetFirstChild(self, id, 0)
        else:
            return wx.TreeCtrl.GetFirstChild(self, id)


    def xxOnCompareItems(self, item1, item2):
        """ alphabetical compare """
        
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        if t1 < t2: return -1
        if t1 == t2: return 0
        return 1
