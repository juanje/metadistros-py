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
 
'''
Gtk

Interfaz gráfica hecha en Gtk, que interactua con el usuario
'''

class Gtk:
    def __init__(self):
	pass

    def make(self, questions={} , configs={}):
        if len(questions) == 0 or len(configs) == 0:
            return None
        return configs

def info():
    print 'Gtk: Interfaz gráfica que interactua con el usuario'

if __name__ == '__main__':
    info()                                                                                
    
# vim:ai:et:sts=4:tw=80:sw=4:
