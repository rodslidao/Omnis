<template>
  <div class="background">
    <span style="display: none">{{ selectedTabIndex }}</span>
    <baklava-editor :plugin="viewPlugin" />
    <ActionMenuForNodes
      :editor="editor"
      class="action-buttons"
    ></ActionMenuForNodes>
  </div>
</template>

<script>
//import ProgressStatus from "../components/ProgressStatus";
// import { mapState, mapMutations } from "vuex";
// import { actions } from "../store/index";

import { Editor } from '@baklavajs/core';
import { ViewPlugin } from '@baklavajs/plugin-renderer-vue';
import { OptionPlugin } from '@baklavajs/plugin-options-vue';
import { Engine } from '@baklavajs/plugin-engine';

import { MoveNode } from '@/components/nodes/MoveNode';
import { IdentifyNode } from '@/components/nodes/IdentifyNode';
import { DelayNode } from '@/components/nodes/DelayNode';
import { VariableNode } from '@/components/nodes/VariableNode';
import { IoNode } from '@/components/nodes/IoNode';
import { InterfaceTypePlugin } from '@baklavajs/plugin-interface-types';
import ActionMenuForNodes from '@/components/nodes/ActionMenuForNodes.vue';
import VideoStreamingOption from '@/components/nodes/options/VideoStreamingOption.vue';

import { mapActions, mapState } from 'vuex';

// Custom Baklava Components
import CustomContextMenu from '@/components/nodes/custom/CustomContextMenu.vue';

export default {
  // mixins: [mixins],
  // name: "NodeEditor",
  props: {},

  data: () => ({
    editor: new Editor(),
    viewPlugin: new ViewPlugin(),
    engine: new Engine(true),
    optionPlugin: new OptionPlugin(),

    tablist2: 2,
  }),

  components: {
    ActionMenuForNodes,
  },

  created() {
    this.init();

    this.editor.events.addNode.addListener(this, () => {
      // this.$store.node.commit("saveNodeConfig", 1);
      this.saveNode(1);
    });

    this.editor.events.addConnection.addListener(this, () => {
      // this.$store.commit("saveNodeConfig", 1);
      this.saveNode(1);
    });

    this.editor.events.removeNode.addListener(this, () => {
      // this.$store.commit("saveNodeConfig", 1);
      this.saveNode(1);
    });

    this.editor.events.removeConnection.addListener(this, () => {
      // this.$store.commit("saveNodeConfig", 1);
      this.saveNode(1);
    });

    // Show a minimap in the top right corner
    this.viewPlugin.enableMinimap = false;

    // register the nodes we have defined, so they can be
    // added by the user as well as saved & loaded.
    this.editor.registerNodeType('MoveNode', MoveNode);
    this.editor.registerNodeType('IdentifyNode', IdentifyNode);
    this.editor.registerNodeType('IoNode', IoNode);
    this.editor.registerNodeType('DelayNode', DelayNode);
    this.editor.registerNodeType('VariableNode', VariableNode);
    this.viewPlugin.registerOption(
      'VideoStreamingOption',
      VideoStreamingOption
    );

    // add some nodes so the screen is not empty on startup
    // const node1 = this.addNodeWithCoordinates(MoveNode, 50, 140);
    // const node2 = this.addNodeWithCoordinates(MoveNode, 300, 140);
    // const node3 = this.addNodeWithCoordinates(IdentifyNode, 50, 480);

    // tipos de interfaces
    this.intfTypePlugin.addType('string', '#8cff00');
    this.intfTypePlugin.addType('array', '#00bfff');
    this.intfTypePlugin.addType('object', '#ff6200');
    this.intfTypePlugin.addType('int', '#ff0055');

    // console.log(this.editor.save());
  },

  computed: {
    ...mapState('node', {
      selectedTabIndex: (state) => state.selectedTabIndex,
      tabList: (state) => state.tabList,
      contentDefault: (state) => state.contentDefault,
      saveNode: (state) => state.saveNode,
    }),

    checkSavedStatus() {
      console.log('checkSavedStatus');
      // if (this.tabList !== []) {
      //   this.setSaved({ index: this.selectedTabIndex, value: false });
      // }
      return 0;
    },

    // updateContentDefault() {
    //   console.log('sdfsdfsdfsdfsd');
    //   this.editor.load(this.tabList[this.selectedTabIndex].content);
    //   return 0;
    // },
  },

  methods: {
    ...mapActions('node', [
      'updateNodeContent',
      'updateContentDefault',
      'setSaved',
    ]),

    init() {
      this.editor.use(this.viewPlugin);
      this.editor.use(this.optionPlugin);

      this.viewPlugin.components.contextMenu = CustomContextMenu;

      const intfTypePlugin = new InterfaceTypePlugin();
      this.editor.use(intfTypePlugin);

      // Register options and nodes
      registerOptions(this.viewPlugin);
      registerNodes(this.editor);
    },

    addNodeWithCoordinates(nodeType, x, y) {
      const n = new nodeType();
      this.editor.addNode(n);
      n.position.x = x;
      n.position.y = y;
      return n;
    },
  },

  mounted() {
    // this.$emit('nodeObject', this.editor.save());
    // console.log("mounted");
    // this.updateNodeEditor(this.editor);
    if (Object.values(this.updateContentDefault).length == 0) {
      this.updateContentDefault(this.editor.save());
    }
    console.log(this.contentDefault);
  },

  watch: {
    '$store.state.node.selectedTabIndex': {
      handler(newValue, oldValue) {
        this.updateNodeContent({
          content: this.editor.save(),
          index: oldValue,
        });

        console.log('newValue', newValue);
        console.log('oldValue', oldValue);
        console.log('this.tabList[newValue]', this.tabList);

        if (this.tabList[newValue].duplicated) {
          console.log('duplicated load', this.tabList[newValue].duplicated);

          this.updateNodeContent({
            content: JSON.parse(JSON.stringify(this.editor.save())),
            index: newValue,
          });

          console.log('duplicated load2', this.tabList[newValue].duplicated);
        }
        this.editor.load(this.tabList[newValue].content);
      },
    },
  },
};
</script>

<style lang="scss" scoped >
.node.--type-MoveNode {
  // background-color: red;
}

.v-main__wrap {
  width: 100vw;
}

.action-buttons {
  bottom: 0;
  right: 0;
  position: absolute;
  // margin: 0 0 32px 16px;
  z-index: 9999;
}
</style>
