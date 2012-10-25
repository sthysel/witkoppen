# bplate

import wx

""" Events send to LED objects on the StatusBar indicating system
activity"""

# -------------------------------- LEDEvent ------------------------------
# -------------------------------- LEDEvent ------------------------------
# -------------------------------- LEDEvent ------------------------------
EVT_LED_ID = wx.NewId()
def EVT_LED(win, func):
    win.Connect(-1, -1, EVT_LED_ID, func)


class LEDEvent(wx.PyEvent):
    """ a led event - network activity status """

    def __init__(self, action='on', service='SQL'):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_LED_ID)
        self.action = action
        self.service = service
