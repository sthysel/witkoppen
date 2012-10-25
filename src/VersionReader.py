# blate

""" version management """

import os.path


pth = os.path.join('.', '.version')
# pth = '.version'

try:
    f = open(pth, 'r')
    ln = f.readline()
    f.close()
    VERSION = ln.strip()
except IOError, x:
    print x
    print "No suitable Version File was found"
    VERSION = '0.0.1'


if __name__ == '__main__':
    unittest()
