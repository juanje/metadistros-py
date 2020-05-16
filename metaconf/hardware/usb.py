#!/usr/bin/python

import re

rex = re.compile('P:\s+Vendor=([a-f0-9]+)\s+ProdID=([a-f0-9]+)\s+Rev= ([0-9]\.[0-9]+)\s*')
drex = re.compile('I:\s+.*Driver=(.+)\s*')

lines = open('/proc/bus/usb/devices').readlines()

for i in lines:
    found = rex.match(i)
    dfound = drex.match(i)
    if found:
        print 'Vendor: %s ProdID: %s Rev: %s' % (found.group(1), found.group(2),found.group(3)),
    if dfound:
        print 'Driver: ' + dfound.group(1)
