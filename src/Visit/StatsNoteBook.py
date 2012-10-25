
import wx


from ANCPanel import ANCPanel

class VisitNoteBook(wx.Notebook):
    """visit NoteBook"""
    def __init__(self, parent, ID):
        wx.Notebook.__init__(self, parent, ID, name=self.__doc__)
        
        ancPanel = ANCPanel(self, -1)

        self.AddPage(ancPanel, ancPanel.__doc__)              
