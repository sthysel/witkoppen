# bplate


""" global timer module, - keeps a consolidated application wide
time. panels register with the time registry to be updated on the
second.  """


import threading
import time

from TimeEvent import *
from TimeRegistry import data as timeRegister

class TMTimer(threading.Thread):
    """Global Timer"""
    def __init__(self):
        threading.Thread.__init__(self, name="GLOBAL_TIMER")
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        """ once a second send a timer signal to all registered panels """
        
        while self.running:
            epoch = time.time()
            now = time.localtime(epoch)
            nowstr = time.strftime("%d-%b-%Y   %H:%M:%S", now)
            evt = TimeEvent(epoch, nowstr)
            for key in timeRegister.keys():
                panel = timeRegister[key]
                wx.PostEvent(panel, evt)

            time.sleep(1)


TIMER = TMTimer()
TIMER.start()
