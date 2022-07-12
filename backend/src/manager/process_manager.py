from src.manager.base_manager import BaseManager
from src.crud import SSPR
from src.nodes.process.process import sample_process as Process
from src.end_points import Process as WebProcess
from api import logger, dbo, auth
from api.mutations import mutation

from threading import Thread
import asyncio

class ProcessObjectManager(SSPR, BaseManager):
    def __init__(self, alias, auth_level, collection):
        SSPR.__init__(self, alias=alias, auth_level=auth_level, collection=collection)
        BaseManager.__init__(self)
        self._id = "status"
        for process in dbo.find_many(self.collection):
            self.add(Process(**process))
            self.selected_process_id = process['_id']

        self.websocket = WebProcess(self._id, self.process)
        Thread(
            target=self.auto_update, name=f"{self._id}_auto_update", daemon=True
        ).start()

        self.loadConfig = (auth(auth_level))(self.loadConfig)
        mutation.set_field(f"loadConfig", self.loadConfig)

    def auto_update(self):
        asyncio.run(self.websocket.broadcast_on_change(self.process.status))

    def start(self, **kwargs):
        self.get_by_id(self.selected_process_id).start()
        # logger.info(f"start: {id(self.status)}, {self.status}")

    def stop(self,  **kwargs):
        self.get_by_id(self.selected_process_id).stop()

    def pause(self,  **kwargs):
        self.get_by_id(self.selected_process_id).pause()
    
    def resume(self, **kwargs):
        self.get_by_id(self.selected_process_id).resume()

    def select(self, _id, **kwargs):
        self.process = _id
        logger.info(self.process)

    def __call__(self, process=None):
        if process: self.process = process
        return self.process

    @property
    def process(self):
        return self.store[self.selected_process_id]
    
    @process.setter
    def process(self, _id):
        self.selected_process_id = _id

    
    def load(self, _id):
        self.process.load(_id)

    def loadConfig(self, _id, user):
        return self.process.load(_id)



ProcessManager = ProcessObjectManager('process', 'operator', 'process')