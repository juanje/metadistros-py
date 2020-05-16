#ifndef _GUI_H_INCLUDED
#define _GUI_H_INCLUDED

#include <glade/glade.h>

struct WzTab;
struct Wizard;

typedef int (*tab_read_value)(struct Wizard*, struct WzTab*, const char*, char*, int);
typedef int (*tab_write_value)(struct Wizard*, struct WzTab*, const char*, const char*);

struct WzTab
{
	char *name;        /* Nombre del tab */
	char *tab_name;    /* Pestaña que se mostará en la ventana de glade */

	/* Funciones para leer y escribir atributos en ese tab */
	tab_write_value write_fn;
	tab_read_value read_fn;
};

struct Wizard
{
	GtkWidget *dialog;
	GladeXML* glade;

	/* TODO
	 * Algo para actuar como un diccionario. Por ejemplo,
	 * un PyObject
	 */
};

typedef struct Wizard Wizard;
typedef struct WzTab WzTab;

Wizard* wizard_create(char*);
void wizard_destroy(Wizard*);
int wizard_show_and_run(Wizard* wizard);

#endif // _GUI_H_INCLUDED
