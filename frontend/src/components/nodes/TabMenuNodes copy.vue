<template>
  <div class="wrapper">
    <div class="menu">
      <p style="color: white">{{ lixo }}</p>
      <p style="color: white">{{ tagAdded }}</p>
      <v-btn fab small dark color="primary" @click="apollo()">
        <v-icon dark>mdi-home</v-icon>
      </v-btn>
      <v-btn fab small dark color="primary" @click="startProcess()">
        <v-icon dark>mdi-show</v-icon>
      </v-btn>

      <div>
        <v-card>
          <v-tabs
            v-model="tab"
            background-color="grey darken-3"
            center-active
            show-arrows
            dark
          >
            <v-tab v-for="(item, index) in tabList" :key="item.name">
              <v-icon
                small
                dark
                color="green accent-3"
                v-if="nameRunning == item.name"
              >
                mdi-play
              </v-icon>
              {{ +!item.saved ? item.name + '*' : item.name }}
              <v-btn
                v-if="tabList.length > 1"
                depressed
                icon
                @click="close(index)"
                small
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
      <v-tab-item v-for="item in tabList" :key="item.name">
        <!-- {{ item.content }} -->
        <NodeEditor class="nodeEditor"></NodeEditor>
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import NodeEditor from '@/components/nodes/NodeEditor.vue';
import { mapActions, mapState } from 'vuex';
import gql from 'graphql-tag';

export default {
  name: 'TabMenuNodes',

  components: {
    NodeEditor,
  },
  data() {
    return {
      tab: null,
      actualNode: null,
      length: 0,
      nameRunning: 'One',
      newTabCount: 1,

      lixo: null,
      tagAdded: {},
    };
  },

  apollo: {
    // Subscriptions
    $subscribe: {
      // When a tag is added
      tagAdded: {
        query: gql`
          subscription {
            alerts {
              title
            }
          }
        `,
        // Result hook
        // Don't forget to destructure `data`
        result({ data }) {
          console.log(data.alerts);
          this.tagAdded = data.alerts;
        },
      },
    },
  },

  computed: {
    ...mapState('node', {
      tabList: (state) => state.tabList,
      selectedTabId: (state) => state.selectedTabId,
    }),
  },

  watch: {
    length(val) {
      this.tab = val - 1;
    },

    tab() {
      this.selectTabByIndex(this.tab);
      console.log('length changed:', this.tab);
    },
  },

  methods: {
    ...mapActions('node', [
      'addTab',
      'removeTabById',
      'selectTabByIndex',
      'removeTabByIndex',
      'play',
    ]),

    async startProcess() {
      this.play();
    },

    async apollo() {
      console.time('apollo');
      const response = await this.$apollo.query({
        query: gql`
          query {
            getProcess {
              data {
                status
              }
            }
          }
        `,
      });
      console.log(this.$apollo.store);
      this.lixo = response.data.getProcess.data.status;
      console.timeEnd('apollo');
    },

    // functcion to gerate unique id based in timestamp
    generateId() {
      return new Date().getTime();
    },

    close(index) {
      console.log('aba fechada, index: ', index);
      this.removeTabByIndex(index);
    },

    add() {
      const idGenerated = this.generateId();
      const newTab = {
        name: `Tab ${this.newTabCount + 1}`,
        id: idGenerated,
        saved: false,
      };
      this.newTabCount += 1;
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
