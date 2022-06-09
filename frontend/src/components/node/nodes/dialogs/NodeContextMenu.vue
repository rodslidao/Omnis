/* eslint-disable no-shadow */
<template>
  <div class="text-center">
    <v-menu dark v-model="menu" :close-on-content-click="false" offset-x>
      <template v-slot:activator="{ on, attrs }">
        <div
          @contextmenu.prevent.stop="on.click"
          v-bind="attrs"
          class="grid-container pa-0"
          :class="classTitle"
          style="padding-top: 1px"
        >
          <h3
            :id="nodeData.id"
            class="name"
            style="text-align: center"
            @click.middle="openSettings()"
            @mousedown.self.prevent.stop="$emit('start-drag')"
            @mouseup.self.prevent.stop="$emit('stop-drag', $event)"
          >
            {{ nodeData.name }}
          </h3>
          <!-- <h5
            :id="nodeData.id"
            class="type"
            style="text-align: center"
            @mousedown.self.prevent.stop="$emit('start-drag')"
            @mouseup.self.prevent.stop="$emit('stop-drag', $event)"
          >
            {{ nodeData.type }}
          </h5> -->
          <v-btn
            v-if="isStoppable"
            icon
            dense
            style="width: 30px; height: 30px"
            @click="activateNode"
            class="btn-ss"
          >
            <v-tooltip
              bottom
              open-delay="300"
              :color="running ? 'green' : 'red'"
            >
              <template v-slot:activator="{ on, attrs }">
                <div v-on="on">
                  <v-btn
                    icon
                    v-bind="attrs"
                    v-on="on"
                    style="pointer-events: none"
                  >
                    <v-icon color="white" v-if="!running"
                      >mdi-play-outline</v-icon
                    >
                    <v-icon color="white" v-else>mdi-pause</v-icon>
                  </v-btn>
                </div>
              </template>
              <span v-if="running">Running. Click to pause.</span>
              <span v-else>Stopped. Click to start.</span>
            </v-tooltip>
          </v-btn>
        </div>
      </template>

      <v-card width="350px" style="max-height: 400px" class="scroll-card">
        <v-list class="pa-0">
          <v-list-item>
            <v-list-item-avatar :color="color" size="56" class="rounded">
              <v-icon :color="color" class="icon-contrast">{{
                typeIcon
              }}</v-icon>
            </v-list-item-avatar>
            <v-list-item-content style="text-align: left">
              <v-list-item-title>
                <TextEditable :text="nodeData.name" @changeText="changeName" />
              </v-list-item-title>
              <v-list-item-subtitle
                >Type: {{ nodeData.type }}</v-list-item-subtitle
              >
              <v-list-item-subtitle>Id: {{ nodeData.id }}</v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action v-if="isStoppable">
              <v-tooltip bottom :color="running ? 'green' : 'red'">
                <template v-slot:activator="{ on, attrs }">
                  <div v-on="on">
                    <v-btn
                      icon
                      v-bind="attrs"
                      v-on="on"
                      style="pointer-events: none"
                    >
                      <v-icon color="green" v-if="running"
                        >mdi-play-outline</v-icon
                      >
                      <v-icon color="red" v-else>mdi-pause</v-icon>
                    </v-btn>
                  </div>
                </template>
                <span v-if="running">Running</span>
                <span v-else>Stopped</span>
              </v-tooltip>
            </v-list-item-action>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>
        <NodeContextMenuListItem
          :title="running ? 'Stop Node' : 'Start Node'"
          :color="running ? 'red' : 'green'"
          :icon="running ? 'mdi-pause' : 'mdi-play-outline'"
          @click="activateNode"
          v-if="isStoppable"
        />
        <NodeContextMenuListItem
          title="Open Settings"
          color="grey"
          icon="mdi-cog-outline"
          @click="openSettings"
          v-if="isConfigurable"
        />
        <NodeContextMenuListItem
          title="Reset Node"
          color="grey"
          icon="mdi-backup-restore"
          @click="resetNode"
          v-if="isResettable"
        />
        <NodeContextMenuListItem
          title="Settings History"
          color="grey"
          icon="mdi-format-list-numbered"
          @click="openHistory"
          v-if="hasHistory"
        />
        <NodeContextMenuColorPicker color="grey" @colorChange="changeColor" />
        <NodeContextMenuListItem
          v-for="(action, i) in actions"
          :key="i"
          :title="action.text"
          :color="action.color"
          :icon="action.icon"
          @click="execute(action.callable)"
        />
        <v-divider></v-divider>
        <v-expansion-panels v-model="expanded" accordion>
          <v-expansion-panel>
            <v-expansion-panel-header> Node Info </v-expansion-panel-header>
            <v-expansion-panel-content>
              <p
                v-html="description"
                style="text-align: left !important; font-size: 13px"
              ></p>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card>
    </v-menu>
  </div>
</template>

<script>
// import { apiBaseUrl } from '@/main.js';
import EventBus from '@/event-bus';
import { mapActions } from 'vuex';
import { getDescription, descriptions } from '@/components/node/nodes/nodeDescription';
import NodeContextMenuListItem from './NodeContextMenuListItem.vue';
import NodeContextMenuColorPicker from './NodeContextMenuColorPicker.vue';
import TextEditable from './TextEditable.vue';

export default {
  components: {
    NodeContextMenuListItem,
    NodeContextMenuColorPicker,
    TextEditable,
  },
  data: () => ({
    fav: true,
    menu: false,
    message: false,
    hints: true,
    color: 'white',
    running: true,
    description: '',
    descriptionsList: descriptions,
    actions: [
      {
        text: 'Create Template',
        color: 'grey',
        callable: 'createTemplate',
        icon: 'mdi-card-bulleted-outline',
      },
      {
        text: 'Delete Node',
        color: 'grey',
        callable: 'deleteNode',
        icon: 'mdi-trash-can-outline',
      },
    ],
    colorCopy: null,
    expanded: [],
  }),
  props: {
    nodeData: Object,
    dragging: Boolean,
  },
  inject: ['editor'],

  created() {
    this.color = this.nodeData.getOptionValue('color');
    this.running = this.nodeData.getOptionValue('running');
    this.description = getDescription(this.nodeData.type);
  },
  methods: {
    ...mapActions('node', ['deletedNode', 'saveNodeConfig']),

    changeColor(event) {
      this.color = event;
      this.$emit('optionChange', 'color', this.color);
    },
    prevent(evt) {
      console.log('prevent');
      evt.preventDefault();
    },
    execute(action) {
      if (action === 'deleteNode') this.deleteNode();
      if (action === 'openSettings') this.openSettings();
      if (action === 'createTemplate') this.createTemplate();
      if (action === 'activateNode') this.activateNode();
      if (action === 'resetNode') this.resetNode();
    },
    save() {
      this.$emit('optionChange', 'color', this.color);
      this.menu = false;
    },
    changeName(data) {
      this.nodeData.name = data;
      this.saveNodeConfig(this.nodeData.id);
      // this.$store.commit('saveNodeConfig', this.nodeData.id);
      this.dialog = false;
    },
    deleteNode() {
      this.deletedNode(this.nodeData);
      // this.$store.commit('deleteNode', this.nodeData); // old
    },
    activateNode() {
      // let action = this.running ? 'stop' : 'start';

      // let lastValueUrl = `${apiBaseUrl}/${action}/${this.nodeData.id}`;
      // this.axios
      //   .get(lastValueUrl)
      //   .then((response) => {
      this.running = true;
      this.$emit('optionChange', 'running', this.running);
      // })
      // .catch((err) => {
      //   console.log(err);
      // });
    },

    openSettings() {
      EventBus.$emit('OPEN_SETTINGS', this.nodeData.id);
      this.menu = false;
    },

    createTemplate() {
      const data = this.nodeData.save();

      const template = { ...data };

      delete template.id;
      delete template.state;

      delete template.interfaces;

      delete template.position;

      template.position = {};
      template.position.x = 0;
      template.position.y = 0;

      // let createTemplateUrl = `${apiBaseUrl}/node-template`;
      // this.axios.post(createTemplateUrl, template).then(() => {
      //   console.log('%cSuccessfully created template. ', this.nodeData.name);
      this.menu = false;
      // });
    },
    resetNode() {
      // let resetUrl = `${apiBaseUrl}/reset/${this.nodeData.id}`;
      // this.axios.get(resetUrl).then(() => {
      //   console.log('%cSuccessfully resetted ', this.nodeData.name);
      this.menu = false;
      // });
    },
    openHistory() {
      this.$router.push({ path: `/manage/nodehistory/${this.nodeData.id}` });
    },
  },

  watch: {
    menu(newVal) {
      if (newVal) {
        // If menu (re-)opened thie block is executed
        this.colorCopy = this.nodeData.getOptionValue('color');
        this.expanded = [];
      }
    },
  },

  computed: {
    typeIcon() {
      const nodeType = this.descriptionsList.find(
        (nodeType) => nodeType.type === this.nodeData.type,
      );
      if (!nodeType) {
        return 'mdi-help-circle-outline';
      }
      return `mdi-${nodeType.icon}`;
    },
    isResettable() {
      const nodeType = this.descriptionsList.find(
        (nodeType) => nodeType.type === this.nodeData.type,
      );
      return nodeType.resettable;
    },
    runningColor() {
      if (this.running) return 'green';
      return 'red';
    },
    isStoppable() {
      return this.descriptionsList.find(
        (nodeType) => nodeType.type === this.nodeData.type,
      ).stoppable;
    },
    isConfigurable() {
      return this.descriptionsList.find(
        (nodeType) => nodeType.type === this.nodeData.type,
      ).configurable;
    },
    hasHistory() {
      return this.descriptionsList.find(
        (nodeType) => nodeType.type === this.nodeData.type,
      ).hasHistory;
    },
    /**
     * Returns different width for title, depending if the node is stoppable or not.
     * - 150px if its stoppable to have space for the stopping button
     * - 180px if its not stoppable to make use of the full title width
     */
    titleStyle() {
      const { stoppable } = this.descriptionsList.find(
        (nodeType) => nodeType.type === this.nodeData.type,
      );
      return {
        width: stoppable ? '150px' : '180px',
      };
    },
    classTitle() {
      return {
        grabbed: this.dragging,
        grabbable: !this.dragging,
      };
    },
  },
};
</script>

<style scoped>
.scroll-card {
  overflow-y: scroll;
  display: flex !important;
  flex-direction: column;
}

.icon-contrast {
  -webkit-filter: invert() grayscale() contrast(100);
}

.grid-container {
  display: grid;
  grid-template-columns: 3fr 3fr;
  grid-template-rows: 1fr;
}

.name {
  grid-column-start: 1;
  grid-column-end: 3;
  grid-row-start: 1;
  grid-row-end: 1;
  height: 90%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 400;
}

.type {
  grid-column-start: 1;
  grid-column-end: 3;
  grid-row-start: 2;
  grid-row-end: 2;
  height: 90%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-ss {
  grid-column-start: 3;
  grid-column-end: 4;
  grid-row-start: 1;
  grid-row-end: 1;
}

.grabbed {
  cursor: grabbing;
}

.grabbable {
  cursor: grab;
}
</style>

<style lang="scss">
.node > .__title {
  padding-top: 2px;
}
</style>
