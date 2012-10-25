# $Id: NSAnalogClockWindow.py,v 1.3 2004/10/18 15:29:16 thys Exp $
# Author: Thys Meintjes et all
# needed a time ofset, copied original here and modified to my needs

# original banner:
#----------------------------------------------------------------------
# Name:        wxPython.lib.analogclock
# Purpose:     A simple analog clock window
#
# Author:      several folks on wxPython-users
#
# Created:     16-April-2003
# RCS-ID:      $Id: NSAnalogClockWindow.py,v 1.3 2004/10/18 15:29:16 thys Exp $
# Copyright:   (c) 2003 by Total Control Software
# Licence:     wxWindows license
#----------------------------------------------------------------------

import math, sys, time
import wx



class NSAnalogClockWindow(wx.Window):
    """A simple analog clock window"""

    TICKS_NONE   = 0
    TICKS_SQUARE = 1
    TICKS_CIRCLE = 2

    def __init__(self, parent, ID=-1, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0, name="clock", houroffset=0):
        # Initialize the wx.Window...
        wx.Window.__init__(self, parent, ID, pos, size, style, name)

        # the hour ofset for local time
        self.houroffset = houroffset

        
        # Initialize the default clock settings...
        self.minuteMarks = 60
        self.hourMarks = 12
        self.tickMarksBrushC = self.GetForegroundColour()
        self.tickMarksPenC   = self.GetForegroundColour()
        self.tickMarkStyle = self.TICKS_SQUARE

        # Make an initial bitmap for the face, it will be updated and
        # painted at the first EVT_SIZE event.
        W, H = size
        self.faceBitmap = wx.EmptyBitmap(max(W,1), max(H,1))

        # Initialize the timer that drives the update of the clock
        # face.  Update every half second to ensure that there is at
        # least one true update during each realtime second.
        self.timer = wx.Timer(self)
        self.timer.Start(500)

        # Set event handlers...
        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_ERASE_BACKGROUND(self, lambda x: None)
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_TIMER(self, -1, self.OnTimerExpire)
        wx.EVT_WINDOW_DESTROY(self, self.OnQuit)


    def SetTickMarkStyle(self, style):
        """
        Set the style of the marks around the edge of the clock.
        Options are TICKS_NONE, TICKS_SQUARE, and TICKS_CIRCLE
        """
        self.tickMarkStyle = style


    def SetTickMarkColours(self, brushC, penC="BLACK"):
        """
        Set the brush colour and optionally the pen colour of
        the marks around the edge of the clock.
        """
        self.tickMarksBrushC = brushC
        self.tickMarksPenC   = penC

    SetTickMarkColour = SetTickMarkColours


    def SetHandsColour(self, c):
        """An alias for SetForegroundColour"""
        self.SetForegroundColour(c)  # the hands just use the foreground colour



    # Using the current settings, render the points and line endings for the
    # circle inside the specified device context.  In this case, the DC is
    # a memory based device context that will be blitted to the actual
    # display DC inside the OnPaint() event handler.
    def OnSize(self, event):
        # The faceBitmap init is done here, to make sure the buffer is always
        # the same size as the Window
        size  = self.GetClientSize()
        self.faceBitmap = wx.EmptyBitmap(size.width, size.height)
        self.DrawFace()


    def OnPaint(self, event):
        self.DrawHands(wx.PaintDC(self))


    def OnQuit(self, event):
        self.timer.Stop()
        del self.timer


    def OnTimerExpire(self, event):
        self.DrawHands(wx.ClientDC(self))


    def DrawHands(self, drawDC):
        # Start by drawing the face bitmap
        drawDC.DrawBitmap(self.faceBitmap,0,0)

        currentTime = time.gmtime(time.time() + self.houroffset * 60 * 60) 
        hour, minutes, seconds = currentTime[3:6]
        
        W,H = self.faceBitmap.GetWidth(), self.faceBitmap.GetHeight()
        centerX = W / 2
        centerY = H / 2

        radius = min(centerX, centerY)
        hour += minutes / 60.0 # added so the hour hand moves continuously
        x, y = self.point(hour, 12, (radius * .65))
        hourX, hourY = (x + centerX), (centerY - y)
        x, y = self.point(minutes, 60, (radius * .85))
        minutesX, minutesY = (x + centerX), (centerY - y)
        x, y = self.point(seconds, 60, (radius * .85))
        secondsX, secondsY = (x + centerX), (centerY - y)

        # Draw the hour hand...
        drawDC.SetPen(wx.Pen(self.GetForegroundColour(), 5, wx.SOLID))
        drawDC.DrawLine(centerX, centerY, hourX, hourY)

        # Draw the minutes hand...
        drawDC.SetPen(wx.Pen(self.GetForegroundColour(), 3, wx.SOLID))
        drawDC.DrawLine(centerX, centerY, minutesX, minutesY)

        # Draw the seconds hand...
        drawDC.SetPen(wx.Pen(self.GetForegroundColour(), 1, wx.SOLID))
        drawDC.DrawLine(centerX, centerY, secondsX, secondsY)


    # Draw the specified set of line marks inside the clock face for the
    # hours or minutes...
    def DrawFace(self):
        backgroundBrush = wx.Brush(self.GetBackgroundColour(), wx.SOLID)
        drawDC = wx.MemoryDC()
        drawDC.SelectObject(self.faceBitmap)
        drawDC.SetBackground(backgroundBrush)
        drawDC.Clear()

        W,H = self.faceBitmap.GetWidth(), self.faceBitmap.GetHeight()
        centerX = W / 2
        centerY = H / 2

        # Draw the marks for hours and minutes...
        self.DrawTimeMarks(drawDC, self.minuteMarks, centerX, centerY, 4)
        self.DrawTimeMarks(drawDC, self.hourMarks, centerX, centerY, 9)


    def DrawTimeMarks(self, drawDC, markCount, centerX, centerY, markSize):
        for i in range(markCount):
            x, y = self.point(i + 1, markCount, min(centerX,centerY) - 16)
            scaledX = x + centerX - markSize/2
            scaledY = centerY - y - markSize/2

            drawDC.SetBrush(wx.Brush(self.tickMarksBrushC, wx.SOLID))
            drawDC.SetPen(wx.Pen(self.tickMarksPenC, 1, wx.SOLID))
            if self.tickMarkStyle != self.TICKS_NONE:
                if self.tickMarkStyle == self.TICKS_CIRCLE:
                    drawDC.DrawEllipse(scaledX - 2, scaledY, markSize, markSize)
                else:
                    drawDC.DrawRectangle(scaledX - 3, scaledY, markSize, markSize)


    def point(self, tick, range, radius):
        angle = tick * (360.0 / range)
        radiansPerDegree = math.pi / 180
        pointX = int(round(radius * math.sin(angle * radiansPerDegree)))
        pointY = int(round(radius * math.cos(angle * radiansPerDegree)))
        return wx.Point(pointX, pointY)




if __name__ == "__main__":
    class App(wx.App):
        def OnInit(self):
            frame = wx.Frame(None, -1, "AnalogClockWindow Test", size=(375,375))

            clock = AnalogClockWindow(frame)
            clock.SetTickMarkColours("RED")
            clock.SetHandsColour("WHITE")
            clock.SetBackgroundColour("BLUE")

            frame.Centre(wx.BOTH)
            frame.Show(True)
            self.SetTopWindow(frame)
            return true

    theApp = App(0)
    theApp.MainLoop()


