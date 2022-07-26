<template>
  <div class="container">
    <v-btn
      dark
      class="tab-button"
      :class="drawer ? 'active' : ''"
      color="#4e4e4e"
      @click.stop="drawer = !drawer"
      >movimentação</v-btn
    >
    <v-navigation-drawer
      dark
      v-model="drawer"
      hide-overlay='true'
      right
      :permanent="drawer"
      width="400px"
      app
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
  data: () => ({
    drawer: false,
    group: null,
  }),

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
