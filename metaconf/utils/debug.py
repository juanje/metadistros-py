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
# Last Modified On: Sab Ene 03 14:48:04 2004
 
'''
Módulo de depuración

Este módulo provee de dos funciones:
- do_debug: que ejecuta alguna orden manando las
    diferentes salidas al syslog del sistema
- echo_debug: esta función manda un mensaje al
    syslog del systema
- read_file: lee el contenido de un archivo y 
lo mete en una lista pasada por parámetro

En estas funciones se mostrarian los mensajes por
pantalla si estuviera definida la variable de 
entorno DEBUG, como 'Y'
'''

                                                                                
def echo_debug(message, tag='MSG'):
    '''echo_debug(message, tag='MSG')

    Manda el mensaje "message" al syslog del sistema,
    con la etiqueta "tag".
    En caso de tener definida la variable de entorno
    DEBUG como 'Y', se mostrara el mensaje por pantalla
    también.
    '''
    import os, syslog
                                                                                
    debug = os.getenv('DEBUG')
    message = tag + ': ' + str( message )
    if debug is 'Y':
        syslog.syslog(message)
        print '\n%s\n' % message
    else:
        syslog.syslog(message)
                                                                                
                                                                                
def do_debug(cmd = None):
    '''do_debug(cmd = None)

    Ejecuta la orden "cmd" mandando la salida estandar
    y la salida de error a el syslog del sistema.
    En caso de tener definida la variable de entorno
    DEBUG como 'Y', se mostrara el mensaje por pantalla
    también.
    '''
    
    import os
    if cmd is None:
        return True
    stdin, stdout, stderr = os.popen3(cmd)
    stdin.close()
    echo_debug(cmd,'CMD')
    error = stderr.readlines()
    if error:
        for i in error:
            echo_debug(i.strip(), 'ERROR')
        return False
    outs = stdout.readlines()
    if outs:
        for i in outs:
            echo_debug(i.strip())
    return True                                                                
def read_file(file, list):
    '''read_file(file, list)

    Lee el contenido del archivo y lo meta en una
    lista pasada por parámetro. Devuelve True si consigue
    leerlo y False si no lo consigue.
    En caso de no poder leer el archivo, se manda el error
    al syslog.
    '''
    try:
	list += open(file).readlines()
    except IOError, error:
	echo_debug(error, 'ERROR')
	return False
    return True

    
# vim:ai:et:sts=4:tw=80:sw=4:
