<template>
  <div class="warpper">
    <h4>{{ value }}</h4>
    <!-- <img src="https://zudesign.com.br/images/logo.svg" alt="alternative" /> -->
    <v-img
      :lazy-src="require(`@/assets/img/lazy-load-parallax.jpg`)"
      class="cameraImg"
      alt="camera"
      :src="`http://${connection.ip}:${connection.portStream}/${stringUrl}?${
        Math.floor(Math.random() * (1000 - 1 + 1)) + 1
      }`"
    >
    </v-img>
    <!-- <p>{{ node.id }}</p> -->
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  data: () => ({
    nodeCopy: null,
    valueCopy: null,
    stringUrl: "video_feed/camera0",
  }),

  props: ["option", "node", "value"],

  mounted() {
    console.log("created");
  },

  computed: {
    ...mapState("node", {
      connection: (state) => state.connection,
    }),
  },

  methods: {
    makeUrl(filter, cameraId) {
      this.stringUrl = "";

      if (filter) {
        this.stringUrl = filter + "/" + cameraId;
      } else {
        this.stringUrl = this.Normal + "/" + cameraId;
      }
      console.log(this.stringUrl);
    },

    updateURL() {
      this.stringUrl = " ";
      console.log(this.stringUrl);
      if (this.filter) {
        this.stringUrl = this.selectedFilter + "/" + this.selectedCamera;
      } else {
        this.stringUrl = "normal" + "/" + this.selectedCamera;
      }
      console.log(this.stringUrl);
    },
  },
};
</script>

<style lang="scss" scoped>
.warpper {
  img {
    width: 100%;
    border-radius: 5px;
  }
}
</style>