# bplate

from Universe.Universe import *

"""
a simple helper class providing a listctrl widget with a
preattached jumptxt ctrl
"""

from NSWidgets.JumpTextCtrl import JumpTextCtrl

FONTSIZE = 5

import wxver
# btn size
if wxver.isver("2.5"): SIZE = (-1, 24)
else: SIZE = (15, -1)


class JumpListBox(wx.PyWindow):
    def __init__(self,
                 parent,
                 LBID,
                 choices=[],
                 label="JumpListBox",
                 size=(200, -1),
                 style=wx.LB_SINGLE,
                 name="JumpListBox",
                 font=None,
                 OnEnterFunction=None):        
        if LBID == -1: LBID = wx.NewId()
        
        wx.PyWindow.__init__(self, parent, LBID, name=name, size=size)
        
        self.completelist = choices # all entries in LB
        self.prune = False
        
        self.LB = wx.ListBox(self,
                             LBID,
                             choices=choices,
                             size=size,
                             style=style,
                             name=name)
        
        if font: self.LB.SetFont(font)
        
        self.searchCtrl = JumpTextCtrl(self, -1, list=self.LB)        
        self.searchCtrl.SetCursor(wx.StockCursor(wx.CURSOR_MAGNIFIER))


        # filter/jump toggle
        self.togbtn = wx.Button(self, -1, 'J', size=SIZE)
        
        searchBox = wx.BoxSizer(wx.HORIZONTAL)
        searchBox.Add(self.searchCtrl, 1, wx.ALIGN_CENTRE)
        searchBox.Add(self.togbtn, 0, wx.ALIGN_CENTRE)

        # layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.LB, 1, wx.GROW)
        sizer.Add(searchBox, 0, wx.GROW)        
                
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        sizer.Fit(self)
        self.Layout()

        self.sizer = sizer

        wx.EVT_SIZE(self, self.size)
        wx.EVT_BUTTON(self, self.togbtn.GetId(), self.setFilterBehaviour)        
        wx.EVT_KEY_DOWN(self.LB, self.OnSearch)

        wx.EVT_KEY_DOWN(self.searchCtrl, self.OnKeySearchBox)
        
        self.OnEnterFunction = OnEnterFunction
    
    def OnKeySearchBox(self,evt):
        key = evt.GetKeyCode()
        if key == 13: # ENTER
            if self.OnEnterFunction is not None:
                self.OnEnterFunction(self)
        else: evt.Skip()
    
    def size(self, evt):
        self.SetSize(evt.GetSize())
        self.sizer.Fit(self)
        self.Layout()
        evt.Skip()

    def OnSearch(self, evt):
        """ search  """
        if evt.ControlDown():
            key = evt.GetKeyCode()
            if key == 83:
                self.searchCtrl.SetFocus()
            elif key == 74 or key == 80:
                self.searchCtrl.SetFocus()
                self.setFilterBehaviour(evt)
                
        evt.Skip()

    def Enable(self, flag):
        """ enable wrapper """
        # i dont need to be disabled
        pass

    def setFilterBehaviour(self, evt):
        """ set the filter behaviour to prune or not """
        if self.togbtn.GetLabel() == "P":
            self.togbtn.SetLabel("J")
            self.prune = False
        else:
            self.togbtn.SetLabel("P")
            self.prune = True

        # refresh the list on filter change
        self.LB.Clear()
        self.LB.InsertItems(self.completelist, 0)


    def GetSelection(self):
        """ getselection wrapper """
        return self.LB.GetSelection()

    def GetSelections(self):
        """ getselection wrapper """
        return self.LB.GetSelections()

    def SetSelection(self, i):
        """ setselection wrapper """
        return self.LB.SetSelection(i)

    def SetFirstItem(self, i):
        """ wrapper """
        return self.LB.SetFirstItem(i)

    def FindString(self, txt):
        """ findstring wrapper """
        return self.LB.FindString(txt)

    def GetStringSelection(self):
        """ wrapper """
        return self.LB.GetStringSelection()

    def GetString(self, i):
        """ wrapper """
        return self.LB.GetString(i)

    def Number(self):
        """ wrapper """
        return self.LB.Number()


    def Deselect(self, i):
        """ wrapper """
        return self.LB.Deselect(i)

    def Append(self, txt):
        """ wrapper """
        return self.LB.Append(txt)


    def SetStringSelection(self, st, select=True):
        """ wrapper """
        return self.LB.SetStringSelection(str(st), select)


    def Delete(self, i):
        """ delete wrapper """
        self.LB.Delete(i)

    def Clear(self):
        """ clear the listbox """
        self.LB.Clear()

    def InsertItems(self, items, position):
        """ Insert items into the LB """

        assert(type(items) == type([]))
        self.LB.InsertItems(items, position)
        self.completelist = self.getCompleteList()
        

    def getCompleteList(self):
        """ gets a complete list of items in LB """
        res = []
        for i in range(0, self.LB.GetCount()):
            st = self.LB.GetString(i)
            res.append(st)
            
        return res


    def DoGetBestSize(self):
        return wx.Size(200, 24)

    def GetClassName(self):
        """ the class name """
        return "JumpListBox"


    def SetBackgroundColour(self, color):
        """ set the LB background colour"""
        self.LB.SetBackgroundColour(color)
