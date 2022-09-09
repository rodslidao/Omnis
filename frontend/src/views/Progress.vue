<template>
  <div class="main d-flex flex-column">
    <side-menu class="side-menu" paddingTop="60px"></side-menu>
    <div class="animation d-flex align-center justify-center">
      <cartesian-3d lockView height="20rem"> </cartesian-3d>
    </div>
    <div class="resume d-flex align-center justify-center">
      <process-manager-button></process-manager-button>
    </div>
  </div>
</template>

<script>
import ProcessManagerButton from '@/components/ProcessManagerButton.vue';
import Cartesian3d from '../components/node/Cartesian3d.vue';
import SideMenu from '../components/node/sideMenu/sideMenu.vue';

export default {
  components: {
    ProcessManagerButton,
    Cartesian3d,
    SideMenu,
  },
};
</script>

<style lang="scss" scoped>
.main {
  height: 100%;
  background-image: linear-gradient(to bottom, #da2829, #c31432, #240b36);

  div {
    // border: 1px solid red;
  }

  .sideMenu {
    top: 50px;
  }

  .speed-dial {
    bottom: 16px;
    right: 16px;
    position: absolute;
    // margin: 0 0 32px 16px;
    z-index: 9999;
  }

  .animation {
    height: 60%;
    width: 100%;
  }
  .resume {
    height: 40%;
  }
}
</style>
