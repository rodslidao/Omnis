<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <TextEditable :text="node.name" @changeText="changeName" />
          <!-- <span class="headline">{{ nodeCopy.name }}</span> -->
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pt-4">
          <v-form v-model="valid">
            <v-col class="">
              <v-row>
                <h3 class="mb-4">
                  Selecione a camera que deseja pegar a imagem
                </h3>
                <v-select
                  :items="cameraListName"
                  :label="
                    cameraCopy === null ? 'Selecione uma placa' : cameraCopy
                  "
                  v-model="cameraCopy"
                  dense
                  outlined
                ></v-select>
              </v-row>
              <v-row>
                <!-- <v-img
                  v-if="dialog"
                  :lazy-src="require(`@/assets/img/lazy-load-parallax.jpg`)"
                  class="cameraImg"
                  alt="camera"
                  :src="UrlMaker()"
                >
                </v-img> -->
                <iframe v-if="dialog" width="560" height="315" src="https://www.youtube.com/embed/7GI_GD8LOPQ?controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
              </v-row>
            </v-col>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false" rounded>
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
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
import { mapActions } from 'vuex';
import gql from 'graphql-tag';
import TextEditable from '@/components/nodes/dialogs/TextEditable.vue';

export default {
  data: () => ({
    dialog: false,
    nodeCopy: null,
    axisListCopy: null,
    cameraCopy: null,
    selectedCamera: null,
    cameraListName: [],
    cameraList: [],
    Description: '',

    rules: {
      required: (value) => !!value || 'Required.',
      positive: (value) => value > 0 || 'Positive number required.',
    },
    valid: false,
    type: null,
  }),
  components: {
    TextEditable,
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

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    save() {
      this.node.setOptionValue('selectedCamera', this.cameraCopy);
      this.saveNodeConfig(this.node.id);
      // this.$store.commit('saveNodeConfig', this.node.id);
      this.dialog = false;
      this.init();
    },

    async getCamera() {
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
      this.cameraList = response.data.getNodeInfo.data.options;
      // make a list of camera name from the response
      response.data.getNodeInfo.data.options.forEach((item) => {
        this.cameraListName.push(item.name);
      }, this);
    },

    async init() {
      this.nodeCopy = { ...this.node };
      this.cameraCopy = this.node.getOptionValue('selectedCamera');
      await this.getCamera();
    },

    getCameraIdByName() {
      let cameraId = null;
      this.cameraList.forEach((item) => {
        if (item.name === this.cameraCopy) {
          // eslint-disable-next-line no-underscore-dangle
          cameraId = item._id;
        }
      }, this);
      return cameraId;
    },

    UrlMaker() {
      // const url = `http://${process.env.VUE_APP_URL_API_IP}:${
      //   process.env.VUE_APP_URL_API_STREAMING_PORT
      // }/videos/${this.getCameraIdByName()}?${
      //   Math.floor(Math.random() * (1000 - 1 + 1)) + 1
      // }`;
      const url = `http://${process.env.VUE_APP_URL_API_IP}:${
        process.env.VUE_APP_URL_API_STREAMING_PORT
      }/videos/${this.getCameraIdByName()}`;
      console.log(url);
      return url;
    },

    changeName(data) {
      console.log(data);
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
</style>
