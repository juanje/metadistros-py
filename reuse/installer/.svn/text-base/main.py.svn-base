# -*- coding: latin1 -*-

def main():
    import os, re

    #### Particionar

    # no mola usar system.. pero para algo rápido pos....
    os.system('cfdisk')

    #### 2- Elegir particion

    # buscar las particiones que se han creado.
    # nota: no estoy seguro si después del cfdisk la informaciónde
    # /proc/partitions está actualizada. Se supone que sí.... =)
    f = open('/proc/partitions')
    regex = re.compile('((hd|sc)\w\d+)') # tanto los hd* como sc*

    parts = []
    for line in f.readlines():
        m = regex.search(line)
        if m:
            parts.append(m.group(1))

    print parts
    partition = raw_input('partición: ')
		
		#### Detecta particion swap
		swap_part = ''
		w, r = os.popen2('fdisk -l')
		for line in r.readlines():
			if line.find('dev') == -1: continue
			array = line.split()
			if array[1] != '*' and array[4] == '82':
				swap_part = array[0]

    #### Formatear la particion con ext3
    os.system('mkfs.ext3 -v ' + particion)

    #### Montar la particion y copiar de /META/* a la particion
    os.system('mount %s /mnt' % partition)

    pid = os.fork()
    if pid == 0:
        os.dup2(os.open('/dev/null', os.RDWR), 0)
        os.dup2(os.open('/dev/null', os.RDWR), 1)
        os.dup2(os.open('/dev/null', os.RDWR), 2)

        os.execv('/usr/bin/cp',
                 ('cp', '-a') + \
                  tuple(os.listdir('/META/')) + ('/mnt',))
        

        import sys
        sys.exit(1)

    #### Preguntar por el nombre de la makina
    hostname = raw_input('Nombre de la máquina: ')

    #### Por el usuario
    username = raw_input('Usuario')
    userpass = raw_input('Contraseña')

    #### Por el root
    rootpass = raw_input('Contraseña de root: ')

    #### Configurar la red
    os.system('ifconfig...')

    #### Detectar los dispositivos que tiene que crear enlaces en /dev/

    #### Comprobar que se ha terminado de copiar al disco
    os.waitpid(pid, 0)

    #### Crear el /etc/fstab

    f = open('/mnt/etc/fstab')
    f.write('%s\t/\text3\tdefaults\t0\t1\n' % partition)
    f.write('%s\tnone\t\tswap\t\tsw\t\t\t\t0\t0' % swap_part)
    f.write('proc\t/proc\t\tproc\t\tdefaults\t\t\t0\t0')

    #### Copiar el XF86Config* al disco
    os.sytem('cp /etc/X11/XF86Config* /mnt/etc/X11/')

    #### Configurar el nombre de la makina
    open('/mnt/etc/hostname', 'w').write(hostname)
    open('/mnt/etc/hosts', 'w').write('127.0.0.1\tlocalhost ' + hostname)

    #### Añadir el usuario y cambiar la clave del root
    os.system('/usr/sbin/useradd -m -d /home/%s %s' % ((self.username,)*2))
    os.system('/usr/sbin/adduser %s audio' % self.username)

    f = open('/tmp/pass', 'w')
    f.write('%s:%s\n' % (username, userpass))
    f.write('root:%s\n' % rootpass)
    f.close()
    os.unlink('/tmp/pass')

    os.system('/usr/sbin/chpasswd < /tmp/pass')

    #### Configurar los archivos de red
    f = open('/mnt/etc/network/interfaces')
    f.write('auto lo\n'
            'iface lo inet loopback\n'
            '\n'
            'auto eth0 o ppp0\n'
            'iface eth0 inet static o dhcp o ...\n'
            '...')
    f.close()

    #### Configurar el archivo /etc/modules
    f = open('/mnt/etc/modules')
    f.write('# /etc/modules: kernel modules to load at boot time.\n'
            '#\n'
            '# This file should contain the names of kernel modules that are\n'
            '# to be loaded at boot time, one per line.  Comments begin with\n'
            '# a #, and everything on the line after them are ignored.\n\n')

    mods = open('/proc/modules')
    for line in mods.readlines():

        if line.find('['):
            continue

        mod = line.split()[0]
        if mod == 'apm':
            f.write('apm power_off=1\n')
        elif mod != 'cloop':
            f.write(mod + '\n')


    mods.close()
    f.close()

    #### Configurar el grub

    f = open('/mnt/boot/grub/menu.lst')
    f.write('default 0\n'
            'timeout 0\n'
            '\n'
            'title windows?\n'
            'rootnoverify (hdX,Y)\n'
            'makeactive\n'
            'chainloader +1\n'
            '\n'
            'title linux\n'
            'root (hdP,Q)\n'
            'kernel /vmlinuz root=%(part)s'  %   {

               'part': partition
            })
    f.close()

    os.sytem('grub ...')

if __name__ == '__main__':
    main()
