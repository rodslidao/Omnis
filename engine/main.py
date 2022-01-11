from python_utils.imports import *
from python_utils.setup_objects import *
# from python_utils.setup_nodes import *
from python_utils.server import Server
# from python_utils.nodes import *
from python_utils.NodeInterpreter.Node import *
from python_utils.NodeInterpreter.nodeClasses import *
from bson.objectid import ObjectId
import threading
from pprint import pprint

temp = {
    "nodes": [
        {
            "type": "MoveNode",
            "id": "node_16414770159090",
            "name": "Movimento",
            "options": [
                [
                    "Hardware",
                    "Octopus V1.1"
                ],
                [
                    "X",
                    None
                ],
                [
                    "Y",
                    True
                ],
                [
                    "Z",
                    True
                ]
            ],
            "state": {},
            "interfaces": [
                [
                    "Entrada",
                    {
                        "id": "ni_16414770159091",
                        "value": 0
                    }
                ],
                [
                    "Velocidade",
                    {
                        "id": "ni_16414770159092",
                        "value": 2500
                    }
                ],
                [
                    "Saida",
                    {
                        "id": "ni_16414770159093",
                        "value": None
                    }
                ],
                [
                    "Y ",
                    {
                        "id": "ni_164147702048110",
                        "value": 100
                    }
                ],
                [
                    "Z ",
                    {
                        "id": "ni_164147702048120",
                        "value": 100
                    }
                ]

            ],
            "position": {
                "x": 50,
                "y": 140
            },
            "width": 245,
            "twoColumn": True,
            "customClasses": ""
        },
        {
            "type": "IdentifyNode",
            "id": "node_16414770159104",
            "name": "Identificação",
            "options": [
                [
                    "Camera",
                    "Camera_0"
                ],
                [
                    "Filtro",
                    "Small_Blue"
                ],
                [
                    "Y",
                    True
                ],
                [
                    "Z",
                    None
                ]
            ],
            "state": {},
            "interfaces": [
                [
                    "Entrada",
                    {
                        "id": "ni_16414770159105",
                        "value": 0
                    }
                ],
                [
                    "Saida",
                    {
                        "id": "ni_16414770159107",
                        "value": None
                    }
                ]
            ],
            "position": {
                "x": 453,
                "y": 143
            },
            "width": 245,
            "twoColumn": True,
            "customClasses": ""
        },
        {
            "type": "MoveNode",
            "id": "node_164147704394712",
            "name": "Movimento",
            "options": [
                [
                    "Hardware",
                    "Octopus V1.1"
                ],
                [
                    "X",
                    None
                ],
                [
                    "Y",
                    True
                ],
                [
                    "Z",
                    True
                ]
            ],
            "state": {},
            "interfaces": [
                [
                    "Entrada",
                    {
                        "id": "ni_164147704394713",
                        "value": 0
                    }
                ],
                [
                    "Velocidade",
                    {
                        "id": "ni_164147704394714",
                        "value": 2500
                    }
                ],
                [
                    "Saida",
                    {
                        "id": "ni_164147704394715",
                        "value": None
                    }
                ],
                [
                    "Y ",
                    {
                        "id": "ni_164147708580719",
                        "value": 0
                    }
                ],
                [
                    "Z ",
                    {
                        "id": "ni_164147702048170",
                        "value": 0
                    }
                ]
            ],
            "position": {
                "x": 827,
                "y": 147
            },
            "width": 245,
            "twoColumn": True,
            "customClasses": ""
        }
    ],
    "connections": [
        {
            "id": "16414770159109",
            "from": "ni_16414770159093",
            "to": "ni_16414770159105"
        },
        {
            "id": "164147704684718",
            "from": "ni_16414770159107",
            "to": "ni_164147704394713"
        }
    ]
}
class Process():
    def __init__(self, filter_name, node_sheet_query):


        # Todo: Create a better way to define 'n' threading.Event()
        self.methods_name={func for func in dir(self) if callable(getattr(self, func)) and func.startswith("_") and not func.endswith("_")}
        [setattr(self, method+"_event", threading.Event()) for method in self.methods_name]

        self.enabled_node_classes = {"MoveNode": MoveNode, "IdentifyNode": IdentifyNode}
        self.node_config = self._update_node_sheet(node_sheet_query)

    def is_set(self, event_name):
        print("Verificando evento:", event_name)
        return getattr(self, event_name+"_event").is_set()
    
    def set_now(self, event_name):
        print("Setando evento:", event_name)
        return getattr(self, event_name+"_event").set()
    
    def clear_now(self, event_name):
        print("Limpando evento:", event_name)
        return getattr(self, event_name+"_event").clear()

    def change_events(event_name_list, mode):
        def wrapper(function):
            def wrapper2(self, *args, **kwargs):
                print("Alternando eventos...")
                for event_name in event_name_list:
                    if mode == "set":
                        self.set_now(event_name)
                    else:
                        self.clear_now(event_name)
                return function(self, *args, **kwargs)
            return wrapper2
        return wrapper

    def skip_if_is_running(event_name):
        def wrapper(f):
            def wrapper2(self, *args, **kwargs):
                if self.is_set(event_name):
                    print(f"Pulando chamada da função [{f.__name__}] pois o evento [{event_name}] está setado.")
                    return
                print(f"Executando chamada da função [{f.__name__}] pois o evento [{event_name}] está limpo.")
                return f(self, *args, **kwargs)
            return wrapper2
        return wrapper

    @skip_if_is_running("_start")
    @change_events(["_start"], "set")
    @change_events(["_resume"], "clear")
    def _start(self, *args, **kwargs):
        print("Dentro de _start")
        self._resume()
        # Imprime a data e hora de início do processo
        print("Starting at: " + (datetime.now()
                                    ).strftime('%m/%d/%Y, %H:%M:%S'))
        # Enquanto o processo não for parado
        while not self.is_set("_stop"):
            self.node_config.reset()
            for node_id in self.node_config.node_sequence:
                node = self.node_config.nodes[node_id]
                _input = self.node_config.in2out[node._input_id] if node_id != self.node_config.node_sequence[0] else "start"
                node.run(_input, self.node_config.output_dict)
                while self.is_set("_pause"):                                    # Enquanto o processo estiver pausado
                    pass

        # Imprime a data e hora de parada do processo
        print("Stopped at:" + (datetime.now()).strftime('%m/%d/%Y, %H:%M:%S'))

    @skip_if_is_running("_stop")
    @change_events(["_stop"], "set")
    @change_events(["_start"], "clear")
    def _stop(self, *args, **kwargs):
        # Para a máquina, e inibe novos movimentos
        [machine.stop() for machine in machine_objects.values()]

    @skip_if_is_running("_pause")
    @change_events(["_pause"], "set")
    @change_events(["_resume"], "clear")
    def _pause(self, *args, **kwargs):
        # Pausa a máquina, e inibe novos movimentos.
        [machine.pause() for machine in machine_objects.values()]

    @skip_if_is_running("_resume")
    @change_events(["_resume"], "set")
    @change_events(["_pause", "_stop"], "clear")
    def _resume(self, *args, **kwargs):
        [machine.resume() for machine in machine_objects.values()]

    @skip_if_is_running("_start")
    def _update_node_sheet(self, query, *args, **kwargs):
        # self.node_config = Reader(database.find_one(
        #     "node_sheets", query), self.enabled_node_classes)
        # print(temp)
        self.node_config = Reader(temp, self.enabled_node_classes)
        return self.node_config

    def _play_node_sheet(self, node_sheet_obj):
        pprint(node_sheet_obj)
        # self._stop()
        # self.node_config = Reader(obj, self.enabled_node_classes)
        # self._start()


# ===========================================================================
# ================================ Main Code ================================
# ===========================================================================


if __name__ == '__main__':
    server_name = "Parallax"
    _process = Process(
        filter_name="small_blue",
        node_sheet_query={
            "_id": ObjectId("61d8678a612a89559c52e62e")
        }
    )

    _process_functions = {"process"+func: getattr(_process, func) for func in _process.methods_name}
    _server_info = database.find_one("servers", {"name": server_name})
    server_app = Server(
        **_server_info,
        app_functions=_process_functions,
        app_cameras=camera_objects,
    )

    server_app.start()
