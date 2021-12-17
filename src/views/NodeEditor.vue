<template>
  <div style="height: 100vh; width: 100vw">
            <baklava-editor :plugin="viewPlugin" />
  </div>
</template>

<script>
//import ProgressStatus from "../components/ProgressStatus";
import { mapMutations } from "vuex";
// import { mapState, mapMutations } from "vuex";
// import { actions } from "../store/index";

import { Editor } from "@baklavajs/core";
import { ViewPlugin } from "@baklavajs/plugin-renderer-vue";
import { OptionPlugin } from "@baklavajs/plugin-options-vue";
import { Engine } from "@baklavajs/plugin-engine";
import { MoveNode } from "../components/nodes/MoveNode";

export default {
  // mixins: [mixins],
  // name: "NodeEditor",

  data: () => ({
    editor: new Editor(),
    viewPlugin: new ViewPlugin(),
    engine: new Engine(true),
  }),

  components: {},

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
    this.viewPlugin.enableMinimap = true;

    // register the nodes we have defined, so they can be
    // added by the user as well as saved & loaded.
    // this.editor.registerNodeType("MathNode", MathNode);
    // this.editor.registerNodeType("DisplayNode", DisplayNode);
    this.editor.registerNodeType("MoveNode", MoveNode);

    // add some nodes so the screen is not empty on startup
    // const node1 = this.addNodeWithCoordinates(MoveNode, 0, 140);

    // this.editor.addConnection(
    //   node1.getInterface("Result"),
    // );

    // this.engine.calculate();
  },

  computed: {
    // ...mapState({
    //   allParts: (state) => state.production.allParts.production,
    // }),
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),

    addNodeWithCoordinates(nodeType, x, y) {
      const n = new nodeType();
      this.editor.addNode(n);
      n.position.x = x;
      n.position.y = y;
      return n;
    },
  },
};
</script>

<style lang="scss" >
</style>
