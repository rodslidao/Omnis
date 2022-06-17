from logging import Logger
from click import command
from cv2 import log
from .custom_serial import Serial
from api import logger, exception
from api.decorators import for_all_methods
from api import logger
from threading import Event
# from src.utility.system.sleep_alternative import sleep
# from time import sleep
from api.subscriptions import SubscriptionFactory
from api.store import controls
from json import loads
from re import split
rtc_status = SubscriptionFactory(controls, f"controls")

@for_all_methods(exception(logger))
class SerialGcodeOBJ(Serial):
    def __init__(
        self,
        _id=None,
        port=None,
        name=None,
        baudrate=9600,
        filters={},
        bytesize=8,
        parity="N",
        stopbits=1,
        timeout=0.01,
        xonxoff=False,
        rtscts=False,
        dsrdtr=False,
        is_gcode=True,
        disabled=False,
        startup_commands = [
            "G28",
        ],
        pins={}
    ):
        super().__init__(
            port,
            name,
            baudrate,
            filters,
            bytesize,
            parity,
            stopbits,
            timeout,
            xonxoff,
            rtscts,
            dsrdtr,
            is_gcode=True,
            _id=_id,
        )
        self.is_open = True
        self.status ={
            "positions":{'X':-1, 'Y':-1, 'Z':-1, 'A':-1, 'B':-1, 'C':-1},
            "endstops":{'X':False, 'Y':False, 'Z':False, 'A':False, 'B':False, 'C':False}
        }
        self.resumed = Event()
        self.resumed_permission = ["stop", "kill", "quick_stop", "resume"]
    
        for msg in startup_commands:
            self.send(msg)
        self.pins = pins
        self.resume()

    def verify(function):
        def wrapper(self, *args, **kwargs):
            if not self.is_open: return
            return function(self, *args, **kwargs)
        return wrapper

    @verify
    def G0(self, *args, **kwargs):
        """
        Send a GCODE movement command (G0) and wait for current position to be reached.
        """
        # Create a coordinate string based in args.
        cords = ""
        for pos in args:
            cords += f"{pos[0].upper()}{pos[1]} "

        # Send machine to the coordinate string
        self.super_send(f"G0 {cords}")

        future = self.M114().items()
        # Wait for the machine to reach the coordinate string
        while (
            any((round(v,3) != round(self.M114("R")[i],3)) for i, v in future)
            #and not self.resumed.is_set()
        ):
            pass

    @verify
    def M114(self, _type="", sequence=["X", "Y", "Z", "A", "B", "C", ":"], *args, **kwargs):
        """
        Get current position of machine.
        _type:
            R - Return the current position of the machine, in real time.
            ''- Return the future postion of the machine.

        """
        echo = self.super_send(f"M114 {_type}", echo=True, log=False)[0]
        txt = echo
        for n in sequence:
            txt = txt.replace(n, "")
        try:
            _echo = dict(
                zip(
                    sequence[:-1],
                    list(map(float, txt.split(" ")[: len(sequence) - 1])),
                )
            )
            if _type == "R":
                self.status["jog_position"] = _echo
                rtc_status.put(self.status)
            return _echo
        except ValueError:  # ! Why this error?
            logger.info('[SerialGcodeOBJ] M114 error: "{}"'.format(echo))
            raise
    
    def M42(self, _id, _value):
        return super().send(self.pins[_id].set_value(_value)) if self.pins.get(_id) else False

    def send(self, msg, echo=False, log=True, *args, **kwargs):
        parms = list(
            filter(
                lambda x: x is not None and x != " " and x != "",
                split(
                    "(\(.*\))|(\{.*)| ",
                    msg,
                ),
            )
        )
        command_splited = list(map(SerialGcodeOBJ.parser, parms))
        if command_splited[0].startswith(">"):
            command_splited[0] = command_splited[0][1:]
        if all(isinstance(n, str) for n in command_splited):
            return super().send(msg, echo, log, *args, **kwargs)

        sender = getattr(self, command_splited[0].upper(), False)
        if sender:
            args = command_splited[1] if len(command_splited) > 1 else []
            kwargs = command_splited[-1] if isinstance(command_splited[-1], dict) else {}
            logger.info(f"{command_splited[0].upper()}: {sender(*args, **kwargs)}")
        else:
            # logger.info(f"Invalid: {command_splited[0].upper()}")
            self.last_value_received=['Invalid: {}'.format(command_splited[0].upper())]
        return self

    def super_send(self, *args, **kwargs):
        return super().send(*args, **kwargs)

    def parser(string):
        if string.startswith("("):
            return eval(string)
        elif string.startswith("{"):
            return loads(string)
        return string

    @verify
    def pause(self):
        """
        The M0 command pause after the last movement and wait for the user to continue.
        """
        self.resumed.clear()
        self.super_send("M0")

    @verify
    def kill(self):
        """
        Used for emergency stopping,
        M112 shuts down the machine, turns off all the steppers and heaters
        and if possible, turns off the power supply.
        A reset is required to return to operational mode.
        """
        self.super_send("M112")

    @verify
    def stop(self):
        """
        Stop all steppers instantly.
        Since there will be no deceleration,
        steppers are expected to be out of position after this command.
        """
        self.super_send("P000")
        self.super_send("M410")
        self.pause()

    def resume(self):
        """
        Resume machine from pause (M0) using M108 command.
        """
        self.super_send("M108")
        self.super_send("R000")
        self.resumed.set()

    def __str__(self) -> str:
        return f"[[SerialGcodeOBJ] {self.name}, {self.port}, {self.baudrate}]"
