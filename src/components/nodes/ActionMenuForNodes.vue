<template>
  <div class="menuList">
    <v-btn class="button" color="primary" fab dark small @click="play">
      <v-icon> mdi-play </v-icon>
    </v-btn>
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
  </div>
</template>

<script>
import { mapState, mapActions, mapMutations,mapGetters } from "vuex";

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

  computed: {
    ...mapState("node", {
      tabList: (state) => state.tabList,
      selectedTabId: (state) => state.selectedTabId,
    }),
     ...mapGetters('node', [
    'selectedTabName',
    'selectedTabObject' // -> this.getTabName
  ])
},

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),
    ...mapActions("node", [
      "updateTabById",
      "removeTabById",
    ]),
    ...mapActions([
      "sendMessage",
    ]),

    play(){
      this.sendMessage({'command':'process_playCicle', 'args':this.editor.save()})
      },

    findFunction(name) {
      this[name]();
    },

    save() {
      let editedNode = this.editor.save();
            console.log(this.selectedTabId);
            console.log(this.getSelectedTabName);

      editedNode["id"] = this.selectedTabId;

      editedNode["sketchName"] = this.getSelectedTabName;
      editedNode["saved"] = false;

      this.updateTabById(editedNode);

      console.log(" :salvo com sucesso!'");
      console.log(this.editor.save());
      this.SEND_MESSAGE({
        type: "SAVE_NODE",
        payload: editedNode,
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

    // play() {
    //   this.$store.dispatch("play");
    // },
  },
  out() {
    console.log(this);
  },
};
</script>

<style lang="scss">
.menuList {
  display: flex;
  flex-direction: row;
  align-items: center;

  .button {
    right: 25px;
    bottom: 16px;
  }
  .v-speed-dial--direction-top .v-speed-dial__list {
    flex-direction: column-reverse;
    bottom: 100%;
    align-items: flex-end;
  }
}
</style>