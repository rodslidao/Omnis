<template>
  <div class="wrapper">
    <div class="menu">
      <div>
        <v-card :loading="isLoading">
          <v-tabs
            v-model="tab"
            background-color="primary"
            center-active
            show-arrows
            dark
          >
            <v-tab v-for="(item, index) in items" :key="item.tab">
              <v-icon
                small
                dark
                color="green accent-3"
                v-if="tabNameRunning == item.tabName"
              >
                mdi-play
              </v-icon>
              {{ +!item.saved ? item.tabName + "*" : item.tabName }}
              <v-btn depressed icon @click="close(index)" small
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
      <v-tab-item v-for="item in items" :key="item.tabName">
        <!-- {{ item.content }} -->
        <NodeEditor @isLoading="getTabLoading" class="nodeEditor"></NodeEditor>
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import NodeEditor from "@/components/nodes/NodeEditor.vue";

export default {
  name: "TabMenuNodes",
  
  data() {
    return {
      tab: null,
      isLoading: false,
      length: 0,
      more: ["News", "Maps", "Books", "Flights", "Apps"],
      tabNameRunning: "Two",
      items: [
        { tabName: "adwa", content: "Tab 1 Content", saved: true },
        { tabName: "Two", content: "Tab 2 Content", saved: true },
        { tabName: "Three", content: "Tab 3 Content", saved: true },
        { tabName: "Four", content: "Tab 4 Content", saved: true },
      ],
    };
  },
  components: {
    NodeEditor,
  },
  
  watch: {
    length(val) {
      this.tab = val - 1;
    },
  },

  methods: {

    close(item) {
      this.items.splice(item, 1);
      this.tab = this.items.length - 1;
    },

    add() {
      this.items.push({
        tabName: "Tab " + (this.items.length + 1),
        content: "Tab " + (this.items.length + 1) + " Content",
        saved: false,
      });
      this.length = this.items.length;
    },

    getTabLoading(value){
            console.log(value); // Raja Tamil
            this.isLoading = value;
    }
  },
};
</script>

<style lang="scss">
.wrapper {
  display: flex;
  // flex-direction: column;
  position: relative;
  width: 100%;

  .menu {
    // justify-content: center;
    // align-items: center;
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