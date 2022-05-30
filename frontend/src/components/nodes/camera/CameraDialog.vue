<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="600px">
      <v-card dark>
        <v-card-title>
          <TextEditable :text="node.name" @changeText="changeName" />
          <!-- <span class="headline">{{ nodeCopy.name }}</span> -->
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pt-4">
          <v-form ref="title" v-model="valid">
            <v-col class="">
              <NodeConfigTitle
                title="Camera"
                description="Selecione a camera que deseja pegar a imagem."
              >
                <div>
                  <v-select
                    :items="getCameras ? getCameras.data : []"
                    v-model="selectedCamera"
                    item-text="name"
                    return-object
                    dense
                    :loading="!getCameras"
                    :rules="requiredRules"
                    required
                  ></v-select>
                </div>
              </NodeConfigTitle>
              <v-row>
                <v-col>
                  <!-- <v-progress-linear
                    v-on="delay(8000)"
                    v-if="selectedCamera"
                    v-show="!frameLoaded"
                    indeterminate
                    rounded
                    height="4"
                  ></v-progress-linear> -->
                  <v-img
                    v-if="selectedCamera"
                    :lazy-src="require(`@/assets/img/estribo-pattern-low.jpg`)"
                    class="cameraImg"
                    alt="camera"
                    :src="UrlMaker()"
                  >
                  </v-img>
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
import { mapActions } from 'vuex';
import NodeConfigTitle from '@/components/nodes/NodeConfigTitle.vue';
import gql from 'graphql-tag';
// import { getNodeInfo } from '@/graphql/nodes/GetInfos.js';
import TextEditable from '@/components/nodes/dialogs/TextEditable.vue';

const GET_CAMERAS = gql`
  query {
    getCameras {
      data {
        _id
        name
      }
    }
  }
`;

export default {
  data: () => ({
    dialog: false,
    nodeCopy: null,
    cameraCopy: [],
    selectedCamera: null,
    cameraList: [],
    Description: '',
    cameraLoading: true,
    frameLoaded: false,
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
    // 'vue-webrtc': WebRTC,
  },

  props: ['option', 'node', 'value'],

  created() {
    this.init();
    EventBus.$on('OPEN_SETTINGS', (nodeId) => {
      if (nodeId === this.node.id) {
        console.log(this.dialog);
        this.dialog = true;
        this.init();
      }
    });
  },

  watch: {
    getCameras() {
      if (this.cameraCopy) {
        this.selectedCamera = this.this.cameraCopy;
      } else {
        // eslint-disable-next-line prefer-destructuring
        this.selectedCamera = this.getCameras.data[0];
      }
    },
  },

  apollo: {
    getCameras: {
      query: GET_CAMERAS,
      fetchPolicy: 'network-only',
      // nextFetchPolicy: 'network-only',
    },
  },

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    save() {
      this.node.setOptionValue('camera', this.selectedCamera);
      this.node.getInterface('Imagem').value = this.selectedCamera;
      console.log('camera define ', this.node.getInterface('Imagem').value);
      this.saveNodeConfig(this.node.id);
      // this.$store.commit('saveNodeConfig', this.node.id);
      this.dialog = false;
      this.init();
    },

    close() {
      this.dialog = false;
    },

    async init() {
      this.nodeCopy = { ...this.node };
      this.cameraCopy = this.node.getOptionValue('camera');
    },

    // eslint-disable-next-line consistent-return
    UrlMaker() {
      const { id } = this.node;
      const url = `http://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_STREAMING_PORT}/videos/${id}`;
      if (id !== null) {
        return url;
      }
      console.log(url);
    },

    changeName(data) {
      this.node.name = data;
      this.saveNodeConfig(this.node.id);
    },
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
