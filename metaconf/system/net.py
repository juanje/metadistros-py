#!/usr/bin/python
# -*- coding: latin1 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Author          : Juan Jesús Ojeda Croissier <juanjesus.ojeda@hispalinux.es>
# Created On      : Vie Ene 02 07:00:12 2003
# Last Modified By: Juan Jesús Ojeda Croissier
# Last Modified On: Jue Ene 08 04:20:04 2004
 
'''
Módulo de manejo de interfaces de red

Este módulo detecta las distintas interfaces de red.
'''
import os.path, sys
PATH = os.path.realpath('..')
if PATH not in sys.path:
    sys.path.append(PATH)
 

def get_interfaces():
    '''get_interface() -> list

    Devuelve una lista con las interfaces de red encontradas.
    '''
    
    import re
    from utils.debug import read_file

    interfaces = []
    lines = []
    dev = re.compile('^\s+([a-z]+[0-9]):')
    if not read_file('/proc/net/dev',lines):
	return interfaces
	
    for line in lines:
        found = dev.match(line)
        if found:
            interfaces.append(found.group(1))
    return interfaces


def get_wireless():
    '''get_wireless() -> list

    Devuelve una lista con las interfaces wireless encontradas.
    '''
    
    import re
    from utils.debug import read_file

    interfaces = []
    lines = []
    dev = re.compile('^\s+([a-z]+[0-9]):')
    if not read_file('/proc/net/wireless',lines):
	return interfaces
	
    for line in lines:
        found = dev.match(line)
        if found:
            interfaces.append(found.group(1))
    return interfaces


def make_interfaces(configs = None, root='/mnt'):
    '''make_interfaces(configs = None, root='/mnt') -> bool

    Crea el archivo /etc/network/interfaces a partir de los
    datos de un diccionario pasado por parametro.
    '''
    
    from os.path import isfile
    from utils.debug import echo_debug, read_file
    from utils.shell import joinpath
    
    filename = joinpath(root, 'etc/network/interfaces')
    if not isfile(filename):
    	echo_debug('make_interfaces: No exite el archivo %s' % filename,'ERROR')
	return False
    file = open(filename, 'w')
    file.write('''
# /etc/network/interfaces -- configuration file for ifup(8), ifdown(8)

# The loopback interface
auto lo
iface lo inet loopback

# The network cards
    ''')
    interfaces = get_interfaces()
    wireless = get_wireless()
    #FIXME: Terminar for 
    for iter in interfaces:
	if iter in wireless:
	    print 'configuraciones wireless'
	else:
	    print 'configuraciones ethernet'

    file.close()
    return True
    

if __name__ == '__main__':
    for interface in get_interfaces():
        print interface


# vim:ai:et:sts=4:tw=80:sw=4:
