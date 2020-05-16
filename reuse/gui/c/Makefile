CC=gcc
CFLAGS=
INCLUDES=-I/usr/include/python2.3/ `pkg-config --cflags libglade-2.0`
LIBS=`pkg-config --libs libglade-2.0`

all: cWizardmodule.so

cWizardmodule.so: cWizard.o wizard.o
	$(CC) -o cWizardmodule.so $(LIBS) -shared -Wall wizard.o cWizard.o

%.o: %.c wizard.h
	$(CC) $(INCLUDES) $(CFLAGS) -c -fPIC -o $@ $<

cWizard.c: cWizard.pyx
	pyrexc cWizard.pyx

clean:
	rm cWizardmodule.so cWizard.c cWizard.o wizard.o
