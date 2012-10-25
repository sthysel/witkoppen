# bplate

""" The menubar """

import wx

from Dialogs.AboutDialog import AboutDialog
from Cleanup.Cleanup import CLEANUP

ID_EXIT = wx.NewId()
ID_HELP_ABOUT = wx.NewId()

# ----------------------------- MenuBar -----------------------------
# ----------------------------- MenuBar -----------------------------
# ----------------------------- MenuBar -----------------------------
class MenuBar(wx.MenuBar):
    def __init__(self, parent, ID):

        wx.MenuBar.__init__(self)

        self.parent = parent
        # the file menu
        self.Append(self.makeFileMenu(), 'File')

        # the tools menu
        self.Append(self.makeToolsMenu(), '&Tools')

        # help menu
        self.Append(self.makeHelpMenu(), '&Help')        




        
    def makeFileMenu(self):
        """ make a file menu """

        menu = wx.Menu()

        i = menu.Append(ID_EXIT, '&Quit', 'Quit gwatch')
        self.parent.Bind(wx.EVT_MENU, CLEANUP.Quit, i)

        return menu


    def makeToolsMenu(self):
        """ a tools menu """

        def export(evt):
            """ Export Database"""

            import popen2
            from BarWriter import BARWRITER
            
            BARWRITER.write("Backup start...")
            popen2.popen2('../SQL/backup.sh')
            BARWRITER.write("Backup complete...")
            
        menu = wx.Menu()

        ID_EXPORT_DB = wx.NewId()
        menu.Append(ID_EXPORT_DB, '&Export Database', 'Export the current Patient Database')
        self.parent.Bind(wx.EVT_MENU, export, id=ID_EXPORT_DB)
        
        return menu

    

    def makeHelpMenu(self):
        """ the help menu """

        menu = wx.Menu()
        menu.Append(ID_HELP_ABOUT, '&About...', 'About Witkoppen Patient Register')
        self.parent.Bind(wx.EVT_MENU, self.OnAbout, id=ID_HELP_ABOUT)

        return menu


    def OnAbout(self, event):
        """ little about dialog """

        dlg = AboutDialog(self, -1)
        dlg.ShowModal()
        dlg.Destroy()


