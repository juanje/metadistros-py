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
# Created On      : Mar Dic 30 07:00:12 2003
# Last Modified By: Juan Jesús Ojeda Croissier
# Last Modified On: Sab Ene 03 09:51:04 2004
 
'''
Módulo de manejo de discos y particiones

Este módulo detecta discos y particiones mediante
libparted y crea entradas para el /etc/fstab
'''

import parted
from metaconf.utils.debug import *
from metaconf.utils.shell import *

fsystems = {'ext2':'ext2\trw', \
        'ext3':'ext3\trw', \
        'reiserfs':'reiserfs\trw',\
        'fat32':'vfat\trw,user,noauto', \
        'fat16':'fat\trw,user,noauto', \
        'linux-swap':'swap\tdefaults', \
        'ntfs':'ntfs\tro,noexec,noauto,user', \
        'xfs':'xfs\trw'}

win_labels = ['a', 'b', 'C', 'D', 'E', 'F', 'G', 'H']
        

class Disks:
    '''Disks

    Esta clase crea dos listas, una con los discos
    duros detectados y otra con las particiones.
    '''
    def __init__(self):
        '''Disks()

        Carga el archivo de información sobre las particiones
        del proc (/proc/partitions), obteniendo los discos y
        particiones del equipo.
        '''
	file = []
	if not read_file('/proc/partitions', file):
            import sys
            sys.exit(1)


        self.disks = []
        self.partitions = []

        for i in file[2:]:
            dev = i.split()
            if len(dev[3]) == 3:
                self.disks.append(dev[3])
            elif len(dev[3]) == 4:
                self.partitions.append(dev[3])


    def get_disks(self):
        '''get_disks(self)

        Devuelve los discos detectados en una lista.
        '''
        return self.disks

    def get_open_disks(self):
        '''get_open_disks(self)

        Devuelve una lista con los descriptores de los
        discos detectados.
        '''
        parted.init()

        disks = []
        for device in self.disks:
            disk = parted.device_get('/dev/' + device).disk_open()
            disks.append(disk)
        return disks


    def get_disk_partitions(self, disk= None):
        '''get_disk_partitions(self, disk=None)

        Devuelve las particiones encontradas en el disco
        disk.
        '''
        partitions = []
        if disk:
            for part in self.partitions:
                if disk in part:
                    partitions.append(part)
        return partitions


    def get_partitions(self):
        '''get_partitions(self)

        Devuelve una lista de tuplas de 2 valores, el primero
        es el nombre de la partición y el segundo el sistema
        de ficheros de la misma.
        '''
        values = []
        disks = self.get_open_disks()
        if len(disks) is 0:
            echo_debug('No se ha podido encontrar ningún Disco Duro', 'ERROR')
            import sys
            sys.exit(2)
    
        for disk in disks:
            if not disk:
                continue
            for partition in disk.get_part_list():
                if partition.get_type() not in (4,8,9):
                    fs = partition.get_fs_type()
                    if fs:
                        num_fs = disk.get_dev().get_path() + str(partition.get_num()),\
                                    partition.get_fs_type().get_name()
                        values.append(num_fs)
        return values


def get_cdroms():
    '''get_cdroms()

    Devuelve una lista con los nombres de los dispositivos
    de cdrom.
    '''
    file = []
    if not read_file('/proc/sys/dev/cdrom/info', file):
        return None
    cdroms = []
    
    line = file[2].split()
    if len(line) < 3:
        return None
    for dev in line[2:]:
        if 'sr' in dev:
            dev = 'scd' + dev[2:]
        cdroms.append(dev)
    return cdroms

def get_floppies():
    '''get_floppies()

    Devuelve una lista con los "floppies" (disquetes)
    detectados.
    '''
    import _kudzu

    floppies = []
    for res in _kudzu.probe(_kudzu.CLASS_FLOPPY, _kudzu.BUS_UNSPEC,0):
        floppies.append(res["device"])
    return floppies
        
        
def fstab_entries(root=''):
    '''fstab_entries(root=)

    Devuelve una lista con las entradas del fstab 
    para las distintas particiones encontradas.

    En caso de pasarse el parámetro root, se establecerá
    éste como partición root en el fstab.
    '''
    linux = 0
    windows = 1
    entries = []

    disks = Disks()
    partitions = disks.get_partitions()
    for part, fs in partitions:
        if 'swap' in fs:
            entry = '%s\tswap\t%s\t0\t0' % (part, fsystems[fs])
        elif fs in ('fat32', 'fat16', 'ntfs'):
            windows += 1
            entry = '%s\t/mnt/%s:\t%s\t0\t0' % (part, win_labels[windows], fsystems[fs])
        elif part in root:
            entry = '%s\t/\t%s\t0\t0' % (root, fsystems[fs])
        else:
            linux += 1
            entry = '%s\t/mnt/linux%d\t%s\t0\t0' % (part, linux, fsystems[fs])
        entries.append(entry)
    # Añadimos las entradas de los USB
    scsi = 0
    for disk in disks.get_disks():
        if 'sd' in disk:
            scsi += 1

    list = ['a','b','c','d','e','f','g']
    for i in range(0,2):
        entry =  'none\t/mnt/usb%i\tsupermount\tdev=/dev/sd%c1,fs=vfat,sync\t0\t0' % \
                  (i, list[scsi])
        entries.append(entry)
	mount_point = joinpath(root,'mnt/usb%i' % i)
	mkdir(mount_point)
        scsi += 1
    # Añadimos los cdroms
    cdrom = 0
    for cd in get_cdroms():
        entry = 'none\t/cdrom%i\tsupermount\tdev=/dev/%s,fs=iso9660\t0\t0' % \
                    (cdrom, cd)
        entries.append(entry)
	mount_point = joinpath(root,'cdrom%i' % cdrom)
	mkdir(mount_point)
        cdrom += 1
    # Añadimos los disquetes (floppies)
    floppy = 0
    for fd in get_floppies():
        # No deberia haber mas de 2 disquetes: a:/, b:/, ¿C:/?
        if floppy > 1:
            break
        entry =  'none\t/%s:\tsupermount\tdev=/dev/%s,fs=vfat,sync\t0\t0' % \
                    (win_labels[floppy], fd)
        entries.append(entry)
	mount_point = joinpath(root,'%s:' % win_labels[floppy])
	mkdir(mount_point)
        floppy += 1

    return entries

def make_fstab(root_dir='/mnt', root_dev=''):
    '''make_fstab(root_dir='/mnt', root_ddev='')

    Crea un archivo /etc/fstab con las entradas devueltas
    por la fuincion fstab_entries().
    
    Puede crear el archivo en otro sitio pasandole como parámetro
    "etc" el directorio(/, /tmp/, /mnt/...) donde se desea crear.
    '''
    try:
	filename = joinpath(root_dir, 'etc/fstab') 
        fstab = open(filename, 'w')
    except IOError:
        echo_debug('No se pudo crear el archivo %s/etc/fstab' % root_dir , 'ERROR')
        return False
    fstab.write('''
# /etc/fstab: static file system information.
#
# The following is an example. Please see fstab(5) for further details.
# Please refer to mount(1) for a complete description of mount options.
#
# Format:
#  <file system>         <mount point>   <type>  <options>      <dump>  <pass>
#
none    /proc       proc   defaults            0 0
none    /dev/pts    devpts mode=0622           0 0
none    /proc/bus/usb   usbdevfs        rw      0 0
''')
    for entry in fstab_entries(root_dev):
        fstab.write(entry + '\n')
    return True


if __name__ == '__main__':
    import sys
    root = ''
    if len(sys.argv) is 2:
        root = sys.argv[1]
    for i in fstab_entries(root):
        print i



# vim:ai:et:sts=4:tw=80:sw=4:
