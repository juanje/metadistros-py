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

