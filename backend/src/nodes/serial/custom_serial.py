from serial.tools import list_ports
from serial import Serial, serialutil
from bson import ObjectId
from src.manager.serial_manager import SerialManager
from api import logger, exception, for_all_methods
from threading import Lock

send_lock = Lock()

@for_all_methods(exception(logger))
class CustomSerial(Serial):
    """
    Class to comunicate with serial port.

    Attributes:
        port (str): Port to comunicate.
        baudrate (int): Baudrate to comunicate.
        is_open (bool): True if port is open.
        is_gcode (bool): True if port is gcode.
        last_value_send (str): Last value send.
        last_value_received (str): Last value received.

    Methods:
        start: Open port.
        close: Close port.
        reset: Close and open port.
        send: Send message to port.
        echo: Read message from port.
        findMostCompatiblePort: Find most compatible port.
        to_dict: Return a dictionary representation of this class instance.

    Notes:
        when a serial port is opened, it is added to the SerialManager.
        when a serial port is closed, it is removed from the SerialManager.

        findMostCompatiblePort:

    """

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
        is_gcode=False,
        _id=None,
    ) -> None:
        self._id = ObjectId(_id)
        super().__init__(
            port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, dsrdtr
        )
        self.port = port
        self.baudrate = baudrate
        #self.is_open = False
        self.is_gcode = is_gcode
        self.last_value_send = None
        self.last_value_received = None

        if name is None:
            self.name = self.vid + self.pid + "_" + self.device
        else:
            self.name = name

        self.filters = filters
        SerialManager.add(self)

    def start(self):
        if not self.is_open:
            if self.port is None:
                compatible = self.findMostCompatiblePort()
                if compatible is not None:
                    for k, v in compatible.__dict__.items():
                        setattr(self, k, v)
                    self.port = self.device
            assert (
                self.port is not None
            ), "Port is not set and no compatible filter found!"
            self.open()
        return self

    def close(self):
        super().close()
    
    def stop(self):
        self.close()
        return self

    def remove(self):
        SerialManager.remove(self)

    def reset(self):
        self.close()
        self.start()
        return self

    def send(self, message, echo=False):
        send_lock.acquire()
        try:
            _ = self.write(message)
            if echo:
                return _
        except serialutil.PortNotOpenError:
            self.open()
            return self.send(message, echo)
        finally:
            send_lock.release()

    def write(self, payload):
        super().write((f"{payload}\n").encode("ascii"))
        self.last_value_send = payload
        return self.echo()

    def echo(self):
        lines = []
        _b = self.readline()
        while _b != b"" and self.inWaiting() != 0:
            lines.append(_b.decode("ascii").rstrip())
            _b = self.readline()
        lines.append(_b.decode("ascii").rstrip())
        self.last_value_received = lines
        return lines

    def findMostCompatiblePort(self):
        ports = {}
        port_list = {f"{p.vid}{p.serial_number}": p for p in list_ports.comports()}
        for port_id, port in port_list.items():
            match = 0
            for filter_key, filter_value in self.filters.items():
                if filter_value != -1 and getattr(port, filter_key) == filter_value:
                    match += 1
            if match > 0:
                ports[port_id] = match
        if ports:
            return port_list.get(max(ports, key=ports.get))

    def to_dict(self):
        return {
            "_id": self._id,
            "port": self.port,
            "name": self.name,
            "baudrate": self.baudrate,
            "is_open": self.is_open == True,
            "is_gcode": self.is_gcode == True,
            "last_value_send": self.last_value_send,
            "last_value_received": self.last_value_received,
        }


@exception(logger)
def checker():
    a = CustomSerial(device="/dev/ttyACM0", baudrate=250000)
    a.open()
    a.close()
