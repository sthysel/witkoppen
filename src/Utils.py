# bplate

""" utility dialogs used throughout the application """

#from Universe.Universe import *
from Registry import Registry
from MonologDialog import MonologDialog
from ConfirmationDialog import ConfirmationDialog

        
def displayMessage(txt, parent=None, sw=1, hdr='GSMPlayer, Attention'):
    """ bring something under user attention """

    txt = str(txt)
    
    appframe = Registry.get('APPFRAME')
    if parent == None: parent = appframe
        
    if sw:
        if appframe:
            bar = appframe.GetStatusBar()
            if bar:
                bar.write(txt)

    dlg = MonologDialog(parent, txt, hdr)
    dlg.ShowModal()

def displayOKBox(txt,parent=None,hdr='Confirmation'):
    """ display an ok/cancel dialog box.
    return true if ok pressed, false otherwse.
    """
    appframe = Registry.get('APPFRAME')
    
    if parent == None:
        parent = appframe
        
    dlg = ConfirmationDialog(parent,msg=txt)    
    return dlg.ShowModal()
    
