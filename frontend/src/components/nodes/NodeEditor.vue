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

// import { Editor } from '@baklavajs/core';
import { ViewPlugin } from '@baklavajs/plugin-renderer-vue';
import { OptionPlugin } from '@baklavajs/plugin-options-vue';
import { Engine } from '@baklavajs/plugin-engine';
import { registerOptions, registerNodes } from '@/registerNodes';

import { InterfaceTypePlugin } from '@baklavajs/plugin-interface-types';
import ActionMenuForNodes from '@/components/nodes/ActionMenuForNodes.vue';

import { mapActions, mapState } from 'vuex';

// Custom Baklava Components
import CustomContextMenu from '@/components/nodes/custom/CustomContextMenu.vue';
import CustomNode from '@/components/nodes/custom/CustomNode.vue';
import CustomInterface from '@/components/nodes/custom/CustomInterface.vue';
import CustomConnection from '@/components/nodes/custom/CustomConnection.vue';

export default {
  // mixins: [mixins],
  // name: "NodeEditor",
  props: {},

  data: () => ({
    // editor: new Editor(),
    viewPlugin: new ViewPlugin(),
    engine: new Engine(true),
    // optionPlugin: new OptionPlugin(),

    tablist2: 2,
  }),

  components: {
    ActionMenuForNodes,
  },

  computed: {
    ...mapState('node', {
      editor: (state) => state.editor,
      selectedTabIndex: (state) => state.selectedTabIndex,
      tabList: (state) => state.tabList,
      contentDefault: (state) => state.contentDefault,
      saveNode: (state) => state.saveNode,
      deletedNode: (state) => state.deletedNode,
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

  created() {
    this.init();

    this.editor.events.addNode.addListener(this, () => {
      // this.$store.node.commit("saveNodeConfig", 1);
      console.log(this.saveNode);
      this.saveNodeConfig(1);
      console.log('save aqui');
    });

    this.editor.events.addConnection.addListener(this, () => {
      // this.$store.commit("saveNodeConfig", 1);
      this.saveNodeConfig(1);
    });

    this.editor.events.removeNode.addListener(this, () => {
      // this.$store.commit("saveNodeConfig", 1);
      this.saveNodeConfig(1);
    });

    this.editor.events.removeConnection.addListener(this, () => {
      // this.$store.commit("saveNodeConfig", 1);
      this.saveNodeConfig(1);
    });

    // Show a minimap in the top right corner
    this.viewPlugin.enableMinimap = false;

    // register the nodes we have defined, so they can be
    // added by the user as well as saved & loaded.

    // this.viewPlugin.registerOption(
    //   'EventButtonOption',
    //   EventButtonOption
    // );

    // add some nodes so the screen is not empty on startup
    // const node1 = this.addNodeWithCoordinates(MoveNode, 50, 140);
    // const node2 = this.addNodeWithCoordinates(MoveNode, 300, 140);
    // const node3 = this.addNodeWithCoordinates(IdentifyNode, 50, 480);

    // tipos de interfaces
    // this.intfTypePlugin.addType('string', '#8cff00');
    // this.intfTypePlugin.addType('array', '#00bfff');
    // this.intfTypePlugin.addType('object', '#ff6200');
    // this.intfTypePlugin.addType('int', '#ff0055');

    // console.log(this.editor.save());
    this.engine.calculate();
  },

  methods: {
    ...mapActions('node', [
      'updateNodeContent',
      'updateContentDefault',
      'setSaved',
      'saveNodeConfig',
    ]),

    init() {
      this.editor.use(this.viewPlugin);
      this.editor.use(new OptionPlugin());
      // this.engine.events.calculated.addListener(this, (r) => {
      //   for (const v of r.values()) {
      //     // tslint:disable-next-line:no-console
      //     console.log(v);
      //     console.log('wtfuckk');
      //   }
      // });
      // this.engine.hooks.gatherCalculationData.tap(this, () => 'def');
      this.editor.use(this.engine);
      console.log(this.engine);

      this.viewPlugin.components.contextMenu = CustomContextMenu;
      this.viewPlugin.components.node = CustomNode;
      this.viewPlugin.components.nodeInterface = CustomInterface;
      this.viewPlugin.components.connection = CustomConnection;

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
    // console.log(this.contentDefault);
  },

  watch: {
    '$store.state.node.deletedNode': {
      handler(newValue) {
        if (newValue) {
          this.editor.removeNode(newValue);
        }
      },
    },
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
        // console.log('this.tabList[newValue].content', this.tabList[newValue].content);
        // let oi = this.editor.save()
        // console.log('oi', oi);
        // this.editor.load(oi);
        // this.editor.load(this.editor.save());
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
