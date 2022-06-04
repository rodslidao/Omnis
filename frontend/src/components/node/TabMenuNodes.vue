<template>
  <div class="tabMenu">
    <vue-tabs-chrome
      ref="tabs"
      theme="dark"
      v-model="selectedTabKey"
      :tabs="tabList"
      @remove="close"
      @contextmenu="contextMenu"
    >
      <span slot="after">
        <v-btn class="add-tab" dark depressed icon @click="addTab" small
          ><v-icon small dark> mdi-plus </v-icon></v-btn
        >
      </span>
    </vue-tabs-chrome>
    <v-menu
      transition="slide-x-transition"
      v-model="showMenu"
      bottom
      dark
      left
      :position-y="context.y"
      :position-x="context.x"
    >
      <v-list>
        <v-list-item
          class="list-item"
          v-for="(item, index) in items"
          :key="index"
          link
        >
          <v-list-item-title @click="item.function()"
            ><v-icon small class="mr-5">mdi-{{ item.btnIcon }}</v-icon
            >{{ item.title }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>
<script>
import { mapActions, mapState } from 'vuex';
import gql from 'graphql-tag';

import VueTabsChrome from 'vue-tabs-chrome';

export default {
  components: {
    VueTabsChrome,
  },
  data() {
    return {
      selectedTabKey: '',
      showMenu: false,
      items: [
        {
          title: 'Duplicar',
          btnIcon: 'content-duplicate',
          function: this.duplicate,
        },
        {
          title: 'Renomear',
          btnIcon: 'form-textbox',
          function: this.setRenamingIndex,
        },
      ],
      context: {
        x: 0,
        y: 0,
      },
    };
  },

  watch: {
    selectedTabKey(newVal, oldVal) {
      this.updateSelectedTab([newVal, oldVal]);
    },
    '$store.state.node.loadedFileTrigger': {
      handler() {
        console.log('loadedFileTrigger');
        this.$refs.tabs.addTab({ ...this.newTab });
        this.selectedTabKey = this.newTab.key;
      },
      // deep: true,
    },
  },

  mounted() {
    this.addTab();
    console.log('criou uma nova aba');
  },

  computed: {
    ...mapState('node', {
      tabList: (state) => state.tabList,
      selectedTab: (state) => state.selectedTab,
      newTab: (state) => state.newTab,
    }),
  },

  methods: {
    ...mapActions('node', [
      'addNewTab',
      'closeTab',
      'updateSelectedTab',
      'removeTabByKey',
      'duplicateTab',
    ]),

    addTab() {
      this.addNewTab();
      console.log(this.newTab);
      this.$refs.tabs.addTab({ ...this.newTab });
      this.selectedTabKey = this.newTab.key;
    },

    close() {
      console.log('close');
      this.removeTabByKey(this.selectedTabKey);
      this.$refs.tabs.removeTab(this.selectedTabKey);
    },

    select(index) {
      this.selectTab(index);
    },

    contextMenu(event, tab, index) {
      this.context.x = event.x;
      this.context.y = event.y;
      this.showMenu = true;
      console.log(event, tab, index);
    },

    duplicate() {
      console.log('duplicate');
      // this.duplicateTab(this.selectedTabKey);
    },

    setRenamingIndex() {
      console.log('setRenamingIndex');
      // this.renamingIndex = index;
    },
  },
};
</script>

<style lang="scss">
$primary-dark: #232323;
$secondary-dark: #272727;
.tabMenu {
  width: 100%;
  background: $primary-dark;
}
</style>
