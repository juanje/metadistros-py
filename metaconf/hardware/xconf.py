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
# Created On      : Mie Dic 31 16:00:12 2003
# Last Modified By: Juan Jesús Ojeda Croissier
# Last Modified On: Jue Ene 08 04:38:04 2004
 
'''
Módulo de detección y configuración de las X

Xconf detecta lo necesario para configurar la
tarjeta gráfica y crea el XF86Config-4
'''
 
class Xconf:
    '''Xconf

    Detecta los valores para los parámetros de
    la tarjéta gráfica:
    - Bus
    - BusId
    - Driver
    - hsync (Frecuencia horizontal)
    - vsync (Frecuencia vertical)
    - Memoria
    '''
    # Valores predeterminados
    busid = '0:0:0'
    bus = 'PCI'
    card = 'vesa'
    vsync = '50 - 90'
    hsync = '31.5 - 57'
    mem = 0
    
    def __init__(self, filename = 'cards.lst'):
        '''Xconf(self, filename = 'cards.lst')

        Detecta el driver de la tarjeta gráfica mediante
        el módulo "metaconf.kmodules", el identificador 
        del Bus lo obtiene del "/proc/bus/pci/devices" y
        usando Kudzu, detecta la frecuencia del monitor
        y la memoria de la tarjeta.

        Guarda todos estos datos en los atributos de 
        la clase
        '''
        # Se detecta el driver de la tarjeta gráfica
	lines = []
	proc = []

	import os.path
	from utils.shell import joinpath
	from utils.debug import read_file
	
	path, file = os.path.split(__file__)
	del file
	filename = joinpath(path, filename)
	if not read_file(filename, lines):
	    import sys
	    sys.exit(1)
	if not read_file('/proc/bus/pci/devices', proc):    
	    import sys
	    sys.exit(1)
	    
	pcitable = []
	for line in lines:
	    fields = line.split()
	    pcitable.append(fields)
	for entry in proc:
	    for line in pcitable:
		if line[0] in entry:
		    bus = entry.split()[0]
		    self.card = line[1]

        devfn = int(bus,16)
        bus = devfn >> 8
        idev = (devfn >> 3) & 0x1F
        func = devfn & 0x07
        # Se establece el identificador del Bus
        self.busid = 'PCI:%d:%d:%d' % (bus, idev, func)
        # Se comprueba si el bus es PCI o AGP
        if bus is 1:
            self.bus = 'AGP'


        # Se detecta la frecuencia del monitor
        import _kudzu


        for res in _kudzu.probe(_kudzu.CLASS_MONITOR, _kudzu.BUS_DDC, 0):
            self.hsync = '%d-%d' % (res["horizSyncMin"],res["horizSyncMax"])
            self.vsync = '%d-%d' % (res["vertRefreshMin"],res["vertRefreshMax"])

        # Se detecta la memoria de la tarjeta gráfica
        for res in _kudzu.probe(_kudzu.CLASS_VIDEO, _kudzu.BUS_DDC, 0):
            self.mem = res["mem"]

                    
    def get_busid(self):
        '''get_busid()

        Devuelve el identificador del Bus de la tarjeta
        gráfica.
        '''
        return self.busid
                    
    def get_bus(self):
        '''get_bus()

        Devuelve el tipo de Bus de la tarjeta gráfica. Puede
        ser PCI o APG.
        '''
        return self.bus
                    
    def get_card(self):
        '''get_card()

        Devuelve el driver de la tarjeta gráfica.
        '''
        return self.card
                    
    def get_vsync(self):
        '''get_vsync()

        Devuelve el rango de frecuencia vertical del monitor.
        '''
        return self.vsync
                    
    def get_hsync(self):
        '''get_hsync()

        Devuelve el rango de frecuencia horizontal del monitor.
        '''
        return self.hsync
                    
    def get_mem(self):
        '''get_mem()

        Devuelve la memoria de la tarjeta gráfica.
        '''
        return self.mem

def make_xf86config(root = '/'):
    '''make_xf86config(root = '/')

    Crea el archivo /etc/X11/XF86Config-4 a partir de la clase
    Xconf.

    Admite el parámetro "root" que indica el directorio
    padre del sistema donde se quieren configurar las X.
    '''
    template = '''
Section "Files"
	FontPath	"unix/:7100"			# local font server
	# if the local font server has problems, we can fall back on these
	FontPath	"/usr/lib/X11/fonts/Type1"
	FontPath	"/usr/lib/X11/fonts/CID"
	FontPath	"/usr/lib/X11/fonts/Speedo"
	FontPath	"/usr/lib/X11/fonts/misc"
	FontPath	"/usr/lib/X11/fonts/cyrillic"
	FontPath	"/usr/lib/X11/fonts/100dpi"
	FontPath	"/usr/lib/X11/fonts/75dpi"
EndSection

Section "Module"
	Load	"GLcore"
	Load	"bitmap"
	Load	"dbe"
	Load	"ddc"
	Load	"dri"
	Load	"extmod"
	Load	"glx"
	Load	"int10"
	Load	"record"
	Load	"speedo"
	Load	"type1"
	Load	"vbe"
	Load	"xtt"
EndSection

Section "InputDevice"
	Identifier	"Generic Keyboard"
	Driver		"keyboard"
	Option		"CoreKeyboard"
	Option		"XkbRules"	"xfree86"
	Option		"XkbModel"	"pc105"
	Option		"XkbLayout"	"es"
EndSection

Section "ServerFlags"
	Option "AllowMouseOpenFail"  "true"
EndSection

Section "InputDevice"
	Identifier	"Generic Mouse Serial"
	Driver		"mouse"
	Option		"CorePointer"
	Option		"Device"		"/dev/ttyS0"
	Option		"Protocol"		"Microsoft"
	Option		"Emulate3Buttons"	"true"
	Option		"ZAxisMapping"		"4 5"
EndSection

Section "InputDevice"
	Identifier  "Generic Mouse PS/2"
	Driver      "mouse"
	Option      "Protocol" "ImPS/2"
	Option      "Device" "/dev/psaux"
	Option      "Emulate3Buttons" "true"
	Option      "Emulate3Timeout" "70"
	Option      "ZAxisMapping"  "4 5"
	Option	    "SendCoreEvents"  "true"
EndSection

Section "InputDevice"
	Identifier	"Generic Mouse USB"
	Driver		"mouse"
	Option		"SendCoreEvents"	"true"
	Option		"Device"		"/dev/input/mice"
	Option		"Protocol"		"ImPS/2"
	Option		"Emulate3Buttons"	"true"
	Option		"ZAxisMapping"		"4 5"
EndSection

Section "Device"
	Identifier	"Generic Video Card"
	Driver		"@@DRIVER@@"
	BusID       "@@BUSID@@"
EndSection

Section "Monitor"
	Identifier	"Generic Monitor"
	HorizSync	@@HSYNC@@
	VertRefresh	@@VSYNC@@
EndSection

Section "Screen"
	Identifier	"Default Screen"
	Device		"Generic Video Card"
	Monitor		"Generic Monitor"
	DefaultDepth	16
	SubSection "Display"
		Depth		1
		Modes		"1024x768" "800x600" "640x480"
	EndSubSection
	SubSection "Display"
		Depth		4
		Modes		"1024x768" "800x600" "640x480"
	EndSubSection
	SubSection "Display"
		Depth		8
		Modes		"1024x768" "800x600" "640x480"
	EndSubSection
	SubSection "Display"
		Depth		15
		Modes		"1024x768" "800x600" "640x480"
	EndSubSection
	SubSection "Display"
		Depth		16
		Modes		"1024x768" "800x600" "640x480"
	EndSubSection
	SubSection "Display"
		Depth		24
		Modes		"1024x768" "800x600" "640x480"
	EndSubSection
EndSection

Section "ServerLayout"
	Identifier	"Default Layout"
	Screen		"Default Screen"
	InputDevice	"Generic Keyboard"
	InputDevice	"Generic Mouse Serial"
	InputDevice	"Generic Mouse PS/2"
	InputDevice	"Generic Mouse USB"
EndSection

Section "DRI"
	Mode	0666
EndSection
    '''
    from utils.debug import echo_debug
    from utils.shell import joinpath, mkdir
    # Se crea un objeto Xconf
    X = Xconf()
    
    # Se sustituyen los valores
    newx = template.replace('@@DRIVER@@',X.get_card())
    newx = newx.replace('@@BUSID@@',X.get_busid())
    newx = newx.replace('@@HSYNC@@',X.get_hsync())
    newx = newx.replace('@@VSYNC@@',X.get_vsync())
    
    # Se crea el archivo con los nuevos valores
    try:
	dirname = joinpath(root, 'etc/X11/')
	mkdir(dirname)
	filename =  dirname + 'XF86Config-4'
        xf86config = open(filename, 'w')
    except IOError:
        echo_debug('''No se ha podido crear el archivo XF86Config-4 en
                %s/etc/X11/, compruebe que existen los directorios.''' % root \
                , 'ERROR')
        import sys
        sys.exit(1)

    xf86config.write(newx)
    xf86config.close()


if __name__ == '__main__':

    x = Xconf()
    print 'Tarjeta gráfica:\t' + x.get_card()
    print 'Bus:\t%s\tBusID:\t%s' % (x.get_bus(), x.get_busid())
    print 'Frecuencia Horizontal:\t' + x.get_hsync()
    print 'Frecuencia Vertical:\t' + x.get_vsync()
    print 'Memoria:\t%d Mb' % (x.get_mem()/1024)
    
# vim:ai:et:sts=4:tw=80:sw=4:
