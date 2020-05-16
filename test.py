#!/usr/bin/python

'''Script de pruebas

Este Script sirve para comprobar que las librarias funcionan bien.
'''

import os.path, sys
PATH = os.path.realpath('metaconf')
if PATH not in sys.path:
    sys.path.append(PATH)
 
from utils import debug, shell

debug.echo_debug('Empieza el script')
shell.mkdir('/tmp/etc')
shell.mkdir('/tmp/etc/X11')

from hardware import kmodules, disks, xconf

for i in kmodules.get_pci_modules():
    print i,
print '\n'

X = xconf.Xconf()
print 'X Driver: %s' % X.get_card()

kmodules.make_modules('/tmp')

disks.make_fstab('/tmp')

for i in disks.get_cdroms():
    print 'CDRom: %s' % i

xconf.make_xf86config('/tmp')

from system import users, net

for i in net.get_interfaces():
    print 'Interfaz de red: %s' % i 
