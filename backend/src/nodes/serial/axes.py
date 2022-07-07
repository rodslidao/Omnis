from threading import Event
class axis:
    def __init__(self, _id, name, board, step=1):
        self._id = _id
        self.name = name
        self.step = step
        self.position = 0
        self.target = 0
        self.moving = Event()
        self.board = board
    
    def is_moving(self):
        return self.moving.is_set()

    def move(self, target):
        self.position = target if target > 0 else 0
        self.moving.set()
        return self.__str__()

    def __call__(self):
        return(self.name, self.position)

    def stop(self):
        self.moving.clear()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def export(self):
        return {
            "name": self.name,
            "step": self.step,
            "position": self.position,
            "target": self.target,
            "_id": self._id
        }
    
    def info(self):
        return {self.name: self.position}
    
    def __str__(self) -> str:
        return f"{self.name}{self.position}"
    
    def __repr__(self) -> str:
        return str(self)