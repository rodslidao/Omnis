from cv2 import log
from .custom_serial import Serial
from api import logger, exception
from api.decorators import for_all_methods
from api import logger
from threading import Event
# from src.utility.system.sleep_alternative import sleep
from time import sleep

#! SLEEP WILL TRIGGER SEGFALUT ERROR, DONT USE.

@for_all_methods(exception(logger))
class SerialGcodeOBJ(Serial):
    def __init__(
        self,
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
        _id=None,
        startup_commands=[
            "G28",
        ]
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
        self.resumed = Event()
        self.resumed_permission = ["stop", "kill", "quick_stop", "resume"]
    
        for msg in startup_commands:
            self.send(msg)

        self.resume()

    def verify(function):
        def wrapper(self, *args, **kwargs):
            if not self.is_open: return
            # self.resumed.wait()
            return function(self, *args, **kwargs)
        return wrapper

    @verify
    def M114(self, _type="", sequence=["X", "Y", "Z", "A", "B", "C", ":"]):
        """
        Get current position of machine.
        _type:
            R - Return the current position of the machine, in real time.
            ''- Return the future postion of the machine.

        """
        echo = self.send(f"M114 {_type}", echo=True, log=False)[0]
        txt = echo
        for n in sequence:
            txt = txt.replace(n, "")
        try:
            return dict(
                zip(
                    sequence[:-1],
                    list(map(float, txt.split(" ")[: len(sequence) - 1])),
                )
            )
        except ValueError:  # ! Why this error?
            logger.info('[SerialGcodeOBJ] M114 error: "{}"'.format(echo))
            raise
            # return self.M114(_type, sequence)

    # @verify
    # def M119(self, cut=": "):
    #     """
    #     Get status of endstops.
    #     """
    #     pos = []
    #     key = []
    #     for _ in range(2):
    #         Echo = (self.send("M119", echo=True))[1:-1]
    #     for info in Echo:
    #         try:
    #             pos.append(info[info.index(cut) + len(cut) : len(info)])
    #             key.append(info[: info.index(cut)])
    #         except ValueError as e:  # ! Why this error?
    #             logger.error(f"{self.name} - {info} : {e}")
    #     return dict(zip(key, pos))

    @verify
    def G28(
        self,
        axis="E",
        endStop="filament",
        status="open",
        offset=-23,
        steps=5,
        speed=50000,
    ):
        self.send("G91")
        while True:
            try:
                if self.M119()[endStop] != status:
                    self.send(f"G0 E{offset * -1} F{speed}")
                break
            except KeyError:
                pass

        while True:
            try:
                while self.M119()[endStop] == status:
                    self.send(f"G0 {axis}{steps} F{speed}")

                self.send("G91")
                self.send(f"G0 E-{10} F{speed}")

                while self.M119()[endStop] == status:
                    self.send(f"G0 {axis}{1} F{speed}")

                self.send("G91")
                self.send(f"G0 E{offset} F{speed}")
                self.send("G90")
                break
            except KeyError:
                pass

    @verify
    def M_G0(self, *args, **kwargs):
        """
        Send a GCODE movement command (G0) and wait for current position to be reached.
        """
        # Create a coordinate string based in args.
        cords = ""
        for pos in args:
            cords += f"{pos[0].upper()}{pos[1]} "

        # Send machine to the coordinate string
        self.send(f"G0 {cords}")

        # Split the atual and future position in 2 lists.
    
        a, b = list(self.M114().values()), len( self.M114("R").values() )
        # a, b = [10,10,10,10,10,10], [100,100,100,100,100,100]

        # Wait for the machine to reach the coordinate string. while all axis real coordinates are not equal to the future coordinates (+- 0.5).
        while (
            not all((a[i] - 0.5 <= list(self.M114("R").values())[i] <= a[i] + 0.5) for i in range(b))
            # not all((a[i] - 0.5 <= b[i] <= list(self.M114("R").values())[i] + 0.5) for i in range(len(b)))
            #and not self.resumed.is_set()
        ):
            pass
            # logger.info(f"{self.name} - waiting for machine to reach {cords}")
            # sleep(1)

    @verify
    def pause(self):
        """
        The M0 command pause after the last movement and wait for the user to continue.
        """
        self.resumed.clear()
        self.send("M0")

    @verify
    def kill(self):
        """
        Used for emergency stopping,
        M112 shuts down the machine, turns off all the steppers and heaters
        and if possible, turns off the power supply.
        A reset is required to return to operational mode.
        """
        self.send("M112")

    @verify
    def stop(self):
        # self.resumed = True
        """
        Stop all steppers instantly.
        Since there will be no deceleration,
        steppers are expected to be out of position after this command.
        """
        self.send("P000")
        self.send("M410")
        self.pause()
        # self.resume()

    def resume(self):
        """
        Resume machine from pause (M0) using M108 command.
        """
        self.send("M108")
        self.send("R000")
        self.resumed.set()

    def callPin(self, name, state, json):
        value = json[name]["command"] + (
            json[name]["values"].replace("_pin_", str(json[name]["pin"]))
        ).replace("_state_", str(json[name][state]))
        self.send(value)

    def __str__(self) -> str:
        return f"[[SerialGcodeOBJ] {self.name}, {self.port}, {self.baudrate}]"
