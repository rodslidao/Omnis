from bson import ObjectId
class pin:
    def __init__(self, name, board, port, _id=None, type="slider",  icon="lightbulb", visible=True, range={"min":0, "max":255, "selected":0}, command="M106 P<pin> S<pwm>",pwm=0):
        self._id = ObjectId(_id)
        self.name = name
        self.type = type
        self.board = board
        self.port = port
        self.icon = icon
        self.visible = visible
        self.range = range
        self.command = command
    
    def activate(self):
        self.range["selected"] = self.range["max"]
        return self.__execute()
    
    def deactivate(self):
        self.range["selected"] = self.range["min"]
        return self.__execute()

    def set_value(self, pwm):
        self.range["selected"] = pwm
        return self.__execute()

    def read(self):
        return self.range["selected"]

    def __execute(self):
        return self.command.replace("<pin>", str(self.port)).replace("<pwm>", str(self.range["selected"]))
    
    def export(self):
        return {
            "name": self.name,
            "type": self.type,
            "board": self.board,
            "port": self.port,
            "icon": self.icon,
            "visible": self.visible,
            "range": self.range,
            "command": self.command,
            "_id": str(self._id)
        }