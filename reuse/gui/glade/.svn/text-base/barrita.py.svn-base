# -*- coding: latin1 -*-
#
#
# Probar con cosas como
# $ (for n in `seq 1 100` ; do echo $(($RANDOM % 100)); LC_ALL=C sleep 0.1; done) | python barrita.py 
# $ (for n in `seq 1 100` ; do echo $n; LC_ALL=C sleep 0.1; done) | python barrita.py 


import select

def step(poll, pbar):

    r = poll.poll(1)
    if r:
        for fd, ev in r:
            if fd == 0: # stdin
                if ev & select.POLLHUP:
                    ### stdin se ha cerrado
                    # cambiar este gtk.mainquit por lo que sea...
                    gtk.mainquit()
                elif ev & select.POLLIN:
                    # hay algo que leer..¿será un valor?
                    # quedar sólo con la última línea
                    import os
                    line = os.read(0, 1000).strip().split('\n')[-1]

                    try:
                        val = float(line)
                    except (ValueError, TypeError):
                        pass
                    else:
                        # actualizar la barra
                        pbar.set_fraction(val / 100)

    return True # llamar otra vez

if __name__ == '__main__':

    import pygtk
    pygtk.require('2.0')
    import gtk, gobject

    main = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main.connect('destroy', lambda *x: gtk.mainquit())

    pbar = gtk.ProgressBar()
    main.add(pbar)

    # leer en idle
    poll = select.poll()
    poll.register(0, select.POLLIN)         # el 0 es del stdin
    gobject.idle_add(step, poll, pbar)

    main.show_all()
    gtk.main()
