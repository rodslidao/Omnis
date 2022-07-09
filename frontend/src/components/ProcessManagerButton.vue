<template>
  <div>
    <v-btn
      rounded
      x-large
      color="warning"
      dark
      class="mr-3"
      @click="sendCommand(status[actualStatus].command)"
    >
      <span
        ><v-icon left>mdi-{{ status[actualStatus].icon }}</v-icon></span
      >
      {{ status[actualStatus].text }}
    </v-btn>
    <v-btn
    v-if="actualStatus != 'stopped'"
      rounded
      x-large
      color="error"
      dark
      @click="sendCommand(stop.command)"
    >
      <span
        ><v-icon left>mdi-{{ stop.icon }}</v-icon></span
      >
      {{ stop.text }}
    </v-btn>
  </div>
</template>

<script>
import gql from 'graphql-tag';

const START = gql`
  mutation START {
    start_process
  }
`;

const PAUSE = gql`
  mutation PAUSE {
    pause_process
  }
`;

const RESUME = gql`
  mutation RESUME {
    resume_process
  }
`;

const STOP = gql`
  mutation STOP {
    stop_process
  }
`;

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
          command: PAUSE,
        },
        stopped: {
          icon: 'play',
          text: this.$t('buttons.start'),
          command: START,
        },
        paused: {
          icon: 'play',
          text: this.$t('buttons.resume'),
          command: RESUME,
        },
      };
    },
    stop() {
      return {
        icon: 'stop',
        text: this.$t('buttons.stop'),
        command: STOP,
      };
    },
  },

  methods: {
    async sendCommand(command) {
      await this.$apollo
        .mutate({
          mutation: command,
        })

        .then(() => {
          this.$alertFeedback(this.$t('alerts.updateMatrixSuccess'), 'success');
        })

        .catch((error) => {
          this.$alertFeedback(
            this.$t('alerts.updateMatrixSuccess'),
            'error',
            error
          );
          // We restore the initial user input
        });
    },

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