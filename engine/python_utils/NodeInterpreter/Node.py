class Reader():
    def __init__(self, node_sheet, avaliable_node_classes, initial_output_dict={"start":True}) -> None:
        self.pre_nodes = node_sheet["nodes"]
        self.connections = node_sheet["connections"]
        self.output_dict = self.reset_dicit = initial_output_dict
       
        self.out2in = {n["from"]:n["to"] for n in self.connections}
        self.in2out = {n["to"]:n["from"] for n in self.connections}

        self.input_connections = {cn["to"] for cn in self.connections}
        self.output_connections = {cn["from"] for cn in self.connections}

        self.avaliable_nodes = avaliable_node_classes
        self.node_sequence = []
        self.node_sequence = self.make_nodes()

    def reset(self):
        print('\n', " -- Resetando Nodes -- ", '\n')
        self.output_dict = self.reset_dicit.copy()
        self.node_sequence = []
        self.in2out = {}
        for node in self.nodes.values():
            node.reset()
            
    def make_nodes(self):
        self.node_by_input_id = {}
        self.node_sequence = []
        self.nodes = {}

        for node in self.pre_nodes:
            if node["type"] in self.avaliable_nodes:
                _node = self.avaliable_nodes[node["type"]](node, self.output_dict, self.in2out)
                self.nodes[node["id"]] = _node
                self.node_by_input_id[self.nodes[node["id"]]._input_id] = self.nodes[node["id"]]
                self.node_by_output_id[self.nodes[node["id"]]._output_id] = self.nodes[node["id"]]
                if _node._output_id not in self.output_connections:
                    self.lastnode = _node
                # if self.nodes[node["id"]]._input_id not in self.input_connections:
                #     self.node_sequence.append(node["id"])
                #     for it_id, it in self.nodes["id"]._interfaces.items():
                #         self.output_dict[it_id] = it.value
        print("\n", " -- Sequenciando Nodes -- ", "\n")
        for node in self.nodes.values():
            print('\t', '--'*10)
            print("\t Node:", node._name, " - ", node._id)
            if node._input_id not in self.input_connections:
                self.node_sequence.append(node._id)
                print("\t Entrada: Sim")
                for it in node._interfaces.values():
                    if it.id in self.out2in.keys():
                        print('\t', it.name,' - ', it.value, " - ", it.id)
                        self.output_dict[it.id] = it.value
            else:
                print("\t Entrada: Não")
            
            
        print("\n -- Nodes -- \n")
        self.node_sequence = self.node_sequencer(self.node_sequence, self.node_sequence[-1])
        for nn, n in enumerate(self.node_sequence):
            print(self.nodes[n]._name, end=f' >>  ')
        print("\n")
        return self.node_sequence
    def node_sequencer(self, lista, _ids, input=False):
        try:
            last_id = self.node_by_input_id[ self.out2in[self.nodes[_ids]._output_id]]._id
            lista.append(last_id)
            lista = self.node_sequencer(lista, last_id)
        except KeyError:
            pass
        return lista

    
    def nds2(self, node):
        for n in node._interfaces.values():
            
    
        

if __name__ == '__main__':
    from nodeClasses import *
    
    template = {
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
                            "id": "ni_16414770159093",
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
                            "id": "ni_16414770159105",
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
                            "id": "ni_16414770159107",
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

    from itertools import cycle
    node_sheet = Reader(template, {"MoveNode": MoveNode})
    licycle = cycle(node_sheet.node_sequence)

    for i in range(3):
        node_sheet.reset()

        for _ in range(len(node_sheet.node_sequence)):
            thisnode = next(licycle)                            #? Acessa o próximo elemento do ciclo (id do nó)
            node = node_sheet.nodes[thisnode]                   #? Acessa o nó pelo id
            if thisnode == node_sheet.node_sequence[0]:         #? Se for o primeiro nó, então o input é predefinido
                _input = "start"
            else:                                               #? Senão, o input é o output do nó anterior
                _input = node_sheet.in2out[node._input_id]

            node.run(_input, node_sheet.output_dict)            #? Executa o nó             
            print("Saida:", node_sheet.output_dict)

        
#! Cada classe de nó tem um tipo de input e um ou mais formatos aceitos.