import wx
from Registry import Registry

from Data.ContactGrid import ContactGrid
from Data import Result
from DBCon.Connect import CONN
import Colors


addressLookup = {'HOME_PHYSICAL': "Home Physical Address",
                 'HOME_POSTAL': "Home Postal Address",
                 'WORK_PHYSICAL': "Work Physical Address",
                 'WORK_POSTAL': "Work Postal Address"}


class Address(wx.Window):
    def __init__(self, parent, name, COLOR):
        wx.Window.__init__(self, parent)

        self.name = name
        
        self.lines = wx.TextCtrl(self, -1, "", size=(300, -1), style=wx.TE_MULTILINE)
        self.lines.SetBackgroundColour(COLOR)
        linesBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Address Lines"), wx.HORIZONTAL)
        linesBox.Add(self.lines, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        self.code = wx.TextCtrl(self, -1, "", size=(100, -1))
        self.code.SetBackgroundColour(COLOR)
        codeBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Code"), wx.HORIZONTAL)
        codeBox.Add(self.code, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)

        addressBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, addressLookup[name]), wx.VERTICAL)
        addressBox.Add(linesBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        addressBox.Add(codeBox, 0, wx.ALIGN_LEFT|wx.ALL, 3)

        self.SetSizer(addressBox)        
        self.SetAutoLayout(True)
        self.Layout()
        
        wx.EVT_SIZE(self, self.OnSize)

    def OnSize(self, evt):
        self.SetSize(evt.GetSize())
        #evt.Skip()
        self.Layout()


    def getLines(self):
        """return the address lines"""
        
        return self.lines.GetValue()

    def setLines(self, lines):
        """set address lines"""
        self.lines.SetValue(lines)

    def getCode(self):
        """return the address code"""
        
        return self.code.GetValue()

    def setCode(self, code):
        """set address code"""
        self.code.SetValue(code)
   


class ContactPanel(wx.Panel):
    """Contacts"""
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)

        Registry.add("CONTACT", self)
        Result.addListener(self)
        
        self.grid = ContactGrid(self, -1)
        gridBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Contact List"), wx.HORIZONTAL)
        gridBox.Add(self.grid, 1, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 3)

        self.physicalAddress = Address(self, "HOME_PHYSICAL", Colors.HOME)
        self.postalAddress = Address(self, "HOME_POSTAL", Colors.HOME)
        self.workPhysicalAddress = Address(self, "WORK_PHYSICAL", Colors.WORK)
        self.workPostalAdress = Address(self, "WORK_POSTAL", Colors.WORK)
        
        # register the widgets for later access
        self.addWidgets = {"HOME_PHYSICAL": self.physicalAddress,
                           "HOME_POSTAL": self.postalAddress,
                           "WORK_PHYSICAL": self.workPhysicalAddress,
                           "WORK_POSTAL": self.workPostalAdress}
                                    
        agrid = wx.GridSizer(1, 2, 3, 3)
        agrid.AddMany([(self.physicalAddress, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3),    
                       (self.workPhysicalAddress, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3),
                       (self.postalAddress, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3),
                       (self.workPostalAdress, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)])

        #agrid.AddGrowableRow(0, 1)   
        #agrid.AddGrowableRow(1, 1) 
        #agrid.SetFlexibleDirection(wx.HORIZONTAL|wx.VERTICAL)

        # save
        saveBtn = wx.Button(self, wx.ID_SAVE)
        self.Bind(wx.EVT_BUTTON, self.__saveData, saveBtn)
        # new
        newBtn = wx.Button(self, wx.ID_NEW)
        self.Bind(wx.EVT_BUTTON, self.new, newBtn)
        
        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        btnBox.Add(newBtn, 0, wx.ALIGN_CENTER|wx.ALL, 3)
        btnBox.Add(saveBtn, 0, wx.ALIGN_CENTER|wx.ALL, 3)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(gridBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        sizer.Add(agrid, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        sizer.Add(btnBox, 0, wx.ALIGN_CENTER|wx.ALL, 3)

        self.SetSizer(sizer)
        
    def new(self, evt):
        """ new contact"""
        self.grid.addNewRow()
        
    def __saveData(self, evt):
        """ save the data"""
        
        # telephone numbers        
        data = self.grid.getData()
        CONN.saveContacts(self.file_number, data)
        
        # addresses
        adata = []
        for k, w in self.addWidgets.items():
            lines = w.getLines().strip()
            code = w.getCode().strip()
            if lines or code:
                adata.append((k, lines, code))
                
        CONN.saveAddress(self.file_number, adata)
        
        
    def reload(self, data=None):
        """ load data"""
        
        if data:
            self.file_number = data["file_number"]
        
        # contact numbers
        contacts = CONN.getContacts(self.file_number)
        self.grid.setData(contacts)
        
        # addresses
        
        for k, w in self.addWidgets.items():
            w.setLines('')
            w.setCode('')
            
        addresses = CONN.getAddresses(self.file_number)
        print addresses
        for ad in addresses:
            desc = ad['description']
            if self.addWidgets.has_key(desc):
                    w = self.addWidgets[desc]                
                    w.setLines(ad["lines"])
                    w.setCode(ad["code"])
        
        