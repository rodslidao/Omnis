
<template>
  <div class="container">
    <v-btn
      class="tab-button"
      outlined
      color="white"
      @click.stop="drawer = !drawer"
      >movimentação</v-btn
    >

    <v-navigation-drawer
      dark
      v-model="drawer"
      absolute
      right
      :permanent="drawer"
      width="300px"
    >
      <jog-buttons></jog-buttons>
    </v-navigation-drawer>
  </div>
</template>

<script>
import JogButtons from '@/components/nodes/sideMenu/move/JogButtons.vue';
export default {
  components: {
    JogButtons,
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
  .tab-button {
    transform: rotate(-90deg);
    transform-origin: 92%;
    position: absolute;
    top: 40px;
    right: 0;
    z-index: 9999;
  }
}
</style>