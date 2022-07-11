<template>
  <div>
    <div class="text-center">
      <v-dialog v-model="dialogStart" width="600">
        <v-card>
          <v-card-title class="text-h4 lighten-2 d-flex flex-nowrap">
            <v-btn v-if="step2" icon @click="(step1 = true), (step2 = false)"
              ><v-icon>mdi-arrow-left</v-icon>
            </v-btn>
            <div class="ml-2">
              {{
                step1 ? $t('dialogs.selectObject') : $t('dialogs.selectMatrix')
              }}
            </div>
          </v-card-title>
          <v-card-text max-height="50vh">
            <v-card
              link
              v-for="(item, index) in step1 ? get_object_list : get_matrix_list"
              :key="index"
              class="d-flex my-2"
              @click="selectedMatrix(item)"
            >
              <div class="viewer">
                <!-- <matrix-viewer
                  edit="distTotalX"
                  v-if="item.slots"
                  :slots="item.slots"
                  :subdivisions="item.subdivisions"
                ></matrix-viewer> -->
              </div>
              <div class="pl-4 pr-4 my-4">
                <span
                  class="text-subtitle text-capitalize font-weight-bold"
                  my-2
                  >{{ item.name }}</span
                >
                <div class="text-subtitle-2">{{ item.description }}</div>
              </div>
            </v-card>
          </v-card-text>
        </v-card>
      </v-dialog>
    </div>
    <v-btn
      rounded
      x-large
      color="warning"
      dark
      class="mr-3"
      @click="(dialogStart = true), (step1 = true)"
    >
      <span
        ><v-icon left>mdi-{{ status[actualStatus].icon }}</v-icon></span
      >
      {{ status[actualStatus].text }}
    </v-btn>
    <!-- <v-btn
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
    </v-btn> -->
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
import MatrixViewer from './node/nodes/matrix/MatrixViewer.vue';

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

const LIST_PROCESS = gql`
  query LIST_PROCESS {
    get_process_list {
      _id
      name
      object
    }
  }
`;

const LIST_OBJECT = gql`
  query LIST_OBJECT {
    get_object_list {
      _id
      name
      variable
    }
  }
`;

const LIST_MATRIX = gql`
  query LIST_MATRIX {
    get_matrix_list {
      _id
      name
      variable
    }
  }
`;

export default {
  components: { MatrixViewer },
  name: 'ProcessManagerButton',
  data() {
    return {
      localData: null,
      actualStatus: 'stopped',
      dialogStart: false,
      filteredList: [],
      step1: false,
      step2: false,
    };
  },

  created() {
    this.connectToWebsocket();
  },

  apollo: {
    get_process_list: LIST_PROCESS,
    get_object_list: LIST_OBJECT,
    get_matrix_list: LIST_MATRIX,
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
    selectedMatrix(item) {
      this.step1 = false;
      this.step2 = true;

      console.log(this.get_process_list);
    },

    selectedObject(item) {
      this.step1 = false;
      this.step2 = false;
    },

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
