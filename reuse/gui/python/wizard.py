# -*- coding: latin1 -*

class T_root_pass:

    def set(self, glade, dict):
        self.glade = glade
        self.dict = dict

        self.entry = glade.get_widget('rootpass_1'), \
                     glade.get_widget('rootpass_2')

        for e in self.entry:
            e.connect('changed', self._changed)

    def _changed(self, entry):
        if entry is self.entry[0]:
            key = 'rootpass_1'
        else:
            key = 'rootpass_2'

        self.dict[key] = entry.get_text()

class T_parts:

    def set(self, glade, dict):
        self.glade = glade
        self.dict_values = dict

        import gobject, gtk

        # Model

        self.treeview = glade.get_widget("parts_tree")
        self.listmodel = gtk.ListStore(gobject.TYPE_STRING,
                gobject.TYPE_STRING, gobject.TYPE_INT)

        self.treeview.set_model(self.listmodel)

        # View

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Partición", renderer, text=0)
        column.set_resizable(True)
        self.treeview.append_column(column)

        column = gtk.TreeViewColumn("Tipo", renderer, text=1)
        column.set_resizable(True)
        self.treeview.append_column(column)

        column = gtk.TreeViewColumn("Tamaño (en megaytes)", renderer, text=2)
        column.set_resizable(True)
        self.treeview.append_column(column)

        self.treeview.show()
        self.treeview.connect('cursor-changed', self._row_changed)

        # Data

        import parts
        for dev, fs, size in parts.freedisk():
            #print dev, fs, size
            myiter = self.listmodel.append()
            self.listmodel.set_value(myiter,0,dev)
            self.listmodel.set_value(myiter,1,fs)
            self.listmodel.set_value(myiter,2,size/1024)

    def _row_changed(self, tree):
        sel = tree.get_selection()
        model, myiter = sel.get_selected()
        self.dict_values['partition'] = model.get_value(myiter, 0)

class T_finish:

    def set(self, glade, dict):
        self.glade = glade
        self.dialog = glade.get_widget('dialog-all')

        glade.get_widget('button_finish').connect('clicked', self._ok)

    def _ok(self, button):
        self.dialog.response(-2)

class WizardCancel(Exception):
    pass

class Wizard:

    TABS = {'root_pass': T_root_pass, 'parts': T_parts, 'finish': T_finish}

    def __init__(self, file_glade):

        self.tabs = {}
        self.dict_values = {}

        import pygtk
        pygtk.require('2.0')

        import gtk.glade
        self.glade = gtk.glade.XML(file_glade)

    
    def set_dialog(self):
        import gtk

        self.w_notebook = self.glade.get_widget('notebook-all')
        self.w_notebook.set_show_tabs(False)

        self.w_button_next = self.glade.get_widget('button_next')
        self.w_button_prev = self.glade.get_widget('button_prev')

        self.w_button_next.connect('clicked', self._next_clicked)
        self.w_button_prev.connect('clicked', self._prev_clicked)

        self.glade.get_widget('button_cancel').connect('clicked', self._cancel)

        self.w_main_dialog = self.glade.get_widget('dialog-all')
        self.w_main_dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.w_main_dialog.resize(600, 300)

        n = 0
        w = self.w_notebook
        while True:
            child = w.get_nth_page(n)
            if not child:
                break
            if w.get_tab_label_text(child) not in self.tabs.keys():
                w.remove_page(n)
            else:
                n += 1

        for t in self.tabs.keys():
            if t in self.TABS.keys():
                self.tabs[t] = self.TABS[t] ()
                self.tabs[t].set(self.glade, self.dict_values)
            else:
                self.tabs[t] = None


    def _cancel(self, button):
        self.w_main_dialog.response(-6)

    def _next_clicked(self, button):
        self.w_notebook.next_page()
        if self.w_notebook.get_current_page() == len(self.tabs)-1:
            self.w_button_next.hide()

        if self.w_notebook.get_current_page() == 1:
            self.w_button_prev.show()

    def _prev_clicked(self, button):
        self.w_notebook.prev_page()
        if self.w_notebook.get_current_page() == 0:
            self.w_button_prev.hide()

        if self.w_notebook.get_current_page() == len(self.tabs)-2:
            self.w_button_next.show()

    def show_and_run(self):
        self.set_dialog()
        self.w_main_dialog.show_all()
        self.w_notebook.set_current_page(0)
        self.w_button_prev.hide()

        try:
            while True:
                r = self.w_main_dialog.run()
                if r == -6:
                    raise WizardCancel
                elif r == -2:
                    break

        finally:

            self.w_main_dialog.destroy()

            # dirty dirty hack
            import gtk
            gtk.main_iteration_do()
            gtk.main_iteration_do()
            gtk.main_iteration_do()

        return self.dict_values

    def add_tab(self, tab_name):
        self.tabs[tab_name] = None


