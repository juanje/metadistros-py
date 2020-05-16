import pygtk
pygtk.require('2.0')

import gtk, gtk.glade

xml = gtk.glade.XML('gui.glade')

n = xml.get_widget('notebook-all')
n.set_show_tabs(False)


import sys
xml.get_widget('button_prev').connect('clicked', lambda *x: n.prev_page())
xml.get_widget('button_next').connect('clicked', lambda *x: n.next_page())
xml.get_widget('button_cancel').connect('clicked', lambda *x: gtk.main_quit())

w = xml.get_widget('dialog-all')
w.connect('destroy', lambda x: gtk.main_quit())
w.show()
w.get_toplevel().set_position(gtk.WIN_POS_CENTER_ALWAYS)
w.get_toplevel().resize(750, 550)
gtk.main()
