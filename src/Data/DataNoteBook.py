
import wx

from ClockPanel import ClockPanel
from ContactPanel import ContactPanel
from Visit.VisitPanel import VisitPanel
from BioPanel import BioPanel

class DataNoteBook(wx.Notebook):
    """data NoteBook"""
    def __init__(self, parent, ID):
        wx.Notebook.__init__(self, parent, ID, name=self.__doc__)
        
        contactPanel = ContactPanel(self, -1)
        clockPanel = ClockPanel(self, -1)
        visitPanel = VisitPanel(self, -1)
        bioPanel = BioPanel(self, -1)

        self.AddPage(bioPanel, bioPanel.__doc__)        
        self.AddPage(contactPanel, contactPanel.__doc__)
        self.AddPage(visitPanel, visitPanel.__doc__)      
        self.AddPage(clockPanel, clockPanel.__doc__)              
