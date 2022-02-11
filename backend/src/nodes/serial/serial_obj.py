import threading
import serial
import time
from .serial_exp import serialclosed, serialnotrespond


class ColorPrint:
    R = "\033[91m"
    G = "\033[92m"
    B = "\033[94m"
    C = "\033[96m"
    Y = "\033[93m"

    WARNING = "\033[93m" + "[⚠ ]: " + "\033[0m"
    ERROR = "\033[91m" + "[⚠ ]:  " + "\033[0m"
    INFO = "\033[96m" + "[🛈 ]:  " + "\033[0m"
    SUCCESS = "\033[92m" + "[✓ ]:  " + "\033[0m"
    U = "\033[4m"
    B = "\033[1m"


def color(string, color):
    return str(getattr(ColorPrint, color) + str(string) + "\033[0m")


class SerialOBJ(object):
    def __init__(self, name, port, baudrate, **kwargs):
        self.name = name
        self.port = port
        self.baudrate = baudrate
        self.code = -1
        self.serial = None
        self.reconnect = 0
        self.kwargs = kwargs

        self.codes = {
            0: ["conexão ok.", "SUCCESS"],
            -1: [f"porta [{self.port}] está ocupada!", "WARNING"],
            -2: ["conexão inexistente!", "ERROR"],
            -3: ["conexão perdida durante a comunicação!", "WARNING"],
        }
        self.lock = threading.Lock()

    def start(self):
        try:
            self.open(self.port, self.baudrate, 3)
            return True
        except serialclosed:
            self.reopen()
        if not self.isAlive():
            raise serialclosed

    def reopen(self, limit=5, timer=2.5):
        if self.reconnect <= limit:
            try:
                self.close()
            except Exception as e:
                print("Não foi possível fechar a conexão!, trate a exceção!", e)
                raise e
            print(
                color(
                    f"{self.name} não conseguiu estabeler conexão, tentanto pela [{self.reconnect}º] vez..",
                    "WARNING",
                )
            )
            self.reconnect += 1
            try:
                self.open(self.port, self.baudrate, 0.3)
            except serialclosed:
                t0 = time.monotonic() + timer
                while time.monotonic() < t0:
                    pass
                self.reopen(limit, timer)
        return self.isAlive()

    def open(self, port, baudrate, timeout):
        print(color(f"{self.name} está conectando...", "INFO"))
        try:
            self.serial = serial.Serial(port, baudrate, timeout=timeout)
            print(self.serial)
        except serial.serialutil.SerialException as exp:
            if "FileNotFoundError" in str(exp):
                self.code = -2
            elif "Acesso negado." in str(exp):
                self.code = -1
        else:
            print(color(f"{self.name} está confirmando a conexão...", "INFO"))
            t0 = time.monotonic() + timeout
            while time.monotonic() < t0 and not self.isAlive():
                pass
            self.code = 0
        self.codePrint(self.code)
        if self.code != 0:
            raise serialclosed
        else:
            self.reconnect = 0

    def isAlive(self):
        try:
            return self.serial.isOpen()
        except AttributeError:
            return False

    def codePrint(self, code):
        print(color(self.name + " >> " + self.codes[code][0], self.codes[code][1]))

    def statusCode(self):
        return self.code

    def close(self):
        self.serial.close()

    def clear(self):
        try:
            self.serial.flush()
            self.serial.flushInput()
            self.serial.flushOutput()

        except serial.serialutil.SerialException:
            if self.kwargs.get("reconnect"):
                self.reopen()

    def send(self, command, **kwargs):
        # Verifica se é possivel enviar dados através da conexão informada.
        if self.isAlive():
            self.lock.acquire(1)
            try:
                self.clear()

                # Verifica se é um unico comando
                if isinstance(command, str):
                    self.serial.write(str(command + "{0}".format("\n")).encode("ascii"))

                # Verifica se é uma lista de comandos
                if isinstance(command, list):
                    for linha in command:
                        self.serial.write(
                            str(linha + "{0}".format("\n")).encode("ascii")
                        )

                # Verifica se é uma lista de comandos do tipo "dicionário".
                if isinstance(command, dict):
                    for linha in command:
                        self.serial.write(
                            str(command[linha] + "{0}".format("\n")).encode("ascii")
                        )

                strr = []
                while True:
                    b = self.serial.readline()
                    string_n = b.decode()
                    strr.append(string_n.rstrip())
                    if self.serial.inWaiting() == 0:
                        break

                if kwargs.get("echo"):
                    return strr

                return True
            except (
                serial.serialutil.SerialException,
                serialnotrespond,
                serialclosed,
            ):
                if self.kwargs.get("reconnect"):
                    if not self.reopen():
                        raise
                else:
                    raise
            finally:
                self.clear()
                self.lock.release()

            # Avisa que o comando não pode ser enviado, pois a conexão não existe.
        else:
            if self.kwargs.get("reconnect"):
                if not self.reopen():
                    raise serialclosed  # (self.name, port=self.port, baudrate=self.baudrate, code=self.code)
            return False