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

# Authors
#	    Juan Jesús Ojeda Croissier <juanjesus.ojeda@hispalinux.es>
#	    Ayose Cazorla León <ayose.cazorla@hispalinux.es>
 
'''
Wizard

Modulo encargado de buscar las configuraciones y
conectar la interfaz de usuario.
'''

def parse(name, dct):

    for line in open(name).readlines():

        line = line.strip()
        if line[0] == '#':
            continue

        for word in line.split():
            if '=' in word:
                name, val = word.split('=', 1)
		NAME = name.upper()
                dct[NAME] = val


def get_questions(vars):

    questions = {}
    for var in vars.keys():
        if not var.startswith('Q'): continue

        questions[var] = vars[var] == 'Y'
        del vars[var]

    return questions


def main():
    
    configs = {}
    
    # Leer variables
    parse('conf/q.conf', configs)
    parse('conf/var.conf', configs)
    parse('/proc/cmdline', configs)

    # separar preguntas
    questions = get_questions(configs)

    from uis import gtk, text, noconf
    UIS = { 'GTK': gtk.Gtk,
	    'TEXT': text.Text,
	    'NO': noconf.Noconf }
	    
    val = configs['UI'].upper()
    try:
	UI = UIS[val]()
    except KeyError:
	UI = noconf.Noconf()

    UI.make(questions, configs)
    
    return configs


if __name__ == '__main__':
    configs = main()
    for key in configs.keys():
	if '_' in configs[key]:
	    val = configs[key].replace('_', ' ')
	else:
	    val = configs[key]
	print "%s : %s" % (key, val)
    
    
# vim:ai:et:sts=4:tw=80:sw=4:
