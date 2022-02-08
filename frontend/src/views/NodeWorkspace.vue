<template>
  <div class="containerNode">
    <div>{{selectedTab}}</div>
    <v-tabs-items v-model="selectedTab">
      <v-tab-item v-for="item in tabList" :key="item.sketchName">
        <!-- {{ item.content }} -->
        <NodeEditor class="nodeEditor"></NodeEditor>
      </v-tab-item>
    </v-tabs-items><!-- <NodeEditor class="nodeEditor" ></NodeEditor> -->
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
      selectedTab: (state) => state.selectedTab,
    }),
  },
};
</script>

<style lang="scss" scoped>
.containerNode {
  height: 100%;
}
.nodeEditor {
    width: 100vw;
    height: 100%;
  }
</style>
