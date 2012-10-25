"""
Keeps data contained
"""

import copy

global data
global register

data = []
register = []
currentIndex = None

def setResult(res):
    global data
    data = copy.copy(res)


def getResult():
    """ return the result """
    return data


def addListener(panel):
    """ a listener must have a reload() method"""
    register.append(panel)
    
    
def notify(index):
    """notify each panel that new data is available """

    global currentIndex
    
    currentIndex = index
    try:
        d = data[index]
    except IndexError, x:
        print x
        return
    
    for p in register:
        try:
            p.reload(d)
        except AttributeError, x:
            print x