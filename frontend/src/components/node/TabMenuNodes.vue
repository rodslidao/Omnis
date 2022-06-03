<template>
  <div class="tabMenu">
    <vue-tabs-chrome
      ref="tabs"
      theme="dark"
      v-model="selectedTabKey"
      :tabs="tabList"
      @remove="close"
    >
      <span slot="after">
        <v-btn class="add-tab" dark depressed icon @click="addTab"  small
          ><v-icon small dark> mdi-plus </v-icon></v-btn
        >
        <p>{{  }}</p>
      </span>
    </vue-tabs-chrome>
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
    };
  },

  watch: {
    selectedTabKey() {
      this.updateSelectedTab(this.selectedTabKey);
      console.log('selectedTabKey', this.selectedTabKey);
    },
    '$store.getter.node.selectedTabKey': (newVal) => {
      console.log('newVal', newVal);
      this.selectedTabKey = this.selectedTab.key;
    },
    // '$store.node.getter.selectedTabKey': (newVal) => {
    //   console.log('newVal2', newVal);
    //   this.selectedTabKey = newVal;
    // },
  },

  created() {
    this.addTab();
    console.log('criou uma nova aba');
  },

  computed: {
    ...mapState('node', {
      tabList: (state) => state.tabList,
      selectedTab: (state) => state.selectedTab,
      newTabCopy: (state) => state.newTab,
    }),
  },

  methods: {
    ...mapActions('node', [
      'addNewTab',
      'closeTab',
      'selectTab',
      'updateSelectedTab',
      'removeTabByKey',
    ]),

    addTab() {
      this.addNewTab();
      this.$refs.tabs.addTab({ ...this.newTabCopy });
    },

    close() {
      console.log('close');
      this.removeTabByKey(this.selectedTabKey);
      this.$refs.tabs.removeTab(this.selectedTabKey);
    },

    select(index) {
      this.selectTab(index);
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
