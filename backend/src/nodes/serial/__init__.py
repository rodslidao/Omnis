from api import dbo, logger
from .custom_serial import Serial
from .gcode_obj import SerialGcodeOBJ as MarlinAPI
from src.nodes.serial.pins_obj import pin
from src.nodes.serial.axes import axis
logger.info('Serial and MarlinAPI modules loaded')
pins = [pin(**p) for p in dbo.find_many("pins")]
axes = [
    axis(**a)
    for a in dbo.find_many(
        "machine_axis", data={"_id": 1, "name": 1, "board": 1, "setup": 1}
    )
]
for config in dbo.find_many("serial-manager", {}):
    if not config.get("disabled", False):
        match config.get("is_gcode"):
            case True:
                logger.info('Creating MarlinAPI...')
                MarlinAPI(
                    pins={
                        str(p._id): p
                        for p in pins
                        if p.board == str(config["_id"])
                    },
                    axes={
                        str(a._id): a
                        for a in axes
                        if a.board == str(config["_id"])
                    },
                    **config
                )
                logger.info('Automatically creating MarlinAPI "{}"'.format(config.get("name")))
            case _:
                Serial(**config, **config.get("options"))
                logger.info('Automatically creating Serial "{}"'.format(config.get("name")))