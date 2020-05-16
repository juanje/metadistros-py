# -*- coding: latin1 -*-

import select

def step(cmd, label, pbar):

    # hay algo que leer..¿será un valor?
    # quedar sólo con la última línea
    print 'antes del popen3'
    stdin, stdout, stderr = os.popen3(cmd)
    print 'despues del popen3'
    while 1:
        line = stdout.readline()
    
        try:
            val = float(line)
        except (ValueError, TypeError):
            #pass
	    pbar.set_text(line)
        else:
            # actualizar la barra
	    if val > 100:
		gtk.mainquit()
	    label.set_text(str(int(val)))
	    pbar.set_fraction(val / 100)
    

if __name__ == '__main__':

    import pygtk
    pygtk.require('2.0')
    import gtk, gobject, os

    main = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main.connect('destroy', lambda *x: gtk.mainquit())

    vbox = gtk.VBox(gtk.FALSE, 8)
    main.add(vbox)
    label = gtk.Label("Porcentaje")
    vbox.add(label)
    pbar = gtk.ProgressBar()
    vbox.add(pbar)

    main.show_all()
    cmd = './test.sh'
    #gobject.idle_add(step, stdout, label, pbar)
    step(cmd, label, pbar)

    gtk.main()
