
from datetime import datetime, timedelta
from threading import Event
# Create a chronometer class to measure time, with a start, pause, resume and stop method
class Chronometer:
    def __init__(self) -> None:
        self.cron_Running = timedelta(0)
        self.pause_delta = timedelta(0)
        self.pause_event = Event()

    def start(self):
        self.cron_Start = datetime.now()
        self.cron_Running = 0
        return self.cron_Start
    
    def trigger(self):
       # self.cron_End = datetime.now()
        self.cron_Running = (datetime.now() - self.cron_Start)-self.pause_delta
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
        self.pause_delta += (datetime.now() if resumed is None else resumed)-self.ps
        self.pause_event.clear()

    def __call__(self):
        return self.__dict__