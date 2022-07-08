<template>
  <div>
    <v-btn rounded x-large color="warning" dark>
      <span
        ><v-icon left>mdi-{{ status[actualStatus].icon }}</v-icon></span
      >
      {{ status[actualStatus].text }}
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'ProcessManagerButton',
  data() {
    return {
      localData: null,
      actualStatus: 'stopped',
    };
  },

  created() {
    this.connectToWebsocket();
  },

  computed: {
    status() {
      return {
        running: {
          icon: 'pause',
          text: this.$t('buttons.pause'),
        },
        stopped: {
          icon: 'play',
          text: this.$t('buttons.start'),
        },
        paused: {
          icon: 'play',
          text: this.$t('buttons.resume'),
        },
      };
    },
  },

  methods: {
    // sendMessage(data) {
    //   if (this.WebSocket.readyState === 1) {
    //     const editedData = {
    //       nodeId: this.node.id,
    //       nodeType: this.node.type,
    //       options: data,
    //     };
    //     this.localData = data;

    //     console.log('data', data);
    //     // this.node.getInterface('Imagem').value = 2;
    //     this.WebSocket.send(JSON.stringify(editedData));
    //     console.log('send:', editedData);
    //   }
    // },

    connectToWebsocket() {
      console.log(this.$t('alerts.wsConnecting'));
      this.WebSocket = new WebSocket(
        `ws://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_STREAMING_PORT}/process`
      );

      this.WebSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.actualStatus = data.status.toLowerCase();
      };

      this.WebSocket.onopen = (event) => {
        console.log(event);
        console.log(this.$t('alerts.wsConnectSuccess'));
      };
    },
  },
};
</script>

<style>
</style>