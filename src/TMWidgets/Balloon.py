# bplate

class Baloon (wxFrame):
    """ A class for providing baloon help. """
    
    def __init__( self, parent, text='' ):
        """
        Constructor
        text is the text to show in the baloon
        """
        wxFrame.__init__(self,parent,-1,'', style=wxSTAY_ON_TOP |
                         wxFRAME_FLOAT_ON_PARENT | wxFRAME_NO_TASKBAR)
        
        self.SetBackgroundColour("#FFFACD")
        sizer = wxBoxSizer(wxHORIZONTAL)
        font = wx.Font(7, wxMODERN , wx.NORMAL, wx.NORMAL, False)
        self.text = text
        self.st = wx.StaticText(self, -1,text,pos=(10,10))
        self.st.SetFont(font)
        sizer.Add(self.st, flag=wxGROW|wxALIGN_CENTER|wxALL, border=10)

        sz = self.st.GetBestSize()
        self.st.SetSize(sz)
        self.SetSize(wxSize(sz[0]+20,sz[1]+20))
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.__pos = wxGetMousePosition()
        self.SetPosition(wxPoint(self.__pos[0]+10,self.__pos[1]+40))
        self.Show(True)
        self.CaptureMouse()
        self.Bind(wx.EVT_MOUSE_CAPTURE_CHANGED, self.UnCapture)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnDown)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)

    def SetText( self, text):
        if text!=self.text and not middleisdown:
            self.text = text
            self.st.SetLabel(text)
            sz = self.st.GetBestSize()
            self.st.SetSize(sz)
            self.SetSize(wxSize(sz[0]+20,sz[1]+20))
            self.__pos = wxGetMousePosition()
            self.SetPosition(wxPoint(self.__pos[0]+10,self.__pos[1]+40))
            if not self.IsShown():
                self.Show(True)
            if not self.HasCapture():
                self.CaptureMouse()
            self.Bind(wx.EVT_MOUSE_CAPTURE_CHANGED, self.UnCapture)
            self.Bind(wx.EVT_MOTION, self.OnMotion)
            self.Bind(wx.EVT_LEFT_DOWN, self.OnDown)


    def OnMiddleDown( self, event ):
        self.UnCapture(event)

    def OnDown( self, event ):
        self.UnCapture(event)
        self.Update()

    def OnMotion( self, event ):
        pos = wxGetMousePosition()
        if abs(pos[0]-self.__pos[0])>3 or abs(pos[1]-self.__pos[1])>3 :
            self.UnCapture()

    def UnCapture( self, event=None ):
        self.text = ''
        while self.HasCapture():
            self.ReleaseMouse()
        if self.IsShown():
            self.Show(False)
