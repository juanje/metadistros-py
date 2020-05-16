/*
 * GUI para el calzador
 */

#include "wizard.h"
#include <gtk/gtk.h>
#include <glade/glade.h>
/*#include <stdlib.h>*/

/*
 * Manejadores de señales
 */

void destroy ()
{
	gtk_main_quit ();
}

void
wzd_on_button_next_clicked (GtkButton* bt, Wizard* wizard)
{
	GtkWidget *notebook;
	
	notebook = glade_xml_get_widget (wizard->glade, "notebook-all");

	if (gtk_notebook_get_current_page (GTK_NOTEBOOK (notebook)) ==
	    gtk_notebook_get_n_pages (GTK_NOTEBOOK (notebook)) - 1) {
		   gtk_dialog_response (GTK_DIALOG (wizard->dialog),
						    GTK_RESPONSE_APPLY);
	}
	
	gtk_notebook_next_page (GTK_NOTEBOOK (notebook));
}

void
wzd_on_button_prev_clicked (GtkButton* bt, Wizard* wizard)
{
	GtkWidget *notebook;
	
	notebook = glade_xml_get_widget (wizard->glade, "notebook-all");
	gtk_notebook_prev_page (GTK_NOTEBOOK (notebook));
}

void
wzd_on_notebook_switch_page (GtkNotebook *notebook, GtkNotebookPage *page,
					    gint pos, gpointer gdata)
{
	   Wizard *wzd;
	   GtkWidget *button_next;
	   GtkWidget *button_prev;

	   wzd = (Wizard *) gdata;

	   button_next = glade_xml_get_widget (wzd->glade, "button_next");
	   button_prev = glade_xml_get_widget (wzd->glade, "button_prev");

	   gtk_button_set_use_stock (GTK_BUTTON (button_next), TRUE);
	   
	   if (pos == 0) {
			 gtk_widget_set_sensitive (button_prev, FALSE);
			 gtk_button_set_label (GTK_BUTTON (button_next),
							   GTK_STOCK_GO_FORWARD);
	   }
	   else if (pos == gtk_notebook_get_n_pages (notebook) - 1) {
			 gtk_button_set_label (GTK_BUTTON (button_next),
							   GTK_STOCK_APPLY);
	   }
	   else {
			 gtk_widget_set_sensitive (button_next, TRUE);
			 gtk_widget_set_sensitive (button_prev, TRUE);
			 gtk_button_set_label (GTK_BUTTON (button_next),
							   GTK_STOCK_GO_FORWARD);
	   }
}		 		 

Wizard* wizard_create (gchar* glade_file)
{
	   Wizard *wzd;
	   GtkWidget *widget;
	   
	   gtk_init (NULL, 0);
	   glade_init ();

	   if (glade_file == NULL)
			 glade_file = "gui.glade";

	   /*wzd = (Wizard*)malloc(sizeof(Wizard));*/
	   wzd = g_new0 (Wizard, 1);

	   wzd->glade = glade_xml_new (glade_file, NULL, NULL);
	   wzd->dialog = glade_xml_get_widget(wzd->glade, "dialog-all");
	   g_signal_connect (G_OBJECT (wzd->dialog), "destroy",
					 G_CALLBACK (destroy), NULL);

	   /* Ocultar las pestañas */
	   widget = glade_xml_get_widget (wzd->glade, "notebook-all");
	   gtk_notebook_set_show_tabs (GTK_NOTEBOOK (widget), FALSE);
	   g_signal_connect (G_OBJECT (widget), "switch_page",
					 G_CALLBACK (wzd_on_notebook_switch_page),
					 (gpointer) wzd);

	   /* Acciones a los botones */
	   widget = glade_xml_get_widget (wzd->glade, "button_next");
	   g_signal_connect (G_OBJECT (widget), "clicked",
					 G_CALLBACK (wzd_on_button_next_clicked),
					 wzd);
	   
	   widget = glade_xml_get_widget (wzd->glade, "button_prev");
	   gtk_widget_set_sensitive (widget, FALSE);
	   g_signal_connect (G_OBJECT (widget), "clicked",
					 G_CALLBACK (wzd_on_button_prev_clicked),
					 wzd);

	   /* poner a un tamaño "ideal" */
	   gtk_window_resize (GTK_WINDOW (wzd->dialog), 600, 400);
	   gtk_window_set_position (GTK_WINDOW (wzd->dialog), GTK_WIN_POS_CENTER_ALWAYS);

	   return wzd;
}

void wizard_destroy (Wizard* wizard)
{
	   gtk_widget_destroy(GTK_WIDGET(wizard->dialog));
	   g_free (wizard);
}

gint
wizard_show_and_run (Wizard* wizard)
{
	   gint response;
	   
	   gtk_widget_show_all (GTK_WIDGET (wizard->dialog));
	   
	   do
			 response = gtk_dialog_run (GTK_DIALOG (wizard->dialog));
	   while ((response != GTK_RESPONSE_CANCEL) &&
			(response != GTK_RESPONSE_APPLY));
	   
	   gtk_widget_hide (GTK_WIDGET (wizard->dialog));
	   
	   return response;
}

