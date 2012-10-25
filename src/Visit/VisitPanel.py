import wx
import copy
import time

from Registry import Registry
from Data import Result
from DBCon.Connect import CONN
from Peripherals.BarWriter import BARWRITER
from Dialogs.Utils import displayMessage

class VisitPanel(wx.Panel):
    """Visits"""
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)

        Registry.add("VISITS", self)
        Result.addListener(self)
        
        self.visits = {}
        self.file_number = None
        self.selected = None
        
        # visit list
        self.visitListCtrl = wx.ListBox(self, -1, size=(100, -1))
        self.Bind(wx.EVT_LISTBOX, self.dateSelected, self.visitListCtrl)
        visitBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Visit List"), wx.HORIZONTAL)
        visitBox.Add(self.visitListCtrl, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        # note
        self.note = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        # self.Bind(wx.EVT_CHAR, self.OnKeyDown, self.note)
        wx.EVT_CHAR(self.note, self.OnKeyDown)
        self.noteLabel = wx.StaticBox(self, -1, "Visit Note")
        noteBox = wx.StaticBoxSizer(self.noteLabel, wx.HORIZONTAL)
        noteBox.Add(self.note, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        topBox = wx.BoxSizer(wx.HORIZONTAL)
        topBox.Add(visitBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        topBox.Add(noteBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        # save
        saveBtn = wx.Button(self, wx.ID_SAVE)
        self.Bind(wx.EVT_BUTTON, self.__saveData, saveBtn)
        
        newBtn = wx.Button(self, wx.ID_NEW)
        self.Bind(wx.EVT_BUTTON, self.__new, newBtn)
        
        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        btnBox.Add(newBtn, 0, wx.ALIGN_CENTER|wx.ALL, 3)
        btnBox.Add(saveBtn, 0, wx.ALIGN_CENTER|wx.ALL, 3)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        sizer.Add(btnBox, 0, wx.ALIGN_CENTER|wx.ALL, 3)

        self.SetSizer(sizer)
    
    def OnKeyDown(self, evt):
        """ sss"""

        evt.Skip()
        i = self.visitListCtrl.GetSelection()
        if i == -1:
            msg = "Select a visit"
            BARWRITER.write(msg)
        else:
            st = self.visitListCtrl.GetString(i)
            if st[0] != "*":
                nst = "*"+st
                self.currentdate = nst
                self.visitListCtrl.SetString(i, nst)
                self.visits[nst] = copy.copy(self.visits[st])
                del self.visits[st]
                
            
    def __saveData(self, evt):
        """ save the data"""

        if not self.visits: 
            displayMessage("Nothing Selected")
            return 
        
        curval = self.visitListCtrl.GetStringSelection()
        self.visits[curval] = self.note.GetValue()
        print self.visits
        
        # only work with visits 
        data = {}
        if self.file_number:
            for k, v in self.visits.items():
                if k[0] == "*":
                 data[k[1:]] = v
            CONN.saveVisits(self.file_number, data)

        self.reload()
        
    def reload(self, data=None):
        """ reload the panel """
        
        self.visits = {}
        self.visitListCtrl.Clear()
        self.note.Clear()
        if data != None:
            self.file_number = data["file_number"]
        self.visits = CONN.getVisits(self.file_number) # dict
        
        
        vd = self.visits.keys()
        vd.sort()
        vd.reverse()
        if vd:
            self.visitListCtrl.Set(vd)
            self.visitListCtrl.SetSelection(0)
            self.currentdate = vd[0]
            self.note.SetValue(self.visits[self.currentdate])
        
    def __new(self, evt):
        """ new note for today"""
        
        # veto if one already exists
        st = time.strftime("%Y%m%d", time.gmtime())
        if self.visitListCtrl.FindString(st) > -1 or self.visitListCtrl.FindString("*"+st) > -1:
            displayMessage("A visit for today already exists")
            return
        st = st + '-NEW'
        # old and busted
        self.visits[self.currentdate] = self.note.GetValue()
        self.note.Clear()
        
        
        self.visitListCtrl.InsertItems([st], 0)
        self.visitListCtrl.SetSelection(0)
        self.visits[st] = ""
        self.noteLabel.SetLabel("Note for visit at %s" % st)
        self.currentdate = st
        
    def dateSelected(self, evt):
        """ a visit has been selected """
        
        
        # old and busted
        # curval = self.visitListCtrl.GetStringSelection()
        self.visits[self.currentdate] = self.note.GetValue()
        self.note.Clear()
        
        # new hotness
        datest = evt.GetString()
        self.noteLabel.SetLabel("Note for visit at %s" % datest)
        self.note.SetValue(str(self.visits[datest]))
        self.currentdate = datest
        