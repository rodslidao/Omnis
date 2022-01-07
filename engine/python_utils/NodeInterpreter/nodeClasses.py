from python_utils.setup_objects import *

class Base_Node():
    def __init__(self, data):
        self._type = data['type']
        self._id = data['id']
        self._options = data['options']
        self._interfaces = data['interfaces']
    def function(self, *args, **kwargs):
        pass
    def run(*args, **kwargs):
        pass

class MoveNode(Base_Node):
    def __init__(self, data):
        super().__init__(data)
        axis = ['X ', 'Y ', 'Z ']
        self._controller = [op[1] for op in self._options if "Hardware" in op][0]
        self._movment = [(op[0], op[1]["value"]) for op in self._interfaces if op[0] in axis]
        self._speed = self._interfaces[1][1]["value"]
        self._movment.append(('F', self._speed))
        self._output_id = [op[1]["id"] for op in self._interfaces if "Saida" in op][0]
        self._input_id = [op[1]["id"] for op in self._interfaces if "Entrada" in op][0]
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
