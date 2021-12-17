from python_utils.imports import *
from python_utils.setup_objects import *

def access_prod_objt_by_name(name, action, *args):
    try:
        getattr(production_objects[name], action)(*args)
    except (KeyError, AttributeError, TypeError):
        print(f"Não foi possivel usar {[*args]} em {name}.{action}()")
        return False
    return True


def get_classMethodNames(class_name):
    return list(set([attribute for attribute in dir(imports[class_name]) if callable(getattr(imports[class_name], attribute)) and attribute.startswith('__') is False]))

def get_classAttributeNames(class_name):
    return list(set([attribute for attribute in dir(imports[class_name]) if not callable(getattr(imports[class_name], attribute)) and attribute.startswith('__') is False]))

def get_classMethodByName(class_name, method_name):
    return getattr(imports[class_name], method_name)

def useClassMethod(method, *args, **kwargs):
    return method(*args, **kwargs)

def useClassMethodByName(class_name, method_name, *args, **kwargs):
    useClassMethod(get_classMethodByName(class_name, method_name), *args, **kwargs)

def default_actions(obj, controller_name, screwCenter, screwLength=25):
    # Usando as corrdenadas do centro do objeto, movimenta a maquina sob a parafusadeira
    x, y = obj.center[0]+screwCenter['X'], obj.center[1]
    y = sizorLift(screwCenter['Y'], y)
    [move.setPositon(steps, function=move.showMoves, replace={
                     "X": x, "Y": y}, id=f"{__name__}:{line()}") for steps in positions_json.value['afterIdentify']]

    # Define um limite de altura.
    limit = (serial_objects[controller_name].M114('R')['Z']+screwLength*0.9)
    # Efefura a 'parafusação',
    # A função é recursiva e só sai caso:
    # o limite seja atingido,
    # o limite seja ultrapassado,
    # o numero de tentativas seja exedido.
    status = parafusa(downlimit=limit)
    return isinstance(status, bool)
    # a variavel status pode conter 2 valores ( Verdadeiro, ou a altua que a maquina parou quando a função rtornou )


def parafusa(controller_name, mm=-2, down=25, timer=5, status="open", counter=0, limit=3, probe_speed=50, downlimit=50):
    serial_objects[controller_name].relative()
    serial_objects[controller_name].send(f'G38.3 Z-{down} F{probe_speed}')
    serial_objects[controller_name].send(f'G0 Z{mm} F{probe_speed}')
    atual_Z = serial_objects[controller_name].M114('R')['Z']
    trigger_timer = monotonic() + timer
    while monotonic() < trigger_timer:
        if serial_objects[controller_name].M119(["z_probe"]) == status:
            return True
    else:
        serial_objects[controller_name].send(f'G0 Z{down} F{probe_speed}')
        if counter < limit and atual_Z > downlimit:
            return parafusa(controller_name, mm, down, timer, status, counter+1, limit, probe_speed, downlimit)
    return serial_objects[controller_name].M114('R')['Z']


def startup(objects):
    [obj.start() if not obj.isAlive() else print(f"{obj.name} already started!")  for obj in objects.values()]

def startup_serials(*args):
    startup(serial_objects)

def isTrigged(trigger):
     return stopreasons_objects[trigger].isStopped()

def Mover(movment_name, replace, controller_name='controller', _id=f"{__name__}:{line()}", *args, **kwargs):
    for steps in positions_json.value[movment_name]:
        ordem = move.setPositon(
            steps,
            replace=replace,
            id=_id
        )
        for pos in ordem:
            machine_objects[controller_name].M_G0(*pos, nonsync=None if isinstance(pos[0], tuple) else True)
       



def filter_objects(Condition, objects):
    return list(filter(Condition, objects))

def getCenter(set_of_objects):
    output = []
    for obj in set_of_objects:
        output.append(obj.center)
    return output

x_bigger_than_y = lambda x, y: x > y
x_smaller_than_y = lambda x, y: x < y
x_equal_to_y = lambda x, y: x == y
x_not_equal_to_y = lambda x, y: x != y
x_bigger_than_or_equal_to_y = lambda x, y: x >= y
x_smaller_than_or_equal_to_y = lambda x, y: x <= y

#! Não é possivel deixar a função 'findContours' como node diretamente, verificar 'override' da function na classe identificador.
def identify_by_name(name) -> set:
    return identificator_objects[name].identify()
