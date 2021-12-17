export const socket_events = {
    my_response(data) {
      console.log("recebi:", data);
    }
  };
  
export var socket_actions = {
    click: function (data) {
        this.$socket.emit("custom_click", data);
        console.log("data:", data);
      },
    call_function: function (function_name) {
      console.log("socket:", this.$socket);
      console.log("data:", function_name);
      this.$socket.emit("call_function", function_name);
      },
      start_updates : function () {
        this.$socket.emit("start_updates");
        console.log("data:", "start_updates");
      }
}