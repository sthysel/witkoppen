# bplate

import wx
import time

"""
This ctrl is a textCtrl that will be asociated with a
listBoxCtrl. An entry will be selected in the listBox
that is closest to the text in THIS text control.
"""

class JumpTextCtrl(wx.TextCtrl):
    """ text box that jumps to the nearest name of a ListBox """

    def __init__( self,
                  parent,
                  id,
                  value = "",
                  pos = wx.DefaultPosition,
                  size = wx.DefaultSize,
                  style = 0,
                  validator = wx.DefaultValidator,
                  name = "",
                  list = None):
        wx.TextCtrl.__init__(self, parent, id, value, pos, size,
                             style, validator, name)
        self.parent = parent
        self.currentcontents = [] # the current list contents
        
        # set a search colour
        self.SetBackgroundColour(wx.Colour(216, 252, 248))
        
        self.doNotChange = False
        self.LB = list
        self.when = 0
        self.prevsel = -1
        self.wasprev = False

        wx.EVT_TEXT(self,id, self.search)

    def search(self, evt):
        """ the user entered text into the search ctrl """

        if self.parent.prune == True:
            self.pruneList(evt)
        else:
            self.jumpList(evt)


    def pruneList(self, evt):
        """ alternative to jump - prune the list to only keep the
        desired entries to select from.  """
        
        curlist = []
        
        # Get the current value of this textCtrl
        value = self.GetValue()
        
        if len(value) == 0:
            self.updateListBox(self.parent.completelist)
            return

        #  value == e[0:len(value)]:
        for e in self.parent.completelist:
            if e.rfind(value, 0, len(value)) == 0:
                curlist.append(e)

        self.updateListBox(curlist)
        


    def updateListBox(self, contents):
        """ update the listBox with the given contents """

        self.LB.Clear()
        self.LB.InsertItems(contents, 0)
        

    def sameSize(self,theString,size):
        """ this function returns a string equal to theString , filled
        with 0's until it is size long """

        if (len(theString) < size):
            newString = theString
            for x in range(size - len(theString)):
                newString += "0"
            return newString
        else:
            return theString


    def jumpList(self, evt):
        """ if this textctrl changes in any way this function will be
        called and the listbox associated with it will be updated.
        """

        # get a list of all the names
        if (self.doNotChange == True):
            self.doNotChange = False
            return

        #self.makeList()
        # load the current list of names into the listbox if cache expired
        if time.time()-self.when > 10:
            self.makeList()

        # Get the current value of this textCtrl
        self.value = self.GetValue()
        if len(self.value) == 0:
            return

        foundlist = []
        indexes = {}
        for i in range(self.count):
            index = self.names[i].lower().find(self.value.lower())
            if index != -1:
                foundlist.append(self.names[i])
                indexes[self.names[i]] = i
        
        if len(foundlist) == 0:
            return
            
        foundlist.sort()
        founditem = indexes[foundlist[0]]
        
        # if same as previously also no reason to go on
        if founditem == self.prevsel:
            return

        # clear the previous selection
        if self.prevsel > 0 and self.wasprev == False:
            self.LB.SetSelection(self.prevsel, False)

        # set new selected
        cursels = self.LB.GetSelections()
        self.wasprev = False
        for cursel in cursels:
            if cursel == founditem:
                self.wasprev = True
                break
        self.prevsel = founditem
        self.LB.SetSelection(founditem, True)
        self.LB.SetFirstItem(founditem)

        # Send an update event to the listbox
        if (founditem != -1):
            self.LB.SetSelection(founditem)

        evt.Skip()        

    def makeList(self):
        """ load strings from listbox """

        # remember when this was last done
        self.when = time.time()

        # build string list
        self.names = []
        self.count = self.LB.Number()
        for x in range(self.count):
            self.names.append(self.LB.GetString(x))

