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
                <v-select
                  :items="cameraList"
                  v-model="selectedCamera"
                  item-text="name"
                  dense
                  :loading="cameraLoading"
                ></v-select>
              </NodeConfigTitle>
              <!-- <v-row>
              <v-col
                ><div class="text-h6 text-uppercase text--darken--primary">Camera</div>
                <p>Selecione a camera que deseja pegar a imagem</p></v-col
              >
              <v-col>
                 <v-select
                  :items="cameraListName"
                  :label="
                    cameraCopy === null ? 'Selecione uma camera' : cameraCopy
                  "
                  v-model="cameraCopy"
                  dense

                ></v-select>
              </v-col>
            </v-row> -->
              <v-row>
                <v-col>
                  <!-- <v-img
                  v-if="dialog"
                  :lazy-src="require(`@/assets/img/lazy-load-parallax.jpg`)"
                  class="cameraImg"
                  alt="camera"
                  :src="imgUrl"
                >
                </v-img> -->
                  <v-progress-linear
                    v-on="delay(8000)"
                    v-if="selectedCamera"
                    v-show="!frameLoaded"
                    indeterminate
                    rounded
                    height="4"
                  ></v-progress-linear>
                  <iframe
                    v-if="selectedCamera"
                    v-show="frameLoaded"
                    :src="UrlMaker()"
                  >
                  </iframe>

                  <!-- <video
                  id="video"
                  class="embed-responsive-item"
                  autoplay="true"
                  playsinline="true"
                  controls="true"
                  muted="true"
                ></video> -->
                  <!-- <v-video
                  v-if="dialog"
                  class="cameraImg"
                  alt="camera"
                  :src="UrlMaker()"
                >
                </v-video> -->
                  <!-- <iframe v-if="dialog" width="560" height="315" src="https://www.youtube.com/embed/7GI_GD8LOPQ?controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> -->
                  <!-- começas aqui -->

                  <!-- termina aqui -->
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
import TextEditable from '@/components/nodes/dialogs/TextEditable.vue';

export default {
  data: () => ({
    dialog: false,
    nodeCopy: null,
    axisListCopy: null,
    cameraCopy: null,
    selectedCamera: null,
    cameraList: [],
    Description: '',
    cameraLoading: true,
    frameLoaded: false,

    rules: {
      required: (value) => !!value || 'Required.',
      positive: (value) => value > 0 || 'Positive number required.',
    },
    valid: false,
    type: null,
    imgUrl: '',
    cameraId: '',

    // img: null,
    // roomId: 'public-room-v3',
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

  mounted() {
    // setInterval(() => {
    //   if (!this.cameraId) {
    //     this.cameraId = this.getCameraIdByName();
    //     console.log('adwadad');
    //   }
    //   const url = `http://${process.env.VUE_APP_URL_API_IP}:${
    //     process.env.VUE_APP_URL_API_STREAMING_PORT
    //   }/videos/${this.cameraId}?${
    //     Math.floor(Math.random() * (1000 - 1 + 1)) + 1
    //   }`;
    //   console.log(this.imgUrl);
    //   this.imgUrl = url;
    // }, 2000);
  },

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    save() {
      this.node.setOptionValue('camera', this.getSelectedCameraObj());

      this.saveNodeConfig(this.node.id);
      // this.$store.commit('saveNodeConfig', this.node.id);
      this.dialog = false;

      this.init();
    },

    close() {
      this.dialog = false;
      // this.$destroy();

      // remove the element from the DOM
      // this.$el.parentNode.removeChild(this.$el);
    },

    async getCamera() {
      this.cameraLoading = true;
      const response = await this.$apollo.query({
        query: gql`
          query {
            getNodeInfo(node_type: "CAMERA") {
              data {
                options
              }
            }
          }
        `,
      });
      // console.log(this.$apollo.store);
      this.cameraList = [];
      this.cameraList = response.data.getNodeInfo.data.options;
      console.log(this.cameraList);
      this.cameraLoading = false;
      // make a list of camera name from the response
      // response.data.getNodeInfo.data.options.forEach((item) => {
      //   this.cameraListName.push(item.name);
      // }, this);
    },

    async init() {
      this.nodeCopy = { ...this.node };
      await this.getCamera();
    },

    delay(time) {
      setTimeout(() => {
        this.frameLoaded = true;
      }, time);
    },

    getSelectedCameraObj() {
      const selectedCameraObj = this.cameraList.find(
        (obj) => obj.name === this.selectedCamera
      );
      console.log(selectedCameraObj);
      return selectedCameraObj;
    },

    UrlMaker() {
      // const url = `http://${process.env.VUE_APP_URL_API_IP}:${
      //   process.env.VUE_APP_URL_API_STREAMING_PORT
      // }/videos/${this.getSelectedCameraObj()}?${
      //   Math.floor(Math.random() * (1000 - 1 + 1)) + 1
      // }`;

      // fetch(
      //   `http://${process.env.VUE_APP_URL_API_IP}:${
      //     process.env.VUE_APP_URL_API_PORT
      //   }/videos/${this.getSelectedCameraObj()}`
      // );
      const url = `http://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_STREAMING_PORT}`;

      // navigator.sendBeacon(`${url}/close_connection`);
      const { id } = this.getSelectedCameraObj();
      if (id !== null) {
        navigator.sendBeacon(
          `http://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_PORT}/videos/${id}`
        );
      }
      console.log(url);

      return url;
    },

    changeName(data) {
      this.node.name = data;
      this.saveNodeConfig(this.node.id);
    },

    // setFrameHeight() {

    //   // set the height of the iframe as
    //   // the height of the iframe content
    //   frame.style.height = `${frame.contentWindow.document.body.scrollHeight}px`;

    //   // set the width of the iframe as the
    //   // width of the iframe content
    //   frame.style.width = `${frame.contentWindow.document.body.scrollWidth}px`;
    // },
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
