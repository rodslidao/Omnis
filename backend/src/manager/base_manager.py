
from bson import ObjectId
from api import logger, exception, for_all_methods
@for_all_methods(exception(logger))
class BaseManager():
    def __init__(self) -> None:
        self.store = {}
        self.queues =[]
    
    def add(self, payload):
        self.store[payload._id] = payload
        self.update()
    
    def update(self):
        for queue in self.queues:
            for payload in self.store.values():
                queue.put_nowait(payload.to_dict())

    def remove(self, payload):
        self.store.pop(payload._id, None)
        self.update()

    def get(self):
        return list(map(lambda x: x.to_dict(), self.store.values()))
    
    def get_ids(self):
        return list(str(self.store.keys()))

    def get_info(self):
        
        return [{'name':V.name, 'id':str(V._id)} for V in self.store.values()]

    def get_by_id(self, id):
        if len(id.encode('utf-8')) >= 12:
            _ = ObjectId(id)
        else:
            _ = None
        return self.store.get(_)            

    def __str__(self) -> str:
        message = "" if len(self.store) != 0 else "Nenhum objeto encontrado!"
        for k,v in self.store.items():
            message += f"{str(k)[0].upper()}{str(k)[1:]}: {v}\n"
        return message