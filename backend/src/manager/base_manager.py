class BaseManager():
    def __init__(self) -> None:
        self.store = {}
    
    def add(self, payload):
        self.store[payload._id] = payload
    
    def remove(self, payload):
        del self.store[payload._id]
    
    def get(self):
        return self.store
    
    def get_by_id(self, id):
        return self.store.get(id)

    def __str__(self) -> str:
        message = "" if len(self.store) != 0 else "Nenhum objeto encontrado!"
        for k,v in self.store.items():
            message += f"{str(k)[0].upper()}{str(k)[1:]}: {v}\n"
        return message

