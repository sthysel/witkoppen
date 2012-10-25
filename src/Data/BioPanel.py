import wx
from TMWidgets.DateEntryWidget import DateEntryWidget
from Registry import Registry
import Colors
from DBCon.Connect import CONN
from Data import Result

datamap = {"birth_date": "Date of bith",
           "gender": "Gender",
           "file_number": "Folder Number"}

editstr = "Patient Browse and Edit Mode"
newstr = "New Patient Mode"

class BioPanel(wx.Panel):
    """Demographic"""
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)

        Registry.add("BIO", self)
        Result.addListener(self)

        modefont = wx.Font(16, wx.NORMAL , wx.BOLD, wx.NORMAL, False)
        self.modeLabel = wx.StaticText(self, -1, editstr, size=(600, -1))
        self.modeLabel.SetFont(modefont)

        # folder number
        bigfont = wx.Font(22, wx.MODERN , wx.BOLD, wx.NORMAL, False)
        self.folderNumber = wx.TextCtrl(self, -1, "", size=(130, -1))
        self.folderNumber.SetBackgroundColour(Colors.LIGHTBLUE)
        self.folderNumber.SetFont(bigfont)
        folderBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Folder Number"), wx.HORIZONTAL)
        folderBox.Add(self.folderNumber, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        # name
        self.name = wx.TextCtrl(self, -1, "", size=(350, -1))
        self.name.SetFont(bigfont)
        self.name.SetBackgroundColour(Colors.PURPLE)
        nameBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "First Names"), wx.HORIZONTAL)
        nameBox.Add(self.name, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)

        # surname
        self.surname = wx.TextCtrl(self, -1, "", size=(250, -1))
        self.surname.SetFont(bigfont)
        self.surname.SetBackgroundColour(Colors.PURPLE)
        surnameBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Surname"), wx.HORIZONTAL)
        surnameBox.Add(self.surname, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)        

        # callname
        self.callname = wx.TextCtrl(self, -1, "", size=(120, -1))
        callnameBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Name"), wx.HORIZONTAL)
        callnameBox.Add(self.callname, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)

        # add the names to the top ass well, they are written in large font
        topBox = wx.BoxSizer(wx.HORIZONTAL)
        topBox.Add(folderBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        topBox.Add(nameBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        topBox.Add(surnameBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)

        # names
        # mainnameBox = wx.BoxSizer(wx.HORIZONTAL)
        # mainnameBox.Add(callnameBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        # mainnameBox.Add(nameBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)        
        # mainnameBox.Add(surnameBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
                
        # birthdate
        #self.birthdate = wx.DatePickerCtrl(self, size=(120,-1),
        #                                   style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.birthdate = wx.TextCtrl(self, -1, "", size=(120, -1))
        birthdayBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Birth Date"), wx.HORIZONTAL)
        birthdayBox.Add(self.birthdate, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
                
        # gender
        self.gender = wx.Choice(self, -1, choices=["Male", "Female", "Undefined"], size=(120, -1))
        genderBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Gender"), wx.HORIZONTAL)
        genderBox.Add(self.gender, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        # marital status
        self.marital_status = wx.Choice(self, -1, choices=["Single", "Married", "Divorced", "Widowed"], size=(120, -1))
        maritalBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Marital Status"), wx.HORIZONTAL)
        maritalBox.Add(self.marital_status, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        bgBox = wx.BoxSizer(wx.HORIZONTAL)
        bgBox.Add(birthdayBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        bgBox.Add(genderBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        bgBox.Add(maritalBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        
        # ID
        self.ID = wx.TextCtrl(self, -1, "", size=(200, -1))
        IDBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "National ID"), wx.HORIZONTAL)
        IDBox.Add(self.ID, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)        
        # nationality                              
        self.nationality = wx.TextCtrl(self, -1, "")
        nationalBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Nationality"), wx.HORIZONTAL)
        nationalBox.Add(self.nationality, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        # language                              
        self.language = wx.TextCtrl(self, -1, "", size=(200, -1))
        languageBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Language"), wx.HORIZONTAL)
        languageBox.Add(self.language, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        # race
        self.race = wx.TextCtrl(self, -1, "", size=(200, -1))
        raceBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Ethnicity"), wx.HORIZONTAL)
        raceBox.Add(self.race, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        # id
        allidBox = wx.BoxSizer(wx.HORIZONTAL)
        allidBox.Add(IDBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        allidBox.Add(nationalBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        allidBox.Add(languageBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        allidBox.Add(raceBox, 0, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        
        # occupation
        self.occupation = wx.TextCtrl(self, -1, "", size=(300, -1))
        occupationBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Occupation"), wx.HORIZONTAL)
        occupationBox.Add(self.occupation, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        # employer
        self.employer = wx.TextCtrl(self, -1, "", size=(300, -1))
        employerBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Employer"), wx.HORIZONTAL)
        employerBox.Add(self.employer, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        workBox = wx.BoxSizer(wx.HORIZONTAL)
        workBox.Add(occupationBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        workBox.Add(employerBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        # dependants
        self.dependants = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.dependants.SetBackgroundColour(Colors.INFOCOL)        
        dependantBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Dependants, Only spouse and Children under 18"), wx.HORIZONTAL)
        dependantBox.Add(self.dependants, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        # note
        self.note = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.note.SetBackgroundColour(Colors.INFOCOL)        
        noteBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Additional Notes"), wx.HORIZONTAL)
        noteBox.Add(self.note, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)

        depnoteBox = wx.BoxSizer(wx.HORIZONTAL)
        depnoteBox.Add(dependantBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        depnoteBox.Add(noteBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        
        # synopsis
        self.synopsis = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)        
        synopsisBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Synopsis"), wx.HORIZONTAL)
        synopsisBox.Add(self.synopsis, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 3)
        
        # save
        saveBtn = wx.Button(self, wx.ID_SAVE)
        self.Bind(wx.EVT_BUTTON, self.__saveData, saveBtn)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.modeLabel, 0, wx.ALIGN_LEFT|wx.ALL, 3)
        sizer.Add(topBox, 0, wx.ALIGN_LEFT|wx.ALL, 3)
        sizer.Add(callnameBox, 0, wx.ALIGN_LEFT|wx.ALL, 3)
        sizer.Add(bgBox, 0, wx.ALIGN_LEFT|wx.ALL, 3)
        sizer.Add(allidBox, 0, wx.ALIGN_LEFT|wx.ALL, 3)
        sizer.Add(workBox, 0, wx.ALIGN_LEFT|wx.ALL, 3)
        sizer.Add(depnoteBox, 2, wx.ALIGN_LEFT|wx.GROW|wx.ALL, 3)
        sizer.Add(synopsisBox, 1, wx.ALIGN_LEFT|wx.GROW|wx.ALL, 3)
        sizer.Add(saveBtn, 0, wx.ALIGN_CENTER|wx.ALL, 3)

        self.SetSizer(sizer)
        
        self.widgetList = [
                           self.folderNumber,
                           self.surname,
                           self.name,
                           self.birthdate,
                           #self.gender,
                           self.ID,
                           self.nationality,
                           self.note,
                           self.callname,
                           self.language,
                           self.occupation,
                           self.synopsis,
                           self.dependants,
                           self.race,
                           self.employer
                           ]
        
        
    def addNew(self):
        """ add a new entry """
        
        for w in self.widgetList:
            w.Clear()
        self.gender.SetStringSelection('Undefined')
        self.marital_status.SetStringSelection('Single')
        self.modeLabel.SetLabel(newstr)
        
        
        
    def __saveData(self, evt):
        """ gather and save data to DB"""
        
        data = {
                 "file_number":int(self.folderNumber.GetValue()),
                 "surname":self.surname.GetValue(),    
                 "first_names":self.name.GetValue(),
                 "birth_date":self.birthdate.GetValue(),
                 "gender":self.gender.GetStringSelection(),
                 "nationalid":self.ID.GetValue(),
                 "nationality":self.nationality.GetValue(),
                 "note":self.note.GetValue(),
                 "callname":self.callname.GetValue(),
                 "language":self.language.GetValue(),
                 "occupation":self.occupation.GetValue(),
                 "marital_status":self.marital_status.GetStringSelection(),
                 "dependants":self.dependants.GetValue(),
                 "ethnicity":self.race.GetValue(),
                 "employer":self.employer.GetValue()
                 }
        
        for k, v in data.items():
            if type(v) == type(u""):
                data[k] = str(v)
                
        if self.modeLabel.GetLabel() == editstr:
            CONN.saveBio(data)
        else:
            CONN.addnewBioEntry(data)    
        
    def reload(self, data):
        """display the data"""
        
        self.modeLabel.SetLabel(editstr)
        
        self.folderNumber.SetValue(str(data["file_number"]))
        self.surname.SetValue(data["surname"])
        self.name.SetValue(data["first_names"])
        self.birthdate.SetValue(str(data["birth_date"]))
        self.gender.SetStringSelection(data["gender"])
        self.marital_status.SetStringSelection(data["marital_status"])
        self.ID.SetValue(str(data["nationalid"]))
        self.nationality.SetValue(data["nationality"])
        self.note.SetValue(data["note"])
        self.callname.SetValue(data["callname"])
        self.language.SetValue(data["language"])
        self.occupation.SetValue(data["occupation"])
        self.dependants.SetValue(data["dependants"])
        self.race.SetValue(data["ethnicity"])
        self.employer.SetValue(data["employer"])
        
        
        self.makeSynopsis(data)
        
    def makeSynopsis(self, data):
        """ Create a synopsis of data for this patient"""
        
        self.synopsis.Clear()
        first_names = data['first_names']
        surname = data['surname']

        # gender
        gender = data['gender']
            
        self.synopsis.AppendText("%s %s Summary Report\n" % (first_names.upper(), surname.upper()))
                
        for k in datamap:
            if data.has_key(k):
                self.synopsis.AppendText("%s: %s \n" % (datamap[k], data[k]))
        
        
        
        