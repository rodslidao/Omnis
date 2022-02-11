from bson import ObjectId
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
        del self.store[payload._id]
        self.update()

    def get(self):
        return list(map(lambda x: x.to_dict(), self.store.values()))
    
    def get_by_id(self, id):
        return self.store.get(ObjectId(id))            

    def __str__(self) -> str:
        message = "" if len(self.store) != 0 else "Nenhum objeto encontrado!"
        for k,v in self.store.items():
            message += f"{str(k)[0].upper()}{str(k)[1:]}: {v}\n"
        return message