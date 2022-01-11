<template>
  <div class="wrapper">
    <div class="menu">
      <div>
        <v-card>
          <v-tabs
            v-model="tab"
            background-color="grey darken-3"
            center-active
            show-arrows
            dark
          >
            <v-tab v-for="(item, index) in tabList" :key="item.sketchName">
              <v-icon
                small
                dark
                color="green accent-3"
                v-if="sketchNameRunning == item.sketchName"
              >
                mdi-play
              </v-icon>
              {{ +!item.saved ? item.sketchName + "*" : item.sketchName }}
              <v-btn v-if="tabList.length > 1" depressed icon @click="close(index)" small
                ><v-icon small dark> mdi-close </v-icon></v-btn
              >
            </v-tab>
          </v-tabs>
        </v-card>
        <div class="moreButton">
          <v-btn fab small dark color="primary" @click="add()">
            <v-icon dark>mdi-plus</v-icon>
          </v-btn>
        </div>
      </div>
    </div>
    <v-tabs-items v-model="tab">
      <v-tab-item v-for="item in tabList" :key="item.sketchName">
        <!-- {{ item.content }} -->
        <NodeEditor class="nodeEditor"></NodeEditor>
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import NodeEditor from "@/components/nodes/NodeEditor.vue";
import { mapActions, mapState } from "vuex";

export default {
  name: "TabMenuNodes",

  components: {
    NodeEditor,
  },
  data() {
    return {
      tab: null,
      actualNode: null,
      length: 0,
      sketchNameRunning: "One",
      newTabCount: 1,
    };
  },

  computed: {
    ...mapState("node", {
      tabList: (state) => state.tabList,
      selectedTabId: (state) => state.selectedTabId,
    }),
  },

  watch: {
     length (val) {
        this.tab = val - 1
    },

    tab() {
      this.selectTabByIndex(this.tab)  
    },
  },

  methods: {
    ...mapActions("node", [
      "addTab",
      "removeTabById",
      "selectTabByIndex",
      'removeTabByIndex',
    ]),

    //functcion to gerate unique id based in timestamp
    generateId() {
      return new Date().getTime();
    },

    close(index) {
      console.log("aba fechada, index: ", index);
      this.removeTabByIndex(index);
    },

    add() {
      let idGenerated = this.generateId();
      let newTab = {
        sketchName: "Tab " + (this.newTabCount + 1),
        id: idGenerated,
        saved: false,
      };
      this.newTabCount += 1
      this.lastSelectedTabId = idGenerated;

      this.addTab(newTab);

      this.length = this.tabList.length;
    },
  },
};
</script>

<style lang="scss">
.wrapper {
  display: flex;
  position: relative;
  width: 100%;

  .menu {

    z-index: 2;
    position: absolute;
    width: 100%;
    margin-top: 3em;

    > div {
      margin: 1em 1em 0 3em;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .moreButton {
      padding: 0 2em 0 1em;
    }
  }

  .nodeEditor {
    width: 100vw;
    height: 100vh;
    position: absolute;
  }
}
</style>