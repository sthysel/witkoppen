# bplate

import wx
import time
from wx.lib.calendar import Calendar, Month


class DateEntryWidget(wx.PyWindow):
    """ class to assist in date entry functionality """
    
    def __init__(self,
                 parent,
                 ID=-1,
                 label="DateEntryWidget",
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=0,
                 caldesc="Select Date",
                 name="",
                 dateformat="%y%m%d%H%M",
                 choices=[],
                 epoch="" # from/to
                 ):

        wx.PyWindow.__init__(self, parent, ID, pos, size, style, name)
        
        self.caldesc = caldesc
        self.dateformat = dateformat
        self.choices = [' '] + choices 
        self.currentTimeStr = ''
        self.epoch = epoch
        
        calBtn = wx.Button( self, -1, "...", size=(20, -1))
        self.dateCtrl = wx.ComboBox(self, -1, size=size, choices=self.choices, name=name)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.dateCtrl, 1, wx.ALIGN_CENTRE)
        sizer.Add(calBtn, 0, wx.ALIGN_CENTRE)
        self.sizer = sizer
        

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.Layout()


        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_BUTTON(self, calBtn.GetId(), self.displayCalendar)

        # update the default time option once a minute
        self.timer = wx.Timer(self, -1)
        wx.EVT_TIMER(self, -1, self.updateToday)
        self.timer.Start(1000 * 60)

        self.updateToday()


    def OnSize(self, evt):
        self.SetSize(evt.GetSize())
        self.sizer.Fit(self)
        self.Layout()
        evt.Skip()

        
    def updateToday(self, evt=None):
        """ change the date today """

        nowstr = time.strftime(self.dateformat, time.localtime(time.time()))
        if self.currentTimeStr != nowstr:
            v = self.dateCtrl.GetValue()
            i = self.dateCtrl.FindString(self.currentTimeStr)
            if i != -1: self.dateCtrl.Delete(i)            
            self.dateCtrl.Append(nowstr)
            self.currentTimeStr = nowstr
            self.dateCtrl.SetValue(v)

        self.setDefaultPeriod()


    def setDefaultPeriod(self):
        """ if the user has filled in a spesific date, do not discard
        his effords if not, suggest the current 24 hour period """

        nowstr = time.strftime(self.dateformat, time.localtime(time.time()))
        if self.dateCtrl.GetValue() != "": return
        if self.epoch == "from":
            self.dateCtrl.SetValue(nowstr[:-4] + "0000")
        elif self.epoch == "to":
            self.dateCtrl.SetValue(nowstr[:-4] + "2359")

    def displayCalendar(self, evt):
        """ display the calendar """
        
        dlg = CalendarDialog(self, caldesc=self.caldesc)
        if dlg.ShowModal() == wx.ID_OK:
            date = dlg.selectedDate
            if date == None:
                return
            else:
                nowstr = time.strftime(self.dateformat, date)
                self.dateCtrl.SetValue(nowstr)
        else: print 'No Date Selected'

        
    def SetValue(self, val):
        """ set the value """

        val = val.strip()
        if val: self.dateCtrl.SetValue(val)
        else: self.dateCtrl.SetValue('')
        
    def GetValue(self):
        """ get the value """        
        return self.ReturnValue()
    
    def ReturnValue(self):
        return self.dateCtrl.GetValue().strip()

    def Clear(self):
        """ clear entry """
        self.dateCtrl.Clear()

    def GetClassName(self):
        return "DateEntryWidget"


# ---------------------------- CalendarDialog ----------------------
# ---------------------------- CalendarDialog ----------------------
# ---------------------------- CalendarDialog ----------------------
class CalendarDialog(wx.Dialog):
    def __init__(self, parent, caldesc='Calendar'):
        wx.Dialog.__init__(
            self,
            parent,
            -1,
            caldesc,
            style = wx.DIALOG_MODAL|wx.CAPTION)

        self.selectedDate = None # the date selected by the user

        # the calendar grid
        self.calend = Calendar(self, -1, size=(200, 180))
                
        # get the current month & year
        start_month = self.calend.GetMonth()        
        start_year = self.calend.GetYear()
               

        # set attributes of calendar
        self.calend.hide_title = True
        self.calend.HideGrid()
        self.calend.SetWeekColor('WHITE', 'BLACK')

        # display routine
        self.ResetDisplay()


        # month selection
        monthlist = self.GetMonthList()        
        self.monthCH = wx.ComboBox(self,
                                   -1,
                                   "",
                                   size=(90, -1),
                                   choices=monthlist,
                                   style=wx.CB_DROPDOWN)        
        self.monthCH.SetSelection(start_month-1)
        

        # year selection
        self.yearCtrl = wx.TextCtrl(self, -1, str(start_year), size=(60, -1))
        h = self.yearCtrl.GetSize().height

        self.spin = wx.SpinButton(self, -1, size=(h*2, h))
        self.spin.SetRange(1980, 2020)
        self.spin.SetValue(start_year)

        
        topBox = wx.BoxSizer(wx.HORIZONTAL)
        topBox.Add(self.monthCH, 0, wx.ALIGN_CENTER)
        topBox.Add(self.yearCtrl, 0, wx.ALIGN_CENTER)
        topBox.Add(self.spin, 0, wx.ALIGN_CENTER)
        
        # scroll bar for month selection
        self.scroll = wx.ScrollBar(self, -1, size=(200, -1), style=wx.SB_HORIZONTAL)
        self.scroll.SetScrollbar(start_month-1, 1, 12, 1, True)
        

        # OK button
        okBtn = wx.Button(self, wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OK, okBtn)
        okBtn.SetFocus()
        
        mainBox = wx.BoxSizer(wx.VERTICAL)
        mainBox.Add(topBox, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        mainBox.Add(self.calend, 1, wx.ALIGN_CENTER|wx.GROW|wx.ALL, 2)
        mainBox.Add(self.scroll, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        mainBox.Add(okBtn, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        
        mainBox.Fit(self)
        self.SetSizer(mainBox)
        self.SetAutoLayout(True)
        self.sizer = mainBox

        self.Centre(wx.BOTH)

        # events
        # mouse click event
        self.Connect(self.calend.GetId(), -1, 2100, self.MouseClick)

        wx.EVT_KEY_DOWN(okBtn, self.OnKeyDown)
        wx.EVT_COMBOBOX(self, -1, self.EvtComboBox)
        wx.EVT_SPIN(self, self.spin.GetId(), self.OnSpin)
        wx.EVT_COMMAND_SCROLL(self, self.scroll.GetId(), self.Scroll)


        
    def GetMonthList(self):
        """ returns list of months """
        
        monthlist = []
        for i in range(13):
            name = Month[i]
            if name != None:
                monthlist.append(name)
            
        return monthlist


    def OnKeyDown(self, evt):
        """ enter is OK """
        
        key = evt.GetKeyCode()
        
        if key == WX.K_RETURN:
            self.OK()
        else:            
            evt.Skip()


    def OK(self, evt=None):        
        self.EndModal(wx.ID_OK)

    

    def OnPreview(self, event):
        """ calendar print preview """
        
        month = self.calend.GetMonth()
        year = self.calend.GetYear()

        prt = PrintCalend(self.frame, month, year)
        prt.Preview()

    
    def OnSpin(self, event):
        """ month and year control events """
        
        year = event.GetPosition()
        self.yearCtrl.SetValue(str(year))
        self.calend.SetYear(year)
        self.calend.Refresh()

    def EvtComboBox(self, event):
        name = event.GetString()
        monthval = self.monthCH.FindString(name)
        self.scroll.SetScrollbar(monthval, 1, 12, 1, True)

        self.calend.SetMonth(monthval+1)
        self.ResetDisplay()


    def Scroll(self, event):
        value = self.scroll.GetThumbPosition()
        monthval = int(value)+1
        self.calend.SetMonth(monthval)
        self.ResetDisplay()

        name = Month[monthval]
        self.monthCH.SetValue(name)


    def MouseClick(self, evt):
        """ remember the clicked value """        
        self.selectedDate = (evt.year, evt.month, evt.day, 0, 0, 0, 0, 0, -1)
        

    def ResetDisplay(self):
        """ set the highlighted days for the calendar """
        self.calend.Refresh()


    # increment and decrement toolbar controls
    def OnIncYear(self, event):
        self.calend.IncYear()
        self.ResetDisplay()

    def OnDecYear(self, event):
        self.calend.DecYear()
        self.ResetDisplay()

    def OnIncMonth(self, event):
        self.calend.IncMonth()
        self.ResetDisplay()

    def OnDecMonth(self, event):
        self.calend.DecMonth()
        self.ResetDisplay()

    def OnCurrent(self, event):
        self.calend.SetCurrentDay()
        self.ResetDisplay()

    def GetClassName(self):
        return "CalendarDialog"

        
if __name__ == '__main__':

    import  wx
    import time
    import sys
    
    sys.path.append("../")
    from Universe.Universe import *

    class TestFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, -1, "Date test")
            
            w = DateEntryWidget(self, -1)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(w, 0)
            self.SetSizer(sizer)


    class App(wx.App):    
        def OnInit(self):
            p = TestFrame(None)
            p.Show()
            return True

    app = App(False)
    app.MainLoop()


