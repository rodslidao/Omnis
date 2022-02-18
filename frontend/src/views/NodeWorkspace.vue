<template>
  <div class="containerNode">
    <!-- <v-tabs-items v-model="selectedTab">
      <v-tab-item v-for="item in tabList" :key="item.name"> </v-tab-item>
    </v-tabs-items> -->

    <NodeEditor
      class="nodeEditor"
    ></NodeEditor>

    <!-- <NodeEditor class="nodeEditor" ></NodeEditor> -->
  </div>
</template>

<script>
// import TabMenuNodes from '@/components/nodes/TabMenuNodes.vue';
import NodeEditor from '@/components/nodes/NodeEditor.vue';
import { mapState } from 'vuex';

export default {
  name: 'ActionMenuForNodes',
  components: {
    // TabMenuNodes,
    NodeEditor,
  },
  data: () => ({}),

  computed: {
    ...mapState('node', {
      tabList: (state) => state.tabList,
      selectedTabIndex: (state) => state.selectedTabIndex,
    }),
  },
};
</script>

<style lang="scss" scoped>
.containerNode {
  height: 100%;
  position: relative;
}
.nodeEditor {
  width: 100vw;
  height: 100%;
}
</style>
