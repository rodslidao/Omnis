<template>
  <div class="tabMenu custom">
    <vue-tabs-chrome
      ref="tabs"
      theme="tab-custom"
      v-model="selectedTabKey"
      :tabs="tabList"
      @remove="close"
      @contextmenu="contextMenu"
      :gap="4"
      label="name"
    >
      <span slot="after">
        <v-btn class="add-tab" dark depressed icon @click="addTab" small
          ><v-icon small dark> mdi-plus </v-icon></v-btn
        >
      </span>
      <!-- <template slot="close-icon">
        <div class="btn-container">
          <v-btn depressed icon @click="close(index)" small dark>
            <v-icon class="align-self-end" small dark>
              mdi-dots-vertical
            </v-icon></v-btn
          >
          <v-btn depressed icon @click="close(index)" small dark>
            <v-icon class="align-self-end" small dark>
              mdi-close
            </v-icon></v-btn
          >
        </div>
      </template> -->
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
      :visible="renameDialog"
      description=" "
      title="Renomear"
      @cancel-event="renameDialog = false"
      @confirm-event="(renameDialog = false), updateName()"
    >
      <template v-slot:description>
        <v-text-field
          label="Nome"
          required
          placeholder="Nome"
          v-model="name"
          :rules="requiredRules"
        ></v-text-field>
        <v-text-field
          label="Descrição"
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
        // {
        //   title: 'Duplicar',
        //   btnIcon: 'content-duplicate',
        //   function: this.duplicate,
        // },
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
        // console.log('loadedFileTrigger');
        this.$refs.tabs.addTab({ ...this.newTab });
        this.selectedTabKey = this.newTab.key;
      },
      // deep: true,
    },
  },

  mounted() {
    // console.log('mounted', this.tabList);

    if (this.selectedTabKey === '' && this.tabList.length > 0) {
      // this.tabList.forEach((tab) => {
      // console.log('tab', tab);
      //   this.$refs.tabs.addTab(tab);
      // });
      this.selectedTabKey = this.selectedTab.key;
      // this.$refs.tabs.setup();
      // this.$refs.tabs.doLayout();
    }

    // console.log('selected tabbbb22222', this.selectedTabKey);

    // console.log(this.tabList.length ? this.tabList : 0);
    if (this.tabList.length === 0) this.addTab();
    if (!this.selectedTabKey) this.selectedTabKey = this.selectedTab.key;
    // this.updateSelectedTab(this.selectedTabKey);
    // console.log('tab list', this.tabList);
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
      // console.log('addTab', this.selectedTabKey);
      // console.log('addTabdddd', this.$refs.tabs.addTab);
      this.addNewTab({ created: true });
      // console.log(this.newTab);
      this.$refs.tabs.addTab({ ...this.newTab });
      this.selectedTabKey = this.newTab.key;
    },

    close(tab) {
      // console.log('close');
      // console.log({ tab, index });
      this.removeTabByKey(tab.key);
      this.$refs.tabs.removeTab(tab.key);
    },

    select(index) {
      this.selectTab(index);
    },

    contextMenu(event, tab) {
      this.context.x = event.x;
      this.context.y = event.y;
      this.showMenu = true;
      this.contextMenuSelectedTab = tab;
      // console.log(event, tab, index);
    },

    duplicate() {
      // console.log('duplicate');
      // this.duplicateTab(this.selectedTabKey);
    },

    getName() {
      this.name = this.contextMenuSelectedTab.label;
      this.description = this.contextMenuSelectedTab.description;
    },

    rename() {
      this.renameDialog = true;
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
$soft-grey: #d1d1d1;
.tabMenu {
  width: 100%;
  background: $primary-dark;
  color: $soft-grey;

  .btn-container {
    display: flex;
    flex-direction: row;
    height: 100%;
    width: 100%;
    justify-content: center;
    align-items: center;
    color: $soft-grey;
    padding-right: 3rem;
    margin-right: 1rem;
  }

  .theme-tab-custom {
    color: #9ca1a7;
    background-color: $secondary-dark;
    box-shadow: inset 0px -6px 0px 0px rgb(25 118 210);
    .tabs-item {
      &:hover {
        .tabs-background-content {
          background-color: #202124;
        }
        .tabs-background-before,
        .tabs-background-after {
          fill: transparent;
        }
      }
      &.is-dragging {
        .tabs-background-content {
          background-color: #202124;
        }
        .tabs-background-before,
        .tabs-background-after {
          fill: transparent;
        }
      }
      &.active {
        color: #fff;
        .tabs-background-content {
          background-color: $primary-dark;
        }
        .tabs-background-before,
        .tabs-background-after {
          fill: $primary-dark;
        }
      }
      .tabs-close-icon {
        stroke: #81878c;
        &:hover {
          stroke: #cfd1d2;
          background-color: #5f6368;
        }
      }
    }
    .tabs-divider {
      background-color: #4a4d51;
    }
    .tabs-footer {
      background-color: $primary-dark;
    }
  }
}
</style>
