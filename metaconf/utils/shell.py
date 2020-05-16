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
# Created On      : Jue Feb 12 16:10:12 2004
 
'''
Módulo de utilidades

Este módulo provee de varias utilidades utiles para el Calzador:
- abspath:
- cp
- cp_a:
- cp_dev:
- cp_f:
- cp_s:
- get_os:
- joinpath: 
- ln:
- mkdir:
- mount_file:
- umount:

'''

from debug import echo_debug, do_debug

def joinpath(path, basename):
    import os.path
    return os.path.join(path, basename)

def abspath(path):
    import os.path
    return os.path.abspath(os.path.normpath(path))

def get_os(root='/'):
    '''Devuelve la distro que es.

    Basarse en lo que hay en las GST'''
    distro = ''
    return distro

def cp(source, dest):
    import shutil
    try:
        shutil.copy2(source, dest)
    except IOError, error:
        echo_debug('cp -p %s %s' % (source, dest))
        echo_debug(error, 'ERROR')
        return False
    return True

def rmdir(dir):
    '''rmdir(dir) -> bool
    
    Borra un directorio y su contenido.
    '''
    import os

    if not os.path.isdir(dir):
        echo_debug('%s no es un directorio' % dir)
        return False
        
    names = os.listdir(dir)
    for name in names:
        name_path = joinpath(dir, name)
        if os.path.exists(name_path):
            if os.path.islink(name_path):
                try:
                    os.remove(name_path)
                except OSError, error:
                    echo_debug('rm -f %s' % name_path)
                    echo_debug(error, 'ERROR')
            elif os.path.isdir(name_path):
                rmdir(name_path)
            else:
                try:
                    os.remove(name_path)
                except OSError, error:
                    echo_debug('rm -f %s' % name_path)
                    echo_debug(error, 'ERROR')
   
    try:
        os.rmdir(dir)
    except OSError, error:
        echo_debug('rmdir %s' % dir)
        echo_debug(error, 'ERROR')
        return False
    return True
   

def cp_f(sorce, dest):
    import os

    if os.path.exists(dest):
        if os.path.isdir(dest):
            rmdir(dest)
        else:
            try:
                os.remove(dest)
            except OSError, error:
                echo_debug('cp -f %s %s' % (source, dest) )
                echo_debug(error, 'ERROR')
                return False
    if os.path.isdir(source):
        if cp_a(source, dest):
            return True
    else:
        if cp(source, dest):
            return True
    return False

def mkdir(dir):
    import os, os.path 
    try:
        if os.path.exists(dir):
            if not os.path.isdir(dir):
                os.remove(dir)
                os.mkdir(dir)
        else: # Si no existe lo crea
	    head, tail = os.path.split(dir)
	    if not os.path.isdir(head):
		if not head.startswith('/') or not head.starstwith('.'):
		    head = './' + head
		mkdir(head)
            os.mkdir(dir)
    except OSError, error:
        echo_debug('mkdir %s' % (dir) )
        echo_debug(error, 'ERROR')
        return False
    return True
        
def ln(source, dest):
    import os 
    try:
	#FIXME: Poner dest por defecto (.)
        os.symlink(source, dest)    
    except OSError, error:
        echo_debug('ln -s %s %s' % (source, dest) )
        echo_debug(error, 'ERROR')
        return False
    return True
   
def cp_dev(source, dest):
    echo_debug('Copiando dispositivos desde %s hasta %s ...' % (source, dest), 'MSG' )    
    # Compruebo que existe dest y que es un directorio
    if not mkdir(dest):
        return False
        
    if do_debug('cp -a %s/* %s/' % (source, dest) ):
        return True
    return False

def cp_a(source, dest):
    import os 
    
    # Compruebo que existe dest y que es un directorio
    if not mkdir(dest):
        return False
        
    try: # Saca el listado de archivos y directorios de source
        names = os.listdir(source)
    except OSError, error:
        echo_debug('cp_dir %s %s' % (source, dest) )
        echo_debug(error, 'ERROR')
        return False
        
    for name in names:
        source_path = joinpath(source, name)
        dest_path   = joinpath(dest, name)
        
        if os.path.exists(dest_path):
            if os.path.isdir(source_path):
                cp_a(source_path, dest_path)
            continue
        # Si es un directorio copia recursivamente su contenido a "dest"
        if os.path.isdir(source_path):
            cp_a(source_path, dest_path)
        # Si es un enlace crea un enlace en su destino
        elif os.path.islink(source_path):
            link_source = os.readlink(source_path)
            ln(link_source, dest_path)
        # Si no es un directorio o un enlace, lo copia    
        else:
            cp(source_path, dest_path)
            
    return True
            

def cp_s(source, dest, deep=1):
    import os 

    # Compruebo que existe dest y que es un directorio
    if not mkdir(dest):
        return False
    
    try:
        names = os.listdir(source)
    except OSError, error:
        echo_debug('cp_ln %s %s' % (source, dest) )
        echo_debug(error, 'ERROR')
        return False
        
    for name in names:
        source_path = joinpath(source, name)
        dest_path   = joinpath(dest, name)
        
        if os.path.isdir(source_path):
            # Si "name" es un directorio, llama recursivamente a la funcion
            if not os.path.exists(dest_path):
                # Comprueba si se ha llegado a la profundidad tope
                if deep <= 0:
                    # Si se ha llegado, crea un enlace de todo la que haya a
                    # dest. Tanto archivos com directorios
                    ln(source_path, dest_path)
                    continue
                cp_s(source_path, dest_path, deep-1)
        else: # Si no es un directorio crea un enlace
            if not os.path.exists(dest_path):
                ln(source_path, dest_path)
            
    return True

def umount(mnt):
    import os

    if os.getuid() != 0:
        echo_debug('No ha podido montar %s, necesita ser root' % image, 'ERROR')
        return False
    
    if do_debug('umount %s' % mnt):
        return True
    return False
        
def mount_file(image, mnt):
    '''Monta un archivo (image) en un punto de montaje o directorio (mnt).

    Montará dicho archivo en loopback y el sistema de ficheros se identificará
    por la extensión (*.cloop, *.squashfs, *.iso). En caso de no tener ninguna
    se supondrá que es iso9660.
    '''
    import os
    from kmodules import is_module

    if os.getuid() != 0:
        echo_debug('No ha podido montar %s, necesita ser root' % image, 'ERROR')
        return False
        
    # Busca la extension del archivo
    name = os.path.basename(image)
    ext = name.split('.')[-1]
    
    if ext == 'squashfs':
        if is_module('squashfs') or do_debug('modprobe squashfs'):
            if do_debug('mount -r -o loop -t squashfs %s %s' % (image, mnt)):
                return True
    elif ext == 'cloop':
        if is_module('cloop') or do_debug('modprobe cloop'):
            for i in range(0,7):
                if do_debug('mount -r -o loop=/dev/cloop%d -t iso9660 %s %s' % (i, image, mnt)):
                    return True
    else: # Si no es ni .cloop, ni .squashfs, supone iso9660
        if do_debug('mount -r -o loop -t iso9660 %s %s' % (image, mnt)):
            return True    
    
    return False

    

# vim:ai:et:sts=4:tw=80:sw=4:
