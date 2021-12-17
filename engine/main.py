# from python_utils.imports import *

from python_utils.setup_objects import *
from python_utils.setup_nodes import *
from python_utils.server import Server
from python_utils.nodes import *
import threading

class Process():
    def __init__(self, filter_name):
        self.inputs = {'start_movment_name':'catch', 'filter_name':filter_name, 'trigger_pin':11, 'actuator_name':'garra', 'speed':{'F':50}, 'mount_movment_name':'drop', 'None':None}

        # Todo: Create a better way to define 'n' threading.Event()
        self.resume_event = threading.Event()
        self.start_event = threading.Event()
        self.pause_event = threading.Event()
        self.stop_event = threading.Event()

    def _start(self):
        if not self.start_event.is_set():                                               # Se o processo não estiver em execução
            self.start_event.set()                                                      # Marca o processo como em execução
            self._resume()                                                              # limpa/Resume o processo
            print ("Starting at: " + (datetime.now()).strftime('%m/%d/%Y, %H:%M:%S'))   # Imprime a data e hora de início do processo
            while not self.stop_event.is_set():                                         # Enquanto o processo não for parado
                NodeReader(                                                             # Lê os nós
                    rules, nodes, self.inputs,
                    stop_event=self.stop_event,
                    pause_event=self.pause_event
                )
            print ("Stopped at:" + (datetime.now()).strftime('%m/%d/%Y, %H:%M:%S'))     # Imprime a data e hora de parada do processo  

    def _stop(self):
        if not self.stop_event.is_set(): # Se o processo não estiver parado
            self.stop_event.set()        # Marca o processo como parado
            machine_objects['controller'].stop() # Para a máquina, e inibe novos movimentos
            self.start_event.clear()     # Limpa o evento de início. (Uma nova requisição de início pode ser feita)

    def _pause(self):                    
        if not self.pause_event.is_set():         # Se o processo não estiver pausado
            self.pause_event.set()                # Pausa o processo
            machine_objects['controller'].pause() # Pausa a máquina, e inibe novos movimentos.
            

    def _resume(self):
        if not self.resume_event.is_set():          # Se uma requisição de resume não estiver em execução
            self.resume_event.set()                 # Marca a requisição de resume como em execução
            machine_objects['controller'].resume()  # Resume a máquina, e permite novos movimentos.
            self.stop_event.clear() # Limpa o evento de parada. (Uma nova requisição de parada pode ser feita)
            self.pause_event.clear() # Limpa o evento de pausa. (Uma nova requisição de pausa pode ser feita)
            self.resume_event.clear() # Limpa o evento de resume. (Uma nova requisição de resume pode ser feita)
    
# ===========================================================================
# ================================ Main Code ================================
# ===========================================================================


if __name__ == '__main__':
    _process = Process(process_json.value["filter"])

    def resume(*args, **kwargs): _process._resume()
    def start(*args, **kwargs): _process._start()
    def pause(*args, **kwargs): _process._pause()
    def stop(*args, **kwargs): _process._stop()

    server_app = Server(
        report_time=server_json.value['updateTime'],
        buildfolder=server_json.value['buildDir'],
        app_port=server_json.value['port'],
        app_ip=server_json.value['ip'],
        functions={
            "resume_process": resume,
            "pause_process": pause,
            "start_process": start,
            "stop_process": stop,
        },
        cameras={
            "camera0": cameras_objects["camera0"]
        }
    )
    server_app.start()
