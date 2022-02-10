from serial.tools import list_ports
from serial import Serial, serialutil
from bson import ObjectId
from src.manager.serial_manager import SerialManager

class CustomSerial(Serial):
    def __init__(self, port=None, baudrate=9600, device=-1, description=-1,vid=-1,pid=-1,serial_number=-1,manufacturer=-1,subsystem=-1, bytesize=8, parity='N', stopbits=1, timeout=0.01, xonxoff=False, rtscts=False, dsrdtr=False, is_gcode=False) -> None:
        super().__init__(port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, dsrdtr)
        self._id = ObjectId()
        self.port = port
        self.baudrate = baudrate
        self.is_open = False
        self.is_gcode = is_gcode
        self.last_value_send = None
        self.last_value_received = None

        self.device=device
        self.description=description
        self.vid=vid
        self.pid=pid
        self.serial_number=serial_number
        self.manufacturer=manufacturer
        self.subsystem=subsystem

        self.filters = {
            "device": self.device,
            "description": self.description,
            "vid": self.vid,
            "pid": self.pid,
            "serial_number": self.serial_number,
            "manufacturer": self.manufacturer,
            "subsystem": self.subsystem
        }

    def start(self):
        try:
            if self.port is None:
                compatible = self.findMostCompatiblePort()
                if compatible is not None:
                    for k, v in compatible.__dict__.items():
                        setattr(self, k, v)
                    self.port = self.device
            assert self.port is not None, "Port is not set and no compatible filter found!"
            super().open()
            self.is_open = True
            SerialManager.add(self)

        except serialutil.SerialException as e:
            if "No such file or directory" in str(e):
                print(f"Porta não encontrada! [{self.port}]")
            raise e
        return self

    def close(self):
        SerialManager.remove(self)
        super().close()
        self.is_open = False
        return self
    
    def reset(self):
        self.close()
        self.start()
        return self

    def send(self, message, echo=False):
        try:
            _ = self.write(message)
            if echo: return _
        except serialutil.PortNotOpenError:
            self.start()
            return self.send(message, echo)
        except Exception as e:
            self.close()
            print("Trigger alert and log error - serial.send()")
            raise e

    def write(self, payload):
        super().write((f"{payload}\n").encode("ascii"))
        self.last_value_send = payload
        return self.echo()

    def echo(self):
        lines = []
        _b = self.readline()
        while _b != b'' and self.inWaiting() !=0:
            lines.append(_b.decode("ascii").rstrip())
            _b = self.readline()
        lines.append(_b.decode("ascii").rstrip())
        self.last_value_received = lines
        return lines


    def findMostCompatiblePort(self):
        ports = {}
        port_list = {f"{p.vid}{p.serial_number}":p for p in list_ports.comports()}
        for port_id, port in port_list.items():
            match = 0
            for filter_key, filter_value in self.filters.items():
                if filter_value != -1 and getattr(port, filter_key) == filter_value:
                    match+=1
            if match > 0:
                ports[port_id] = match
        if ports:
            return port_list.get(max(ports, key=ports.get))

    def to_dict(self):
        return {
            "port": self.port,
            "baudrate": self.baudrate,
            "is_open": self.is_open,
            "is_gcode": self.is_gcode,
            "last_value_send": self.last_value_send,
            "last_value_received": self.last_value_received
        }

def checker():
    a = CustomSerial(device="/dev/ttyACM0", baudrate=250000)
    a.open()
    a.close()