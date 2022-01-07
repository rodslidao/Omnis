from python_utils.imports import *
from python_utils.setup_objects import *
# from python_utils.setup_nodes import *
from python_utils.server import Server
# from python_utils.nodes import *
from python_utils.NodeInterpreter.Node import *
from python_utils.NodeInterpreter.nodeClasses import *

import threading

#! Isso deve mudar.
node_config = Reader(database.find_one("node_sheets", {}), {"MoveNode":MoveNode})
server_name = "Parallax"
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
                node_config.reset()
                for node_id in node_config.node_sequence:
                    node = node_config.nodes[node_id]
                    _input = node_config.in2out[node._input_id] if node_id != node_config.node_sequence[0] else "start"
                    node.run(_input, node_config.output_dict)
                    while self.pause_event.is_set():                                    # Enquanto o processo estiver pausado
                        pass

            print ("Stopped at:" + (datetime.now()).strftime('%m/%d/%Y, %H:%M:%S'))     # Imprime a data e hora de parada do processo  

    def _stop(self):
        if not self.stop_event.is_set():                                                # Se o processo não estiver parado
            self.stop_event.set()                                                       # Marca o processo como parado
            [machine.stop() for machine in machine_objects.values()]                    # Para a máquina, e inibe novos movimentos
            self.start_event.clear()                                                    # Limpa o evento de início. (Uma nova requisição de início pode ser feita)

    def _pause(self):                    
        if not self.pause_event.is_set():                                               # Se o processo não estiver pausado
            self.pause_event.set()                                                      # Pausa o processo
            [machine.pause() for machine in machine_objects.values()]                   # Pausa a máquina, e inibe novos movimentos.
            

    def _resume(self):
        if not self.resume_event.is_set():                                              # Se uma requisição de resume não estiver em execução
            self.resume_event.set()                                                     # Marca a requisição de resume como em execução
            [machine.resume() for machine in machine_objects.values()]                  # Resume a máquina, e permite novos movimentos.      
            self.stop_event.clear()                                                     # Limpa o evento de parada. (Uma nova requisição de parada pode ser feita)
            self.pause_event.clear()                                                    # Limpa o evento de pausa. (Uma nova requisição de pausa pode ser feita)
            self.resume_event.clear()                                                   # Limpa o evento de resume. (Uma nova requisição de resume pode ser feita)
    
# ===========================================================================
# ================================ Main Code ================================
# ===========================================================================


if __name__ == '__main__':
    _process = Process(filter_name="small_blue")

    def resume(*args, **kwargs): _process._resume()
    def start(*args, **kwargs): _process._start()
    def pause(*args, **kwargs): _process._pause()
    def stop(*args, **kwargs): _process._stop()

    server_app = Server(
        report_time=server_objects[server_name]['updateTime'],
        buildfolder=server_objects[server_name]['buildDir'],
        app_port=server_objects[server_name]['port'],
        app_ip=server_objects[server_name]['ip'],
        functions={
            "resume_process": resume,
            "pause_process": pause,
            "start_process": start,
            "stop_process": stop,
        },
        cameras=camera_objects,
    )
    server_app.start()