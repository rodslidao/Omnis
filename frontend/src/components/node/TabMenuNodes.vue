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
    <dialog-confirmation
      v-on="getName()"
      confirmText="salvar"
      dark
      v-if="renameDialog"
      description=" "
      title="Renomear"
      @cancel-event="renameDialog = false"
      @confirm-event="renameDialog = false, updateName()"
    >
      <template v-slot:description>
        <v-text-field
          required
          placeholder="Nome"
          v-model="name"
          :rules="requiredRules"
        ></v-text-field>
        <v-text-field
          placeholder="Descrição"
          v-model="description"
        ></v-text-field>
      </template>
    </dialog-confirmation>
  </div>
</template>
<script>
import { mapActions, mapState } from 'vuex';
// import gql from 'graphql-tag';

import VueTabsChrome from 'vue-tabs-chrome';
import DialogConfirmation from '@/components/settings/DialogConfirmation.vue';

export default {
  components: {
    VueTabsChrome,
    DialogConfirmation,
  },
  data() {
    return {
      selectedTabKey: '',
      contextMenuSelectedTab: null,
      showMenu: false,
      renameDialog: false,
      requiredRules: [(v) => !!v || 'Campo não pode ficar em branco'],
      name: '',
      description: '',
      items: [
        {
          title: 'Duplicar',
          btnIcon: 'content-duplicate',
          function: this.duplicate,
        },
        {
          title: 'Renomear',
          btnIcon: 'form-textbox',
          function: this.rename,
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
      'updateByProperty',
    ]),

    addTab() {
      this.addNewTab();
      console.log(this.newTab);
      this.$refs.tabs.addTab({ ...this.newTab });
      this.selectedTabKey = this.newTab.key;
    },

    close(tab, index) {
      console.log('close');
      console.log({ tab, index });
      this.removeTabByKey(tab.key);
      this.$refs.tabs.removeTab(tab.key);
    },

    select(index) {
      this.selectTab(index);
    },

    contextMenu(event, tab, index) {
      this.context.x = event.x;
      this.context.y = event.y;
      this.showMenu = true;
      this.contextMenuSelectedTab = tab;
      console.log(event, tab, index);
    },

    duplicate() {
      console.log('duplicate');
      // this.duplicateTab(this.selectedTabKey);
    },

    getName() {
      this.name = this.contextMenuSelectedTab.label;
      this.description = this.contextMenuSelectedTab.description;
    },

    rename() {
      this.renameDialog = true;
      console.log('rename');
      // this.renamingIndex = index;
    },

    updateName() {
      this.updateByProperty({
        label: this.name,
        description: this.description,
        key: this.contextMenuSelectedTab.key,
      });
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
