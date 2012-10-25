# bplate

""" Global object registry  """

data = {}

def add(label, object):
    """ add a object """

    data[label] = object


def get(label):
    """ return reference to object """

    if data.has_key(label):
        return data[label]
    else:
        return None


# lists of objects maintained by the registry. Usually used
# to send events to

listDict = {}
def addList(label, object):
    """ add object to a named list, if a list name does not exist - add it """
    
    if listDict.has_key(label):
        listDict[label].append(object)
    else:
        lst = [object]
        listDict[label] = lst

def getList(label):
    """ returns named list """
    
    if listDict.has_key(label):        
        return listDict[label]
    else:
        return []
    

