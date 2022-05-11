from .custom_serial import Serial
from api import logger, exception
from api.decorators import for_all_methods


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
        _id=None,
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
        self.pause = False
        self.pause_permission = ["stop", "kill", "quick_stop", "resume"]

    def verify(function):
        def wrapper(self, *args, **kwargs):
            if self.pause or not self.is_open:
                return
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
        echo = self.send(f"M114 {_type}", echo=True)[0]
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
            print("\n" * 3, echo)
            return self.M114(_type, sequence)

    @verify
    def M119(self, cut=": "):
        """
        Get status of endstops.
        """
        pos = []
        key = []
        for _ in range(2):
            Echo = (self.send("M119", echo=True))[1:-1]
        for info in Echo:
            try:
                pos.append(info[info.index(cut) + len(cut) : len(info)])
                key.append(info[: info.index(cut)])
            except ValueError as e:  # ! Why this error?
                logger.critical(f"{self.name} - {info} : {e}")
        return dict(zip(key, pos))

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

        # if does not have a wait parameter, return.
        if not kwargs.get("sync"):
            return

        # Split the atual and future position in 2 lists.
        future, real = self.M114(), self.M114("R")
        a, b = [v for v in future.values()], [v for v in real.values()]

        # Wait for the machine to reach the coordinate string. while all axis real coordinates are not equal to the future coordinates (+- 0.5).
        while (
            not all((a[i] - 0.5 <= b[i] <= a[i] + 0.5) for i in range(len(b)))
            and not self.pause
        ):
            # Update the real position.
            b = [v for v in self.M114("R").values()]

    @verify
    def pause(self):
        self.pause = True
        """
        The M0 command pause after the last movement and wait for the user to continue.
        """
        self.send("M0")

    @verify
    def kill(self):
        self.pause = True
        """
        Used for emergency stopping,
        M112 shuts down the machine, turns off all the steppers and heaters
        and if possible, turns off the power supply.
        A reset is required to return to operational mode.
        """
        self.send("M112")

    @verify
    def stop(self):
        self.pause = True
        """
        Stop all steppers instantly.
        Since there will be no deceleration,
        steppers are expected to be out of position after this command.
        """
        self.send("M410")

    def resume(self):
        self.pause = False
        """
        Resume machine from pause (M0) using M108 command.
        """
        self.send("M108")

    def callPin(self, name, state, json):
        value = json[name]["command"] + (
            json[name]["values"].replace("_pin_", str(json[name]["pin"]))
        ).replace("_state_", str(json[name][state]))
        self.send(value)

    def __str__(self) -> str:
        return f"[[SerialGcodeOBJ] {self.name}, {self.port}, {self.baudrate}]"
