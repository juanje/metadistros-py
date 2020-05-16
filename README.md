# Metadistros: Calzador 2.0

This repo has the implementation of some new ideas. Also it was an experiment
to see how to convert the old shell scripts into Python modules.


## Original description

Este directorio contiene la version inestable del Calzador de Metadistros.
En el se encuentran los directorios:
- **metaconf**: librerias en Python para su utilizacion en el Calzador. Se 
encargan de la deteccion de hardware y demas tareas de arranque e instalacion.
- **utils**: contiene archivos con informacion necesaria para construir un "initrd"
en el que ejecutar el Calzador. Tambien algunos scripts utiles.
- **reuse**: contiene versiones anteriores o pruebas que serviran para reutilizar 
codigo en ciertas partes del nuevo Calzador.
- **kernel**: los parches aplciados y las configuraciones de compilación.

---

## From the old website

### Metadistros' loader (aka Calzador)

This is how I have called it, instead of "boot, hardware detector, installer, live", what it's a bit longer ;) It's superficially explained at metadistros' web and in a mail in the list[1] (Spanish only). I'm going to show first specifications that I have get from ideas exposed in the list.
Specifications

* It should be modular
* Easily adaptable and configurable
* I18n support
* Easy from the user point of view
* It must be able to boot the live system
* It must be able of installing the system
* It must detect all the hardware and configure it
* It must not damage the hardware, if it's ecessary, user should be asked (This refers to partitions and old monitors)
* Hardware detection must be transpartent to the end user
* It should use a graphic interface, but also allow text or expert mode
* It should allow choosing between booting as non-priviledged user or as root (This when adaptig it, not as end user)
* It should be able to detect other installed OS and add them to lilo/grub boot menu
* Live system must be equal than installed system
* It must be possible to use the system compressed or uncompressed
* Live system or installation must be launched from CD-Rom, a partition, or a server (in a network)
* Loader must be launched from CD-Rom or a floppy
* It must allow making unattended installations
* It must be able to load old cofigurations from a floppy or a file in a local or remote partition
* Live System should have a persistent /home in a file in a local or remote device
* It must be able to load different systems from one or more places, and ask which one must be loaded

### Secuence

1.  Welcome screen. At the same time, kernel boots and modules for CD or network card are loaded. Also system is unzipped from CD, so hardware autodetection can begin.
    *   Some kind of help will be available, as now. There possible parameters for booting process will be listed. For doing this easy, I bet for three options:
        *   Install
        *   Easy (Do not ask anything)
        *   Intermediate (Asks for language, user, ...) -> Default
        *   Expert (So you can configure things by hand)
2.  User is asked about language (this will depend on the mestadistribution). He will be also asked for the option (boot/install, net/cd). Meanwhile hardware is still being detected and configuration files created (CF86Config, fstab, modules, ...)
    *   If "install" option was chosen, hard disk will be partitioned. This will be asked and done. While this is being made, images or a little game could be showed ;)
3.  Username and hostname are asked. Meanwhile, system is being copied to HD in case of installation or being created and modified in RAM, in case of executig directly from CD. Also, user will be created and hostname set.
    *   If there is some kind of problem with graphic card or any other device, it will be manually configured at this point.
4.  Loader warns about everything being ready to boot. At the same time, configuration files are being copied to RAM or HD, depending on the option taken. And one or the other system is booted.
5.  If the chose was "live", when finishing a farewell screen should appear while system is being closed. CD is ejected and system powered off.



And now, I'm showing you a Case of Use picture (I'm not an expert in UML; sorry about it being so fool) that explains user and loader interaction, and different tasks that will be made.

Have into account some details about the diagram. Tasks in which user intervention is required are in continue line ellipses. Those in discontinue line ellipses are tasks that loader launches, and for which user intervention is not required. Also, those tasks will be executed in background, as don't provide anything useful for end users and can distract them.

In addition, tasks with a dotted arrow and name as {Optional} are such, optional. This means that those are tasks that can not be run, but that will be in the loader to be executed if it's necessary.

All this process will be held out of the system that it's going to be installed or booted "live", so it is independient of the system: debian (stable, testing, unstable), Red Hat, Mandrake, Gentoo. Also the system can be compressed or not. Once installed, it won't be any diference between this installed system and one installed using packages and default instalation method (unless the easy installation, of course ;)

[1] Where this mail says "Arranque": https://listas.hispalinux.es/pipermail/meta-distros/2003-January/000627.html
