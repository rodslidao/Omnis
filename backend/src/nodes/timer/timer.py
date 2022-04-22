
from datetime import datetime, timedelta
from threading import Event
# Create a chronometer class to measure time, with a start, pause, resume and stop method
class Chronometer:
    """
    A Simple class to measure time, with a start, pause, resume and stop method

    Usage:
        Chronometer = Chronometer()\n
        Chronometer.start()\n
        Chronometer.pause()\n
        Chronometer.resume()\n
        Chronometer.stop()\n
        print(Chronometer.trigger()) or print(Chronometer()) or print(Chronometer.con_Running)\n
    """
    def __init__(self) -> None:
        self.cron_Running = timedelta(0)
        self.pause_delta = timedelta(0)
        self.pause_event = Event()
        self.ps = None

    def start(self):
        self.cron_Start = datetime.now()
        self.cron_Running = 0
        return self.cron_Start
    
    def trigger(self):
       # self.cron_End = datetime.now()
        # print(self.pause_delta)
        self.cron_Running = (self.cron_End - self.cron_Start)-self.pause_delta
        return self.cron_Running
    
    def stop(self):
        if self.pause_event.is_set():
            self.resume()
        self.cron_End = datetime.now()
        return self.cron_End

    def pause(self, paused=None):
        self.pause_event.set()
        self.ps  = datetime.now() if paused is None else paused

    def resume(self, resumed=None):
        self.pause_delta += (datetime.now() if resumed is None else resumed)-self.ps if self.ps is not None else timedelta(0)
        self.pause_event.clear()

    def __call__(self):
        return self.__dict__