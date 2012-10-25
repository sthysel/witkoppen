
import wx
import os
import sys
import time


""" a set of general user tools """

def getBaseClass(obj):
    """ returns the base class name of an object.
    i.e. if obj.__class__ == GrandParent.Parent.Object
    will return Object. """
    return "".join((str(obj.__class__).split('.'))[-1:])
        
def getAbsPath():
    """ return absolute path"""

    modname = globals()["__file__"]
    modpath = os.path.join(os.path.split(os.path.dirname(modname))[:-1])[0]
    
    return modpath


def getChildPanels(window, lst):
    """ returns a list of child panels. Usefull when I need to send a evt
    to a set of related panels
    """
    tpe = window.GetClassName()
    if tpe == "wxPanel":
        lst.append(window)

    children = window.GetChildren()
    for child in children:
        tpe = child.GetClassName()
        if tpe == "wxNotebook":        
            for index in range(child.GetPageCount()):
                panel = child.GetPage(index)
                getChildPanels(panel, lst)
                
    return lst


def getListBoxList(listbox, sorted=True, sortfunc=None):
    """ returns a list of listbox contents, possibly sorted """
    
    res = []
    for i in range(0, listbox.GetCount()):
        st = listbox.GetString(i)
        res.append(st)

    if sorted:
        res.sort(sortfunc)
        
    return res



def sortListBox(listbox):
    """ sort the fir listbox alphabetically """

    lst = getListBoxList(listbox)
    listbox.Clear()
    listbox.InsertItems(lst, 0)



def getTime():
    """ returns a tuple of now and now formated as a string """
    
    epoch = time.time()
    now = time.localtime(epoch)
    nowstr = time.strftime("%d-%b-%Y   %H:%M:%S", now)
    nowNameStr = time.strftime("%d-%b-%Y-%H-%M-%S", now)
    
    return epoch, now, nowstr, nowNameStr


