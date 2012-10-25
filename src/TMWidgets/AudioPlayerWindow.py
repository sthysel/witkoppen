# bplate

from Universe.Universe import *
from wx.lib.evtmgr import eventManager
from PlayerManager.PlayerManager import PLAYERMANAGER
from Tools import Explore

# value used in forwarding or rewinding
SKIPVAL = 50

class AudioPlayerWindow(TMPanel):
    """ impliments the audio player controlls """
    def __init__(self, parent, ID):
        TMPanel.__init__(self, parent, ID, registrykey="AUDIOCONTROL")        

        # pause flag
        self.paused = False

        # left volume        
        self.leftvol = wx.Slider(self,
                                 -1,
                                 80,
                                 0,
                                 100,
                                 name="leftvolume",
                                 style=wx.SL_HORIZONTAL|wx.SL_LABELS)
        leftvolBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Left Volume"), wx.HORIZONTAL)
        leftvolBox.Add(self.leftvol, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 2)
        
        # right volume
        self.rightvol = wx.Slider(self,
                                 -1,
                                  80,
                                  0,
                                  100,
                                  name="rightvolume",
                                  style=wx.SL_HORIZONTAL|wx.SL_LABELS)
        rightvolBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Right Volume"), wx.HORIZONTAL)
        rightvolBox.Add(self.rightvol, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 2)

        # volume lock
        self.vollockCB = wx.CheckBox(self, -1, "Volume Lock", style=wx.NO_BORDER, name="volumelock")
        self.vollockCB.SetValue(True)

        
        volumeBox = wx.BoxSizer(wx.HORIZONTAL)
        volumeBox.Add(leftvolBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 2)
        volumeBox.Add(rightvolBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 2)
        volumeBox.Add(self.vollockCB, 0, wx.ALIGN_CENTER|wx.ALL, 2)

        # loop 
        def recordLoopFlag(evt):
            """ record the loopflag position """

            evt.Skip()
            # send player status change to player thread
            data = self.getPanelSettings()
            PLAYERMANAGER.put(data)
            # save loopflag to configuration file
            GSMCONF.set("playercontrol", "loopflag", evt.IsChecked())
            
        self.loopCB = wx.CheckBox(self, -1, "Loop Playback", style=wx.NO_BORDER, name="loopflag")
        self.loopCB.SetValue(GSMCONF.getboolean("playercontrol", "loopflag"))
        self.Bind(wx.EVT_CHECKBOX, recordLoopFlag, self.loopCB, self)

        # capture to wav
        self.captureCB = wx.CheckBox(self, -1, "Save Playback to wav", style=wx.NO_BORDER, name="captureflag")
        self.captureCB.SetValue(False)

        flagBox = wx.BoxSizer(wx.HORIZONTAL)
        flagBox.Add(self.loopCB, 0, wx.ALIGN_LEFT|wx.GROW|wx.ALL, 2)
        flagBox.Add(self.captureCB, 0, wx.ALIGN_LEFT|wx.GROW|wx.ALL, 2)

        # progres
        self.progres = wx.Slider(self,
                                 -1,
                                 0,
                                 0,
                                 100,
                                 name="progres",
                                 style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)
        progresBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Progress"), wx.HORIZONTAL)
        progresBox.Add(self.progres, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 2)

        mainprogresBox = wx.BoxSizer(wx.HORIZONTAL)
        mainprogresBox.Add(progresBox, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 2)

        # fencing
        self.leftpost = wx.Slider(self,
                                  -1,
                                  0,
                                  0,
                                  100,
                                  name="leftfence",
                                  style=wx.SL_HORIZONTAL)
        
        self.rightpost = wx.Slider(self,
                                   -1,
                                   100,
                                   0,
                                   100,
                                   name="rightfence",
                                   style=wx.SL_HORIZONTAL)

        fenceBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Fencing"), wx.VERTICAL)
        fenceBox.Add(self.leftpost, 0, wx.ALIGN_CENTER|wx.GROW)
        fenceBox.Add(self.rightpost, 0, wx.ALIGN_CENTER|wx.GROW)


        # play buttons
        bmp = ART["player-play"]
        playBtn = wx.BitmapButton(self, -1, bmp, size=(bmp.GetWidth(), bmp.GetHeight()))
        bmp = ART["player-forward"]
        forwardBtn = wx.BitmapButton(self, -1, bmp, size=(bmp.GetWidth(), bmp.GetHeight()))
        bmp = ART["player-backward"]
        backwardBtn = wx.BitmapButton(self, -1, bmp, size=(bmp.GetWidth(), bmp.GetHeight()))
        bmp = ART["player-stop"]
        stopBtn = wx.BitmapButton(self, -1, bmp, size=(bmp.GetWidth(), bmp.GetHeight()))
        bmp = ART["player-pause"]
        pauseBtn = wx.BitmapButton(self, -1, bmp, size=(bmp.GetWidth(), bmp.GetHeight()))
        
        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        btnBox.Add(backwardBtn, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        btnBox.Add(playBtn, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        btnBox.Add(pauseBtn, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        btnBox.Add(stopBtn, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        btnBox.Add(forwardBtn, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(volumeBox, 0, wx.ALIGN_CENTRE|wx.GROW|wx.ALL, 2)
        sizer.Add(flagBox, 0, wx.ALIGN_LEFT|wx.GROW)
        sizer.Add(mainprogresBox, 0, wx.ALIGN_CENTRE|wx.GROW|wx.ALL, 2)
        sizer.Add(fenceBox, 0, wx.ALIGN_CENTRE|wx.GROW|wx.ALL, 2)
        sizer.Add(btnBox, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
        
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.Fit()

        eventManager.Register(self.OnScroll, wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.progres)
        eventManager.Register(self.OnScroll, wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.leftvol)
        eventManager.Register(self.OnScroll, wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.rightvol)

        # fencing events
        eventManager.Register(self.OnScroll, wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.leftpost)
        eventManager.Register(self.OnScroll, wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.rightpost)

        # flag evts
        # eventManager.Register(self.OnScroll, wx.EVT_CHECKBOX, self.loopCB)
        eventManager.Register(self.OnScroll, wx.EVT_CHECKBOX, self.captureCB)
        
        # btn events
        eventManager.Register(self.OnPlay, wx.EVT_BUTTON, playBtn)
        eventManager.Register(self.OnStop, wx.EVT_BUTTON, stopBtn)
        eventManager.Register(self.OnPause, wx.EVT_BUTTON, pauseBtn)
        eventManager.Register(self.OnBackward, wx.EVT_BUTTON, backwardBtn)
        eventManager.Register(self.OnForward, wx.EVT_BUTTON, forwardBtn)
        
        EVT_AUDIOINFO(self, self.OnAudioInfoEvent)

    def OnScroll(self, evt):
        """ handle end of scroll events"""

        # lock the volume controls if asked to
        vollist = [self.leftvol, self.rightvol]
        if evt.GetEventObject() in vollist:
            if self.vollockCB.GetValue() == True:
                val = evt.GetEventObject().GetValue()
                for o in vollist:
                    o.SetValue(val)


        # fence the progress controll in
        if evt.GetEventObject() == self.progres:
            maxval = self.rightpost.GetValue()
            minval = self.leftpost.GetValue()
            val = self.progres.GetValue()
            if val >= maxval: self.progres.SetValue(maxval)                
            if val <= minval: self.progres.SetValue(minval)                


        # fencing controll            
        if evt.GetEventObject() == self.leftpost:
            if self.leftpost.GetValue() >= self.rightpost.GetValue():
                self.rightpost.SetValue(self.leftpost.GetValue())
            if self.progres.GetValue() <=  self.leftpost.GetValue():
                self.progres.SetValue(self.leftpost.GetValue())
                
        if evt.GetEventObject() == self.rightpost:
            if self.rightpost.GetValue() <= self.leftpost.GetValue():
                self.leftpost.SetValue(self.rightpost.GetValue())
            if self.progres.GetValue() >=  self.rightpost.GetValue():
                self.progres.SetValue(self.rightpost.GetValue())

        data = self.getPanelSettings()
        PLAYERMANAGER.put(data)
        
    def OnAudioInfoEvent(self, evt):
        """ audio info message arrived """
        
        info = evt.msg        
        if hasattr(info, "range"):
            self.progres.SetRange(0, info.range)
            self.rightpost.SetRange(0, info.range)
            self.leftpost.SetRange(0, info.range)

            self.rightpost.SetValue(info.range)
            self.leftpost.SetValue(0)

            
        if hasattr(info, "progress"):
            self.progres.SetValue(info.progress)
            

    def OnStop(self, evt):
        """ Stop btn pressed"""

        self.progres.SetValue(0)
        PLAYERMANAGER.put({"stop":True})

    def OnPause(self, evt):
        """ Pause btn pressed"""

        PLAYERMANAGER.put({"pause":True})
        self.paused = True

    def OnPlay(self, evt):
        """ Play btn pressed"""

        # if previously paused, continue at last play point
        if self.paused:
            PLAYERMANAGER.put({"pause":False})
            self.paused = False
            return
            
        self.progres.SetValue(0)

        panel = Registry.get("SELECT_LIST_PANEL")
        if not panel: return
        
        selection = panel.slist.GetSelection()
        tablename = panel.slist.tablename
        
        # for play btn play firs in selection
        if len(selection) == 0:            
            return
        
        item, oid = selection[0]  
        PLAYERMANAGER.PlaySelection(tablename, oid, immediate=True)


    def OnBackward(self, evt):
        """ rewind a bit """
        
        minval = self.leftpost.GetValue()
        curval = self.progres.GetValue()

        # rewind 10 frames with cognizance of current minimum value
        if curval - SKIPVAL >= minval:
            self.progres.SetValue(curval - SKIPVAL)
        else:
            return
        
        data = self.getPanelSettings()
        data["progres"] = curval - SKIPVAL
        PLAYERMANAGER.put(data)


    def OnForward(self, evt):
        """ forward a bit """

        maxval = self.rightpost.GetValue()
        curval = self.progres.GetValue()

        # forward 10 frames with cognizance of current maximum value
        if curval + SKIPVAL <= maxval:
            self.progres.SetValue(curval + SKIPVAL)
        else:
            return
            
        data = self.getPanelSettings()
        data["progres"] = curval + SKIPVAL
        PLAYERMANAGER.put(data)

        
    def getPanelSettings(self):
        """ retuns panel controll values"""
        return Explore.explore(self, {})

    def SetProgress(self, value):
        """ set the progress value """
        self.progres.SetValue(value)

    def prepareForNewPlay(self):
        """ about to play a new intercept"""

        self.progres.SetValue(0)
        self.rightpost.SetValue(self.rightpost.GetMax())
        self.leftpost.SetValue(0)

