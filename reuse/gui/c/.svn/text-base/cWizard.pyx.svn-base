
cdef extern from "wizard.h":

    struct c_wizard "Wizard"
    
    c_wizard* wizard_create(char*)
    void wizard_destroy(c_wizard*)
    int wizard_show_and_run(c_wizard*)

class WizardError(Exception):
    pass

cdef class Wizard:
    cdef c_wizard* _wiz

    def __init__(self, char* file_glade = 'gui.glade'):
        self._wiz = wizard_create(file_glade)
        if self._wiz == NULL:
            raise WizardError, "No se pudo crear el wizard"

    def show_and_run(self):
        return wizard_show_and_run(self._wiz)

    def __del__(self):
        wizard_destroy(self._wiz)
        self._wiz = NULL
