from os import replace
from python_utils.imports import *
from python_utils.nodes import *
import numpy as np

nodes = {
    'get_obj_attribute_in_dataset': lambda atribute, set_of_objects: [getattr(obj, atribute) for obj in set_of_objects],
    'set_this_to_that_here': lambda this, that, here: setattr(here, this, that),
    'use_this_function_in_that_iterable': lambda this, that: map(this, that),
    "trigger_pin": lambda actuator_name, pin: print(actuator_name, pin),
    'filter_this_using_that': lambda this, that: filter(that, this),
    'get_this_from_that': lambda this, that: getattr(that, this),
    'startup_serials': lambda *args: startup_serials(*args),
    "obj_center_getter": lambda *args: getCenter(*args),
    "coordinates_movments":lambda *args: Mover(*args),
    "named_movments": lambda *args: Mover(*args),
    "identify_by_name": identify_by_name,
    'x<=y': x_smaller_than_or_equal_to_y,
    'x>=y': x_bigger_than_or_equal_to_y,
    'x!=y': x_not_equal_to_y,
    'x<y': x_smaller_than_y,
    'x>y': x_bigger_than_y,
    'x=y': x_equal_to_y,
    'getattr':getattr,
    'setattr':setattr,
    'filter':filter,
    'print':print,
    'map':map,
}

rules = [
    {'input': ['None'], 'node': 'startup_serials'},
    # {'define':{'att_center':"rectangle"}},
    {'input': ['start_movment_name','speed'], 'node': 'coordinates_movments'},
    # {'input': ['filter_name'], 'node': 'identify_by_name', 'output': 'obj_to_process'},
    # {'input': ['att_center','obj_to_process'], 'node': 'get_obj_attribute_in_dataset', 'output': 'centers'},
    #{'input': ['obj_to_process'], 'node': 'obj_center_getter', 'output': 'centers'},
    # {'input': ['centers'], 'node': 'print'},
    {'input': ['mount_movment_name', 'speed'], 'node': 'coordinates_movments'},
    # {'input': ['trigger_pin', 'actuator_name'], 'node': 'trigger_pin'},
]

def NodeReader(rules, available_nodes, inputs, stop_event=None, pause_event=None):
    answer=inputs.copy()
    for _id, step in enumerate(rules):

        if stop_event.is_set(): return      # Se o evento de parada foi setado, interrompe a execução
        while pause_event.is_set():         # Se o evento de pausa foi setado, aguarda
            if stop_event.is_set(): return      # Se o evento de parada foi setado, interrompe a execução

        if step.get('define'):             # Se o passo tem uma definição, cria um novo objeto nas respectivas variáveis
            answer[next(iter(step.get('define')))] = next(iter(step.get('define').values()))
            continue                       # Pula para o próximo passo

        print('\n', '-'*20, '\n', f'Running {_id}º node >> {step}', '\n', '-'*20, '\n')
        _use = answer if all(x in answer for x in step.get('input')) else inputs   # Decisão de qual dicionário de inputs será usado
        value = np.array([_use[k] for k in step.get('input')]).ravel()             # Converte os inputs para um array

        print(f"Usando o valor: {value} no node {step.get('node')}...")
        _output = available_nodes[step.get('node')](*value)                        # Executa o node com o array definido acima e pega o output
        print(f"O Node {step.get('node')} respondeu com : {_output}")
        if step.get('output'):                                                      # Se o passo requer um output, define o output
            print(f"Salvando o valor {_output} como \"{step.get('output')}\" ...")
            answer[step.get('output')] = _output if _output is not None else [None]
            print(f"Valor salvo como \"{step.get('output')}: {_output}\"")