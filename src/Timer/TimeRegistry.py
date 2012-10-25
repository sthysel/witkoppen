# bplate


""" Panels/objects that are interested in timer events register here"""

data = {}

def add(label, object):
    """ add a object """
    
    if not data.has_key(label):
        data[label] = object
    else:
        return False
    return True


def get(label):
    """ return reference to object """

    if data.has_key(label):
        return data[label]
    else:
        return None

