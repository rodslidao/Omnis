from python_utils.setup_objects import *
from time import sleep

class Base_Node():
    def __init__(self, data):
        self._type = data['type']
        self._id = data['id']
        self._options = data['options']
        self._interfaces = data['interfaces']
        self._name=data['name']
        self._output_id = [op[1]["id"] for op in self._interfaces if "Saida" in op][0]
        self._input_id = [op[1]["id"] for op in self._interfaces if "Entrada" in op][0]
    def function(self, *args, **kwargs):
        pass
    def run(*args, **kwargs):
        pass
    def reset(*args, **kwargs):
        pass


#! Verificar se o nome "Octopus V1.1" foi trocado para "Octopus V1.1"
class MoveNode(Base_Node):
    def __init__(self, data):
        super().__init__(data)
        axis = ['X ', 'Y ', 'Z ']
        self._controller = [op[1] for op in self._options if "Hardware" in op][0]
        print(self._options)
        self._movment = [(op[0], op[1]["value"]) for op in self._interfaces if op[0] in axis]
        self._speed = self._interfaces[1][1]["value"]
        self._movment.append(('F', self._speed))
        self.move = [{"axis":mv[0], "coordinate":mv[1], "channel":0, "await":True} for mv in self._movment]
        self._output = None
    
    def run(self, _id, output_dict):
        if output_dict[_id]:    #! Validar input
            print(f"Movendo com {self._controller} para {self.move}")
            machine_objects[self._controller].M_G0(*self._movment, nonsync=None if isinstance(self.move[0], tuple) else True)
            # self.function(*self.move, nonsync=None if isinstance(self.move[0], tuple) else True)
            self._output = True
            output_dict[self._output_id] = True
        
    def reset(self):
        self._output = None

    # output
    # """ [
    #         {
    #             "axis": "X",
    #             "coordinate": 0.0,
    #             "channel": 0,
    #             "await": false
    #         },
    # ] """

class IdentifyNode(Base_Node):
    def __init__(self, data):
        super().__init__(data)
    
    def run(self, _id, output_dict):
        output_dict[self._output_id] = Identifyer_objects["small_blue"].identify()
        cv2.imshow("Identificador", Identifyer_objects["small_blue"].drawData())
        cv2.waitKey(1)

    def reset(self):
        self._output = None

class FilterNode(Base_Node):
    def __init__(self, data):
        super().__init__(data)
        self._this = [op[1] for op in self._options if "A" in op][0]
        self._that = [op[1] for op in self._options if "B" in op][0]
        self.image
    
    def run(self, _id, output_dict):
        if output_dict[_id]:
            output_dict[self._output] = cv2.cvtColor(getattr(cv2, f"COLOR_{self.this}2{self.that}"))

    def reset(self):
        self._output = None

class DelayNode(Base_Node):
    def __init__(self, data):
        super().__init__(data)
        self._delay = [op[1]["value"] for op in self._interfaces if "Tempo" in op][0]
    
    def run(self, _id, output_dict):
        sleep(self._delay)
        output_dict[self._output_id] = True
    
    def reset(self):
        self._output = None

class IoNode(Base_Node):
    def __init__(self, data):
        super().__init__(data)
        self._input = [op[1]["id"] for op in self._interfaces if "Entrada" in op][0]
        self._output = [op[1]["id"] for op in self._interfaces if "Saida" in op][0]
        self._pin = [op[1] for op in self._options if "Pino" in op][0]
        self._state = [op[1] for op in self._options if "Estado" in op][0]

    def run(self, _id, output_dict):
        machine_objects[self._controller].send(F"M42 P{self._pin} S{self._state}")
        output_dict[self._output] = True
    
    def reset(self):
        self._output = None