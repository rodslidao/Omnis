<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="600px">
      <v-card dark>
        <v-card-title>
          <TextEditable :text="node.name" @changeText="changeName" />
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pt-4">
          <v-form ref="title" v-model="valid">
            <v-col class="">
              <NodeConfigTitle
                title="Cores"
                description="Selecione as duas cores que serão filtradas,
                lembrando que o filtro pegara todo o intervalo entre as duas cores.
                Digamos que você coloque preto e branco, o filtro pegara o preto passando
                pelo cinza até chegar no branco"
                no-content
              >
              </NodeConfigTitle>
              <!-- <v-select
                @click="getCamera()"
                :items="cameraList"
                v-model="selectedCamera"
                item-text="name"
                return-object
                dense
                :loading="cameraLoading"
              ></v-select> -->
              <ColorPikerHSV
                v-if="dialog"
                @colors="sendMessage"
              ></ColorPikerHSV>
              <v-row>
                <v-col>
                  <v-progress-linear
                    v-on="delay(8000)"
                    v-if="selectedCamera"
                    v-show="!frameLoaded"
                    indeterminate
                    rounded
                    height="4"
                  ></v-progress-linear>
                  <iframe :src="UrlMaker()"> </iframe>
                </v-col>
              </v-row>
            </v-col>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="close()" rounded large>
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
            large
            :disabled="!valid"
            text
            @click="save"
            rounded
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import EventBus from '@/event-bus';
// import WebRTC from 'vue-webrtc';
import { mapActions, mapState } from 'vuex';
import NodeConfigTitle from '@/components/nodes/NodeConfigTitle.vue';
import gql from 'graphql-tag';
import TextEditable from '@/components/nodes/dialogs/TextEditable.vue';
import ColorPikerHSV from '@/components/nodes/filters/hsv/ColorPikerHSV.vue';

export default {
  data: () => ({
    dialog: false,
    nodeCopy: null,
    selectedCamera: null,
    cameraList: [],
    cameraCopy: [],
    Description: '',
    cameraLoading: true,
    frameLoaded: false,
    WebSocket: null,
    isConnected: false,
    lower: 0,
    upper: 0,

    requiredRules: [(v) => !!v || 'Campo não pode ficar em branco'],

    rules: {
      required: (value) => !!value || 'Required.',
      positive: (value) => value > 0 || 'Positive number required.',
    },
    valid: false,
    type: null,
    imgUrl: '',
    cameraId: '',
  }),
  components: {
    TextEditable,
    NodeConfigTitle,
    ColorPikerHSV,
  },

  props: ['option', 'node', 'value'],

  created() {
    this.connectToWebsocket();
    this.init();
    EventBus.$on('OPEN_SETTINGS', (nodeId) => {
      if (nodeId === this.node.id) {
        console.log(this.dialog);
        this.dialog = true;
        this.init();
      }
    });
  },

  computed: {
    ...mapState('node', {
      editor: (state) => state.editor,
    }),
  },

  mounted() {},

  apollo: {
    getStreamNodeId: {
      query: gql`
        query {
          getStreamNodeId
        }
      `,
    },
  },

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    init() {
      this.nodeCopy = { ...this.node };
      this.cameraCopy = this.node.getOptionValue('camera');

      // await this.getCamera();
    },

    // async getCamera() {
    //   this.cameraLoading = true;
    //   const response = await this.$apollo.query({
    //     query: gql`
    //       query {
    //         getNodeInfo(node_type: "CameraNode") {
    //           data {
    //             options
    //           }
    //         }
    //       }
    //     `,
    //   });
    //   // console.log(this.$apollo.store);

    //   this.cameraList = [];
    //   this.cameraList.push(...response.data.getNodeInfo.data.options);

    //   if (!this.cameraCopy) {
    //     this.cameraList.push(this.cameraCopy);
    //     this.selectedCamera = this.cameraCopy;
    //   }
    //   console.log(this.cameraList);

    //   this.cameraLoading = false;
    // },

    sendMessage(data) {
      if (this.WebSocket.readyState === 1) {
        const editedData = {
          nodeId: this.node.id,
          nodeType: this.node.type,
          options: this.optionsMaker(data),
        };

        this.lower = data.rgb.lower;
        this.upper = data.rgb.upper;

        console.log('data', data);
        // this.node.getInterface('Imagem').value = 2;
        this.WebSocket.send(JSON.stringify(editedData));
        console.log('send:', editedData);
      }
    },

    connectToWebsocket() {
      console.log('Starting WebSocket to WebSocket Server');
      this.WebSocket = new WebSocket(
        `ws://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_PORT}/ws`
      );

      this.WebSocket.onmessage = (event) => {
        console.log(event);
      };

      this.WebSocket.onopen = (event) => {
        console.log(event);
        console.log('Successfully connected to the echo websocket server...');
      };
    },

    save() {
      this.node.setOptionValue('camera', this.selectedCamera);
      this.node.setOptionValue('lower', this.lower);
      this.node.setOptionValue('upper', this.upper);
      this.saveNodeConfig(this.node.id);
      // this.$store.commit('saveNodeConfig', this.node.id);
      this.dialog = false;
      this.init();
    },

    close() {
      this.dialog = false;
    },

    getNodeInfos() {
      let a = null;
      this.editor.save().nodes.forEach((node) => {
        if (node.id === this.node.id) {
          a = node;
        }
      });
      return a;
    },

    delay(time) {
      setTimeout(() => {
        this.frameLoaded = true;
      }, time);
    },

    optionsMaker(data) {
      const options = [
        ['lower', data.rgb.lower],
        ['upper', data.rgb.upper],
      ];
      return options;
    },

    // eslint-disable-next-line consistent-return
    UrlMaker() {
      const url = `http://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_STREAMING_PORT}`;

      const { id } = this.node;
      if (id !== null) {
        navigator.sendBeacon(
          `http://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_PORT}/videos/${id}`
        );
        console.log('url', url);
        return url;
      }

      console.log(url);
    },

    changeName(data) {
      this.node.name = data;
      this.saveNodeConfig(this.node.id);
    },
  },

  beforeDestroy() {
    this.WebSocket.close();
    console.log('Closed WebSocket to WebSocket Server');
  },
};
</script>
<style lang="scss" scoped>
img {
  width: 100%;
  border-radius: 20px;
}
iframe {
  width: 100%;
  border: none;
  // height: 414px;
  border-radius: 7px;
  aspect-ratio: 4/3;
  overflow: hidden;
}
video {
  border: 1px solid salmon;
}
</style>
