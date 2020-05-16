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
# Contributions   : Ayose Cazorla León
# Created On      : Lun Dic 15 8:37:12 2003
# Last Modified By: Juan Jesús Ojeda Croissier
# Last Modified On: Mie Dic 17 05:04:44 2003
 
'''
Módulo de detección y configuración de hardware en sistemas GNU/Linux.

Este módulo pretende cubrir las necesidades de detección y configuración
de hardware del proyecto Metadistros (http://metadistros.hispalinux.es).
Para ello se usarán todas las bases de datos de hardware posibles, con 
el fin de ser lo más completo posible.

En este momento consta de una clase Pci que se encarga de la detección y
configuración de todos los dispositivos conectados al bus pci, y la clase
Isapnp, que realiza la misma función, pero a patir del bus isapnp.
En el futuro se esperan tener clases para desempeñar los siguientes cometidos:
- Pci: Detección y configuración del bus pci
- Isapnp: Detección y configuración del bus isa(pnp)
'''
 
from utils.debug import *
from utils.shell import joinpath

def get_pci_modules(filename = 'pci.lst'):
    '''get_pci_modules(filename = 'pci.lst') -> list of modules

    Busca en el proc información sobre los dispositivos
    PCI y los compara con los mapas de módulos del kernel
    y la base de datos de hardware de Kudzu
    '''

    drivers = []
    lines = []
    proc = []

    import os.path
    path, file = os.path.split(__file__)
    del file
    filename = joinpath(path, filename)
    if not read_file(filename, lines):
        print 'pcimap'
        import sys
        sys.exit(1)
    if not read_file('/proc/bus/pci/devices', proc):    
        print 'proc'
        import sys
        sys.exit(1)
    
    pcitable = []
    for line in lines:
        fields = line.split()
        pcitable.append(fields)
    for entry in proc:
        for line in pcitable:
	    if line[0] in entry:
		drivers.append(line[1])

    return drivers
    

class Isapnp:
    '''Isapnp

    Esta clase tiene un atributo, una lista de módulos
    detectados (drivers).
    '''

    def __init__(self, config = None):
        '''Isapnp(config)

        Busca en el proc información sobre los dispositivos
        ISAPNP y los compara con los mapas de módulos del kernel
        '''

        self.drivers = []
        if config is None:
            procfile = '/proc/bus/isapnp/devices'
            try:
                kernel = open('/proc/sys/kernel/osrelease').readline().strip()
            except IOError:
                echo_debug('''
  Se ha producido un error al no tener permisos para leer
  la información de su kernel. Revise su configuración, o
  ejecute el programa como root.''', 'ERROR')
                import sys
                sys.exit(1)
        else:
            procfile = config.get('isapnp', '/proc/bus/isapnp/devices')

            if config.has_key('isapnpmap'):
                mapfile = config['isapnpmap']
            else:
                try:
                    kernel = open('/proc/sys/kernel/osrelease').readline().strip()
                except IOError:
                    echo_debug('''
  Se ha producido un error, al no tener permisos para leer
  la información de su kernel. Revise su configuración, o
  ejecute el programa como root.''', 'ERROR')
                    import sys
                    sys.exit(1)
                
                mapfile = '/lib/modules/%s/modules.isapnpmap' % kernel
            
        try:
            proc = open(procfile).readlines()
        except IOError:
            echo_debug('''
  Parece ser que no tiene dispositivos ISAPNP.
  Se detectarán unicamente los PCI.''', 'ERROR')
            return None
            
        isapnpmap = open(mapfile).readlines()

        for line in proc:
            line = line.split()
            a = line[1]
            dev_hex = ('0x' + a[-4:][2:] + a[-4:][:2] , '0x' + a[:7][-4:][2:] +  a[:7][-4:][:2] )
            for line in isapnpmap:
                line = line.split()
                if (line[2] == dev_hex[1]) and (line[5] == dev_hex[0]):
                    driver = line[0]
                    if driver not in self.drivers:
                        self.drivers.append(driver)
         

    def get_modules(self):
        '''show_modules
    
        Devuelve la lista de módulos a cargar
        '''
        return self.drivers

        

def make_modules(root = '/'):
    '''make_modules(root = '/')

    Crea el archivo /etc/modules, con los drivers necesarios en
    el arranque.

    Puede crear el archivo en otro sitio pasandole como parámetro
    el directorio(/, /mnt/tmp/...) donde se desea crear.
    '''
    f = open(root + '/etc/modules', 'w')
    f.write('''
# /etc/modules: kernel modules to load at boot time.
#
# This file should contain the names of kernel modules that are
# to be loaded at boot time, one per line.  Comments begin with
# a "#", and everything on the line after them are ignored.
''')
    mods_isa = Isapnp()
    mods_pci = get_pci_modules()
    if mods_isa:
        modules = mods_pci + mods_isa.drivers
    else:
        modules = mods_pci
        
    for driver in modules:
        f.write(driver + '\n')
    f.close()

def load_modules():
    '''load_modules()

    Carga los módulos(drivers) detectados
    '''
    import os
       
    if os.getuid() != 0:
        echo_debug('No ha podido cargar los módulos, necesita ser root', 'ERROR')
        return None
        
    mods_isa = Isapnp()
    mods_pci = get_pci_modules()
    if mods_isa:
        modules = mods_pci + mods_isa.drivers
    else:
        modules = mods_pci
        
    for driver in modules:
        do_debug('modprobe %s' % driver)
   

def is_module(module=False):
    '''is_module(module)

    Comprueba si está cargado o no un módulo.
    '''
    if not module:
        echo_debug('No se ha pasado ningún módulo', 'ERROR')
        return False
    lines = open('/proc/modules').readlines()
    for line in lines:
        if  line.startswith(module):
            return True

    return False

   

if __name__ == '__main__':
                   
    pci = get_pci_modules()
    isa = Isapnp(config = config)
    
    print 'Módulos:\n\t' + '\n\t'.join(pci)
    print '\t' + '\n\t'.join(isa.get_modules())
    

# vim:ai:et:sts=4:tw=80:sw=4:
