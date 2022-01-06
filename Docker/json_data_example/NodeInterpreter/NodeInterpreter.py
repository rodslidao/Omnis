
class Node():
    def __init__(self, data):
        self._type = data['type']
        self._id = data['id']
        self._options = data['options']
        self._interfaces = data['interfaces']

    def run(*args, **kwargs):
        pass

class MoveNode(Node):
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
    
    def run(self, **kwargs):
        print(f"Movendo com {self._controller} para {self.move}")
        self._output = True
        #machine_objects[self._controller].M_G0(*self.move, nonsync=None if isinstance(self.move[0], tuple) else True)


    # output
    # """ [
    #         {
    #             "axis": "X",
    #             "coordinate": 0.0,
    #             "channel": 0,
    #             "await": false
    #         },
    # ] """

nodes = [
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
                    True
                ],
                [
                    "Y",
                    None
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
                        "id": "AA",
                        "value": None
                    }
                ],
                [
                    "X ",
                    {
                        "id": "ni_164147702048110",
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
            "type": "MoveNode",
            "id": "node_16414770159104",
            "name": "Movimento",
            "options": [
                [
                    "Hardware",
                    "Octopus V1.1"
                ],
                [
                    "X",
                    True
                ],
                [
                    "Y",
                    None
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
                        "id": "BB",
                        "value": 0
                    }
                ],
                [
                    "Velocidade",
                    {
                        "id": "ni_16414770159106",
                        "value": 2500
                    }
                ],
                [
                    "Saida",
                    {
                        "id": "CC",
                        "value": None
                    }
                ],
                [
                    "X ",
                    {
                        "id": "ni_164147703486511",
                        "value": -100
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
                    True
                ],
                [
                    "Y",
                    None
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
                        "id": "DD",
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
                    "X ",
                    {
                        "id": "ni_164147708580719",
                        "value": 300
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
    ]

connections = [
        {
            "id": "16414770159109",
            "from": "AA",
            "to": "BB"
        },
        {
            "id": "164147704684718",
            "from": "CC",
            "to": "DD"
        }
    ]

input_connections = {cn["to"]:None for cn in connections}
output_connections = {cn["from"]:None for cn in connections}
links = {cd["from"]:cd["to"] for cd in connections}
print(links)
# print(input_connections, output_connections)
new_nodes = {}
node_by_input_id = {}
node_by_output_id = {}
node_sequence = []

for node in nodes:
    n = MoveNode(node)
    new_nodes[n._id] = n
    node_by_input_id[n._input_id] = new_nodes[n._id]
    node_by_output_id[n._output_id] = new_nodes[n._id]
    if n._input_id not in input_connections:
        node_sequence.append(n._id)


def acess(lista, _ids, input=False):
    try:
        last_id = node_by_input_id[links[new_nodes[_ids]._output_id]]._id
        lista.append(last_id)
        lista = acess(lista, last_id)
    except KeyError:
        pass
    return lista

node_sequence = acess(node_sequence, node_sequence[0])
print(node_sequence)

for n in node_sequence:
    print(new_nodes[n]._input_id, new_nodes[n]._output_id)

#? Sequencia de nodes esá aparetemente correta, ( aplicar nome em algus nodes e verificar se está correto)
#! Definir como a classe do nó executa a função, e relação de argumentos/ outputs de cada nó.