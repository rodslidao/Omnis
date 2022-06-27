<template>
  <div class="p-2 pl-4 d-flex flex-column">
    <jog-buttons
      :axisDistances="axisDistances"
      @send="sendMessage"
    ></jog-buttons>
    <scale-movement @send="sendMessage"></scale-movement>
    <output-devices @send="sendMessage"></output-devices>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import OutputDevices from './OutputDevices.vue';
import JogButtons from './JogButtons.vue';
import ScaleMovement from './ScaleMovement.vue';

export default {
  components: { JogButtons, ScaleMovement, OutputDevices },
  data() {
    return {
      axisDistances: {},
    };
  },

  created() {
    this.connectToWebsocket();
  },

  methods: {
    ...mapActions('node', [
      'updateControls',
    ]),

    sendMessage(data) {
      console.log('sendMessage', data);
      if (this.WebSocket.readyState === 1) {
        console.log('Ws sended:', data);
        this.WebSocket.send(JSON.stringify(data));
      }
    },

    connectToWebsocket() {
      console.log('Starting WebSocket to WebSocket Server');
      this.WebSocket = new WebSocket(
        `ws://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_PORT}/controls/6244b0ad3a8338aceae46cf1`
      );

      this.WebSocket.onmessage = (event) => {
        // console.log(event);
        this.axisDistances = JSON.parse(event.data);
        this.updateControls(this.axisDistances);
      };

      this.WebSocket.onopen = (event) => {
        console.log(event);
        console.log('Successfully connected to the echo websocket server...');
      };
    },
  },
};
</script>
