<template>
  <div class="main d-flex flex-column">
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

export default {
  components: { ProcessManagerButton, Cartesian3d },
};
</script>

<style lang="scss" scoped>
.main {
  height: 100%;
  background-image: linear-gradient(
    to bottom,
     #da2829,
     #c31432,
     #240b36
  );

  div {
    // border: 1px solid red;
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