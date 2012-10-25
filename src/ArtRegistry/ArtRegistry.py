# bplate

""" This module facilitates art """

import wx
import os
import sys
from Tools import Tools

abspath = Tools.getAbsPath()

artpath = abspath + '/graphics/'
print artpath
app = wx.PySimpleApp()

DEFAULTPIC = "greensphere"

# a path and mask color key tuple is associated with each
# artname, if a mask color key is set, apply  it
artDict = {
           "question":("question.png", "w"),
           "underconstruction":("underconstruction.png","" ,),           
           "roadwarning":("roadwarning.png","" ,),
           "yellowsphere":("yellowsphere.png", "w",),
           "brownsphere":("brownsphere.png", "w",),
           "logbrownsphere":("brownsphere.png", "w",),
           "redsphere":("redsphere.png", "w",),
           "greensphere":("greensphere.png", "w",),
           "32x32editor":("32x32editor.png","" ,),
           "32x32error":("32x32error.png","" ,),
           "32x32warning":("32x32warning.png","" ,),
           "roadwarning":("roadwarning.png","" ,),
           
           "brown_mon":("brown_mon.png","" ,),
           "green_mon":("green_mon.png","" ,),
           "blue_mon":("blue_mon.png","w" ,),
           "yellow_mon":("yellow_mon.png","" ,),
           "14x14check":("14x14check.png","" ,),
               
                
           "24x24hart":("24x24hart.png","" ,),
           "16x16tag":("tag.png","" ,),
           "16x16SMS":("16x16SMS.png","" ,),
           
           "24x24jollyroger":("24x24jollyroger.png","" ,),
           "32x32info":("32x32info.png","" ,),
           "48x48logo":("48x48logo.png","" ,),

           # mail
           "48x48mail":("48x48mail.png","" ,),
           
           # replay
           "player-play":("player-play.png", "", "Play"),
           "player-stop":("player-stop.png", "", "Stop"),
           "player-pause":("player-pause.png", "", "Pause"),
           "player-forward":("player-forward.png", "", "Forward"),
           "player-backward":("player-backward.png", "", "Backward")
           }


maskDict = {'w':wx.WHITE}


class ArtRegistry(dict):
    """ allows [] syntax """    

    def __init__(self):
        dict.__init__(self)

    def __getitem__(self, key):
        """ handle the [] syntax, return the asked  bitmap"""

        if not artDict.has_key(key):
            key = DEFAULTPIC

        path = artpath + artDict[key][0]
        
        if path.find('.png') != -1:
            bmp = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        elif path.find('.xpm') != -1:
            bmp = wx.Bitmap(path, wx.BITMAP_TYPE_XPM)
        elif path.find('.pnm') != -1:
            bmp = wx.Bitmap(path, wx.BITMAP_TYPE_PNM)

        elif path.find('.ico') != -1:
            bmp = wx.Bitmap(path, wx.BITMAP_TYPE_PNM)


        try:
            maskclr = maskDict[(artDict[key])[1]]
            mask = wx.Mask(bmp, maskclr)
            bmp.SetMask(mask)            
        except IndexError:
            pass 
        except KeyError, x:
            pass
        
        return bmp

    def getDescription(self, desc):
        """ returns the description """

        try:
            return wx.ToolTip(artDict[desc][2])
        except IndexError:
            return wx.ToolTip('')
        except KeyError:
            return wx.ToolTip('')
                           
ART = ArtRegistry()

