<template>
  <v-speed-dial
    v-model="fab"
    :top="top"
    :bottom="bottom"
    :right="right"
    :left="left"
    :direction="direction"
    :open-on-hover="hover"
    :transition="transition"
    class="d-flex flex-end"
  >
    <template v-slot:activator>
      <v-btn color="primary" fab dark>
        <v-icon v-if="fab"> mdi-close </v-icon>
        <v-icon dark v-else> mdi-dots-vertical </v-icon>
      </v-btn>
    </template>
    <v-btn
      color="primary"
      class=""
      dark
      v-for="(item, index) in items"
      :key="index"
      @click="findFunction(item.method)"
    >
      <v-icon left dark>{{ item.icon }} </v-icon>{{ item.title }}
    </v-btn>
  </v-speed-dial>
</template>

<script>
import { mapMutations } from "vuex";

export default {
  name: "ActionMenuForNodes",
  props: {
    editor: Object,
  },

  data() {
    return {
      direction: "top",
      fab: false,
      fling: false,
      hover: false,
      tabs: null,
      top: false,
      right: true,
      bottom: true,
      left: false,

      transition: "slide-y-reverse-transition",
      items: [
        {
          title: "Salvar",
          icon: "mdi-content-save",
          method: "save",
        },
        { title: "Download", icon: "mdi-file-download", method: "download" },
        { title: "Upload", icon: "mdi-file-upload", method: "upload" },
      ],
    };
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),

    findFunction(name) {
      this[name]();
    },

    save() {
      console.log("save");
      console.log(this.editor.save());
      this.SEND_MESSAGE({
        type: "SAVE_NODE",
        payload: this.editor.save(),
      });
    },

    download() {
      function download(content, fileName, contentType) {
        var a = document.createElement("a");
        var file = new Blob([content], { type: contentType });
        a.href = URL.createObjectURL(file);
        a.download = fileName;
        a.click();
      }
      download(JSON.stringify(this.editor.save()), "nodes.json", "text/plain");
    },

    upload() {
      console.log("upload");
    },
  },
  out() {
    console.log(this);
  },
};
</script>

<style lang="scss">
.v-speed-dial--direction-top .v-speed-dial__list {
  flex-direction: column-reverse;
  bottom: 100%;
  align-items: flex-end;
}
</style>