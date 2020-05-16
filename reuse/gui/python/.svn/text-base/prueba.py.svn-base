import wizard
w = wizard.Wizard('../glade/gui.glade')
w.add_tab('welcome')
w.add_tab('root_pass')
w.add_tab('parts')
w.add_tab('finish')

import pprint
try:
    pprint.pprint(w.show_and_run())
except wizard.WizardCancel:
    print 'Asistente cancelado'

