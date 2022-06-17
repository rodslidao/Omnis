<template>
  <div class="p-2 pl-4 d-flex flex-column">
    <jog-buttons @send="sendMessage"></jog-buttons>
    <scale-movement @send="sendMessage"></scale-movement>
    <output-devices @send="sendMessage"></output-devices>
  </div>
</template>

<script>
import OutputDevices from './OutputDevices.vue';
import JogButtons from './JogButtons.vue';
import ScaleMovement from './ScaleMovement.vue';

export default {
  components: { JogButtons, ScaleMovement, OutputDevices },
  data() {
    return {};
  },

  created() {
    this.connectToWebsocket();
  },

  methods: {
    sendMessage(data) {
      if (this.WebSocket.readyState === 1) {
        console.log('Ws sended:', data);
        this.WebSocket.send(JSON.stringify(data));
      }
    },

    connectToWebsocket() {
      console.log('Starting WebSocket to WebSocket Server');
      this.WebSocket = new WebSocket(
        `ws://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_PORT}/controls`
      );

      this.WebSocket.onmessage = (event) => {
        console.log(event);
      };

      this.WebSocket.onopen = (event) => {
        console.log(event);
        console.log('Successfully connected to the echo websocket server...');
      };
    },
  },
};
</script>
