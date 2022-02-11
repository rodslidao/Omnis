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
import { mapMutations } from 'vuex';
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

export default {
  // mixins: [mixins],
  // name: "NodeEditor",
  props: {},

  data: () => ({
    editor: new Editor(),
    viewPlugin: new ViewPlugin(),
    engine: new Engine(true),
    intfTypePlugin: new InterfaceTypePlugin(),
    tablist2: 2,
  }),

  components: {
    ActionMenuForNodes,
  },

  created() {
    // Register the plugins
    // The view plugin is used for rendering the nodes
    this.editor.use(this.viewPlugin);
    // The option plugin provides some default option UI elements
    this.editor.use(new OptionPlugin());
    // The engine plugin calculates the nodes in the graph in the
    // correct order using the "calculate" methods of the nodes
    this.editor.use(this.engine);

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

    this.editor
      .addConnection
      // node1.getInterface('Saida'),
      // node2.getInterface('Entrada'),
      // node3.getInterface('Entrada')
      ();

    this.engine.calculate();

    //tipos de interfaces
    this.editor.use(this.intfTypePlugin);
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
    }),

    // updateContentDefault() {
    //   console.log('sdfsdfsdfsdfsd');
    //   this.editor.load(this.tabList[this.selectedTabIndex].content);
    //   return 0;
    // },
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
          console.log('duplicated load');

          this.updateNodeContent({
            content: JSON.parse(JSON.stringify(this.editor.save())),
            index: newValue,
            duplicated: false,
          });
        }
        this.editor.load(this.tabList[newValue].content);
      },
    },
  },

  methods: {
    ...mapActions('node', ['updateNodeContent', 'updateContentDefault']),

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
