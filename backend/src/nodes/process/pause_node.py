from src.nodes.process.process_node import ProcessNode

NODE_TYPE = "PauseNode"

class PauseNode(ProcessNode):
    def __init__(self, name, id, options, output_connections, input_connections):
        self.options = options
        self.options["action"] = "pause"
        self.options["auto_run"] = False
        super().__init__(name, id, options, output_connections, input_connections)

    # def execute(self, message):
    #     super().execute(message)
    #     while not self.process.is_paused():
    #         if self.process.is_stopped():
    #             return
    #     else:
    #         self.on("Saida", message.payload)