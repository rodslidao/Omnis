from .custom_serial import Serial
from api import logger, exception
from api.decorators import for_all_methods
from api import logger
from threading import Event, Thread
from json import loads
from re import split
from src.end_points import Controls
import asyncio


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
            # "G28",
        ],
        pins={},
        axes={}
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
        self.resumed = Event()
        self.resumed_permission = ["stop", "kill", "quick_stop", "resume"]
        self.__status = {"jog_position":{'X':0, 'Y':0, 'Z':0, 'A':0, 'B':0, 'C':0}}
        for msg in startup_commands:
            self.send(msg)
        self.pins = pins
        self.axes = axes
        self.resume()
        self.websocket = Controls(self._id, self)
        Thread(target=self.auto_update, name=f"{_id}_auto_update", daemon=True).start()

    def auto_update(self):
        asyncio.run(self.websocket.broadcast_on_change(self.status, self.status))


    
    def status(self):
        return self.__status


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
            cords += f"{pos[0].upper()}{round(float(pos[1]), 1)} "

        # Send machine to the coordinate string
        self.super_send(f"G1 {cords}")
        for _ in range(5):
            try:
                future = self.M114().items()
                if future: break
            except AttributeError:
                pass
        if not future: raise AttributeError("SERIAL DEAD")
        while (
            any((round(v,1) != round(self.M114("R")[i],1)) for i, v in future) #! Round is mandatory
            # any((v != self.M114("R")[i]) for i, v in future)
        ):
            continue
        return self.M114("R")
    
    @verify
    def M114(self, _type="", sequence=["X", "Y", "Z", "A", "B", "C", ":"], *args, **kwargs):
        """
        Get current position of machine.
        _type:
            R - Return the current position of the machine, in real time.
            ''- Return the future postion of the machine.

        """
        for echo in self.super_send(f"M114 {_type}", echo=True, log=False):
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
                    self.__status["jog_position"] = _echo
                    
                return _echo
            except ValueError:  # ! Why this error?
                logger.warning(f"Serial: {self.name} fail to decode custom M114. Raw payload: {echo}")
                pass

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
            logger.debug(f"Serial: [Custom GCODE] {command_splited[0].upper()}: {sender(*args, **kwargs)}")
        else:
            logger.warning(f"Serial: [Custom GCODE] {command_splited[0].upper()} can't be found.")
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
