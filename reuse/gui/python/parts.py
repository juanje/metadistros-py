# -*- coding: latin1 -*-

def memtotal():
    '''memtotal() -> int

    Devuelve al memoria física del sistema, en kilobytes.'''

    f = open('/proc/meminfo')
    while True:
        line = f.readline()
        if not line:
            break

        if line.startswith('MemTotal:'):
            return int(line.split()[1])


def freedisk():
    '''freedisk() -> list

    Devuelve una lista, donde cada elemento es una tupla de tres elementos.
    El primero elemento de la tupla es una cadena indicando la partición
    ('hda1', por ejemplo), el segundo el tipo ('xfs', por ejemplo) y el último
    el espacio total en kbytes.

    La función sólo trabaja con particiones que el kernel pueda montar'''

    # Primero, sacar los puntos ya montados del mtab
    # XXX ¿Hay otro sitio "mejor" que el mtab? mount(1) lo saca de ahí..
    mounts = []
    f = open("/proc/mounts")
    while True:
        l = f.readline()
        if not l:
            break

        if l.startswith('/dev/'):
            # meter una lista de 3 elementos, que son 
            # la partición (dev/...) y el punto de montaje
            mounts.append(l.split()[:2])


    # Sacar las particiones de /proc/partitions
    # XXX ¿Ahí están todas?

    import re
    parts = re.compile(r'(?:\s+\d+){3}\s+(\S+\d+)')

    result = []

    f = open('/proc/partitions')
    while True:
        line = f.readline()
        if not line:
            break

        m = parts.match(line)
        if m:
            # Se ha encontrado una posible partición. Su espacio
            # libre y su tipo se hallarán con statvfs

            point = ''
            type = '<unknown>'
            unmount = False
            dev = '/dev/' + m.group(1)

            import os

            # Primero comprobar si ya está montada

            for i in mounts:
                if i[0] == dev:
                    # ya está montada
                    point = i[1]

            if not point:
                # No estaba montada. Intentar montarla
                # TODO Buscar un sitio mejor que /mnt
                point = '/mnt'
                ret = os.system('mount -o ro %s %s &> /dev/null' % (dev, point))
                if ret != 0:
                    # no se ha podido montar
                    continue

                unmount = True # desmontar después

            # sacar el tipo de partición, directamente del /proc/mounts
            fm = open('/proc/mounts')
            while True:
                lm = fm.readline()
                pm = lm.split()
                if lm.startswith('/dev/') and pm[1] == point:
                    type = pm[2]
                    break

            # sacar el espacio libre
            from statvfs import F_BSIZE, F_BLOCKS
            fs = os.statvfs(point)
            freespace = fs[F_BSIZE] * fs[F_BLOCKS] / 1024

            if unmount:
                os.system('umount %s &> /dev/null ' % point)

            result.append((dev, type, freespace))


    return result

if __name__ == '__main__':
    r = freedisk()
    for t in r:
        print '%15s %7s %9d' % t
