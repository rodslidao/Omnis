<template>
  <div class="content">
    <v-tabs align-with-title grow v-model="tab">
      <v-tab
        class="tab-item d-flex justify-space-between"
        @contextmenu="show"
        v-for="(item, index) in tabList"
        :key="item.sketchName"
        @click="selectTab(index)"
        @click.middle="close(index)"
        @click.right="contextMenuSelectedTabIndex = index"
      >
        <div>
          <v-icon
            small
            dark
            color="green accent-3"
            v-if="sketchNameRunning == item.sketchName"
          >
            mdi-play
          </v-icon>
          {{ +!item.saved ? item.sketchName + '*' : item.sketchName }}
        </div>

        <!-- dropdown -->
        <v-menu
          transition="slide-x-transition"
          v-model="showMenu"
          bottom
          right
          :position-y="y"
          :position-x="x"
        >
          <v-list>
            <v-list-item v-for="(item, index) in items" :key="index" link>
              <v-list-item-title @click="item.function"
                ><v-icon class="mr-5">mdi-{{ item.btnIcon }}</v-icon
                >{{ item.title }}</v-list-item-title
              >
            </v-list-item>
          </v-list>
        </v-menu>

        <v-btn depressed icon small class="context-menu-btn">
          <v-icon small dark> mdi-dots-vertical </v-icon></v-btn
        >
        <v-btn
          v-if="tabList.length > 1"
          depressed
          icon
          @click="close(index)"
          small
        >
          <v-icon class="align-self-end" small dark> mdi-close </v-icon></v-btn
        >
      </v-tab>
      <v-btn class="add-tab" depressed icon @click="add()" small
        ><v-icon small dark> mdi-plus </v-icon></v-btn
      >
    </v-tabs>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import gql from 'graphql-tag';

export default {
  name: 'TabMenuNodes',

  data() {
    return {
      tab: null,
      actualNode: null,
      length: 0,
      sketchNameRunning: 'One',
      newTabCount: 0,
      lixo: null,
      tagAdded: {},
      contextMenuSelectedTabIndex: null,

      showMenu: false,
      x: 0,
      y: 0,
      items: [
        {
          title: 'Duplicar',
          btnIcon: 'content-duplicate',
          function: this.duplicate,
        },
        { title: 'Renomear', btnIcon: 'form-textbox', function: this.add },
        { title: 'Remove', btnIcon: 'delete-outline', function: this.add },
      ],
    };
  },

  computed: {
    ...mapState('node', {
      tabList: (state) => state.tabList,
      selectedTabId: (state) => state.selectedTabId,
      contentDefault: (state) => state.contentDefault,
    }),
  },

  watch: {
    length(val) {
      this.tab = val - 1;
    },

    tab() {
      this.selectTabByIndex(this.tab);
      this.updateSelectedTab(this.tab);
      console.log('tab changed:', this.tab);
    },
  },

  methods: {
    ...mapActions('node', [
      'addTab',
      'removeTabById',
      'selectTabByIndex',
      'removeTabByIndex',
      'play',
      'updateSelectedTab',
      'duplicateTab',
    ]),

    show(e) {
      e.preventDefault();
      this.showMenu = false;
      this.x = e.clientX;
      this.y = e.clientY;
      this.$nextTick(() => {
        this.showMenu = true;
      });
    },

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

    selectTab(index) {
      this.updateSelectedTab(index);
    },

    // functcion to gerate unique id based in timestamp
    generateId() {
      return new Date().getTime();
    },

    close(index) {
      if (this.tabList.length > 1) {
        console.log('aba fechada, index: ', index);
        this.removeTabByIndex(index);
      }
    },

    add() {
      const tabLength = this.tabList.length;
      let tabSketchName = `Aba ${this.newTabCount}`;
      if (tabLength === 0 ) tabSketchName = 'Aba 1';
      const idGenerated = this.generateId();
      this.newTabCount += 1;
      const newTab = {
        sketchName: tabSketchName,
        id: idGenerated,
        saved: false,
        content: this.contentDefault,
      };

      this.lastSelectedTabId = idGenerated;

      this.addTab(newTab);
      this.updateSelectedTab(tabLength);
      this.tab = tabLength - 1;
      this.length = tabLength;
    },

    duplicate(index, sketchName) {
      const idGenerated = this.generateId();

      const newTab = {
        sketchName: `${sketchName} - Cópia`,
        id: idGenerated,
        saved: false,
      };

      this.lastSelectedTabId = idGenerated;

      this.duplicateTab({
        tab: newTab,
        indexContextMenu: this.contextMenuSelectedTabIndex,
      });

      this.length = this.tabList.length;
    },
  },

  mounted() {
    if (this.tabList.length === 0) {
      this.add();
    }
  },
};
</script>

<style scoped>
.content {
  width: 100%;
}
.add-tab {
  align-self: center;
  margin: 9px;
}

.context-menu-btn {
  display: none;
}

.tab-item:hover + .context-menu-btn {
  display: block;
}
</style>
