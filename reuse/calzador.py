# -*- coding: latin1 -*-

def parse(name, dct):

    for line in open(name).readlines():

        line = line.strip()
        if line[0] == '#':
            continue

        for word in line.split():
            if '=' in word:
                name, val = word.split('=', 1)
                dct[name] = val


def define_questions(vars):

    qsts = {}
    for v in vars.keys():
        if not v.startswith('Q'): continue

        qsts[v] = vars[v] == 'Y'
        del vars[v]

    return qsts

class Thread:

    def start(self):
        import threading
        self.thread = threading.Thread(target = self.main)

        self.thread.start()

    def isAlive(self):
        return self.thread.isAlive()

    def main(self):
        pass

class HwDetect(Thread):

    def main(self):
        # TODO Buscar el hardware
        pass

class Install(Thread):

    def start(self, partition):
        self.partition = partition
        Thread.start(self)

    def main(self):
        # TODO Instalar en la partición indicada por
        # self.partition
        pass


if __name__ == '__main__':

    # variables para almacenar los posibles hilos para
    # instalar y detectar hw.
    hwdetect_thread = None
    install_thread = None

    vars = {}

    # Leer variables
    parse('q.conf', vars)
    parse('var.conf', vars)
    parse('/proc/cmdline', vars)

    # separar preguntas
    questions = define_questions(vars)

    # 
    # XXX multihilo???
    hwdetect_thread = HwDetect()
    hwdetect_thread.start()

    if questions.get('QLANGUAGE', False):
        # TODO preguntar por el lenguaje.. una lista muy chula
        # con los lenguajes soportados por la distro
        pass

    if questions.get('QSPLASH', True):
        # TODO Mostrar splash..
        # ¿definición de splash?? ¿ventana de introducción? ¿barra
        # de progreso?
        pass

    if questions.get('QINSTALL', False):
        # TODO instalar

        # 1º particionar
        particionar() # :-P

        # 2º lista mona de particiones para seleccionar una
        #    de ellas para instalar.
        # *  ui es un objeto para la interfaz
        partition = ui.select_partitions()

        # 3º formatear
        # A:> format c:
        #
        # La función install_main recibe un único argumento, que
        # será la partición a instalar
        install_thread = Install()
        install_thread.start(partition)


    if questions.get('QHOST', False):
        ui.hostname()
    else:
        # valor por defecto del var.conf
        pass

    if questions.get('QUSER', False):
        ui.pedir_usuario()
    else:
        # valores de USERNAME y UPASSWORD del var.conf
        pass

    if questions.get('QPASS', False):
        ui.pedir_pass_root()
    else:
        # valor de RPASSWORD
        pass


    # Configurar la red
    # TODO levantar la red loopback
    if questions.get('QNET', False):
        
        # TODO ¿configurar la red?
        if ui.preguntar_por_red():
            # ¿manual o automática?
            if ui.red_manual():
                ui.red_pedir_ips()
            else:
                leer_DHCP()


    if install_thread is not None:
        # Si install_thread no es None, significa que se está
        # instalando.

        # Mostrar una barra de progreso durante la instalación.
        # La instalación se dará por finalizada cuando el hilo
        # haya terminado
        import time
        while install_thread.isAlive():
            ui.show_installation_status()
            time.sleep(1)

    if hwdetect_thread is not None:
        # esperar a que la detección de hardware termine (si 
        # no lo ha hecho aún)
        import time
        while hwdetect_thread.isAlive():
            time.sleep(1)

        hwdetect_thread = None

    if install_thread is not None:
        # terminar la instalación, con la información que se
        # ha recopilado (preguntas, valores del var.conf y 
        # el HW detectado.
        pass

    else:
        # terminar de configurar el sistema live, con la 
        # información que se ha recopilado (preguntas,
        # valores del var.conf y el HW detectado.
        pass



    # Acabado
