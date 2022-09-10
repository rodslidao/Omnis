<template>
  <div class="container">
    <v-btn
      dark
      :style="tabButton"
      class="tab-button"
      :class="drawer ? 'active' : ''"
      color="#4e4e4e"
      @click.stop="drawer = !drawer"
      >movimentação</v-btn
    >
    <v-navigation-drawer
      :style="navigationDrawer"
      v-model="drawer"
      width="400px"
      right
      dark
      app
      :absolute="drawer"
      :permanent="drawer"
    >
      <move></move>
    </v-navigation-drawer>
  </div>
</template>

<script>
import Move from '@/components/node/sideMenu/move/Move.vue';

export default {
  components: {
    Move,
  },

  props: {
    paddingTop: String,
  },

  data: () => ({
    drawer: false,
    group: null,
  }),

  computed: {
    navigationDrawer() {
      return {
        'padding-top': this.paddingTop,
      };
    },
    tabButton() {
      return {
        'margin-top': this.paddingTop,
      };
    },
  },

  watch: {
    group() {
      this.drawer = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  padding: 0;
  .tab-button {
    transform: rotate(-90deg);
    transform-origin: 92%;
    position: absolute;
    top: 20px;
    z-index: 1;
    right: 3px;
  }
  .active {
    transform: rotate(-90deg) translateY(-398px);
  }
}
</style>