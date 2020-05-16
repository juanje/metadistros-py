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
Módulo de manejo de usuarios del sistema

Este módulo comprueba si existen usuarios en el sistema, los
crea y les cambia la password.
'''
import os.path, sys
PATH = os.path.realpath('..')
if PATH not in sys.path:
    sys.path.append(PATH)
 

def user_exist(user='', root='/mnt/'):
    '''user_exist(user='', root='/mnt/')

    Devuelve True si esiste el usuario y False si no existe
    '''
    
    import re
    from utils import debug, shell

    if user == '':
	debug.echo_debug('No se ha pasado un nombre de usuario', 'ERROR')
	return False
	
    is_user = re.compile('^(%s):' % user)
    passwd = shell.joinpath(root, 'etc/passwd')
    lines = open(passwd).readlines()
    for line in lines:
        found = is_user.match(line)
        if found:
	    return True
    return False

def is_shadow(root='/mnt/', file='shadow'):
    from os.path import isfile
    from utils import debug, shell
    filename = shell.joinpath(root, 'etc/' + file)
    if file in ['shadow', 'gshadow']:
	return isfile(filename)
    else:
	debug.echo_debug('is_shadow: No ha introducido un nombre de archivo válido', 'ERROR')
	return False


def change_pass(user='', passwd='', root='/mnt/'):
    '''change_pass(user='', passwd='', root='/mnt/')

    Cambia la clave a un usuario
    '''
    from utils import debug
	
    if user == '' or passwd == '':
	debug.echo_debug('No se han pasado los parámetros correctos', 'ERROR')
	return False
    elif not user_exist(user):
	debug.echo_debug('El usuario %s, no existe, no se ha podido cambiar la clave' % user , 'ERROR')	
	return False
    
    import crypt
    from utils import shell
    
    pass_list = []
    if is_shadow(root):
	file = 'shadow'
    else:
	file = 'passwd'
    passfile = shell.joinpath(root, 'etc/' + file)
    lines = open(passfile).readlines()
    for line in lines:
        fields = line.split(':')
        if fields[0] == user:
	    fields[1] = crypt.crypt(passwd, 'o3l*2_X<.3q¡^')
	    line = ':'.join(fields)
	pass_list.append(line)

    filename = open(passfile, 'w')
    for line in pass_list:
	filename.write(line)

    filename.close()
    return True

def add_group(group='', guid='1000', root='/mnt/'):
    '''add_group(group='', guid=1000', root='/mnt/')

    Añade un grupo
    '''
    from utils import debug
	
    if group == '':
	debug.echo_debug('No se han pasado los parámetros correctos', 'ERROR')
	return False
    elif group_exist(group):
	return True
    from utils import shell
    
    file = 'etc/group'
    pass_list = []
    if is_shadow(root):
	file = 'shadow'
    else:
	file = 'passwd'
    filename = shell.joinpath(root, file)
    groupfile = open(filename, 'a')
    groupfile.write('%s:x:%s:' % (group, guid))
    if is_shadow('gshadow'):
	filename = shell.joinpath(root, 'etc/gshadow')
        groupfile = open(filename, 'a')
        groupfile.write('%s:!::' % group)
    return True
	
def add_to_group(user='', group='', root=''):
    '''

    Añade un usuario a un grupo
    '''
    #FIXME: Acabar funcion
    pass

def add_user(user='', passwd='', root='/mnt/'):
    '''add_user(user='', passwd='', root='/mnt/')

    Añade un usuario
    '''
    from utils import debug
	
    if user == '' or passwd == '':
	debug.echo_debug('No se han pasado los parámetros correctos', 'ERROR')
	return False
    if user_exist(user):
	change_pass(user, passwd, root)
    else:
    #FIXME: Acabar funcion
	pass

	
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 2:
	print 'ERROR: Debe pasar un argumento. El usuario'
	sys.exit(1)
	
    user = sys.argv[1]
    if user_exist(user):
	print 'Sí, existe el usuario: %s' % user
    else:
	print 'No, no existe el usuario: %s' % user


# vim:ai:et:sts=4:tw=80:sw=4:
