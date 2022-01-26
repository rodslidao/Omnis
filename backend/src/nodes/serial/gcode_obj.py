from .serial_obj import SerialOBJ


class SerialGcodeOBJ(SerialOBJ):
    def __init__(self, name, port, baudrate, **kwargs):
        super().__init__(name, port, baudrate, **kwargs)
        self.pause = False
        self.pause_permission = ["stop", "kill", "quick_stop", "resume"]

    def verify(function):
        def wrapper(self, *args, **kwargs):
            if self.pause:
                return
            return function(self, *args, **kwargs)

        return wrapper

    @verify
    def M114(self, _type="", sequence=["X", "Y", "Z", "A", "B", "C", ":"]):
        if self.isAlive():
            echo = self.send(f"M114 {_type}", echo=True)[0]
            # print(echo)
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
            except ValueError:
                print("\n" * 3, echo)
                return self.M114(_type, sequence)

    @verify
    def M119(self, cut=": "):
        if self.isAlive():
            pos = []
            key = []
            for _ in range(2):
                Echo = (self.send("M119", echo=True))[1:-1]
            for info in Echo:
                try:
                    pos.append(info[info.index(cut) + len(cut): len(info)])
                    key.append(info[: info.index(cut)])
                except ValueError:
                    print("ERROR:", info)
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
        if self.isAlive():
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
        cords = ""
        for pos in args:
            axis = pos[0].upper()
            pp = pos[1]
            cords += f"{axis}{pp} "
        self.send(f"G0 {cords}")
        if kwargs.get("nonSync"):
            return
        future = self.M114()
        real = self.M114("R")
        # while True:
        a = [v for v in future.values()]
        b = [v for v in real.values()]
        while (
            not all((a[i] - 0.5 <= b[i] <= a[i] + 0.5) for i in range(len(b)))
            and not self.pause
        ):
            b = [v for v in self.M114("R").values()]
            # print(a, b)

        real = self.M114("R")
        print(real, future)

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
        # self.write(str("M410"+ '{0}'.format('\n')).encode('ascii'))

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
        print(value)
        self.send(value)
