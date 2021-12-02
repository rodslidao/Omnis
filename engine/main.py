
# import datetime
# from time import sleep, monotonic
# from externallibs.new_serial.connection import new_connection

# # from imports import *

# a = macro.objeto((20,20), 1, 1,1,1,1)
# b = macro.objeto((30,30), 1, 1,1,1,1)
# c = macro.objeto((10,10), 1, 1,1,1,1)
# x = [a, b, c]

from os import access, makedirs, replaceue
from time import sleep
from codetiming import Timer
import numpy as np
actuators = {
    "all": {"condition": lambda obj: obj, "action": lambda x: default_actions(x)},
    "<10": {"condition": lambda obj: obj.center[0] <= 10, "action": lambda x: print(f"{x.center[0]} é menor que 10")},
    "print": {"condtion": lambda _: True, "action": lambda _: print("deu certo, carai!")}
}

relations = {
    "all": "print",
}


def run(node, _input, _all=None): 
    if _all is None: 
        return list(map(node["action"], list(filter(node["condition"], _input))))
    else:
        return node["action"](list(filter(node["condition"], _input)))



teste = {
    "*1": {"condition": lambda _: True, "action": lambda x: x*1},
    "+2": {"condition": lambda _: True, "action": lambda x: x+2},
    "+3": {"condition": lambda _: True, "action": lambda x: x+3},
    "+4": {"condition": lambda _: True, "action": lambda x: x+4},
    "+5": {"condition": lambda _: True, "action": lambda x: x+5},
    "soma_a_b": {"condition": lambda _: True, "action": lambda x: sum(x)},
    "output":{"condition": lambda _,: True, "action": lambda _: print(f"Resposta:{_}")},
}

regras = [
    {"input":['a'], "node":'*1', "save_as":'A'},
    {"input":['b'], "node":'+5', "save_as":'B'},
    {"input":['B'], "node":'*1', "save_as":'C'},
    {"input":['A', 'C'], "node":'soma_a_b', "save_as":'R', "all":True},
    {"input":['R'], "node":"output", "save_as":'R'}
]


def A(relation=regras, inputs={'a': 0, 'b': 6}, answer={}):
    for step in relation:
        if any(x in answer for x in step['input']):
            
            print(f"valor {step['input']} já é conhecido...")
            value = np.array([answer[k] for k in step['input']]).ravel()
            answer[step['save_as']] = run(teste[step['node']], value, step.get('all'))

        elif any(x in inputs for x in step['input']):
            print(f"valor {step['input']} será calculado...")
            value = np.array([inputs[k] for k in step['input']]).ravel()
            answer[step['save_as']] = run(teste[step['node']], value, step.get('all'))

        print(f"Usando valor: {value}, no node {step['node']}...")
        print(f"node {step['node']} respondeu com : {answer[step['save_as']]}, salvando como {step['save_as']}")
A()
exit()
path = r'C:\Users\osche\OneDrive\Documentos\GitHub\Rose_ADP\engine\data\log\config\config.json'
logging.config.dictConfig(js.load(open(f"{path}", 'r', encoding='utf8')))
logger = logging.getLogger(__name__)

script_dir = os.path.dirname(__file__)

config_json_dir = './data/json/config'
data_json_dir = './data/json/data'
data_images_dir = script_dir+'./data/images'
default_cam_bkg = cv2.resize(cv2.imread(
    f"{data_images_dir}/static/background.jpg"), (0, 0), fx=0.5, fy=0.5)

# ===========================================================================
# ============================ Define json object ===========================
# ===========================================================================
devicefilter_json = json.new(
    f"{config_json_dir}/devicefilter.json", "devicefilter", script_dir)
positions_json = json.new(
    f"{config_json_dir}/machine/positions.json", "positions", script_dir)
stopreasons_json = json.new(
    f"{config_json_dir}/stopreasons.json", "stopreasons", script_dir)
templates_json = json.new(
    f"{config_json_dir}/templates.json", "templates", script_dir)
keypoints_json = json.new(
    f"{config_json_dir}/keypoints.json", "keypoints", script_dir)
filters_json = json.new(
    f"{config_json_dir}/filters.json", "filters", script_dir)
cameras_json = json.new(
    f"{config_json_dir}/cameras.json", "cameras", script_dir)
process_json = json.new(
    f"{config_json_dir}/process.json", "process", script_dir)
pins_json = json.new(
    f"{config_json_dir}/machine/pins.json", "pins", script_dir)
server_json = json.new(f"{config_json_dir}/server.json", "server", script_dir)
debug_json = json.new(f"{config_json_dir}/debug.json", "debug", script_dir)
user_json = json.new(f"{config_json_dir}/users.json", "users", script_dir)
production_json = json.new(
    f"{config_json_dir}/production.json", "production", script_dir)

# ===========================================================================
# ========================== Define camera objects ==========================
# ===========================================================================
cameras_objects = {}
for cam in cameras_json.value["cameras"]:
    device_cam = device.new_camera(cam, background=default_cam_bkg)
    cameras_objects[cam["name"]] = device_cam

# ===========================================================================
# ======================== Define identifier objects ========================
# ===========================================================================
identificator_objects = {}
for identificator_name in filters_json.value["enable"]:
    identificator_objects[identificator_name] = macro.identificador(
        identificator_name, filters_json.value, templates_json.value[identificator_name])

# ===========================================================================
# ===================== Define area_processing objects ======================
# ===========================================================================
processing_objects = {}
for area in devicefilter_json.value:
    cam_obj = cameras_objects[area["camera_device"]]
    ide_obj = identificator_objects[area["filter"]]
    process = macro.AreaProcessing(
        area["filter"], cam_obj, keypoints_json.value, ide_obj, blur=(5, 5))
    processing_objects[area["filter"]] = process

# ===========================================================================
# ======================= Define stop reasons objects =======================
# ===========================================================================
stopreasons_objects = {}
for stop_obj in stopreasons_json.value:
    stopreasons_objects[stop_obj['name']] = stop.reason(
        stop_obj['name'], logging.getLogger("stop_logger"), stop_obj['initial'])

# ===========================================================================
# ======================= Define productions objects =======================
# ===========================================================================
production_objects = {}
for prod_model in production_json.value["models"]:
    prod_obj = json.production(data_json_dir+'/production', prod_model,
                               production_json.value["template"], script_dir, autoSave=True)
    production_objects[prod_model["name"]] = prod_obj

# ===========================================================================
# ======================== Define auxiliar functions ========================
# ===========================================================================


def access_prod_objt_by_name(name, action, *args):
    try:
        getattr(production_objects[name], action)(*args)
    except (KeyError, AttributeError, TypeError):
        print(f"Não foi possivel usar {[*args]} em {name}.{action}()")
        return False
    return True


class counter():
    def __init__(self, function, trigger, start=0, step=1) -> None:
        self.function = function
        self.start = start
        self.count = start
        self.step = step
        self.trigger = trigger

    def _next(self, *args, **kwargs):
        if self._canPull():
            self.count = self.start
            return self.function(*args, **kwargs)
        self.count+1
        return self.trigger-self.count

    def _canPull(self):
        return self.count >= self.trigger


crescer_board = new_connection('crescer_board', 0, 125000)
cartesian = gcode.gcode(crescer_board)
defaut_speed = 5000

selecteds = [0, 3, 4, 5]
model = 0


class counter():
    def __init__(self) -> None:
        self.value = 0
        pass

    def getvalue(self):
        return self.value

    def add(self, value):
        if value:
            self.value += 1
        else:
            self.value -= 1

    def reset(self):
        self.value = 0


@Timer(name="UseTimer")
def basic_process(filter_name, *args, **kwargs):
    [move.setPositon(steps,  function=move.showMoves,
                     id=f"{__name__}:{line()}") for steps in positions_json.value['catch']]
    cartesian.callPin('garra', "on", pins_json)
    cartesian.send('G28 Y')
    select_counter = counter()
    for select in selecteds:
        # select_counter.reset()

        # Para cada lado selecionado
        # extrai as posições definidas
        _as = positions_json['anlise'][model][select]

        # Movimenta a maquina.
        [
            move.setPositon(
                steps,
                function=move.showMoves,
                replace={
                    "X": _as['X'],
                    "Y":_as['Y'],
                    "Z":_as['Z'],
                    "A":_as['A'],
                    "F":defaut_speed
                },
                id=f"{__name__}:{line()}"
            ) for steps in positions_json.value['analisisHole']]

        # Realiza o reconhecimento
        data = processing_objects[filter_name].process(autoColor=True)

        # select_counter.add(bool(data)) # Provavelmente vai dar erro por não poder converter dict -> true/false
        def run(node, _input): return list(
            map(node["action"], list(filter(node["condition"], _input))))
        actuators_results = {}
        # Para cada objeto encontrado ( nesse caso espera-se somente um )
        for _id, obj_list in enumerate(data):
            # Filtra os resultados e executa uma ação para aquele objeto.
            # Ação padrão  ( para todos os objetos ) - @default_actions;
            # Estado = {"atuatorname":[T,F,T,F], at:value, ...}

            {run(actuators[B], run(actuators[A], obj_list))
             for A, B in relations.items()}
            actuators_results[_id] = {name: list(map(run["action"], list(
                filter(run["condition"], obj_list)))) for name, run in actuators.items}


def default_actions(obj, screwCenter, screwLength=25):
    # Usando as corrdenadas do centro do objeto, movimenta a maquina sob a parafusadeira
    x, y = obj.center[0]+screwCenter['X'], obj.center[1]
    y = sizorLift(screwCenter['Y'], y)
    [move.setPositon(steps, function=move.showMoves, replace={
                     "X": x, "Y": y}, id=f"{__name__}:{line()}") for steps in positions_json.value['afterIdentify']]

    # Define um limite de altura.
    limit = (cartesian.M114('R')['Z']+screwLength*0.9)
    # Efefura a 'parafusação',
    # A função é recursiva e só sai caso:
    # o limite seja atingido,
    # o limite seja ultrapassado,
    # o numero de tentativas seja exedido.
    status = parafusa(downlimit=limit)
    return isinstance(status, bool)
    # a variavel status pode conter 2 valores ( Verdadeiro, ou a altua que a maquina parou quando a função rtornou )


def parafusa(mm=-2, down=25, timer=5, status="open", counter=0, limit=3, probe_speed=50, downlimit=50):
    cartesian.relative()
    cartesian.send(f'G38.3 Z-{down} F{probe_speed}')
    cartesian.send(f'G0 Z{mm} F{probe_speed}')
    atual_Z = cartesian.M114('R')['Z']
    trigger_timer = monotonic() + timer
    while monotonic() < trigger_timer:
        if cartesian.M119(["z_probe"]) == status:
            return True
    else:
        cartesian.send(f'G0 Z{down} F{probe_speed}')
        if counter < limit and atual_Z > downlimit:
            return parafusa(mm, down, timer, status, counter+1, limit, probe_speed, downlimit)
    return cartesian.M114('R')['Z']
# ===========================================================================
# ================================ Main Code ================================
# ===========================================================================


if __name__ == '__main__':

    _process = node.Process(
        node.loop(
            _loop_type=process_json.value["loop"]["type"],
            break_function=stopreasons_objects[process_json.value["loop"]
                                               ["break_function"]].isStopped,
            range=process_json.value["loop"]["range"]
        ),
        locals()[process_json.value["function"]],
        process_json.value["filter"]
    )

    server_app = flask_app.Server(
        server_json.value['ip'],
        server_json.value['port'],
        server_json.value['updateTime'],
        functions={
            "reset_process": stopreasons_objects[server_json.value["reset_process"]].reset,
            "stop_process": stopreasons_objects[server_json.value["stop_process"]].stop,
            "start_process": _process.start
        },
        cameras={
            "camera0": cameras_objects["camera0"],
            'area': processing_objects["small_blue"]
        }
    )
    server_app.start()
