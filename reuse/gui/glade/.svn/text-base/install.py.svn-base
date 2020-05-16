# -*- coding: latin -*-

class Wzd:
    def __init__(self):
        import pygtk
        pygtk.require('2.0')
        import gtk, gtk.glade

	self.pids = []
        xml = gtk.glade.XML('gui.glade')

        self.notebook = xml.get_widget('notebook-all')
        self.notebook.set_show_tabs(False)

        # botoncitos
        for w in ('button_prev', 'button_next', 'button_cancel', 'button_install'):
            setattr(self, w, xml.get_widget(w))

        self.button_prev.connect('clicked', lambda *x: self.change_page(-1))
        self.button_next.connect('clicked', lambda *x: self.change_page(1))
        self.button_cancel.connect('clicked', lambda *x: self.main_quit())
        self.button_install.connect('clicked', lambda *x: self.make_install())

	# pantalla de Instalacion
	self.install_top = xml.get_widget('install_top')
	self.install_label = xml.get_widget('install_label')
	self.progressbar = xml.get_widget('progressbar')

        # mostrar el cuadrecito
        w = xml.get_widget('dialog-all')
        w.connect('destroy', lambda x: gtk.main_quit())
        w.show()
        w.get_toplevel().set_position(gtk.WIN_POS_CENTER_ALWAYS)
#        w.get_toplevel().resize(750, 550)
        
        self.check_bt_visibility()


    def main_quit(self):
	if len(self.pids) != 0:
	    import os
	    for pid in self.pids:
		os.kill(pid,9)
	gtk.main_quit()

    def change_page(self, direction):
        '''change_page(direction)

        Cambia la pestaña. Si direction < 0, cambia a la de la izquierda.
        Si direction > 0, a la de la derecha
        '''

        if direction > 0:
            self.notebook.next_page()
        else:
            self.notebook.prev_page()

        self.check_bt_visibility()

    def check_bt_visibility(self):
        # método simplista para ocultar el botón no querido
        # si está en la última y/o primera
	self.button_prev.set_sensitive(1)
	self.button_next.set_sensitive(1)
	self.button_next.show()
	self.button_prev.show()
        n = self.notebook.get_current_page()
        if n == 0:
            self.button_prev.hide()
        next = self.notebook.get_nth_page(n+1)
        if next is None:
            self.button_next.hide()

    def step(self, poll):
    
        import select
        r = poll.poll(1)
        if r:
            for fd, ev in r:
                if ev & select.POLLIN:
                    # hay algo que leer..¿será un valor?
                    import os
                    entry = os.read(fd, 60).strip()
    
		    for line in entry.split('\n'):
		        if line.startswith('XXX'):
		            text = line.replace('XXX','')
		            self.install_label.set_text(text)
		        else:
		            try:
                                val = float(line)
                            except (ValueError, TypeError):
		                pass
                            else:
                                # actualizar la barra
		                if val > 100:
		                    self.change_page(1)
		                    return False
                                else:
		                    percent = val / 100
                                    self.progressbar.set_text('%s %%' % int(val))
                                    self.progressbar.set_fraction(percent)
    
        return True # llamar otra vez

    def make_install(self):
	# Empieza la instalación
	# leer en idle
	import os, select, gobject
        poll = select.poll()
        read, write = os.pipe()
	pid = os.fork()
	self.pids.append(pid)
        if pid == 0:
            os.close(read)
            os.dup2(write, 1)   # stdout
            os.execv('/bin/sh', ('sh', 'test.sh'))

        os.close(write)
        poll.register(read, select.POLLIN)

	# ocultar boton y conectar la barra
	self.button_install.hide()
	self.button_prev.set_sensitive(0)
	self.button_next.set_sensitive(0)
	self.install_top.set_text('Comienza la Instalacion')
	self.install_label.set_text('Instalando...')
        gobject.idle_add(self.step, poll)

if __name__ == '__main__':
    a = Wzd()
    import gtk
    gtk.main()
