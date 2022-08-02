class status:
    DISABLED = "DISABLED"
    IDLE = "IDLE"
    OK = "OK"
    ERROR = "ERROR"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"

class device:
    def __init__(self, max_reconnect_attemps, reconnect_interval, disabled=False) -> None:
        self. max_reconnect_attemps = max_reconnect_attemps
        self.reconnect_interval = reconnect_interval
        self.status = status.IDLE if not disabled else status.DISABLED
    
    def connect(self):
        self.status = status.CONNECTING
    
    def disconnect(self):
        self.status = status.DISCONNECTING
    
    def send(self, data):
        raise NotImplementedError
    
    def receive(self):
        raise NotImplementedError
    
    def is_connected(self):
        return self.status == status.CONNECTED
    
    def is_connecting(self):
        return self.status == status.CONNECTING
    
    def is_disconnected(self):
        return not self.is_connected()
    
    def is_disconnecting(self):
        return not self.is_connecting()