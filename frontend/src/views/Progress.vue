<template>
  <div class="main d-flex flex-column">
    <div class="animation"><cartesian-3d></cartesian-3d></div>
    <div class="resume d-flex align-center justify-center">
      <process-manager-button></process-manager-button>
    </div>
  </div>
</template>

<script>
import ProcessManagerButton from '@/components/ProcessManagerButton.vue';
import Cartesian3d from '../components/node/Cartesian3d.vue';

export default {
  components: { ProcessManagerButton, Cartesian3d, },
};
</script>

<style lang="scss" scoped>
.main{
  height: 100%;
  div{
    // border: 1px solid red;
  }
  .animation{
    height: 60%;
    width: 100%;
    background: rgb(75, 75, 75);
background: linear-gradient(180deg, rgb(44, 44, 44) 48%, rgba(255,255,255,0) 100%);
  }
  .resume{
 height: 40%;
  }
}
</style>