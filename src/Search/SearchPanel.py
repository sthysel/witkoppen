import wx
import time
import os
import pickle

from Registry import Registry
from DBCon.Connect import CONN
from Data import Result
import Colors

LASTQFILE = '.lastquery' # file to save last query dump

class SearchPanel(wx.Panel):
    """ Search DB"""
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        Registry.add("SEARCH", self)

        # search
        searchBox = self.makeSearchBox()       
        # normal result 
        normalResultBox = self.makeNormalResultBox()
                
        # patient actions
        newBtn = wx.Button(self, wx.ID_NEW)
        self.Bind(wx.EVT_BUTTON, self.newEntry, newBtn)
        delBtn = wx.Button(self, wx.ID_DELETE)
        self.Bind(wx.EVT_BUTTON, self.deleteEntry, delBtn)
        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        btnBox.Add(newBtn, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        btnBox.Add(delBtn, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        # panel sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(searchBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)        
        sizer.Add(normalResultBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        sizer.Add(btnBox, 0, wx.ALIGN_CENTER|wx.ALL, 3)
       
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        sizer.SetSizeHints(self)


        # reload last query
        self.__reloadLastQuery()

        # self.Bind(wx.EVT_BUTTON, self.__killRunningWatchdog, killBtn)
        
        # tooltips
        # self.watchName.SetToolTip(wx.ToolTip("The current running Watchdog configuration"))

    def newEntry(self, evt):
        """ create a new patient"""
        
        panel = Registry.get('BIO')
        panel.addNew()
        
    def deleteEntry(self, evt):
        """ delete selected entry"""
        
        from Dialogs.ConfirmationDialog import ConfirmationDialog
        
        i = self.normalResult.GetSelection()
        data = Result.getResult()[i]
        file_number = data["file_number"]
        
        msg = "Delete %(surname)s, %(first_names)s Folder %(file_number)d from database ?" % data
        
        dlg = ConfirmationDialog(self, msg=msg)
        if dlg.ShowModal() == wx.ID_OK:
            CONN.deleteEntry(file_number)
            self.__searchDB()
            Result.notify(self.normalResult.GetSelection())


    def __reloadLastQuery(self):
        """ reload the last query"""
        
        if os.path.exists(LASTQFILE):
            data = pickle.load(open(LASTQFILE, 'r'))
            
            # qdata = {"folderno": folderno,
            #         "surname": surname,
            #         "name": name}
            
            if data["folderno"]:
                self.folderNumber.SetValue(data["folderno"])
            if data["surname"]:
                self.surname.SetValue(data["surname"])
            if data["name"]:
                self.name.SetValue(data["name"])
            if data["bdate"]:
                self.bdate.SetValue(data["bdate"])
                
            CONN.search(data)
            self.presentResult()

    def makeSearchBox(self):
        """ make a search box"""
        
        
        # folder number
        self.folderNumber = wx.TextCtrl(self, -1, "")
        self.folderNumber.SetBackgroundColour(Colors.LIGHTBLUE)        
        folderBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Folder Number"), wx.HORIZONTAL)
        folderBox.Add(self.folderNumber, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        # surname
        self.surname = wx.TextCtrl(self, -1, "")
        surnameBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Surname"), wx.HORIZONTAL)
        surnameBox.Add(self.surname, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)        
        # name
        self.name = wx.TextCtrl(self, -1, "")
        nameBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Name"), wx.HORIZONTAL)
        nameBox.Add(self.name, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        # allname
        allnameBox = wx.BoxSizer(wx.HORIZONTAL)
        allnameBox.Add(surnameBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        allnameBox.Add(nameBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        
        # birth date
        self.bdate = wx.TextCtrl(self, -1, "")
        bdateBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Birth Date"), wx.HORIZONTAL)
        bdateBox.Add(self.bdate, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)

        searchBtn = wx.Button(self, wx.ID_FIND)
        self.Bind(wx.EVT_BUTTON, self.__searchDB, searchBtn)
        
        Box = wx.BoxSizer(wx.VERTICAL)
        Box.Add(folderBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        Box.Add(allnameBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        Box.Add(bdateBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        

        wBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Registry Search"), wx.VERTICAL)
        wBox.Add(Box, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        wBox.Add(searchBtn, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        return wBox
    
    def makeNormalResultBox(self):
        """ The Normal result """
        
        self.normalResult = wx.ListBox(self, -1)
        self.Bind(wx.EVT_LISTBOX, self.__resultSelected, self.normalResult)
        wBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Register Result"), wx.VERTICAL)
        wBox.Add(self.normalResult, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        return wBox
    
    def __resultSelected(self, evt):
        """user selected a result"""        
        
        Result.notify(evt.GetInt())
                    
    def __searchDB(self, evt=None):
        """Search the DB using the given values"""

        folderno = None
        surname = None
        name = None
        
        try:
            folderno = int(self.folderNumber.GetValue())
        except ValueError, e:
            pass

        name = str(self.name.GetValue().strip())
        surname = str(self.surname.GetValue().strip())
        bdate = str(self.bdate.GetValue().strip())
        
        qdata = {"folderno": folderno,
                 "surname": surname,
                 "name": name,
                 "bdate":bdate}
        
        # save query for posterity
        pickle.dump(qdata, open(LASTQFILE, 'w'))
        
        
        CONN.search(qdata)
        self.presentResult()

    def presentResult(self):
        """format and present the result"""
        
        res = Result.getResult()
        formatlist = []
        for d in res:
            formatlist.append("%(surname)s, %(first_names)s" % d)
            
        self.normalResult.Clear()
        self.normalResult.InsertItems(formatlist, 0)    
    
        if Result.currentIndex:
            self.normalResult.SetSelection(Result.currentIndex)
        