# bplate

import sys
import os
import wx


class Cleanup:
    """ Destroys application cleanly"""
    def __init__(self):
        pass

    def Quit(self, event=None):
        """quit aplication"""

        from Dialogs.ConfirmationDialog import ConfirmationDialog
        dlg = ConfirmationDialog(None, msg = "Quit Witkoppen Registry ?")
        if dlg.ShowModal() == wx.ID_OK:
            # self.locker.unlock() # remove the lockfile 
            # close running threads
            import threading
            for thread in threading.enumerate():
                try:
                    thread.stop()
                except (AttributeError, TypeError):
                    pass

            os._exit(0)

        
CLEANUP = Cleanup()        
